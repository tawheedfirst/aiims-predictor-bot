# app.py
import os
import requests
from flask import Flask, request
from predictor import predict_aiims

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# Admin contact
ADMIN_ID = 1289957753  # سَلِيمٌ

@app.route("/")
def home():
    return "AIIMS Guwahati Predictor Bot (PW Rank Booster) running ✅"

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        handle_message(chat_id, text)
    return {"ok": True}

def handle_message(chat_id, text):
    try:
        parts = text.strip().split()
        if len(parts) == 2:
            gmc = float(parts[0])
            score = float(parts[1])
            result = predict_aiims(gmc, score)
            reply = format_reply(result)
        else:
            reply = (
                "❓ Usage:\n"
                "<GMC_min_score> <Your_score>\n"
                "Example: 485 420\n\n"
                "This bot is ONLY for *PW Rank Booster Test Series → AIIMS Guwahati*."
            )
        send_message(chat_id, reply)
    except Exception as e:
        send_message(chat_id, f"⚠️ Error: {e}")

def format_reply(result):
    return (
        f"📊 *AIIMS Guwahati Prediction (PW Booster)*\n\n"
        f"🏥 GMC input: {result['gmc_input']}\n"
        f"🧑‍🎓 Your score: {result['user_score']}\n\n"
        f"📈 Predicted AIIMS mean: {result['predicted_mean']} ± {result['predicted_sd']}\n"
        f"🎯 Chance: {result['probability_pct']}%\n"
        f"✅ Safe target: {result['recommended_safe_target']}\n\n"
        f"🧭 Advice: {result['advice']}\n\n"
        f"📌 Note: Based on PW Rank Booster → AIIMS Guwahati relation.\n"
        f"💬 Feedback: @mdselimibn"
    )

def send_message(chat_id, text):
    url = f"{TELEGRAM_URL}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
