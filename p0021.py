"""
Let d(n) be defined as the sum of proper divisors of n (numbers less than n which divide evenly into n).
If d(a) = b and d(b) = a, where a ≠ b, then a and b are an amicable pair and each of a and b are called amicable numbers.

For example, the proper divisors of 220 are 1, 2, 4, 5, 10, 11, 20, 22, 44, 55 and 110; therefore d(220) = 284. The proper divisors of 284 are 1, 2, 4, 71 and 142; so d(284) = 220.

Evaluate the sum of all the amicable numbers under 10000.
"""
from functools import reduce, lru_cache
from operator import mul

from lib.prime import prime_factors

limit = 10000


def sum_raised_primes(p, power_of_p):
    return int((p**(power_of_p + 1) - 1) / (p - 1))


@lru_cache(maxsize=None)
def sum_divisors(n):
    if n == 1:
        return 0
    factorization = prime_factors(n)
    return reduce(mul, (sum_raised_primes(p, k) for p, k in factorization.items())) - n


amicable_sums = 0
for n in range(2, limit + 1):
    d = sum_divisors(n)
    if n > limit or n == 1 or d == n:
        continue
    elif sum_divisors(d) == n:
        amicable_sums += n


print(amicable_sums)
