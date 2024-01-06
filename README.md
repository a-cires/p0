# P0: GroupMe Bot

## Due: uhhh, last day of classes?

## Overview

- create a GroupMe bot that will be able to read/respond to messages in a GroupMe chat

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
SENDER_ID=""  # Obtain using --config flag
BOT_SENDER_ID=""  # Obtain using --config flag
DEBUG="False"
NO_SEND="False"
RESPOND_ALL="False"
SELF_REPLY="False"
```

- `BOT_ID` is the id of your bot, you can find this on the [dev page](https://dev.groupme.com/bots)
- This is file is what is loaded in [`bot.py`](./groupme-bot/bot.py#L7) via the `load_dotenv()` function

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

## Tasks

We have provided you with an outline of the bot in [`bot.py`](./groupme-bot/bot.py) that is able to read/send messages to the GroupMe chat. Your task is to implement the following features:

- [x] respond to you
  - you should be able to run your script and send a message in the GroupMe chat and have your bot respond to you and **only you**, meaning that if someone else sends the same message, **even with the same name**, your bot should not respond to them
    - hint: look at the [`sample.json`](./groupme-bot/sample.json) that shows what other fields you can extract from a response (i.e. `sender_id`)
    - you can view the contents of a response itself by printing `response.json().get("response", {})` located [here](./groupme-bot/bot.py#L31)(this is what is inside the `response` field of the `sample.json` file)
- [x] good morning/good night
  - if _anyone_ says good morning/good night, your bot should respond with a good morning/good night with their name
    - i.e. if someone says "good morning", your bot should respond with "good morning, <name>"
    - think about how you're going to stop your bot from responding to itself and the other bots in the chat
    - **caution:** if you start spamming the chat, please `ctrl+c` your script to stop it
    - feel free to mute the chat, we will use piazza for any important announcements
- [x] create 1 (or more, for extra-credit) additional features that you think would be cool
  - you may incorporate other API's (i.e. [Giphy](https://developers.giphy.com/docs/api/endpoint#search))
  - you can have the bot perhaps have tell the weather of a particular city
- [x] create a doc (markdown, `*.md` file) that outlines the features of your bot, how to run it
  - please put this file in the [`groupme-bot`](./groupme-bot) folder and name it `README.md`
  - refer to markdown syntax [here](https://www.markdownguide.org/basic-syntax/)

## Running

```bash
# activate virtual environment
source venv/bin/activate # for mac/linux
venv\Scripts\activate # for windows

# run bot
python3 bot.py --config "Your Groupme Name" # outputs SENDER_ID and BOT_SENDER_ID

# Store given SENDER_ID and BOT_SENDER_ID from --config flag into .env to skip --config in the future
python3 bot.py  # runs using .env variables
```

### Flags

Usage: `python3 bot.py [OPTION]`

Options:
`python3 bot.py --help` Display help message
`python3 bot.py --config "Respondent Name"` Configures the chatbot to respond to the person whos name is specified. Can be the bot itself
`python3 bot.py --test` Test the bot by sending a message to the group
`python3 bot.py --debug` Print debug messages
`python3 bot.py --respondall` Causes the bot to respond to all users. Good morning/good night works as expected
`python3 bot.py --nosend` Prohibits the bot from sending messages to the chat. Best used with --debug
`python3 bot.py --self-reply` Allows the bot to respond to itself. Warning: This option may get weird

## Submission

as you complete tasks, edit **this** markdown file to reflect your progress. if you have completed something just put an "x" in the checkbox. here's an example:

- [ ] respond to you (not done)
- [x] respond to you (done)

once you are done, commit your changes and push to your forked repo

```bash
# adds all files that have been changed in the current directory
git add .
# commit changes with message "completed p0" (you can change this to whatever you want)
git commit -m "completed p0"
# if this is your first time pushing, you'll need to set the upstream branch
git push --set-upstream origin main
# otherwise, you can just push
git push
```

then, on gradescope submit a `submission.txt` file that has the following contents:

```
username
repo
```

where `username` is your github username and `repo` is the name of your forked repo (i.e. `p0`)
