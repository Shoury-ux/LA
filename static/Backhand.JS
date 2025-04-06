document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM fully loaded and parsed");

    const form = document.getElementById("conversationForm");
    const modeSelect = document.getElementById("modeSelect");
    const baseStatementInput = document.getElementById("baseStatementInput");
    const emotionInput = document.getElementById("emotionInput");
    const conversationInput = document.getElementById("conversationInput");
    const mode1Inputs = document.getElementById("mode1Inputs");
    const mode2Input = document.getElementById("mode2Input");
    const messagesContainer = document.getElementById("messages");
    const saveButton = document.getElementById("saveButton");
    const deleteButton = document.getElementById("deleteButton");

    // Toggle input fields based on the selected mode
    modeSelect.addEventListener("change", () => {
        if (modeSelect.value === "1") {
            mode1Inputs.style.display = "block";
            mode2Input.style.display = "none";
        } else {
            mode1Inputs.style.display = "none";
            mode2Input.style.display = "block";
        }
    });

    form.addEventListener("submit", (event) => {
        event.preventDefault(); // Prevent form submission

        const selectedMode = modeSelect.value;
        let payload = {};

        if (selectedMode === "1") {
            // Mode 1: Collect base statement and emotion
            const baseStatement = baseStatementInput.value.trim();
            const emotion = emotionInput.value.trim();

            if (!baseStatement || !emotion) {
                alert("Please fill in both the base statement and emotion.");
                return;
            }

            payload = { mode: selectedMode, baseStatement, emotion };
        } else if (selectedMode === "2") {
            // Mode 2: Collect single input
            const userMessage = conversationInput.value.trim();

            if (!userMessage) {
                alert("Please enter a message.");
                return;
            }

            payload = { mode: selectedMode, message: userMessage };
        }

        // Send the data to the server
        fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
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