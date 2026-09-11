# Mathematics AI

A domain-restricted chatbot built with **Flask** and the **Gemini API**
(`gemini-3.1-flash-lite`). Mathematics AI only answers questions about
**mathematics: concepts, problem-solving, and step-by-step solutions** and politely declines anything outside that scope.

## Project structure
```
mathematics_ai/
├── app.py               # Flask app + Gemini chat logic
├── chatbot_config.py    # Bot name + system prompt (persona & rules)
├── templates/
│   └── index.html       # UI (HTML + CSS + JS in one file)
├── requirements.txt
├── .env                 # Put your GEMINI_API_KEY here (not committed)
└── .gitignore
```

## Setup
1. Create a virtual environment and install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Open `.env` and replace `your_gemini_api_key_here` with your real
   Gemini API key from Google AI Studio.
3. Run the app locally:
   ```
   python app.py
   ```
4. Open `http://127.0.0.1:5000` in your browser.

## Deploying with Gunicorn
```
gunicorn app:app
```
Point your host's start command to `gunicorn app:app` (Render, Railway,
Fly.io, a VPS, etc.) and set the `GEMINI_API_KEY` environment variable
in that platform's dashboard instead of committing `.env`.
