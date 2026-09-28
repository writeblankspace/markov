import sqlite3

import f.misc
import f.sql


def get_next(word1: str | None, word2: str | None) -> str | None:
    # Connect to the db
    con = sqlite3.connect("markov.db")
    cur = con.cursor()

    # Get possible next words from the db
    # If word1 is also a match, triple the frequency
    res: sqlite3.Cursor = cur.execute(
        f"""
        SELECT
            next,
            IF({f.sql.eq("word1", word1)}, freq*3, freq)
        FROM Chain
        WHERE {f.sql.eq("word2", word2)}""",
        f.sql.remove_none(word1, word2),
    )

    # Pick a random next word
    next_word: str | None = f.misc.pick_rand_weighted(
        iterable=res.fetchall(), get_weight=lambda x: x[1], get_out=lambda x: x[0]
    )

    con.close()  # close db connection
    return next_word


def build(start_words: list[str | None]) -> str:
    """
    Builds a blagh which starts with `start_words`."""

    # See README to see what a blagh is
    blagh: list[str | None] = start_words

    # To make our lives easier. See README
    blagh.insert(0, None)
    blagh.insert(0, None)

    # Points to the word to be added
    n: int = len(blagh)
    next_word: str | None = ""

    # Keep making the blagh until the next word is None
    while next_word != None:
        next_word = get_next(blagh[n - 2], blagh[n - 1])

        if next_word:
            blagh.append(next_word)

        n += 1

    # We have a blagh!
    return " ".join([x if x else "" for x in blagh])
