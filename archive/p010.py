"""
The sum of the primes below 10 is 2 + 3 + 5 + 7 = 17.

Find the sum of all the primes below two million.
"""
from datetime import datetime

from common import elapsed
from prime import sieve_primes

start_time = datetime.now()

max_prime = 2000000
print(sum(sieve_primes(max_prime=max_prime)))
elapsed()
