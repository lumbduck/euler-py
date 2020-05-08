"""
Goldbach's Other Conjecture

It was proposed by Christian Goldbach that every odd composite number can be written as the sum of a prime and twice a square.

9 = 7 + 2×1^2
15 = 7 + 2×2^2
21 = 3 + 2×3^2
25 = 7 + 2×3^2
27 = 19 + 2×2^2
33 = 31 + 2×1^2

It turns out that the conjecture was false.

What is the smallest odd composite that cannot be written as the sum of a prime and twice a square?
"""
from itertools import count
from math import sqrt
import time
from timeit import timeit

from prime import is_prime, primes, sieve_primes

start_time = time.time()


def is_pass(n, remove_prime_first=False):
    """Return True if n passes the criteria for the given conjecture."""
    if remove_prime_first:
        for p in primes():
            if p > n:
                return False

            elif sqrt((n - p) / 2).is_integer():
                return True

    else:
        for i in range(1, n // 2):
            if is_prime(n - 2 * i**2):
                return True


def gen_odd_composites():
    step_size = 10000
    sieve_primes(step_size)  # Cache primes

    # Avoiding lower limit. This avoids running an unnecessary filter for each caching step
    for j in range(9, step_size + 1, 2):
        if not is_prime(j):
            yield j

    for i in count(2):
        sieve_primes(i * step_size + 1)  # Cache primes
        for j in range(step_size * (i - 1) + 1, step_size * i + 1, 2):
            if not is_prime(j):
                yield j


def find_first_failure(remove_prime_first=False):
    for n in gen_odd_composites():
        if not is_pass(n, remove_prime_first):
            return n
            break


print("First failure: {}".format(find_first_failure()))
print("Execution time: {}".format(time.time() - start_time))

# NOTE: Performance when canceling prime factors first (using :param remove_prime_first:) is dramatically worse.
# Backwards from what I expected. Possibly an issue with primes() generator...?
print(timeit('find_first_failure()', globals={'find_first_failure': find_first_failure}, number=100))
print(timeit('find_first_failure(True)', globals={'find_first_failure': find_first_failure}, number=100))
