"""
2520 is the smallest number that can be divided by each of the numbers from 1 to 10 without any remainder.

What is the smallest positive number that is evenly divisible by all of the numbers from 1 to 20?
"""
from functools import reduce
from operator import mul
from collections import defaultdict


def factor(n):
    prime_factors = defaultdict(int)

    trial_factor = 2
    while n > 1:
        q, r = divmod(n, trial_factor)
        if r == 0:
            n = q
            prime_factors[trial_factor] += 1
        else:
            trial_factor += 1

    return prime_factors


prime_factorization = defaultdict(int)

for n in range(1, 21):
    new_factors = factor(n)
    for j in new_factors:
        prime_factorization[j] = max(prime_factorization[j], new_factors[j])

factors_exp_generator = (p**n for (p, n) in prime_factorization.items())

lcm = reduce(mul, factors_exp_generator)

print(lcm)
