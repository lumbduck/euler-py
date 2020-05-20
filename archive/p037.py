"""
The number 3797 has an interesting property. Being prime itself, it is possible to continuously remove digits from left to right, and remain prime at each stage: 3797, 797, 97, and 7. Similarly we can work from right to left: 3797, 379, 37, and 3.

Find the sum of the only eleven primes that are both truncatable from left to right and right to left.

NOTE: 2, 3, 5, and 7 are not considered to be truncatable primes.
"""
from prime import is_prime, primes

import time

start_time = time.time()

limit = 11
trunc_set = set()
trunc_count = 0


def r_truncatable(p):
    """Return True if all right-side truncations of p are prime (does not test p itself)."""
    if p < 10:
        return is_prime(p)
    else:
        r_trunc = p // 10
        return is_prime(r_trunc) and r_truncatable(r_trunc)


def l_truncatable(p):
    """Return True if all left-side truncations of p are prime (does not test p itself)."""
    if p < 10:
        return is_prime(p)
    else:
        l_trunc = int(str(p)[1:])
        return is_prime(l_trunc) and l_truncatable(l_trunc)


def truncatable(p):
    """Return True if all left- and right-side truncations of p are prime (does not test p itself)."""
    return r_truncatable(p) and l_truncatable(p)


for p in primes():
    if p < 10:
        continue
    if truncatable(p):
        trunc_set.add(p)
        trunc_count += 1
        print(p)
        if trunc_count >= limit:
            break


print("Truncatable primes: {}\nSum: {}".format(sorted(trunc_set), sum(trunc_set)))
print("Execution time: {}".format(time.time() - start_time))
