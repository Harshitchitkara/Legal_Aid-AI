import requests
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

OPENROUTER_API_KEY = "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"  # <-- Replace this with your actual key

@app.route("/", methods=["POST"])
def bot_reply():
    incoming_msg = request.values.get("Body", "").strip()
    print(f"Received message: {incoming_msg}")

    reply = "Sorry, I couldn't respond right now."

    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "openrouter/openai/gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a helpful legal aid assistant."},
                {"role": "user", "content": incoming_msg}
            ]
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", json=data, headers=headers)
        result = response.json()

        if "choices" in result:
            reply = result["choices"][0]["message"]["content"].strip()
        else:
            reply = "Sorry, no reply from AI."

    except Exception as e:
        print(f"[OpenRouter Error] {e}")
        reply = "Sorry, something went wrong."

    twilio_resp = MessagingResponse()
    twilio_resp.message(reply)
    return str(twilio_resp)
