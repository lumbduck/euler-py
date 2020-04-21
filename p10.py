"""
The sum of the primes below 10 is 2 + 3 + 5 + 7 = 17.

Find the sum of all the primes below two million.
"""
from datetime import datetime
from lib import prime

start_time = datetime.now()

max_prime = 2000000
print(sum(prime.sieve_primes(max_prime=max_prime)))

print("Execution time: {}".format(datetime.now() - start_time))
