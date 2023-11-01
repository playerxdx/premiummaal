from pyrogram import Client, filters
import re
import nltk
import random
import os
from threading import Thread
from flask import Flask


nltk.download("words")

API_ID = os.environ.get("API_ID") 
API_HASH = os.environ.get("API_HASH") 
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Bot
app = Client(
    "word9",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# flask server
server = Flask(__name__)

# flask home route
@server.route("/")
def home():
    return "I'm alive"


# Regular expressions to match the criteria
starting_letter_pattern = r"start with ([A-Z])"
min_length_pattern = r"include at least (\d+) letters"
time_limit_pattern = r"You have (\d+)s to answer."
game_start_pattern = r"A classic game is starting."
your_turn_pattern = r"Turn: ()"

@app.on_message(filters.text)
def handle_incoming_message(client, message):
    puzzle_text = message.text

    starting_letter_match = re.search(starting_letter_pattern, puzzle_text)
    min_length_match = re.search(min_length_pattern, puzzle_text)
    time_limit_match = re.search(time_limit_pattern, puzzle_text)

    if re.search(game_start_pattern, puzzle_text):
        client.send_message(message.chat.id, "/join")
        return

    if re.search(your_turn_pattern, puzzle_text):
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