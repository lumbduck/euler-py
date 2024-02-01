"""
By listing the first six prime numbers: 2, 3, 5, 7, 11, and 13, we can see that the 6th prime is 13.

What is the 10,001st prime number?
"""
from datetime import datetime

from lib.common import elapsed
from lib.prime import sieve_primes

start_time = datetime.now()

limit = 10001

print("Prime {}: {}".format(limit, sieve_primes(num_primes=limit)[-1]))
elapsed()
