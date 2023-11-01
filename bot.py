from pyrogram import Client, filters
import re
import nltk
import random
import os
from threading import Thread
from flask import Flask

# nltk
nltk.download("words")

API_ID = os.environ.get("API_ID") 
API_HASH = os.environ.get("API_HASH") 
SESSION = os.environ.get("SESSION")

# Bot
app = Client(
    "word9",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION
)

# flask server
server = Flask(__name__)

# flask home route
@server.route("/")
def home():
    return "I'm alive"

# Regular expressions to match the criteria
starting_letter_pattern = r"start with ([A-Z])"  #Your word must start with S and include at least 10 letters
min_length_pattern = r"include at least (\d+) letters"
time_limit_pattern = r"You have (\d+)s to answer."
trigger_pattern = r"Turn: ᖇᗩᕼᑌᒪ"


@app.on_message(filters.me & filters.command("start", prefixes="."))
async def start(client, message):
    await message.edit("Hi, I can play word9 game with you")

@app.on_message(filters.text)
def handle_incoming_message(client, message):
    puzzle_text = message.text

    # Check if the trigger pattern is found in the puzzle text
    if re.search(trigger_pattern, puzzle_text):
        starting_letter_match = re.search(starting_letter_pattern, puzzle_text)
        min_length_match = re.search(min_length_pattern, puzzle_text)
        time_limit_match = re.search(time_limit_pattern, puzzle_text)

        if starting_letter_match and min_length_match and time_limit_match:
            starting_letter = starting_letter_match.group(1)
            min_length = int(min_length_match.group(1))

            english_words = set(nltk.corpus.words.words())

            valid_words = [word for word in english_words if word.startswith(starting_letter) and len(word) >= min_length]

            if valid_words:
                random_word = random.choice(valid_words)

                response_message = f"{random_word}"
                client.send_message(message.chat.id, response_message)
            else:
                client.send_message(message.chat.id, "No valid words found for the given criteria.")
        else:
            print("Criteria not found in the puzzle text.")
    return
    

def run():
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 8080)))

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    app.run()