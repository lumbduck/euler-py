"""
A Pythagorean triplet is a set of three natural numbers, a < b < c, for which,

a^2 + b^2 = c^2
For example, 3^2 + 4^2 = 9 + 16 = 25 = 5^2.

There exists exactly one Pythagorean triplet for which a + b + c = 1000.
Find the product abc.
"""
from math import floor

target_sum = 1000


def find_pythagorean_triple(sum_of_terms):
    """
    Will only print out the first valid triple found.
    """
    for a in range(1, 333):
        b_max = floor((1000 + a) / 2)
        for b in range(a + 1, b_max):
            c = 1000 - b - a
            if a**2 + b**2 == c**2:
                print("{}^2 * {}^2 = {}^2".format(a, b, c))
                print("--> {} * {} * {} = {}".format(a, b, c, a * b * c))
                return True


find_pythagorean_triple(target_sum)
