import re

from f import db


def train_chain(data: str):
    """
    Parses the data and adds it to the database."""

    data_list: list[str | None] = []
    data_list.extend(data.split())  # split data by whitespace

    # To make our lives easier. See README
    data_list.insert(0, None)
    data_list.insert(0, None)
    data_list.append(None)

    # Start at the first not-None item, i.e. index 2
    for i in range(2, len(data_list)):
        # Sanitise user, role and everyone mentions
        if re.fullmatch(
            pattern=r"<@&?\d{0,20}>|@everyone",
            string=data_list[i] or ""
        ):
            data_list[i] = "@mention"

        # Add the word to the database
        db.update(
            db = db.Databases.CHAIN,
            word1 = data_list[i - 2],
            word2 = data_list[i - 1],
            next_word = data_list[i]
        )
