import sqlite3
from enum import Enum

import f.sql


class Tables(Enum):
    CHAIN = "Chain"
    RESPONSE = "Response"


def connect() -> sqlite3.Connection:
    """
    Connects to the database using `sqlite3.connect()`.

    Using this allows the database filename to be changed in only one
    location."""

    return sqlite3.connect("markov.db")

def check_exists(
    table: Tables,
    word1: str | None,
    word2: str | None,
    next_word: str | None,
    existing_con: sqlite3.Connection | None = None,
) -> bool:
    """
    Checks if a record exists in the table.

    Uses an existing sqlite3 Connection if provided."""

    if not existing_con:
        # Connect to the db
        con = connect()
    else:
        con = existing_con

    cur = con.cursor()

    # Check if an existing record exists
    res: sqlite3.Cursor = cur.execute(
        f"""
        SELECT * FROM {table.name}
        WHERE {f.sql.eq("word1", word1)}
            AND {f.sql.eq("word2", word2)}
            AND {f.sql.eq("next", next_word)}""",
        f.sql.remove_none(word1, word2, next_word),
    )

    exists: bool = res.fetchone() is not None

    if not existing_con:
        # The connection was opened within this subroutine; close it
        con.close()

    return exists


def update(table: Tables, word1: str | None, word2: str | None, next_word: str | None):
    """
    Updates the chosen database."""

    # Connect to the db
    con = connect()
    cur = con.cursor()

    # Check if an existing record exists
    exists: bool = check_exists(table, word1, word2, next_word, con)

    if exists:
        # An existing record exists; update it
        cur.execute(
            f"""
            UPDATE {table.name}
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
            INSERT INTO {table.name}(word1, word2, next)
            VALUES(?, ?, ?)""",
            (word1, word2, next_word),
        )

    con.commit()
    con.close()
