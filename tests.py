import modules.blagh as x
import random

def test_randomness():
    """
    Tests the randomness of `pick_rand_weighted()` using the alphabet."""

    alphabet = "abcdefghijklmnopqrstuvwxyz"
    iterable = [(x, i + 1) for i, x in enumerate(alphabet)]

    # Get the cumulative frequency of the iterables
    # then perform a binary search
    cum_freqs: List[int] = [iterable[0][1]]

    for i in range(1, len(iterable)):
        cum_freqs.append(iterable[i][1] + cum_freqs[i - 1])

    print([(alphabet[i], cum_freqs[i]) for i in range(0, len(alphabet))])

    for i in [0, 1, 2, 3, 81, 89, 325, 350, 351, 352]:
        #print(i, x.binary_search_cum_freq(cum_freqs, i))
        pass

    table = {}

    for i in alphabet:
        table[i] = 0

    for i in range(999):
        res = x.pick_rand_weighted(
            iterable = iterable,
            get_weight = lambda x: x[1],
            get_out = lambda x: x[0]
        )
        table[res] += 1

    print(table)

print("Done.")