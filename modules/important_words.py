import re


class Word:
    __word: str
    __weight: int # kind of like frequency, but dependent on length
    __length: int
    __pos: int
    __isupper: bool

    def __init__(self, word: str, weight: int, pos: int, isupper: bool):
        self.__word = word
        self.__weight = weight
        self.__length = len(word)
        self.__pos = pos
        self.__isupper = isupper

    def get_word(self) -> str:
        return self.__word

    def get_weight(self) -> int:
        return self.__weight

    def get_length(self) -> int:
        return self.__length

    def get_pos(self) -> int:
        return self.__pos

    def get_isupper(self) -> bool:
        return self.__isupper

    def inc_weight(self):
        """
        Increments the weight of the word."""
        self.__weight += 1

    def set_upper(self):
        """
        Sets isupper to True."""
        self.__isupper = True

    def get_sort_key(self) -> tuple[int, int, int]:
        """
        Returns the tuple key for comparing words with one another for sorting.

        `(weight, length, -pos)`

        `pos` is negative because it is sorted inversely from the other values."""
        return (self.get_weight(), self.get_length(), -self.get_pos())

    def get_sort_key_upper(self) -> tuple[int, int, int, int]:
        """
        Returns the tuple key for comparing words with one another for sorting.

        Same as `.get_sort_key()` but considers uppercaseness for sorting.

        `(isupper, weight, length, -pos)`

        - `isupper` follows the usual Python behavior for `bool` to `int`.
        - `pos` is negative because it is sorted inversely from the other values."""
        return (
            int(self.get_isupper()), self.get_weight(),
            self.get_length(), -self.get_pos()
        )


def extract(data: str) -> list[str]:
    """
    Extracts important words from the data string.
    Criteria for 'important words' are in the README."""

    # Go through the data and get all the words
    extracted_words: list[Word] = []

    for i, word_str in enumerate(data.split(" ")):
        # Remove the following symbols:
        # . , : ; ! ? * ( ) [ ] ` { } / " '
        word_clean: str = re.sub(
            pattern = r"""[.,:;!?*_()\[\]`{}/"'\\]""",
            repl = "",
            string = word_str
        )
        isupper: bool = word_clean[0].isupper() # before we .lower() it
        word_clean = word_clean.lower()

        # Check if the word already exists in extracted_words
        extracted_word: Word | None = None

        for word in extracted_words:
            if word.get_word() == word_clean:
                extracted_word = word
                # We assume that extracted_words only contain unique entries
                break

        if not extracted_word:
            # Word does not exist yet, so we must add it
            extracted_word = Word(
                word = word_clean,
                weight = 1, # because this is the first time we've seen it
                pos = i, # its position in the data string
                isupper = isupper
            )
            extracted_words.append(extracted_word)
        else:
            # It exists! Update the word's attributes
            # Increase the weight of sufficiently long words
            if extracted_word.get_length() >= 4:
                extracted_word.inc_weight()
            # Update the uppercase status
            if isupper: extracted_word.set_upper()


    # Start getting the important words from extracted_words

    # Sort and prioritise capitalized words
    extracted_words.sort(
        key = lambda x: x.get_sort_key_upper(),
        reverse = True
    )

    # Truncate the list so we only get the 7 most important words
    extracted_words = extracted_words[:7]

    # Sort all the remaining words based on the criteria
    extracted_words.sort(
        key = lambda x: x.get_sort_key(),
        reverse = True
    )

    return [x.get_word() for x in extracted_words]
