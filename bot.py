from pyrogram import Client, filters
import re
import nltk
import random
import os
from threading import Thread
from flask import Flask
import config
# nltk
nltk.download("words")

API_ID = config.API_ID 
API_HASH = config.API_HASH
SESSION = config.STRING_SESSION

# Bot
app = Client(
    "word9",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION
)

server = Flask(__name__)

@server.route("/")
def home():
    return "Bot is running"

starting_letter_pattern = r"start with ([A-Z])"
min_length_pattern = r"include at least (\d+) letters"
trigger_pattern = r"Turn: shizukaroo.*" # Replace "ᖇᗩᕼᑌᒪ" with your own trigger pattern (Your telegram profile name)


@app.on_message(filters.me & filters.command("ping", prefixes="!"))
async def start(client, message):
    await message.edit("pong!")


@app.on_message(filters.text)
async def handle_incoming_message(client, message):
    print(69)
    puzzle_text = message.text
    print(70)
    if re.search(trigger_pattern, puzzle_text):
        starting_letter_match = re.search(starting_letter_pattern, puzzle_text)
        min_length_match = re.search(min_length_pattern, puzzle_text)

        if starting_letter_match and min_length_match:
            starting_letter = starting_letter_match.group(1)
            min_length = int(min_length_match.group(1))

            english_words = set(nltk.corpus.words.words())

            valid_words = [word for word in english_words if word.startswith(starting_letter) and len(word) >= min_length]

            if valid_words:
                random_word = random.choice(valid_words)

                response_message = f"{random_word}"
                await client.send_message(message.chat.id, response_message)
            else:
                print("i am out")
        else:
            print("ye wala nhi khelunga")
    return
    
    
def run():
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 8080)))

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    app.run()
