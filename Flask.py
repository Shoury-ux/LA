import os
from flask import Flask, render_template, request

app = Flask(__name__)

# Get the absolute path to the conversations.txt file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONVERSATIONS_FILE = os.path.join(BASE_DIR, "static", "conversations.txt")

@app.route("/")
def index():
    # Load conversations from the file
    if os.path.exists(CONVERSATIONS_FILE):
        with open(CONVERSATIONS_FILE, "r") as file:
            conversations = file.read().split("\n\n")  # Split conversations by double newlines
    else:
        conversations = []  # No conversations yet
    return render_template("index.html", conversations=conversations)

@app.route("/save", methods=["POST"])
def save_conversation():
    conversation = request.form.get("conversation")
    if conversation:
        try:
            with open(CONVERSATIONS_FILE, "a", encoding="utf-8") as file:
                file.write(conversation.strip() + "\n\n")  # Save conversation with a separator
            return "Conversation saved!", 200
        except Exception as e:
            print(f"Error saving conversation: {e}")
            return "Failed to save conversation.", 500
    return "No conversation provided.", 400



if __name__ == "__main__":
    app.run(debug=True)