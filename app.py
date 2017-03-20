# -*- coding: utf-8 -*-

#import bot
#print "done bot import"
from bot import get_bot

import os
import sys
import json

import requests
from flask import Flask, request

print "done all imports"

app = Flask(__name__)

print "assigned flask to app"

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log_wrapper(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = "" if "text" not in messaging_event["message"] else messaging_event["message"]["text"] # the message's text

                    bot_reply =  "meh"#bot.get_response(None)

                    send_message(sender_id, bot_reply)

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def send_message(recipient_id, message_text):

    log_wrapper("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log_wrapper(r.status_code)
        log_wrapper(r.text)


def log_wrapper(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()

# def run_server(dom):
#         _run_on_start("%s" % dom)
#         app.run(debug=True, use_reloader=False)

print "almost into main - name is " + __name__ 
if __name__ == '__main__':
    print "going into main"
    app.run(debug=True)

# if __name__ == '__main__':
#     if len(sys.argv) < 2:
#         raise Exception("Must provide domain for application execution.")
#     else:
#         DOM = sys.argv[1]
#         run_server(DOM)
