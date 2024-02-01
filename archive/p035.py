"""
The number, 197, is called a circular prime because all rotations of the digits: 197, 971, and 719, are themselves prime.

There are thirteen such primes below 100: 2, 3, 5, 7, 11, 13, 17, 31, 37, 71, 73, 79, and 97.

How many circular primes are there below one million?
"""
from lib.prime import sieve_primes
import time

start_time = time.time()

limit = 1000000

# Will be removing primes from this as it is traversed to avoid duplicate work
primes_filtered = set(sieve_primes(max_prime=limit))


def get_rotations(n):
    n_str = str(n)
    return set(int(n_str[m:] + n_str[:m]) for m in range(len(n_str)))


def is_prime(n):
    if n in primes_filtered:
        return True


count = 0

print("Testing {} primes less than {}".format(len(primes_filtered), limit))
for p in filter(is_prime, range(1, limit)):
    rotations = get_rotations(p)
    if rotations.issubset(primes_filtered):
        print("Found match: {}".format(rotations))
        count += len(rotations)

    primes_filtered.difference_update(rotations)


print(count)
print("Execution time: {}".format(time.time() - start_time))
