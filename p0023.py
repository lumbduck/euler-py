"""
A perfect number is a number for which the sum of its proper divisors is exactly equal to the number. For example, the sum of the proper divisors of 28 would be 1 + 2 + 4 + 7 + 14 = 28, which means that 28 is a perfect number.

A number n is called deficient if the sum of its proper divisors is less than n and it is called abundant if this sum exceeds n.

As 12 is the smallest abundant number, 1 + 2 + 3 + 4 + 6 = 16, the smallest number that can be written as the sum of two abundant numbers is 24. By mathematical analysis, it can be shown that all integers greater than 28123 can be written as the sum of two abundant numbers. However, this upper limit cannot be reduced any further by analysis even though it is known that the greatest number that cannot be expressed as the sum of two abundant numbers is less than this limit.

Find the sum of all the positive integers which cannot be written as the sum of two abundant numbers.
"""
from datetime import datetime
from functools import lru_cache

from lib.prime import sum_divisors

start_time = datetime.now()

limit = 28123
min_abund = 12  # Smallest abundant number


@lru_cache(maxsize=None)
def is_abundant(n):
    if n < min_abund:
        return
    elif sum_divisors(n) > n:
        return True


# Sum of terms which are NOT the sum of two abundant numbers
running_total = 0

for n in range(1, limit - min_abund + 1):
    will_count = True
    # Only count if cannot be written as sum of two abundant numbers
    for i in range(min_abund, n // 2 + 1):
        if is_abundant(i) and is_abundant(n - i):
            will_count = False
            break

    if will_count:
        running_total += n

print(running_total)
print("Execution time: {}".format(datetime.now() - start_time))
