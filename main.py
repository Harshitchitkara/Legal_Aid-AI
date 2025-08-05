import requests
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# ✅ Your actual OpenRouter API key (must be enabled and allowed to access the model)
API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

@app.route("/", methods=["POST"])
def bot_reply():
    incoming_msg = request.values.get("Body", "").strip()
    print(f"Received message: {incoming_msg}")

    reply = "Sorry, no reply from AI."

    # 🔧 Payload for OpenRouter
    data = {
        "model": "openai/gpt-3.5-turbo",  # ✅ You can test with "mistralai/mistral-7b" if needed
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a helpful legal aid assistant. "
                    "Reply concisely in simple, easy-to-understand language. "
                    "Avoid legal jargon. Give helpful answers that a common person can understand."
                )
            },
            {
                "role": "user",
                "content": incoming_msg
            }
        ]
    }

    # 🔐 Proper headers with required Referer and X-Title
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://legal-aid-ai.onrender.com",  # ✅ Use your actual Render domain
        "X-Title": "WhatsApp Legal Bot"  # Optional but recommended
    }

    # 🧠 Call OpenRouter
    try:
        response = requests.post(API_URL, headers=headers, json=data)
        result = response.json()
        print("API Response:", result)

        if "choices" in result:
            reply = result["choices"][0]["message"]["content"].strip()
        else:
            reply = "AI didn't respond. Please try again."

    except Exception as e:
        print(f"[OpenRouter Error] {e}")
        reply = "Something went wrong while contacting AI."

    # 💬 Send back to WhatsApp via Twilio
    twilio_resp = MessagingResponse()
    twilio_resp.message(reply)
    return str(twilio_resp)

# 🧪 Local testing only
if __name__ == "__main__":
    app.run(debug=True)
