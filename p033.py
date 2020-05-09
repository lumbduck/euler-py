"""
The fraction 49/98 is a curious fraction, as an inexperienced mathematician in attempting to simplify it may incorrectly believe that 49/98 = 4/8, which is correct, is obtained by cancelling the 9s.

We shall consider fractions like, 30/50 = 3/5, to be trivial examples.

There are exactly four non-trivial examples of this type of fraction, less than one in value, and containing two digits in the numerator and denominator.

If the product of these four fractions is given in its lowest common terms, find the value of the denominator.
"""
from math import isclose
import time

from lib.prime import cancel_common_factors, expand_factorization, prime_factors

start_time = time.time()


def generate_test_fractions(i, j, digits):
    """
    Returns a generator of 2-tuples.

    Each tuple is create by taking a digit from :param digits: and removing the first instance of that digit from both i and j. If this would cause either i or j to be 0, then that tuple is skipped.
    """
    return filter(lambda x: x[0] > 0 and x[1] > 0, ((int(str(i).replace(d, '', 1)), int(str(j).replace(d, '', 1))) for d in digits))


fract = [1, 1]
for i in range(10, 100):
    i_digits = set(str(i))

    for j in range(i + 1, 100):
        if i % 10 == 0 and j % 10 == 0:
            continue

        j_digits = set(str(j))
        inter = i_digits.intersection(j_digits)

        for n, d in generate_test_fractions(i, j, inter):
            if isclose(i / j, n / d):
                print("{}/{} == {}/{}".format(i, j, n, d))
                fract[0] *= n
                fract[1] *= d


fract = cancel_common_factors(prime_factors(fract[0]), prime_factors(fract[1]))

print("Denominator of products: {}".format(expand_factorization(fract[1])))
print("Execution time: {}".format(time.time() - start_time))
