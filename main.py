from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests

app = Flask(__name__)


API_KEY = "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"

@app.route("/", methods=["POST"])
def bot_reply():
    incoming_msg = request.values.get("Body", "").strip()
    print(f"Received message: {incoming_msg}")

    # Default reply in case something breaks
    reply = "Sorry, I couldn't respond right now."

    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "openrouter/openai/gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a helpful legal advisor chatbot that gives legal aid in easy terms."},
                {"role": "user", "content": incoming_msg}
            ]
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", json=data, headers=headers)

        if response.status_code == 200:
            reply = response.json()["choices"][0]["message"]["content"].strip()
        else:
            print("OpenRouter Error:", response.text)
            reply = "Sorry, something went wrong with the AI."

    except Exception as e:
        print(f"[Error] {e}")
        reply = "Sorry, there was an error."

    twilio_resp = MessagingResponse()
    twilio_resp.message(reply)
    return str(twilio_resp)
