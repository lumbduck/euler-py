"""
We shall say that an n-digit number is pandigital if it makes use of all the digits 1 to n exactly once. For example, 2143 is a 4-digit pandigital and is also prime.

What is the largest n-digit pandigital prime that exists?
"""
import time

from lib.prime import is_prime
from lib.seq import pandigitals

start_time = time.time()


def largest_pandigital_prime():
    for l in range(9, 0, -1):
        for p in pandigitals(l, True):
            if is_prime(p, False):
                return p


print(largest_pandigital_prime())
