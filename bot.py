import os
import sqlite3

import discord
from dotenv import load_dotenv

import modules.blagh
import modules.response
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

    # TODO: replying to bot also triggers
    if f"<@{client.user.id}>" in message.content:

        msg_str: str = message.clean_content

        if message.content.startswith(f"<@{client.user.id}>"):
            # Remove bot mention from clean_content
            display_name: str

            # Get its display name if in guild
            if message.guild:
                client_member: discord.Member | None = \
                    await message.guild.fetch_member(client.user.id)
                assert client_member
                display_name = client_member.display_name
            else:
                display_name = client.user.display_name

            # Get rid of mention, plus leading whitespace
            msg_str = msg_str.replace(f"@{display_name}", "", count=1).lstrip()

        # Pick out start words
        start_words = modules.response.pick_response_start_words(
            invoking_str = msg_str
        )

        # Build-a-blagh
        blagh: str = modules.blagh.build(start_words)

        if blagh:
            await message.reply(blagh)
        else:
            await message.reply("...")

    elif message.content != "":
        # Train on message (with mentions cleaned)
        modules.train.chain(message.clean_content)

        #TODO: enable by taking the previous message from another user

        if message.type == discord.MessageType.reply:
            # This is in reply to something
            # So we can train the bot how to respond to messages

            assert message.reference # because it is a reply
            invoker_msg_id: int | None = message.reference.message_id

            assert invoker_msg_id
            # It is not None in this case, because message is a reply
            # https://discordpy.readthedocs.io/en/stable/api.html?highlight=reply#discord.MessageReference.message_id

            invoker: discord.Message = \
                await message.channel.fetch_message(invoker_msg_id)

            modules.train.response(
                invoking_str=invoker.clean_content,
                response_str=message.clean_content
            )





client.run(DISCORD_TOKEN)
