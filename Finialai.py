import sqlite3
import os
import openai
from datetime import datetime, timedelta

# 🔐 Replace with your OpenAI API key
client = openai.OpenAI(api_key="**apI_key_here**")  # Make sure to replace with your actual OpenAI API key

# Fetch conversation history from a specific phone number
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

        results = [{
            'text': row[0],
            'timestamp': row[1],
            'time': row[2],
            'sender': row[3],
            'is_from_me': row[4]
        } for row in cursor.fetchall()]

        print(f"📦 Loaded {len(results)} messages.")
        return results

    except Exception as e:
        print(f"❌ Error reading DB: {e}")
        return []

# 🧠 Morph message with conversation awareness
def morph_message_with_context():
    number = input("📱 Enter phone number to base message on (or 'exit'): ").strip()
    if number.lower() == "exit":
        return

    msgs = fetch_conversation(number)
    if not msgs:
        print("⚠️ No messages found.")
        return

    # Only take the other person's messages
    them = [f"Them: {m['text'].strip()}" for m in msgs if not m['is_from_me']]
    convo_sample = "\n".join(them[-100:])  # last 100 messages max

    while True:
        print("\n✍️ Enter your base message (or 'exit'):", end=" ")
        base_message = input().strip()
        if base_message.lower() == "exit":
            break

        print("🎯 Enter the emotion you want them to feel (e.g., comforted, excited, guilty):", end=" ")
        emotion = input().strip()

        if not base_message or not emotion:
            print("⚠️ Please provide both a message and an emotion.")
            continue

        prompt = f"""
Below is a sample of how a person communicates:

{convo_sample}

Based on how this person tends to talk and respond, rewrite the following message so that it keeps the same meaning, 
but makes them feel **{emotion}**, and matches their usual tone and communication style.

Original: "{base_message}"

Rewritten:
"""

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8,
                max_tokens=100
            )
            result = response.choices[0].message.content.strip()
            print(f"\n📝 Rewritten Message (to make them feel '{emotion}'):\n{result}\n")
        except Exception as e:
            print(f"❌ GPT Error: {e}")

# === Helper functions for Option 2 ===

def is_question(text):
    return "?" in text

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

    for q, r in history[-10:]:  # Only the last 10 messages for context
        prompt += f"Person A: {q}\nPerson B: {r}\n"

    prompt += f"\nPerson A: {new_message}\nHow would Person B likely feel?\nRespond with 1-2 words only."

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

# === MAIN MENU ===
def main():
    while True:
        print("\n🧠 What would you like to do?")
        print("1️⃣ Morph a message based on their tone and make them feel a certain way")
        print("2️⃣ Analyze chat history & predict emotional response")
        print("0️⃣ Exit")

        choice = input("\nChoose (0/1/2): ").strip()
        if choice == "0":
            break
        elif choice == "1":
            morph_message_with_context()
        elif choice == "2":
            number = input("📱 Enter phone number to analyze (or 'exit'): ").strip()
            if number.lower() == "exit":
                continue
            msgs = fetch_conversation(number)
            if not msgs:
                continue
            history = analyze_and_collect(msgs)
            if history:
                while True:
                    new_msg = input("\n📝 Enter a new message to see how they'd feel (or 'exit'): ").strip()
                    if new_msg.lower() == "exit":
                        break
                    predict_emotion(history, new_msg)
        else:
            print("❗ Invalid choice. Try again.")

# Run the tool!
if __name__ == "__main__":
    main()
