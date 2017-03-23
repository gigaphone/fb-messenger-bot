# -*- coding: utf8 -*-

#import bot
#print "done bot import"
#from bot import get_bot
#from chatterbot import ChatBot

import json
import os
import sys
import traceback

import requests
from flask import Flask, request

print "done all imports"

app = Flask(__name__)

print "assigned flask to app"

#needs try catch
f = open('answers.json')
answers = json.load(f)
f.close()

f = open('qa.json')
qa_dict = json.load(f)
f.close()


import distance
def answer(message):
    message = message.lower()
    try:
        count = 0
        smallest_distance = 999
        closest_key = ""
        closest_word = ""

        for word in message.split():
            count += 1
            if len(word) < 3 or word == 'beli':
                continue

            for key in qa_dict.keys():
                current_distance = distance.levenshtein(key, word)
                #print "distance: " + str(current_distance)
                if current_distance < smallest_distance:
                    closest_key = key
                    closest_word = word
                    smallest_distance = current_distance
            if count > 10:
                #print 1
                #log_wrapper("no words in first 11 match - going for the best one")
                break
            if smallest_distance < 2:
                #print 2
                #log_wrapper("found the best one after " + str(count) + " tries." )
                break
        if closest_key == "":
            closest_key = "belo"

        log_wrapper("::".join([str(closest_key), str(closest_word), str(smallest_distance)]))

        return answers[qa_dict[closest_key]]

    except:
        log_wrapper(traceback.print_exc())
        return "#samojakobot"


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
                    try:
                        sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                        recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                        message_text = "jako" if "text" not in messaging_event["message"] else messaging_event["message"]["text"] # the message's text

                        bot_reply =  answer(message_text.encode('utf-8'))

                        log_wrapper(bot_reply.encode('utf-8'))

                        send_message(sender_id, bot_reply.encode('utf-8'))
                    except:
                        log_wrapper("Could not answer due to error")
                        log_wrapper(traceback.print_exc())

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
    try:
        print str(message)
        sys.stdout.flush()
    except:
        print traceback.print_exc()


if __name__ == '__main__':
    print "Going into main"
    app.run(debug=False)

