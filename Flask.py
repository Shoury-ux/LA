from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    # Example conversations to pass to the template
    conversations = [
        "Hello, how are you?\nI'm fine, thank you!",
        "What are you doing?\nJust working on a project.",
    ]
    return render_template("index.html", conversations=conversations)

if __name__ == "__main__":
    app.run(debug=True)