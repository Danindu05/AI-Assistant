const chatLog = document.getElementById('chat-log');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');

function addMessage(message, isUser) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    messageDiv.classList.add(isUser ? 'user-message' : 'bot-message');
    messageDiv.innerHTML = `<p>${message}</p>`; 
    chatLog.appendChild(messageDiv);

    
    chatLog.scrollTop = chatLog.scrollHeight;
}

sendButton.addEventListener('click', async () => {
    const userMessage = userInput.value.trim();
    if (userMessage) {
        addMessage(userMessage, true);
        userInput.value = '';

        addMessage("Thinking...", false); 

        try {
            const response = await fetch('/get_response', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: `user_query=${encodeURIComponent(userMessage)}`
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
            const chatbotResponse = data.response;

            
            chatLog.removeChild(chatLog.lastChild);
            addMessage(chatbotResponse, false);

        } catch (error) {
            console.error("Error fetching response from server:", error);
            
            chatLog.removeChild(chatLog.lastChild);
            addMessage("Sorry, I'm Lily, and I encountered an error. Please try again later.", false);
        }
    }
});

userInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        sendButton.click();
    }
});