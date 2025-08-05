import requests
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Your OpenRouter API Key
API_KEY = "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"  # 🔒 Replace with your actual key
API_URL = "https://openrouter.ai/api/v1/chat/completions"

@app.route("/", methods=["POST"])
def bot_reply():
    incoming_msg = request.values.get("Body", "").strip()
    print(f"Received message: {incoming_msg}")

    reply = "Sorry, no reply from AI."

    # Choose model and user message
    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful legal aid assistant. Answer briefly and clearly in simple language."},
            {"role": "user", "content": incoming_msg}
        ]
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(API_URL, json=data, headers=headers)
        result = response.json()
        print("API Response:", result)

        if "choices" in result:
            reply = result["choices"][0]["message"]["content"].strip()
        else:
            reply = "Sorry, no reply from AI."

    except Exception as e:
        print(f"[OpenRouter Error] {e}")
        reply = "Sorry, something went wrong."

    # Send the reply back to the user
    twilio_resp = MessagingResponse()
    twilio_resp.message(reply)
    return str(twilio_resp)

# For local testing only
if __name__ == "__main__":
    app.run(debug=True)
