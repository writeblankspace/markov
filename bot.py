import os
import sqlite3

import discord
from dotenv import load_dotenv

import f.discord_utils
import modules.blagh
import modules.response
import modules.training

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

    # Change presence of bot
    activity = discord.Activity(
       type = discord.ActivityType.watching,
       name = f"Ping me! @{client.user.name}",
       state = modules.blagh.build([], censor=True)
    )

    await client.change_presence(activity=activity)


# Requires #message_content intent
@client.event
async def on_message(message: discord.Message):
    assert client.user

    # Prevent training on its own messages
    if message.author == client.user:
        return

    # Get the message that the message is replying to, if any
    replied_message: discord.Message | None
    replied_message = await f.discord_utils.get_replied_message(message)

    # Set the flag for whether or not the bot's triggers are invoked
    triggered: bool = False

    if f"<@{client.user.id}>" in message.content:
        # The bot was mentioned
        triggered = True
    elif replied_message and replied_message.author.id == client.user.id:
        # The bot was replied to
        triggered = True

    # TODO: put all these into functions
    if triggered:
        await message.channel.typing()

        msg_str: str = message.content

        if msg_str.startswith(f"<@{client.user.id}>"):
            # Get rid of mention, plus leading whitespace
            msg_str = msg_str.replace(f"<@{client.user.id}>", "", count=1).lstrip()

        # Pick out start words
        start_words = modules.response.pick_response_start_words(invoking_str=msg_str)

        # Build-a-blagh
        blagh: str = modules.blagh.build(start_words, censor=True)

        if blagh:
            await message.reply(blagh, allowed_mentions=discord.AllowedMentions.none())
        else:
            await message.reply("...")

    elif message.content != "":
        # Train on message (with mentions cleaned)
        modules.training.train_chain(message.clean_content)

        if replied_message:
            # This is in reply to something
            # So we can train the bot how to respond to messages

            modules.training.train_response(
                invoking_str=replied_message.clean_content,
                response_str=message.clean_content,
            )


client.run(DISCORD_TOKEN)
