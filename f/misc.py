import random
from collections.abc import Callable

# Miscellaneous algorithm functions


def binary_search_cum_freq(cum_freqs: list[int], key: int) -> int | None:
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
            return key <= cum_freqs[i]
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
    assert found(mid), "The index should be found by now."


def pick_rand_weighted(
    iterable: list[tuple],
    get_weight: Callable[[tuple], int],
    get_out: Callable[[tuple], str],
) -> str | None:
    """
    Picks out a random element from `iterable`.
    Considers the weight (from `get_weight`).
    Outputs whatever is gotten from `get_out` from the tuple."""

    # If it's empty, there's nothing we can do
    if not iterable:
        return None

    # Get the cumulative frequency of the iterables
    cum_freqs: list[int] = [get_weight(iterable[0])]

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
    i: int | None = binary_search_cum_freq(cum_freqs, key)

    assert i is not None
    return get_out(iterable[i])

    # For guidance, here is what the unoptimised solution looked like:
    """
    iter_weighted: list[str] = []

    # Probably a better way to do this, but whatever
    for elem in iterable:
        # Add each elem in iter_weighted freq number of times
        for i in range(get_weight(elem)):
            iter_weighted.append(get_out(elem))

    rand: int = random.randint(0, len(iter_weighted) - 1)

    return iter_weighted[rand]
    """
