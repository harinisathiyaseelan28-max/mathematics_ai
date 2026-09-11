import os
import uuid
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

from chatbot_config import BOT_NAME, BOT_SUBTITLE, SYSTEM_PROMPT, WELCOME_MESSAGE

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing. Add it to your .env file before running the app."
    )

genai.configure(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-3.1-flash-lite"

model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    system_instruction=SYSTEM_PROMPT,
)

app = Flask(__name__)

# In-memory chat history per browser session (fine for small/single-worker deployments).
chat_sessions = {}


@app.route("/")
def home():
    return render_template(
        "index.html",
        bot_name=BOT_NAME,
        bot_subtitle=BOT_SUBTITLE,
        welcome_message=WELCOME_MESSAGE,
    )


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = (data.get("message") or "").strip()
    session_id = data.get("session_id") or "default"

    if not user_message:
        return jsonify({"reply": "Please type a message before sending."}), 400

    if session_id not in chat_sessions:
        chat_sessions[session_id] = model.start_chat(history=[])

    chat_session = chat_sessions[session_id]

    try:
        response = chat_session.send_message(user_message)
        reply_text = response.text
    except Exception as exc:  # noqa: BLE001
        print(f"Gemini API error: {exc}")
        reply_text = "Sorry, I ran into a problem generating a response. Please try again in a moment."

    return jsonify({"reply": reply_text})


@app.route("/reset", methods=["POST"])
def reset():
    data = request.get_json(silent=True) or {}
    session_id = data.get("session_id") or "default"
    chat_sessions.pop(session_id, None)
    return jsonify({"status": "reset"})


@app.route("/new-session", methods=["GET"])
def new_session():
    return jsonify({"session_id": str(uuid.uuid4())})


if __name__ == "__main__":
    app.run(debug=True)
