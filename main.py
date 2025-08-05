from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def whatsapp_bot():
    incoming_msg = request.form.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()

    # Simple reply logic
    if 'hello' in incoming_msg:
        msg.body("Hi! I'm your Flask AI bot 😄")
    elif 'bye' in incoming_msg:
        msg.body("Goodbye 👋")
    else:
        msg.body("You said: " + incoming_msg)

    return str(resp)
