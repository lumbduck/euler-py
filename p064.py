"""
Odd Period Square Roots

(Omitted problem statement due to formatting. See problem at https://projecteuler.net/problem=64)

A better explanation of the process of creating these fraction expansions can be seen here:
https://math.stackexchange.com/questions/265690/continued-fraction-of-a-square-root
"""
from math import sqrt

from common import elapsed


def is_odd_period(n):
    # Get whole number term
    dec_value = sqrt(n)
    if dec_value.is_integer():
        # No cycle / not counted if n is square
        return 0

    # The following terms represent an intermediate step where the innermost fraction is:
    #   (sqrt(n) + numerator_term) / denominator_term.
    # Each subsequent step implicitly takes the reciprocal of this and then rationalizes the denominator before computing the next terms.
    numerator_term = int(dec_value)
    denominator_term = n - numerator_term**2

    # Keep track of the above terms to see when they repeat.
    cache = set()

    # This loops stops when we would recalculate the same terms as a previous iteration
    while (numerator_term, denominator_term) not in cache:
        cache.add((numerator_term, denominator_term))

        whole_value = int((sqrt(n) + numerator_term) / denominator_term)

        numerator_term = whole_value * denominator_term - numerator_term
        denominator_term = int((n - numerator_term**2) / denominator_term)

    return len(cache) % 2


print(sum(is_odd_period(n) for n in range(2, 10_001)))
elapsed()
