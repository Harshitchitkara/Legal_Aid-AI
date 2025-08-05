import requests
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Your OpenRouter API details
API_KEY = "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"  # 🔐 Replace with your actual OpenRouter API key
API_URL = "https://openrouter.ai/api/v1/chat/completions"

@app.route("/", methods=["POST"])
def bot_reply():
    incoming_msg = request.values.get("Body", "").strip()
    print(f"Received message: {incoming_msg}")

    reply = "Sorry, no response from AI."

    # The improved system prompt to ensure clear legal aid responses
    system_prompt = (
        "You are LegalBot, a legal aid assistant helping ordinary people. "
        "Always reply in easy-to-understand, non-technical Hindi + English mix. "
        "Avoid legal jargon. Keep replies short and helpful like a human legal advisor."
    )

    # Request payload
    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": incoming_msg}
        ]
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://legal-aid-ai.onrender.com",  # ✅ Must match your Render domain
        "X-Title": "LegalBot WhatsApp Assistant"              # Optional but good for tracking
    }

    try:
        response = requests.post(API_URL, json=data, headers=headers)
        result = response.json()
        print("API Response:", result)

        if "choices" in result and result["choices"]:
            reply = result["choices"][0]["message"]["content"].strip()
        else:
            reply = "AI didn't respond properly. Try again later."

    except Exception as e:
        print(f"[OpenRouter Error] {e}")
        reply = "Something went wrong contacting AI."

    twilio_resp = MessagingResponse()
    twilio_resp.message(reply)
    return str(twilio_resp)

# Only for local testing
if __name__ == "__main__":
    app.run(debug=True)
