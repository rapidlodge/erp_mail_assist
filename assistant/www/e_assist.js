

function checkMail() {
    var user_input = document.getElementById("inputField").value;
	const chatContainer = document.getElementById('chat-container');
	const messageDiv = document.createElement('div');
	messageDiv.innerHTML = `<div class='font-weight-bolder text-right alert alert-dark shadow'> 'User': ${user_input} </div>`;
	chatContainer.appendChild(messageDiv);
	// frappe.throw(user_input);
	// document.getElementById("response").innerText = user_input;
	frappe.call({
			method: 'assistant.www.e_assist.mail_assists',
			args: {
					'user_input': user_input
			},
			callback: function(response) {
					// const messageDiv = document.createElement('div')
					// messageDiv.textContent = `'User': ${user_input}`;
					const responseDiv = document.createElement('div');
					responseDiv.innerHTML = `<div class='font-weight-bold alert alert-light shadow bg-white rounded'> 'Bot': ${response.message}</div>`;
					chatContainer.appendChild(responseDiv);
					// var user_text = user_input;
					// var processed_response = response.message;
					// document.getElementById("response").innerText = processed_response;
				
			}
	})

}