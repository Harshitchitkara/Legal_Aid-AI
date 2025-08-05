import openai
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

openai.api_key = "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"
openai.api_base = "https://openrouter.ai/api/v1"

@app.route("/", methods=["POST"])
def bot_reply():
    incoming_msg = request.values.get("Body", "").strip()
    print(f"Received message: {incoming_msg}")

    reply = "Sorry, I couldn't respond right now."

    try:
       client = openai.OpenAI(api_key="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")
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": incoming_msg}
    ]
)
 reply = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[OpenRouter Error] {e}")

    twilio_resp = MessagingResponse()
    twilio_resp.message(reply)
    return str(twilio_resp)
