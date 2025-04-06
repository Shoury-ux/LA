document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("conversationForm");
    const input = document.getElementById("conversationInput");
    const messagesContainer = document.getElementById("messages");

    form.addEventListener("submit", (event) => {
        event.preventDefault(); // Prevent form submission

        const messageText = input.value.trim();
        if (messageText) {
            // Create a new message element
            const newMessage = document.createElement("div");
            newMessage.classList.add("message");
            newMessage.textContent = messageText;

            // Add the new message to the messages container
            messagesContainer.appendChild(newMessage);

            // Clear the input field
            input.value = "";

            // Remove "No messages yet." if it exists
            const noMessages = messagesContainer.querySelector(".message");
            if (noMessages && noMessages.textContent === "No messages yet.") {
                noMessages.remove();
            }
        }
    });

    // Function to load a conversation into the message history
    window.loadConversation = (conversation) => {
        // Clear the current messages
        messagesContainer.innerHTML = "";

        // Split the conversation into lines and display each as a message
        const messages = conversation.split("\n");
        messages.forEach((message) => {
            const messageElement = document.createElement("div");
            messageElement.classList.add("message");
            messageElement.textContent = message;
            messagesContainer.appendChild(messageElement);
        });
    };
});