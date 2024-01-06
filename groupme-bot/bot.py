import requests
import time
import json
import os
import sys
import re
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
BOT_ID = os.getenv("BOT_ID")
GROUP_ID = os.getenv("GROUP_ID")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
SENDER_ID = os.getenv("SENDER_ID")
LAST_MESSAGE_ID = None
DEBUG = os.getenv("DEBUG", "").lower() == "true"
RESPOND_ALL = os.getenv("RESPOND_ALL", "").lower == "true"
BOT_SENDER_ID = os.getenv("BOT_SENDER_ID")
NO_SEND = os.getenv("NO_SEND", "").lower() == "true"
SELF_REPLY = os.getenv("SELF_REPLY", "").lower() == "true"


def send_message(text, attachments=None):
    global DEBUG
    global NO_SEND
    """Send a message to the group using the bot."""
    post_url = "https://api.groupme.com/v3/bots/post"
    pattern = r'^.*?:\s'
    text = re.sub(pattern, '', text)
    data = {"bot_id": BOT_ID, "text": text, "attachments": attachments or []}
    if DEBUG:
        print("Sending message...")
        print(data)
    if not NO_SEND:
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
    global DEBUG
    global SELF_REPLY
    """Process and respond to a message."""
    global LAST_MESSAGE_ID
    text = message["text"].lower()
    if DEBUG:
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
    # Skip bot good morning/good night
    elif "good morning" in text or "good night" in text:
        pass
    # Personal response
    elif message["sender_id"] == SENDER_ID:
        response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=convert_messages(messages))
        send_message(response.choices[0].message.content)
        if "let's go to sleep" in text.lower():
            return True
    # Respond to all messages
    elif RESPOND_ALL and message["sender_type"] == "user":
        response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=convert_messages(messages))
        send_message(response.choices[0].message.content)
    elif message["sender_id"] == BOT_SENDER_ID and SELF_REPLY:
        response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=convert_messages(messages))
        send_message(response.choices[0].message.content)

    LAST_MESSAGE_ID = message["id"]
    return False


def convert_messages(messages):
    global BOT_SENDER_ID
    global SELF_REPLY
    converted = [{"role": "system", "content": "You are a witty and sarcastic chatbot named Robotto v2. You send VERY SHORT one-liners."}]
    for message in reversed(messages):
        if message['sender_id'] == BOT_SENDER_ID:
            if SELF_REPLY:
                role = "user"
                content = f"{message['name']}: {message['text']}"
            else:
                role = "assistant"
                content = message['text']
        else:
            role = "user"
            content = f"{message['name']}: {message['text']}"
        converted.append({"role": role, "content": content})
    return converted


def main():
    global LAST_MESSAGE_ID
    global DEBUG
    global RESPOND_ALL
    global SENDER_ID
    global BOT_SENDER_ID
    global NO_SEND
    global SELF_REPLY
    first = True
    found_user = False

    argn = len(sys.argv)
    if argn > 1:
        for i in range(1, argn):
            if sys.argv[i] == "--help":
                print(
"""Usage: python3 bot.py [OPTION]\n\nOptions:
\t--help\t\t\tDisplay this help message
\t--config \"GroupMe Name\"\tPrints sender_id of specified person and configures bot to respond to them
\t\t\t\tPerson must have sent a recent message in the group
\t\t\t\tHint: Add this to your .env file as SENDER_ID=##### to skip this step next time.
\t--debug\t\t\tPrint debug messages
\t--test\t\t\tTest the bot by sending a message to the group
\t--respondall\t\tBot responds to anyone in the group. good morning/good night works as expected
\t--nosend\t\tProhibits bot from sending messages. Best used with --debug
\t--self-reply\t\tAllows the bot to respond to itself. Warning: This may get weird.

Hint: You can also add these options to your .env file as DEBUG=True, RESPOND_ALL=True, NO_SEND=True, SENDER_ID=#####, etc. to skip this step next time.
Hint: Try running python3 bot.py --config \"Robotto v2\" for some wacky fun.""")
                return
            elif sys.argv[i] == "--test":
                print("Testing bot...")
                send_message("Hello, some TA is pushing my buttons right now.")
            elif sys.argv[i] == "--debug":
                print("Debug mode enabled.")
                DEBUG = True
            elif sys.argv[i] == "--respondall":
                print("Warning: Responding to all messages in the group may use up your OpenAI API credits.")
                RESPOND_ALL = True
            elif sys.argv[i] == "--config":
                if i + 1 < argn:
                    name = sys.argv[i + 1]
                    print(f"Getting sender_id for {name}...")
                    messages = get_group_messages()
                    for message in reversed(messages):
                        if message['name'] == name:
                            print(f"sender_id for {name} is {message['sender_id']}")
                            print(f"Configuring bot to respond to {name}.")
                            print(f"Hint: Add this to your .env file as SENDER_ID={message['sender_id']} to skip this step next time.")
                            found_user = True
                            SENDER_ID = message['sender_id']

                            # Configuring BOT_SENDER_ID
                            print("Getting BOT_SENDER_ID...")
                            send_message("Beep boop. Coming online...")
                            messages = get_group_messages()
                            for message in reversed(messages):
                                if message['sender_type'] == "bot" and message['text'] == "Beep boop. Coming online...":
                                    print(f"BOT_SENDER_ID is {message['sender_id']}")
                                    print(f"Hint: Add this to your .env file as BOT_SENDER_ID={message['sender_id']} to skip this step next time.")
                                    BOT_SENDER_ID = message['sender_id']
                                    break
                            if BOT_SENDER_ID == SENDER_ID:
                                print("Warning: BOT_SENDER_ID is the same as SENDER_ID. This may get weird.")
                                SELF_REPLY = True
                            break
                    if not found_user:
                        print(f"Error: {name} has not recently sent a message in the group. Defaulting to .env SENDER_ID.")

                else:
                    print("Error: No name specified.")
                    return
            elif sys.argv[i] == "--nosend":
                print("Warning: Bot will not send messages.")
                NO_SEND = True
            elif sys.argv[i] == "--self-reply":
                print("Warning: Bot will respond to itself. This may get weird.")
                SELF_REPLY = True
                
    if not found_user:
        SENDER_ID = os.getenv("SENDER_ID")
        if SENDER_ID == None:
            print("Error: No SENDER_ID specified in .env file. Please run bot.py with the --config option.")
            return
        
    if DEBUG:
        print("DEBUG: " + str(DEBUG))
        print("SENDER_ID: " + SENDER_ID)
        print("BOT_SENDER_ID: " + BOT_SENDER_ID)
        print("Self-reply: " + str(SELF_REPLY))
        print("RESPOND_ALL: " + str(RESPOND_ALL))
        print("NO_SEND: " + str(NO_SEND))

    # this is an infinite loop that will try to read (potentially) new messages every 10 seconds, but you can change this to run only once or whatever you want
    while True:
        if DEBUG: 
            print("Checking for new messages...")
        messages = get_group_messages(LAST_MESSAGE_ID)
        if first:
            LAST_MESSAGE_ID = messages[0]["id"] if messages else None
            LAST_MESSAGE_ID = messages[1]["id"] if BOT_SENDER_ID == SENDER_ID else LAST_MESSAGE_ID  # If bot configured to respond to itself, it'll start yapping
            first = False
        else:
            for message in reversed(messages):
                if process_message(message, messages):
                    return

        time.sleep(10)


if __name__ == "__main__":
    main()
