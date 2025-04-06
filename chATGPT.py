import sqlite3
import os
import openai
from datetime import datetime, timedelta

# 🔐 Your OpenAI API Key
client = openai.OpenAI(api_key="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")

def fetch_conversation(phone_number):
    db_path = os.path.expanduser('~/Library/Messages/chat.db')
    if not os.path.exists(db_path):
        print("❌ iMessage DB not found.")
        return []

    start_date = datetime.now() - timedelta(days=180)
    start_ts = int(start_date.timestamp())

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                message.text,
                message.date/1000000000 + strftime('%s','2001-01-01'),
                datetime(message.date/1000000000 + strftime('%s','2001-01-01'), 'unixepoch', 'localtime'),
                handle.id,
                message.is_from_me
            FROM message
            LEFT JOIN handle ON message.handle_id = handle.ROWID
            WHERE handle.id = ?
            AND message.text IS NOT NULL
            AND message.text != ''
            AND message.date/1000000000 + strftime('%s','2001-01-01') >= ?
            ORDER BY message.date ASC
        """, (phone_number, start_ts))

        results = []
        for row in cursor.fetchall():
            results.append({
                'text': row[0],
                'timestamp': row[1],
                'time': row[2],
                'sender': row[3],
                'is_from_me': row[4]
            })

        print(f"📦 Loaded {len(results)} messages.")
        return results

    except Exception as e:
        print(f"❌ Error reading DB: {e}")
        return []

def is_question(text):
    return "?" in text  # Simplified check — feel free to enhance

def analyze_and_collect(messages):
    history_pairs = []

    print("\n🧠 Past Questions, Replies & Emotional Tone:\n")

    for i, msg in enumerate(messages):
        if not msg['is_from_me']:
            continue

        text = msg['text'].strip()
        if not text or not is_question(text):
            continue

        print(f"❓ You [{msg['time']}]: {text}")

        reply = None
        for j in range(i + 1, len(messages)):
            if not messages[j]['is_from_me']:
                reply = messages[j]
                break

        if reply:
            print(f"💬 Them [{reply['time']}]: {reply['text']}")
            try:
                emotion_prompt = f"How is the person feeling in this reply?\n\"{reply['text']}\"\nRespond with 1-2 words only."
                emotion_result = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": emotion_prompt}],
                    temperature=0.2,
                    max_tokens=10
                )
                emotion = emotion_result.choices[0].message.content.strip()
                print(f"🤔 GPT Emotion: {emotion}")
                history_pairs.append((text, reply['text']))
            except Exception as e:
                print(f"❌ GPT emotion analysis error: {e}")
        else:
            print("❌ No reply found.")

        print("-" * 60)

    return history_pairs

def predict_emotion(history, new_message):
    prompt = "You are analyzing how Person B typically feels when receiving messages from Person A.\n"
    prompt += "Based on the conversation history below, determine how Person B would likely feel if they received this new message.\n\n"
    
    for q, r in history[-10:]:  # Only the last 10 for context
        prompt += f"Person A: {q}\nPerson B: {r}\n"

    prompt += f"\nPerson A: {new_message}\nHow would Person B likely feel?\n"
    prompt += "Respond with 1-2 words only (e.g., 'happy', 'annoyed', 'interested')."

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=10
        )
        predicted = response.choices[0].message.content.strip()
        print(f"\n🔮 Predicted Emotion if they receive this:\n🤔 {predicted}")
    except Exception as e:
        print(f"❌ GPT emotion prediction error: {e}")

# === Run ===
while True:
    number = input("📱 Enter phone number to analyze (or 'exit'): ").strip()
    if number.lower() == "exit":
        break

    msgs = fetch_conversation(number)
    if not msgs:
        continue

    history = analyze_and_collect(msgs)

    if history:
        while True:
            new_msg = input("\n📝 Enter a new message to see how they’d feel (or 'exit'): ").strip()
            if new_msg.lower() == "exit":
                break
            predict_emotion(history, new_msg)
