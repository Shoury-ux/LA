from flask import Flask, render_template, request
import sqlite3
import os
import openai
from datetime import datetime, timedelta

app = Flask(__name__)

client = openai.OpenAI(api_key="your_api_key_here")  # 🔐 Replace with your actual key

def fetch_conversation(phone_number):
    db_path = os.path.expanduser('~/Library/Messages/chat.db')
    if not os.path.exists(db_path):
        return []

    start_ts = int((datetime.now() - timedelta(days=180)).timestamp())

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT message.text,
                   message.date / 1000000000 + strftime('%s','2001-01-01'),
                   datetime(message.date / 1000000000 + strftime('%s','2001-01-01'), 'unixepoch', 'localtime'),
                   handle.id,
                   message.is_from_me
            FROM message
            LEFT JOIN handle ON message.handle_id = handle.ROWID
            WHERE handle.id = ?
              AND message.text IS NOT NULL
              AND message.text != ''
              AND (message.date / 1000000000 + strftime('%s','2001-01-01')) >= ?
            ORDER BY message.date ASC
        """, (phone_number, start_ts))
        return [{'text': row[0], 'timestamp': row[1], 'time': row[2], 'sender': row[3], 'is_from_me': row[4]} for row in cursor.fetchall()]
    except:
        return []

@app.route("/", methods=["GET", "POST"])
def home():
    response_text = ""
    if request.method == "POST":
        phone = request.form.get("phone")
        base_message = request.form.get("base_message")
        emotion = request.form.get("emotion")
        mode = request.form.get("mode")

        msgs = fetch_conversation(phone)
        if not msgs:
            response_text = "❌ No messages found for this phone number."
        else:
            convo_sample = "\n".join([f"Them: {m['text'].strip()}" for m in msgs if not m['is_from_me']][-100:])

            if mode == "rewrite":
                prompt = f"""
Below is a sample of how a person communicates:

{convo_sample}

Based on how this person tends to talk and respond, rewrite the following message so that it keeps the same meaning, 
but makes them feel **{emotion}**, and matches their usual tone and communication style.

Original: "{base_message}"

Rewritten:
"""
            elif mode == "predict":
                prompt = f"""
Below is a sample of how a person communicates:

{convo_sample}

Based on how this person tends to talk and respond, how would they likely feel if they received this message:

"{base_message}"

Respond with 1-2 words only.
"""
            else:
                response_text = "❌ Invalid mode selected."
                return render_template("index.html", response=response_text)

            try:
                result = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=100
                )
                response_text = result.choices[0].message.content.strip()
            except Exception as e:
                response_text = f"❌ GPT Error: {e}"

    return render_template("index.html", response=response_text)

if __name__ == "__main__":
    import webbrowser
    webbrowser.open("http://127.0.0.1:5001")
    app.run(debug=True, port=5001)
