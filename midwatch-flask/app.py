from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import httpx
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

GAPGPT_API_KEY = os.getenv("GAPGPT_API_KEY")

MIDWATCH_PROMPT = """
You are Midwatch — a movie and TV show companion.

You feel like texting a smart, emotionally invested friend during movie night.

Be conversational, natural, emotionally reactive, observant, and casually funny.
Keep replies short by default.
Do not sound like a fandom wiki.
Ask for show/season/episode before answering spoiler-sensitive questions.
Never invent plot details.
Understand Persian and English. Reply in the same language the user used.
"""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        if not GAPGPT_API_KEY:
            return jsonify({"error": "Missing GAPGPT_API_KEY"}), 500

        body = request.get_json()
        messages = body.get("messages", [])

        conversation_messages = [
            {
                "role": "user" if m["role"] == "user" else "assistant",
                "content": m["text"],
            }
            for m in messages
        ]

        payload = {
            "model": "gpt-5.2",
            "messages": [
                {"role": "system", "content": MIDWATCH_PROMPT},
                *conversation_messages,
            ],
            "temperature": 1,
        }

        response = httpx.post(
            "https://api.gapgpt.app/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {GAPGPT_API_KEY}",
            },
            json=payload,
            timeout=60,
        )

        print("RAW GAPGPT RESPONSE:", response.text)

        if response.status_code != 200:
            return jsonify({"error": response.text}), response.status_code

        data = response.json()
        reply = data.get("choices", [{}])[0].get("message", {}).get(
            "content", "okay wait something broke"
        )

        return jsonify({"reply": reply})

    except Exception as e:
        print("GAPGPT ERROR:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)