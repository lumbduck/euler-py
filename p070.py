"""
Totient Permutation

Euler's totient function, phi(n) [sometimes called the phi function], is used to determine the number of positive numbers less than or equal to n which are relatively prime to n. For example, as 1, 2, 4, 5, 7, and 8, are all less than nine and relatively prime to nine, phi(9) = 6.
The number 1 is considered to be relatively prime to every positive number, so phi(1) = 1.

Interestingly, phi(87109) = 79180, and it can be seen that 87109 is a permutation of 79180.

Find the value of n, 1 < n < 10^7, for which phi(n) is a permutation of n and the ratio n/phi(n) produces a minimum.
"""
from math import prod

from lib.common import elapsed
from lib.numb import is_permutation
from lib.prime import prime_factors, sieve_primes, reduce_factorization

MAX_RANGE = 10**7


# We need a function to calculate phi(n) from a prime factorization
# See https://en.wikipedia.org/wiki/Euler%27s_totient_function
def phi(n: int, factors: dict[int, int]) -> int:
    "Take a dict in the form specified by :lib.prime.prime_factors: and compute phi(n) for the given composite number."
    return prod(p**(k - 1) * (p - 1) for (p, k) in factors.items() if k > 0)


# We need a function that checks whether a given number solves the base criteria for a solution
def get_ratio_if_valid(n: int = None, factors: dict[int, int] = {}, max_value: int = MAX_RANGE) -> float | None:
    if not n:
        n = reduce_factorization(factors)
    elif not factors:
        factors = prime_factors(n)

    if n <= 1 or n >= max_value:
        return

    phi_n = phi(n, factors)
    ratio = n / phi_n
    if is_permutation(n, phi_n):
        print(f"Candidate: phi({n:7}) = {phi_n:7}\t({ratio:.05f})")
        return ratio


def get_prime_range(max_value: int = MAX_RANGE) -> list[int]:
    return sieve_primes(max_prime=MAX_RANGE)


def multiply_factors(factors: dict[int, int]):
    if not any(factors.values()):
        return 1
    return reduce_factorization(factors)


# Brute force attempt, using phi() and factorization of every number. Too slow
def depth_first_search(factors: dict[int, int] = {}, primes: list[int] = get_prime_range(), res: tuple[int, int] | None = None, max_value: int = MAX_RANGE) -> tuple[int, int]:
    if not factors:
        factors = dict.fromkeys(primes, 0)
    elif not primes:
        return res
    elif (n := multiply_factors(factors)) >= max_value:
        return res
    elif (new_ratio := get_ratio_if_valid(n, factors=factors)):
        if not res or new_ratio < res[1]:
            res = (n, new_ratio)

    for i in range(len(primes)):
        res = depth_first_search(
            factors={p: k + 1 if p == primes[i] else k for p, k in factors.items()},
            primes=primes[i:],
            res=res
        )

    return res


# Faster (but still slow) brute force algorithm, using sieve described here: https://cp-algorithms.com/algebra/phi-function.html
def sieve_phis(max_value: int = MAX_RANGE):
    phis = [i for i in range(max_value)]
    for i in range(2, max_value):
        if phis[i] == i:
            for j in range(i, max_value, i):
                phis[j] -= phis[j] // i
    return phis


def search_sieved_phis(max_value: int = MAX_RANGE):
    best = None
    phis = sieve_phis(max_value=max_value)
    for n in range(2, max_value):
        if is_permutation(n, phis[n]):
            ratio = n / phis[n]
            if not best or best[1] > ratio:
                best = (n, ratio)

    return best


# n, ratio = depth_first_search()
n, ratio = search_sieved_phis()
if ratio:
    print(f"Best: n={n} ({ratio:.08f})")

elapsed()
