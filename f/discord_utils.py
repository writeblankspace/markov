import discord


async def get_replied_message(message: discord.Message) -> discord.Message | None:
    # Get the message that the message is replying to, if any
    replied_message: discord.Message | None

    if message.type == discord.MessageType.reply:
        assert message.reference  # because it is a reply
        replied_message_id: int | None = message.reference.message_id

        assert replied_message_id
        # It is not None in this case, because message is a reply
        # https://discordpy.readthedocs.io/en/stable/api.html?highlight=reply#discord.MessageReference.message_id

        replied_message = await message.channel.fetch_message(replied_message_id)
    else:
        replied_message = None

    return replied_message
