import f.important_words as y
import f.misc
from modules import response


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
        # print(i, x.binary_search_cum_freq(cum_freqs, i))
        pass

    table = {}

    for i in alphabet:
        table[i] = 0

    for i in range(3000):
        res = f.misc.pick_rand_weighted(
            iterable=iterable, get_weight=lambda x: x[1], get_out=lambda x: x[0]
        )
        print(res)
        table[res] += 1

    print(table)

def test_important_words():
    data: list[str] = [
        "My father’s family name being Pirrip, and my Christian name Philip, my infant tongue could make of both names nothing longer or more explicit than Pip. So, I called myself Pip, and came to be called Pip.",
        "How now, my love? Why is your cheek so pale? How chance the roses there do fade so fast?",
    ]

    for string in data:
        print(y.extract(string))

def test_response():
    print(response.pick_response_start_words("Are gonna?"))

    for _ in range(10):
        x = input("Enter text: ")
        print(response.pick_response_start_words(x))

test_response()

print("Done.")
