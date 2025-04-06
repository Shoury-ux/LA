import os
from flask import Flask, render_template, request, jsonify
from Finialai import predict_emotion  # Import the AI function

app = Flask(__name__)

# Get the absolute path to the conversations.txt file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONVERSATIONS_FILE = os.path.join(BASE_DIR, "static", "conversations.txt")

@app.route("/")
def index():
    print("Index route called")  # Debug statement
    if os.path.exists(CONVERSATIONS_FILE):
        with open(CONVERSATIONS_FILE, "r") as file:
            conversations = file.read().split("\n\n")
    else:
        conversations = []
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

@app.route("/chat", methods=["POST"])
def chat_with_ai():
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # Simulate a conversation history (you can replace this with actual history)
        history = [("Hello", "Hi there!"), ("How are you?", "I'm just a program, but I'm doing well!")]

        # Predict the emotion or generate a response
        response = predict_emotion(history, user_message)  # Call the function from Finialai.py
        return jsonify({"response": response}), 200
    except Exception as e:
        print(f"Error during AI chat: {e}")
        return jsonify({"error": "Failed to process the message"}), 500

if __name__ == "__main__":
    app.run(debug=True)