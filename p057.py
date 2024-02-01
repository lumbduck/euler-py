"""
Square Root Convergents

It is possible to show that the square root of two can be expressed as an infinite continued fraction...
1 + (1 / (2 + 1 / (2 + 1 / (2 + 1 / (2 + ...)))))

First 7 iterations:
1 + 1/2 = 3/2 = 1.5
1 + 1 / (2 + 1/2) = 7/5 = 1.4
17/12 = 1.41666...
41/29 = 1.41379...
99/70
239/169
577/408

The eighth expansion, 1393/985, is the first example where the number of digits in the numerator exceeds the number of digits in the denominator.

In the first one-thousand expansions, how many fractions contain a numerator with more digits than the denominator?

(Abridged problem statement due to formatting. See full explanation at https://projecteuler.net/problem=57)
"""
from collections import deque
from itertools import accumulate, cycle, islice, takewhile
from fractions import Fraction

from lib.common import elapsed

limit = 1000


def expand_root():
    """Generator of terms in the expansion sequence of the continued infinite fraction expressing sqrt(2)."""
    n, d = 3, 2

    while True:
        yield n, d
        n, d = 2 * d + n, n + d


def expand_root_swap():
    """Same as expand_root, using an intermediate swap to calculate terms (slightly faster for some reason)."""
    n, d = 3, 2

    while True:
        yield n, d

        d0 = d
        d = n + d
        n = d + d0


def expand_root_tuple():
    """Same as expand_root, using tuples for expansion."""
    q = (3, 2)

    while True:
        yield q
        q = (2 * q[1] + q[0], q[1] + q[0])


def expand_root_fraction():
    """Same as expand_root, using fraction.Fraction class to directly mimic the given expression."""
    q = Fraction(1, 2) + 1
    while True:
        yield q.numerator, q.denominator
        q = 1 + 1 / (1 + q)


def brute_force(func):
    """Use one of the provided expand_root* generators to count digits and return solution."""
    return sum(map(lambda q: len(str(q[0])) > len(str(q[1])), islice(func(), None, limit)))


def analytical_solution():
    """
    Return solution by directly counting the number of valid terms without calculating them. Fastest.

    Using any of the generators above, you can observe that there is a repeating
        cycle of spaces between each valid term in the sequence. It is given by:

    8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8

    That is, the 8th term is valid, the 13th (8 + 5) term is valid, the 21st (8 + 5 + 8), and so on.
    Thus simply accumulating these gap sizes in a cycle until the upper limit of 1000 is exceeded
        will yield the exact number of valid terms. This function does that.

    NOTE: I have not determined if this cycle repeats indefinitely. If I had to guess I would say it doesn't.
    """
    gaps = (8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 3, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8, 5, 8, 8, 5, 8, 5, 8)

    cummulative = deque(enumerate(takewhile(lambda x: x <= limit, accumulate(cycle(gaps))), start=1), maxlen=1)
    return cummulative.pop()[0]


print(analytical_solution())
elapsed()

###############
# Performance
###############
# from timeit import timeit

# for func in (
#     expand_root,  # ~21.7s
#     expand_root_swap,  # 20.8s
#     expand_root_tuple,  # ~22.6s
#     expand_root_fraction  # ~332s
# ):
#     print(func.__name__, timeit("brute_force(func)", number=10000, globals={
#         'brute_force': brute_force,
#         'func': func
#     }))

# # And the winner by a spectacular margin (for obvious reasons), at 0.23s
# print('analytical_solution', timeit(analytical_solution, number=10000))
