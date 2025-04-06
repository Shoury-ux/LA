document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM fully loaded and parsed");

    const form = document.getElementById("conversationForm");
    const input = document.getElementById("conversationInput");
    const messagesContainer = document.getElementById("messages");

    if (!form || !input || !messagesContainer) {
        console.error("One or more elements are missing from the DOM");
        return;
    }

    form.addEventListener("submit", (event) => {
        event.preventDefault(); // Prevent form submission
        console.log("Form submitted");

        const messageText = input.value.trim();
        if (messageText) {
            // Save the conversation to the server
            fetch("/save", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: `conversation=${encodeURIComponent(messageText)}`,
            })
                .then((response) => {
                    if (response.ok) {
                        console.log("Conversation saved!");
                    } else {
                        console.error("Failed to save conversation.");
                    }
                })
                .catch((error) => {
                    console.error("Error saving conversation:", error);
                });

            // Add the message to the UI
            const newMessage = document.createElement("div");
            newMessage.classList.add("message");
            newMessage.textContent = messageText;
            messagesContainer.appendChild(newMessage);

            input.value = ""; // Clear the input field
        }
    });

    // Function to load a conversation into the message history
    window.loadConversation = (conversation) => {
        console.log("Loading conversation:", conversation);

        // Clear the current messages
        messagesContainer.innerHTML = "";

        // Split the conversation into lines and display each as a message
        const messages = conversation.split("\\n");
        messages.forEach((message) => {
            const messageElement = document.createElement("div");
            messageElement.classList.add("message");
            messageElement.textContent = message;
            messagesContainer.appendChild(messageElement);
        });
    };
});