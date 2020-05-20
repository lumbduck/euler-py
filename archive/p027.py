"""
Euler discovered the remarkable quadratic formula:

n^2+n+41

It turns out that the formula will produce 40 primes for the consecutive integer values 0≤n≤39. However, when n=40, 40^2+40+41=40(40+1)+41 is divisible by 41, and certainly when n=41,41^2+41+41 is clearly divisible by 41.

The incredible formula n2−79n+1601 was discovered, which produces 80 primes for the consecutive values 0≤n≤79. The product of the coefficients, −79 and 1601, is −126479.

Considering quadratics of the form:

n^2+an+b, where |a|<1000 and |b|≤1000

where |n| is the modulus/absolute value of n
e.g. |11|=11 and |−4|=4
Find the product of the coefficients, a and b, for the quadratic expression that produces the maximum number of primes for consecutive values of n, starting with n=0.
"""
import time

from prime import is_prime, sieve_primes

start_time = time.time()

coefficient_limit = 1000


def count_primes_from_quadratic(a, b):
    n = 0
    while is_prime(n ** 2 + a * n + b):
        n += 1
    return n


best_ab = None
seq_len = 0

for b in sieve_primes(max_prime=coefficient_limit):
    for a in range(-coefficient_limit, coefficient_limit + 1):
        count = count_primes_from_quadratic(a, b)
        if count > seq_len:
            seq_len = count
            best_ab = (a, b)

print("Best pair is {}, {} (generated {} primes), giving: {}".format(*best_ab, seq_len, best_ab[0] * best_ab[1]))
print("Execution time: {}".format(time.time() - start_time))
