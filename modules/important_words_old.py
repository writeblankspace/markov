import collections
import re
from typing import Union

"""
Important words prioritise capitalized words to add into important_words.

They are then sorted by frequency, length and position in the data string.
"""


class Word(object):
    __word: str
    __freq: int
    __length: int
    __pos: int
    __isupper: bool

    def __init__(self, word: str, freq: int, pos: int, isupper: bool):
        self.__word = word
        self.__freq = freq
        self.__length = len(word)
        self.__pos = pos
        self.__isupper = isupper

    def get_word(self) -> str:
        return self.__word

    def get_freq(self) -> int:
        return self.__freq

    def get_length(self) -> int:
        return self.__length

    def get_pos(self) -> int:
        return self.__pos

    def get_isupper(self) -> bool:
        return self.__isupper

    def inc_freq(self):
        """
        Increments the frequency of the word."""
        self.__freq += 1

    def set_upper(self):
        """
        Sets isupper to True."""
        self.__isupper = True


# A dict to store Word objects, grouped by freq, then length, and sorted by pos
"""
# "The quick brown fox jumps over the lazy dog.
#  The dog was brown, and not quick. Did I mention that it was lazy too?"
{
    3: {
        3: ["the"]
        },
    2: {
        5: ["quick", "brown"],
        4: ["lazy"],
        3: ["dog"]
        },
    1: {
        7: ["mention"],
        5: ["jumps"],
        3: ["fox", ...],
        ...
        }
}"""
# The below comment reminds me of furigana... no? Oh well.
#                     freq      length    word
extracted_words: dict[int, dict[int, list[Word]]] = {}


def insert_word(word: Word, freq: int):
    """
    Inserts word into extracted_words."""

    # Initialize the value of the keys we'll be using, if they don't exist
    extracted_words.setdefault(freq, {})
    extracted_words[freq].setdefault(word.get_length(), [])

    sib_words: list[Word] = extracted_words[freq][word.get_length()]

    # Insert into list by pos
    for i, sib_word in enumerate(sib_words):
        if sib_word.get_pos() > word.get_pos():
            # We've gone past the pos we need; we found where to insert
            sib_words.insert(i, word)
            break

        if i == len(sib_words) - 1:
            # Last element; we must append instead
            extracted_words[freq][word.get_length()].append(word)


def remove_word(word: Word, freq: int):
    """
    Removes the word from extracted_words."""

    sib_words: list[Word] = extracted_words[freq][word.get_length()]
    sib_words.remove(word)


def extract(data: str) -> list[str]:
    """
    Returns a list of up to 7 important words from `data`."""
    # See README for details on how this works

    extracted_words: dict[int, dict[int, list[Word]]] = {}

    # Used to make the program more time-efficient
    # Think of it as a cache
    unique_words: set[str] = set()
    capitalized_words: set[str] = set()

    # Extract the data first
    for i, word_str in enumerate(data):
        # Remove the following symbols:
        # . , : ; ! ? * ( ) [ ] ` { } / " '
        word_clean: str = re.sub(
            pattern = r"""[.,:;!?*_()\[\]`{}/"'\\]""",
            repl = "",
            str = word_str
        )
        isupper: bool = word_clean[0].isupper() # before we .lower() it
        word_clean = word_clean.lower()

        # Who cares about checking the capitalized_words before adding?
        # It's a set anyway
        if isupper:
            capitalized_words.add(word_clean)

        # No need to do a loop through the *entire* extracted_words
        # Because that makes this thing O(n^2)
        if word_clean in unique_words:
            # Find the word in extracted_words so we can update it
            # And put it in its right place

            for freq, freq_item in extracted_words.items():
                for words in freq_item.values():

                    for i in range(len(words)):
                        if word_clean == words[i].get_word():
                            word = words[i]
                            # Remove from here
                            words.pop(i)
                            # Update info about the word before reinsertion
                            word.inc_freq() # Increment the frequency
                            if isupper: word.set_upper()
                            # Insert into its proper place
                            insert_word(word, freq)
                            break
        else:
            # We haven't seen this word before
            unique_words.add(word_clean)

            # *Resists urge to comment some really obvious things*
            # *Fails, because this may not be so obvious later on*
            extracted_word = Word(
                word = word_clean,
                freq = 1, # because this is the first time we've seen it
                pos = i, # its position in the data string
                isupper = isupper
            )

            insert_word(extracted_word, 1)


    # Note that extracted_words is already sorted!
    # Capitalized

    # Capitalized words are prioritised
    # Then the rest are added based on frequency, length and pos

    important_words: list[Word] = []

    i: int = 0

    # Add capitalized words
    important_words.extend(important_words)

    #TODO: Points based on frequency of word
    #TODO: Add the longest words
    #TODO: Sort by points, then sort by length and position

    #TODO: create a more efficient version of this
