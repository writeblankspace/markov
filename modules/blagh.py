import sqlite3
import random
from typing import List, Union
from collections.abc import Callable
import f.sql


def binary_search_cum_freq(cum_freqs: List[int], key: int) -> int | None:
    """
    Returns the index where `key` fits in for a sorted cumulative frequency list
    (i.e. `cum_freqs[i - 1] < key <= cum_freqs[i]`)
    
    Returns `None` if `key > cum_freqs[-1]`"""

    # Won't find key anywhere
    if key < 0 or key > cum_freqs[-1]:
        return None

    start: int = 0
    end: int = len(cum_freqs) - 1
    mid: int = (start + end) // 2

    def found(i: int) -> bool:
        if i == 0:
            # We can't check i - 1
            if key <= cum_freqs[i]:
                return True
        else:
            return key > cum_freqs[i - 1] and key <= cum_freqs[i]
    
    # We can't do i - 1 when i == 0
    # so it's easier to handle this separately
    if found(0):
        return 0

    # The basic binary search
    while start <= end:
        mid = (start + end) // 2

        if found(mid):
            # We have found it!
            return mid 
        elif key > cum_freqs[mid]:
            # Search the right of mid
            start = mid + 1
        elif key < cum_freqs[mid]:
            # Search the left of mid
            end = mid - 1
    
    # Not found; we shouldn't get this result if all went well
    raise Exception("This shouldn't happen.")


def pick_rand_weighted(iterable: List[tuple], 
        get_weight: Callable[[tuple], int], 
        get_out: Callable[[tuple], str] = lambda x: x) -> str | None:
    """
    Picks out a random element from `iterable`.
    Considers the weight (from `get_weight`).
    Outputs whatever is gotten from `get_out` from the tuple."""

    # If it's empty, there's nothing we can do
    if not iterable:
        return None
    
    # Get the cumulative frequency of the iterables
    cum_freqs: List[int] = [get_weight(iterable[0])]

    for i in range(1, len(iterable)):
        cum_freqs.append(get_weight(iterable[i]) + cum_freqs[i - 1])
    
    # We can consider the cum_freqs as a representation of repeated items
    # where the value of each elem is how many times the item appears + how many
    # items came before it.
    #
    # We have a total of cum_freqs[-1] items. 
    #
    # From those items, we pick one:
    key: int = random.randint(0, cum_freqs[-1])

    # Use a binary search to find where the key fits in
    return get_out(iterable[binary_search_cum_freq(cum_freqs, key)])

    # For guidance, here is what the unoptimised solution looked like:
    """
    iter_weighted: List[str] = []

    # Probably a better way to do this, but whatever
    for elem in iterable:
        # Add each elem in iter_weighted freq number of times
        for i in range(get_weight(elem)):
            iter_weighted.append(get_out(elem))
    
    rand: int = random.randint(0, len(iter_weighted) - 1)

    return iter_weighted[rand]
    """


def get_next(word1: str | None, word2: str | None) -> str | None:
    # Connect to the db
    con = sqlite3.connect("markov.db")
    cur = con.cursor()

    # Get possible next words from the db
    # If word1 is also a match, triple the frequency
    res: List[tuple[str | None, int]] = cur.execute(
        f"""
        SELECT 
            next, 
            IF({f.sql.eq("word1", word1)}, freq*3, freq)
        FROM Chain
        WHERE {f.sql.eq("word2", word2)}""",
        f.sql.remove_none(word1, word2)
    )
    
    # Pick a random next word
    next_word: str | None = pick_rand_weighted(
        iterable = res.fetchall(),
        get_weight = lambda x: x[1],
        get_out = lambda x: x[0] 
    )

    con.close() # close db connection
    return next_word


def build(start_words: List[str | None]) -> str:
    """
    Builds a blagh which starts with `start_words`."""

    # See README to see what a blagh is
    blagh: List[str | None] = start_words

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

    