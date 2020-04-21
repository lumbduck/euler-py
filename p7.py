"""
By listing the first six prime numbers: 2, 3, 5, 7, 11, and 13, we can see that the 6th prime is 13.

What is the 10,001st prime number?
"""
from datetime import datetime
# from itertools import takewhile
# from math import sqrt
from lib import prime

start_time = datetime.now()

limit = 10001

# XXX: OLD VERSION
# def sieve_n_primes(n):
#     primes = [3]  # ignoring 2 because we won't be testing even numbers

#     i = 5
#     while len(primes) < n - 1:  # since 2 is left out of the algorithm below, we need one less prime in our list
#         is_composite = False
#         for p in takewhile(lambda x: x <= sqrt(i), primes):
#             if i % p == 0:
#                 is_composite = True
#                 break
#         if not is_composite:
#             primes.append(i)

#         # XXX: WHY DOES THIS RUN 3 TIMES SLOWER?! (Possibility that python 3.8 might fix it)
#         # filtered_primes = takewhile(lambda x: x <= sqrt(i), primes)
#         # if not any(i % p == 0 for p in filtered_primes):
#         #     primes.append(i)

#         i += 2
#     primes.insert(0, 2)
#     return primes


print("Prime {}: {}".format(limit, prime.sieve_primes(num_primes=limit)[-1]))
print("Execution time: {}".format(datetime.now() - start_time))
