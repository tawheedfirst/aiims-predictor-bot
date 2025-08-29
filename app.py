# app.py
import os
from flask import Flask, request
import requests
from predictor import predict_aiims

app = Flask(__name__)
BOT_TOKEN = os.getenv("BOT_TOKEN")
TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

@app.route("/")
def home():
    return "AIIMS Predictor Bot running"

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
            reply = (
                f"📊 AIIMS Guwahati Prediction\n\n"
                f"GMC input: {result['gmc_input']}\n"
                f"Your score: {result['user_score']}\n"
                f"Predicted AIIMS mean: {result['predicted_mean']} ± {result['predicted_sd']}\n"
                f"Chance: {result['probability_pct']}%\n"
                f"Safe target: {result['recommended_safe_target']}\n\n"
                f"{result['advice']}"
            )
        else:
            reply = "❓ Please enter: <GMC_min_score> <Your_score>\nExample: `485 420`"
        send_message(chat_id, reply)
    except Exception as e:
        send_message(chat_id, f"⚠️ Error: {e}")

def send_message(chat_id, text):
    url = f"{TELEGRAM_URL}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
