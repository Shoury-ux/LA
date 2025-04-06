document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM fully loaded and parsed");

    const form = document.getElementById("conversationForm");
    const input = document.getElementById("conversationInput");
    const messagesContainer = document.getElementById("messages");
    const saveButton = document.getElementById("saveButton");
    const deleteButton = document.getElementById("deleteButton");

    form.addEventListener("submit", (event) => {
        event.preventDefault(); // Prevent form submission

        const userMessage = input.value.trim();
        if (userMessage) {
            // Display the user's message in the chatbox
            const userMessageElement = document.createElement("div");
            userMessageElement.classList.add("message");
            userMessageElement.textContent = `You: ${userMessage}`;
            messagesContainer.appendChild(userMessageElement);

            // Clear the input field
            input.value = "";

            // Send the message to the server
            fetch("/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ message: userMessage }),
            })
                .then((response) => response.json())
                .then((data) => {
                    if (data.response) {
                        // Display the AI's response in the chatbox
                        const aiMessageElement = document.createElement("div");
                        aiMessageElement.classList.add("message");
                        aiMessageElement.textContent = `AI: ${data.response}`;
                        messagesContainer.appendChild(aiMessageElement);
                    } else {
                        console.error("Error from server:", data.error);
                    }
                })
                .catch((error) => {
                    console.error("Error sending message:", error);
                });
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
});