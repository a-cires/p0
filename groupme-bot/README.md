# P0: GroupMe Bot -- ROBOTTO v2

## Overview

- GroupMe bot that reads and responds to messages in a GroupMe chat

## Pre-Requisites

- `python3` installed
  - see [here](https://www.python.org/downloads/) for download
- GroupMe:
  - account, sign up [here](https://groupme.com/en-US/register)
  - bot, see how to create one [here](https://dev.groupme.com/tutorials/bots)
    - you'll need an access token, it's basically just top right of the dev page
    - you'll need to use method 2 to get a BOT_ID
  - class GroupMe, join [here](https://groupme.com/join_group/98324520/GpX1Owv6)
- OpenAI:
  - account, sign up [here](https://auth0.openai.com/u/login/identifier?state=hKFo2SBKY1BEMjJkMUtRWTJudWpoX0VFRFJ5UDJEV0N1SFlONqFur3VuaXZlcnNhbC1sb2dpbqN0aWTZIDhpQXZXcl93czJFdWswOVF2TlhNQ2VQaUVCXy1QR2xKo2NpZNkgRFJpdnNubTJNdTQyVDNLT3BxZHR3QjNOWXZpSFl6d0Q)
  - Choose API Keys on the left
  - Select "+ Create new secret key"
  - Name the key (ex. "GroupMe Robotto key") and copy/paste the key into a .env file
    - The variable name for the OpenAI key must be named OPENAI_API_KEY in your .env file
    - Ex. OPENAI_API_KEY="your API key"

## Setup

1. Fork te repo to your own account
   - on this repo, click the fork button in the top right
   - ensure that when you fork, it is public, otherwise we won't be able to see your submission
2. Set up your `.env` file based on your GroupMe information and OpenAI key. You just create a file called `.env` to represent your environment variables. Here is a template for your `.env` file:

```bash
BOT_ID=""
GROUP_ID="98324520" # our GroupMe chat id
ACCESS_TOKEN=""
OPENAI_API_KEY=""
SENDER_ID=""  # Obtain using --config flag, ID of person the bot will respond to
BOT_SENDER_ID=""  # Obtain using --config flag, ID of the bot
DEBUG="False"
NO_SEND="False"
RESPOND_ALL="False"
SELF_REPLY="False"
```

- `BOT_ID` is the id of your bot, you can find this on the [dev page](https://dev.groupme.com/bots)
- `BOT_SENDER_ID` and `SENDER_ID` are both obtained from running the program with the `--config` flag
  - `python3 bot.py --config "Target User Name"` will override the .env variable (or lack thereof), but will not write to .env
- `SENDER_ID` is the sender_id of the person to whom the bot is supposed to reply to
- This file is what is loaded in [`bot.py`](./groupme-bot/bot.py#L7) via the `load_dotenv()` function

```bash
# clone the **forked** repo to your local machine and cd into it
git clone https://github.com/<your-username>/p0.git && cd p0

# create virtual environment (this creates a folder called venv)
python3 -m venv venv

# activate virtual environment
source venv/bin/activate # for mac/linux
venv\Scripts\activate # for windows


# install dependencies
pip install -r requirements.txt
```

To deactivate the virtual environment, run `deactivate`

## Running

```bash
# activate virtual environment
source venv/bin/activate # for mac/linux
venv\Scripts\activate # for windows

# run bot for the first time
python3 bot.py --config "Your Groupme Name" # outputs SENDER_ID and BOT_SENDER_ID, configures bot to respond to user with the given name

# Store given SENDER_ID and BOT_SENDER_ID from --config flag into .env to skip --config in the future
python3 bot.py  # runs using .env variables
```

### Flags

Usage: `python3 bot.py [OPTION]`

Options:
`python3 bot.py --help` Display help message (more information than given here)
`python3 bot.py --config "Respondent Name"` Configures the chatbot to respond to the person whos name is specified. Can be the bot itself
`python3 bot.py --test` Test the bot by sending a message to the group
`python3 bot.py --debug` Print debug messages
`python3 bot.py --respondall` Causes the bot to respond to all users. Good morning/good night works as expected
`python3 bot.py --nosend` Prohibits the bot from sending messages to the chat. Best used with --debug
`python3 bot.py --self-reply` Allows the bot to respond to itself. Warning: This option may get weird

### Bot Abilities

- Anyone who says "Good morning" or "Good night" is responded to by Robotto with "Good morning/night" followed by their name
  - The "Good morning/night" message can be anywhere in the message
  - Ex. "Good morning" is responded to by Robotto as "Good morning, UserName!"
- Messages writen by the configured user (see --config flag) are responded to with wit and sarcasm
  - If the --respondall flag is passed in or set as true in .env then Robotto will respond like this to any user message
  - If either the self-reply flag (or .env variable) or "Robotto v2" is specified as the target in --config then Robotto will respond to itself. This can lead to some wacky (and expensive) dialogue!
- Sending a message containing the text "let's go to sleep" as the configured user will cause the program to exit (Robots need their beauty sleep too!).
