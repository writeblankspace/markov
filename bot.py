import os
import sqlite3

import discord
from dotenv import load_dotenv

import modules.blagh
import modules.train

# Get the discord token from .env
load_dotenv()
DISCORD_TOKEN: str | None = os.getenv("DISCORD_TOKEN")
assert DISCORD_TOKEN, "DISCORD_TOKEN must be set."

# Connect to Discord
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# Connect to the database
con = sqlite3.connect("markov.db")
cur = con.cursor()  # create a db cursor

# Initialize db
# Consult the README for a detailed explanation of the tables
cur.execute("""
    CREATE TABLE IF NOT EXISTS Chain (
        word1 TEXT,
        word2 TEXT,
        next TEXT,
        freq INTEGER DEFAULT 1,
        CONSTRAINT pk_Chain PRIMARY KEY (word1, word2, next)
    ); """)
# Note that word1 < word2, i.e. the words must be in alphabetical order (A < B)
cur.execute("""
    CREATE TABLE IF NOT EXISTS Response (
        word1 TEXT,
        word2 TEXT,
        next TEXT,
        freq INTEGER DEFAULT 1,
        CONSTRAINT pk_Response PRIMARY KEY (word1, word2, next),
        CONSTRAINT chk_Words CHECK (word1 < word2)
    ); """)

cur.close()


# Discord stuff
@client.event
async def on_ready():
    assert client.user
    print(f"> {client.user.id}: logged in")


# Requires #message_content intent
@client.event
async def on_message(message: discord.Message):
    assert client.user

    # Prevent training on its own messages
    if message.author == client.user:
        return

    if message.content.startswith("$test") or f"<@{client.user.id}>" in message.content:
        # Basic command
        blagh: str = modules.blagh.build([])
        if blagh:
            await message.channel.send(blagh)
        else:
            await message.channel.send("...")
    elif message.content != "":
        # Train on message
        modules.train.chain(message.content)


client.run(DISCORD_TOKEN)
