import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
SECRET = os.environ["SECRET"]


@app.route("/", methods=["GET"])
def home():
    return "TradingView Telegram Bot is running", 200


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "No JSON received"}), 400

    if data.get("secret") != SECRET:
        return jsonify({"error": "Invalid secret"}), 403

    message = data.get("message", "TradingView signal")

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    try:
        response = requests.post(
            url,
            json={
                "chat_id": CHAT_ID,
                "text": message
            },
            timeout=10
        )

        if response.ok:
            return jsonify({"status": "ok"}), 200

        return jsonify({
            "error": "Telegram API error",
            "details": response.text
        }), 500

    except requests.RequestException as e:
        return jsonify({
            "error": "Telegram request failed",
            "details": str(e)
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
