import sqlite3
from enum import Enum

import f.sql


class Databases(Enum):
    CHAIN = "Chain"
    RESPONSE = "Response"


def update(
    db: Databases, word1: str | None, word2: str | None, next_word: str | None
):
    """
    Updates the chosen database."""

    db_name: str = db.name

    # Connect to the db
    con = sqlite3.connect("markov.db")
    cur = con.cursor()

    # Check if an existing record exists
    res: sqlite3.Cursor = cur.execute(
        f"""
        SELECT * FROM {db_name}
        WHERE {f.sql.eq("word1", word1)}
            AND {f.sql.eq("word2", word2)}
            AND {f.sql.eq("next", next_word)}""",
        f.sql.remove_none(word1, word2, next_word),
    )

    if res.fetchone():
        # An existing record exists; update it
        cur.execute(
            f"""
            UPDATE {db_name}
            SET freq = freq + 1
            WHERE {f.sql.eq("word1", word1)}
                AND {f.sql.eq("word2", word2)}
                AND {f.sql.eq("next", next_word)}""",
            f.sql.remove_none(word1, word2, next_word),
        )
    else:
        # Create a new record
        cur.execute(
            f"""
            INSERT INTO {db_name}(word1, word2, next)
            VALUES(?, ?, ?)""",
            (word1, word2, next_word),
        )

    con.commit()
    con.close()
