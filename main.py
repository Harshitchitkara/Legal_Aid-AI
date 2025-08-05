from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

API_KEY = "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"  

def ask_legal_bot(user_msg):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "You are a legal help assistant. Respond in simple English. Always say: 'I'm not a lawyer but I can help.'"
            },
            {"role": "user", "content": user_msg}
        ]
    }
    res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    return res.json()["choices"][0]["message"]["content"]

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    user_msg = request.form.get("Body")
    reply = ask_legal_bot(user_msg)

    response = MessagingResponse()
    response.message(reply)
    return str(response)

app.run(host="0.0.0.0", port=8080)
