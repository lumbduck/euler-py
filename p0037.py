"""
The number 3797 has an interesting property. Being prime itself, it is possible to continuously remove digits from left to right, and remain prime at each stage: 3797, 797, 97, and 7. Similarly we can work from right to left: 3797, 379, 37, and 3.

Find the sum of the only eleven primes that are both truncatable from left to right and right to left.

NOTE: 2, 3, 5, and 7 are not considered to be truncatable primes.
"""
from lib.prime import is_prime, sieve_primes

from itertools import count
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


# NOTE: Non-recursive truncation loop. This is not used.
def truncations(p):
    trunc_set = set()
    p_left = p_right = str(p)
    trunc_set.add(p_left)
    trunc_set.add(p_right)
    while len(p_left) > 1:
        p_left = p_left[:-1]
        p_right = p_right[1:]
        trunc_set.add(p_left)
        trunc_set.add(p_right)

    return sorted(trunc_set)


done = False
for order in count():
    if done:
        break
    next_primes = filter(lambda x: x > 10**(order - 1), sieve_primes(max_prime=10**order))
    print("Finished sieving for order {}\nTesting truncations...".format(order))
    for p in next_primes:
        if p < 10:
            continue
        if truncatable(p):
            trunc_set.add(p)
            trunc_count += 1
            print(p)
            if trunc_count >= limit:
                done = True
                break

# XXX: Why does this run slower??
# cProfile says sieve_primes gets called about the same number of times, which should NOT be the case here. It should be called once.
# for p in sieve_primes(max_prime=10**6):
#     if p < 10:
#         continue
#     if truncatable(p):
#         trunc_set.add(p)
#         trunc_count += 1
#         print(p)
#         if trunc_count >= limit:
#             break

print("Truncatable primes: {}\nSum: {}".format(sorted(trunc_set), sum(trunc_set)))
print("Execution time: {}".format(time.time() - start_time))
