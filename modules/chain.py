import sqlite3
import re
from typing import List, Union
import f.sql


def update_db(word1: str | None, word2: str | None, next_word: str | None):
    """
    Updates the chain database."""

    # Connect to the db
    con = sqlite3.connect("markov.db")
    cur = con.cursor()

    # Check if an existing record exists
    res: List[tuple] = cur.execute(
        f"""
        SELECT * FROM Chain
        WHERE {f.sql.eq("word1", word1)}
            AND {f.sql.eq("word2", word2)}
            AND {f.sql.eq("next", next_word)}""",
        f.sql.remove_none(word1, word2, next_word)
    )
    
    if res.fetchone():
        # An existing record exists; update it
        cur.execute(
            f"""
            UPDATE Chain
            SET freq = freq + 1
            WHERE {f.sql.eq("word1", word1)}
                AND {f.sql.eq("word2", word2)}
                AND {f.sql.eq("next", next_word)}""",
            f.sql.remove_none(word1, word2, next_word)
        )
    else:
        # Create a new record
        cur.execute("""
            INSERT INTO Chain(word1, word2, next)
            VALUES(?, ?, ?)""", (word1, word2, next_word))

    con.commit()
    con.close()


def train(data: str):
    """
    Parses the data and adds it to the database."""

    data_list: List[str | None] = data.split() # split data by whitespace

    # To make our lives easier. See README
    data_list.insert(0, None)
    data_list.insert(0, None)
    data_list.append(None)

    # Start at the first not-None item, i.e. index 2
    for i in range(2, len(data_list)):

        # Sanitise user, role and everyone mentions
        if re.fullmatch(r"<@&?\d{0,20}>|@everyone", data_list[i] if data_list[i] else ""):
            data_list[i] = "@mention"

        # Add the word to the database
        update_db(
            data_list[i - 2],
            data_list[i - 1],
            data_list[i]
        )