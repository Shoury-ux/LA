document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM fully loaded and parsed");

    const form = document.getElementById("conversationForm");
    const input = document.getElementById("conversationInput");
    const messagesContainer = document.getElementById("messages");
    const saveButton = document.getElementById("saveButton");
    const deleteButton = document.getElementById("deleteButton");

    if (!form || !input || !messagesContainer || !saveButton || !deleteButton) {
        console.error("One or more elements are missing from the DOM");
        return;
    }

    form.addEventListener("submit", (event) => {
        event.preventDefault(); // Prevent form submission
        console.log("Form submitted");

        const messageText = input.value.trim();
        if (messageText) {
            // Remove "No messages yet." placeholder if it exists
            const placeholder = messagesContainer.querySelector(".message");
            if (placeholder && placeholder.textContent === "No messages yet.") {
                placeholder.remove();
            }

            // Add the new message to the UI
            const newMessage = document.createElement("div");
            newMessage.classList.add("message");
            newMessage.textContent = messageText;
            messagesContainer.appendChild(newMessage);

            input.value = ""; // Clear the input field
        }
    });

    saveButton.addEventListener("click", () => {
        console.log("Save button clicked");
    
        // Collect all messages in the conversation
        const messages = Array.from(messagesContainer.querySelectorAll(".message"))
            .map((message) => message.textContent)
            .join("\n");
    
        if (messages.trim()) {
            // Send the conversation to the server
            fetch("/save", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: `conversation=${encodeURIComponent(messages)}`,
            })
                .then((response) => {
                    if (response.ok) {
                        console.log("Conversation saved!");
                        alert("Conversation saved successfully!");
    
                        // Dynamically update the conversation list
                        const conversationList = document.getElementById("conversationList");
                        const newListItem = document.createElement("li");
                        newListItem.textContent = messages.slice(0, 50) + (messages.length > 50 ? "..." : "");
                        newListItem.onclick = () => loadConversation(messages);
                        conversationList.appendChild(newListItem);
                    } else {
                        console.error("Failed to save conversation.");
                        alert("Failed to save conversation.");
                    }
                })
                .catch((error) => {
                    console.error("Error saving conversation:", error);
                    alert("Error saving conversation.");
                });
        } else {
            alert("No conversation to save.");
        }
    });

    deleteButton.addEventListener("click", () => {
        console.log("Delete button clicked");

        // Clear the current messages
        messagesContainer.innerHTML = "";

        // Add the "No messages yet." placeholder
        const placeholder = document.createElement("div");
        placeholder.classList.add("message");
        placeholder.textContent = "No messages yet.";
        messagesContainer.appendChild(placeholder);
    });

    // Function to load a conversation into the message history
    window.loadConversation = (conversation) => {
        console.log("Loading conversation:", conversation);

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