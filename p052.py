"""
Permuted Multiples

It can be seen that the number, 125874, and its double, 251748, contain exactly the same digits, but in a different order.

Find the smallest positive integer, x, such that 2x, 3x, 4x, 5x, and 6x, contain the same digits.
"""
from itertools import count

from lib.numb import same_digits

# Load last
from lib.common import elapsed


def run():
    """Return the first integer, x, for which 2x through 6x all contain exactly the same digits as x."""
    # NOTE: The acceptable range of testable values, x, within a given order of magnitude, 10**j, is
    #   (10**j, 10**j * 10/6)
    #   because of that fact that 6x must be within the same order of magnitude as x to have matching digits.

    # Start from 100, since 3 digits are required to give at least 6 permutations of those digits
    for i in count(3):
        for x in range(10**i, 10**(i + 1) // 6):
            digits = str(x)
            if all(map(lambda n: same_digits(n, digits), (x * j for j in range(1, 7)))):
                return x


print(f"Smallest integer with 6x permuted multiples: {run()}")
elapsed()
