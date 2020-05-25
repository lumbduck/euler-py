"""
Spiral Primes

Starting with 1 and spiralling anticlockwise in the following way, a square spiral with side length 7 is formed.

37 36 35 34 33 32 31
38 17 16 15 14 13 30
39 18  5  4  3 12 29
40 19  6  1  2 11 28
41 20  7  8  9 10 27
42 21 22 23 24 25 26
43 44 45 46 47 48 49

It is interesting to note that the odd squares lie along the bottom right diagonal, but what is more interesting is that 8 out of the 13 numbers lying along both diagonals are prime; that is, a ratio of 8/13 ≈ 62%.

If one complete new layer is wrapped around the spiral above, a square spiral with side length 9 will be formed. If this process is continued, what is the side length of the square spiral for which the ratio of primes along both diagonals first falls below 10%?
"""
from collections import deque
from itertools import accumulate, count, takewhile

from prime import is_prime

from common import elapsed

ratio_limit = 10


def is_prime_no_cache(n):
    return is_prime(n, cache_primes=False)


def side_len(n):
    """
    Return 1/4 of the number of terms in the nth iteration of the spiral square.

    NOTE: Actual side length is 1 greater than this number
    """
    return 2 * n


def count_primes_at_level(n):
    """
    Return number of primes on the four corners of the nth iteration of the spiral square.

    NOTE: n = 0 is the first level, with the single value 1 (which has 0 primes).
    Subsequent levels can have at most 3 primes, since one corner is a square number.
    """
    side = side_len(n)
    last_corner = (side + 1) ** 2  # Square number given in last corner at this level
    other_corners = (last_corner - i * side for i in range(1, 4))
    return sum(map(is_prime_no_cache, other_corners))


def run():
    """Return target iteration count and side length of square after final iteration."""
    # Generate cumulative count of primes starting from level 1,
    #   which has 8 elements, 4 corners, and 1 element in the interior (at level 0)
    counter = accumulate(count_primes_at_level(n) for n in count(1))

    # Generator will end one iteration before the ratio of primes to diagonal elements falls below 10%
    evaluator = takewhile(lambda x: x[1] * 10 > x[0] * 4, enumerate(counter, 1))
    iterations = deque(evaluator, maxlen=1)  # last element

    # print(side_len(iterations.pop()[0]))

    # Taking 1 more iteration would cause primes to fall below 10% of diagonal elements, which is what we want
    target_iteration = iterations.pop()[0] + 1
    return target_iteration, side_len(target_iteration) + 1


target_iter, target_side_len = run()
print(f"Finished on level {target_iter}, with side length {target_side_len}")

elapsed()
