import sqlite3

import f.important_words
import f.misc
import f.sql


def pick_response_start_words(invoking_str: str) -> list[str]:
    """
    Picks starting words for a response based on invoking_str."""

    # It's empty, so why bother?
    if invoking_str == "":
        return []

    # Extract important words from invoking_str
    important_words: list[str | None] = []
    important_words.extend(
        f.important_words.extract(invoking_str, 7, sort_alphabetically=True)
    )

    # We need at least word1 and word2
    if len(important_words) < 2:
        # Fill important_words with None until we get the desired length
        for _ in range(2 - len(important_words)):
            important_words.append(None)

    # We need to fetch records that contain any combination of important words

    # Connect to the db
    con = sqlite3.connect("markov.db")
    cur = con.cursor()

    # Get possible next words from the db
    #
    # For a particular match where word1Match and word2Match, weight = freq * 3
    # Otherwise (i.e. only one match), weight = freq
    #
    # Freq is

    res: sqlite3.Cursor = cur.execute(
        f"""
        WITH t AS (
            SELECT
                next,
                word1 IN ({f.sql.value_list(len(important_words))}) AS word1Match,
                word2 IN ({f.sql.value_list(len(important_words))}) AS word2Match,
                freq
            FROM Response
            WHERE word1Match OR word2Match
        )
        SELECT
            next,
            IF(MAX(word1Match & word2Match), SUM(freq) * 3, SUM(freq)) AS weight,
            SUM(freq)
        FROM t
        GROUP BY next, word1Match + word2Match""",
        important_words * 2,
    )

    res_list: list = res.fetchall() # in case I need to print() it

    start_words: str | None = f.misc.pick_rand_weighted(
        iterable=res_list, get_weight=lambda x: x[1], get_out=lambda x: x[0]
    )

    con.close()

    if start_words:
        return start_words.split(" ")
    else:
        return []
