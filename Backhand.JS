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
});