const startButton = document.getElementById('startButton');
const outputDiv = document.getElementById('output');
const recognition = new webkitSpeechRecognition() || new SpeechRecognition();

recognition.interimResults = true;
recognition.continuous = true;

startButton.addEventListener('click', () => {
    recognition.start();
    startButton.disabled = true;
    startButton.textContent = 'Recording...';
});

recognition.onresult = event => {
    const result = event.results[event.results.length - 1][0].transcript;
    outputDiv.textContent = result;
};

recognition.onend = () => {
    startButton.disabled = false;
    startButton.textContent = 'Start Recording';
};

recognition.onerror = event => {
    console.error('Speech recognition error:', event.error);
};

recognition.onnomatch = () => {
    console.log('No speech was recognized.');
};