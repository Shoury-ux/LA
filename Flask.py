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
    mode = request.json.get("mode", "1")  # Default to Mode 1 if no mode is provided

    if mode == "1":
        # Mode 1: Process base statement and emotion
        base_statement = request.json.get("baseStatement", "")
        emotion = request.json.get("emotion", "")

        if not base_statement or not emotion:
            return jsonify({"error": "Base statement and emotion are required for Mode 1."}), 400

        # Call the AI function to generate a response
        try:
            response = predict_emotion(base_statement, emotion)  # Call the AI function
        except Exception as e:
            print(f"Error in Mode 1 AI logic: {e}")
            return jsonify({"error": "Failed to process Mode 1 inputs."}), 500

    elif mode == "2":
        # Mode 2: Process single message
        user_message = request.json.get("message", "")

        if not user_message:
            return jsonify({"error": "Message is required for Mode 2."}), 400

        # Generate a response for the message
        response = f"Mode 2 response to: {user_message}"
    else:
        response = "Invalid mode selected."

    return jsonify({"response": response}), 200

if __name__ == "__main__":
    app.run(debug=True)