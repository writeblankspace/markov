import re

import f.important_words
from f import db


def chain(data_str: str):
    """
    Parses the message data and adds it to the Chain database."""

    # I don't want to fill the database with empty strings
    if data_str == "":
        return

    data_list: list[str | None] = []
    data_list.extend(data_str.split())  # split data by whitespace

    # To make our lives easier. See README
    data_list.insert(0, None)
    data_list.insert(0, None)
    data_list.append(None)

    # Start at the first not-None item, i.e. index 2
    for i in range(2, len(data_list)):
        # Sanitise user, role and everyone mentions
        if re.fullmatch(pattern=r"<@&?\d{0,20}>|@everyone", string=data_list[i] or ""):
            data_list[i] = "@mention"

        # Add the word to the database
        db.update(
            table=db.Tables.CHAIN,
            word1=data_list[i - 2],
            word2=data_list[i - 1],
            next_word=data_list[i],
        )


def response(invoking_str: str, response_str: str):
    """
    Adds stuff to the Response database.

    I can't even explain it..."""

    # I don't want empty strings!
    if invoking_str == "" or response_str == "":
        return

    # I'm hungry; I want Jollibee® ChickenJoy™
    # Not sponsored by Jollibee®

    # Extract the important words from the invoking_str
    important_words: list[str | None] = []
    important_words.extend(
        f.important_words.extract(invoking_str, 5, sort_alphabetically=True)
    )

    # Get the first two words from response_str
    response: str = " ".join(response_str.split(" ")[:2])

    # We need at least word1 and word2
    if len(important_words) < 2:
        # Fill important_words with None until we get the desired length
        for _ in range(2 - len(important_words)):
            important_words.append(None)

    # Make a database entry for every combination of the first 5 important words
    # 5C2 = 10 (from 5 choose 2, there are 10 possible combinations)
    # Who knew I would apply permutations and combinations here?

    # The best way to do this is to loop through each item,
    # then do a sub-loop through each item that comes after it.
    # So for a sequence [A, B, C, D, E], we get:
    # AB, AC, AD, AE, BC, BD, BE, CD, CE, DE

    # Loops from A to D in example
    for i, word1 in enumerate(important_words[: len(important_words) - 1]):
        # Loops from B to E in example, when i = 0
        for word2 in important_words[i + 1 :]:
            # important_words is sorted alphabetically
            # and the TABLE Response has a constraint to ensure word1 < word2
            # so we needn't worry about different permuations existing
            db.update(
                table=db.Tables.RESPONSE,
                word1=word1,
                word2=word2,
                next_word=response
            )

    # TODO: continue this.
