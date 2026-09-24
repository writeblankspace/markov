import timeit

import modules.blagh as x
import modules.important_words as y


def test_randomness():
    """
    Tests the randomness of `pick_rand_weighted()` using the alphabet."""

    alphabet = "abcdefghijklmnopqrstuvwxyz"
    iterable = [(x, i + 1) for i, x in enumerate(alphabet)]

    # Get the cumulative frequency of the iterables
    # then perform a binary search
    cum_freqs: list[int] = [iterable[0][1]]

    for i in range(1, len(iterable)):
        cum_freqs.append(iterable[i][1] + cum_freqs[i - 1])

    print([(alphabet[i], cum_freqs[i]) for i in range(len(alphabet))])

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

def test_important_words():
    data: list[str] = [
        "My father’s family name being Pirrip, and my Christian name Philip, my infant tongue could make of both names nothing longer or more explicit than Pip. So, I called myself Pip, and came to be called Pip.",
        "How now, my love? Why is your cheek so pale? How chance the roses there do fade so fast?"
    ]

    for string in data:
        print(y.extract(string))


def f(input: list[int]):
    res = []
    for i in input:
        if i in [x*2 for x in res]:
            pass

def time_loop():
    for i in range(5):
        x = 500
        input = list(range(x))
        print(
            f"({x}, ",
            min(timeit.repeat(f"f({input})", "from __main__ import f")),
            ")"
        )

test_important_words()

print("Done.")
