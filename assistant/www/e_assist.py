import frappe 
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
    SystemMessagePromptTemplate,
)
import os

os.environ["OPENAI_API_KEY"] = ""

@frappe.whitelist()
def mail_assists(user_input):
    # URI for MariaDB connection
    mariadb_uri = "mariadb+pymysql://root:Cse01306135@localhost:3306/_1746c1c5436f7769"

    # Created an SQLDatabase instance for MariaDB
    db = SQLDatabase.from_uri(mariadb_uri)

    
    dt = db.run("SELECT * FROM tabCommunication;")
    # print(dt)
    
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)
    examples = [
            {"input": "List all email.", "query": "SELECT * FROM tabCommunication;"},
            {
                "input": "Find all email for the sender 'Shahadat'.",
                "query": "SELECT * FROM tabCommunication WHERE sender='shahadatshuvo96@gmail.com'",
            },
            {
                "input": "Find latest email",
                "query": "SELECT content FROM tabCommunication WHERE sent_or_received ='Received' ORDER BY creation DESC LIMIT 1;",
            },
    ]
    example_selector = SemanticSimilarityExampleSelector.from_examples(
            examples,
            OpenAIEmbeddings(),
            DocArrayInMemorySearch,
            k=2,
            input_keys=["input"],
        )
    system_prefix = """You are an agent designed to interact with a SQL database.
                        Given an input question, create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
                        Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most {top_k} results.
                        You can order the results by a relevant column to return the most interesting examples in the database.
                        Never query for all the columns from a specific table, only ask for the relevant columns given the question.
                        You have access to tools for interacting with the database.
                        Only use the given tools. Only use the information returned by the tools to construct your final answer.
                        You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

                        DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

                        If the question does not seem related to the database, just return "I don't know" as the answer.

                        Here are some examples of user inputs and their corresponding SQL queries:"""

    few_shot_prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=PromptTemplate.from_template(
            "User input: {input}\nSQL query: {query}"
        ),
        input_variables=["input", "dialect", "top_k"],
        prefix=system_prefix,
        suffix="",
    )
    full_prompt = ChatPromptTemplate.from_messages(
                                    [
                                        SystemMessagePromptTemplate(prompt=few_shot_prompt),
                                        ("human", "{input}"),
                                        MessagesPlaceholder("agent_scratchpad"),
                                    ]
                                )
    agent = create_sql_agent(
                llm=llm,
                db=db,
                prompt=full_prompt,
                verbose=True,
                agent_type="openai-tools",
            )
    res = agent.invoke({"input": user_input})
    return res