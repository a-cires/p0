import requests
import time
import json
import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
BOT_ID = os.getenv("BOT_ID")
GROUP_ID = os.getenv("GROUP_ID")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
LAST_MESSAGE_ID = None


def send_message(text, attachments=None):
    global debug
    """Send a message to the group using the bot."""
    post_url = "https://api.groupme.com/v3/bots/post"
    data = {"bot_id": BOT_ID, "text": text, "attachments": attachments or []}
    if debug:
        print(data)
    response = requests.post(post_url, json=data)
    return response.status_code == 202


def get_group_messages(since_id=None):
    """Retrieve recent messages from the group."""
    params = {"token": ACCESS_TOKEN}
    if since_id:
        params["since_id"] = since_id

    get_url = f"https://api.groupme.com/v3/groups/{GROUP_ID}/messages"
    response = requests.get(get_url, params=params)
    if response.status_code == 200:
        # this shows how to use the .get() method to get specifically the messages but there is more you can do (hint: sample.json)
        return response.json().get("response", {}).get("messages", [])
    return []


def process_message(message, messages):
    global debug
    """Process and respond to a message."""
    global LAST_MESSAGE_ID
    text = message["text"].lower()
    if debug:
        print("Processing message...")
        print(f"\tsender_id: {message['sender_id']}")
        print(f"\tsender_name: {message['name']}")
        print(f"\tsender_type: {message['sender_type']}")
        print(f"\tMessage text: {text}")


    # Good morning
    if "good morning" in text and message["sender_type"] == "user":
        bot_message = "Good morning, {}!".format(message["name"])
        send_message(bot_message)
    # Good night
    elif "good night" in text and message["sender_type"] == "user":
        bot_message = "Good night, {}!".format(message["name"])
        send_message(bot_message)
    # Personal response
    elif message["sender_id"] == "54613132":
        response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=convert_messages(messages))
        send_message(response.choices[0].message.content)



    # i.e. responding to a specific message (note that this checks if "hello bot" is anywhere in the message, not just the beginning)
    if "hello bot" in text:
        send_message("sup")

    LAST_MESSAGE_ID = message["id"]

def convert_messages(messages):
    converted = [{"role": "system", "content": "You are a witty and sarcastic chatbot named Robotto. You send VERY SHORT one-liners."}]
    for message in reversed(messages):
        if message['sender_id'] == "883722":
            role = "assistant"
            content = message['text']
        else:
            role = "user"
            content = f"{message['name']}: {message['text']}"
        converted.append({"role": role, "content": content})
    return converted

def main():
    global LAST_MESSAGE_ID
    global debug
    first = True
    debug = False

    argn = len(sys.argv)
    if argn > 1:
        for i in range(1, argn):
            if sys.argv[i] == "--help":
                print("Usage: python3 bot.py [OPTION]\n\nOptions:\n\t--help\t\t\tDisplay this help message\n\t--test\t\t\tTest the bot by sending a message to the group\n\t--debug\t\t\tPrint debug messages")
                return
            elif sys.argv[i] == "--test":
                print("Testing bot...")
                send_message("Hello, some TA is pushing my buttons right now.")
            elif sys.argv[i] == "--debug":
                print("Debug mode enabled.")
                debug = True

    # this is an infinite loop that will try to read (potentially) new messages every 10 seconds, but you can change this to run only once or whatever you want
    while True:
        if debug: 
            print("Checking for new messages...")
        messages = get_group_messages(LAST_MESSAGE_ID)
        if first:
            for message in messages:
                LAST_MESSAGE_ID = message["id"]
                break
            first = False
        else:
            for message in reversed(messages):
                process_message(message, messages)
        time.sleep(10)


if __name__ == "__main__":
    main()
