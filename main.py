import requests
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

@app.route("/", methods=["POST"])
def bot_reply():
    incoming_msg = request.values.get("Body", "").strip()
    print(f"Received message: {incoming_msg}")

    reply = "Sorry, no reply from AI."

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful legal aid assistant. Reply in simple, non-technical language suitable for everyone."
            },
            {
                "role": "user",
                "content": incoming_msg
            }
        ]
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://legal-aid-ai.onrender.com",  # 🔁 Your actual domain!
        "X-Title": "Whatsapp Legal Bot"
    }

    try:
        response = requests.post(API_URL, json=data, headers=headers)
        result = response.json()
        print("API Response:", result)

        if "choices" in result:
            reply = result["choices"][0]["message"]["content"].strip()
        else:
            reply = "AI didn't reply. Please try again later."

    except Exception as e:
        print(f"[OpenRouter Error] {e}")
        reply = "Something went wrong while contacting AI."

    twilio_resp = MessagingResponse()
    twilio_resp.message(reply)
    return str(twilio_resp)

if __name__ == "__main__":
    app.run(debug=True)
