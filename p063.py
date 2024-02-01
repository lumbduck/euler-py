"""
Powerful Digit Counts

The 5-digit number, 16807=7^5, is also a fifth power. Similarly, the 9-digit number, 134217728=8^9, is a ninth power.

How many n-digit positive integers exist which are also an nth power?
"""
from itertools import count

from lib.numb import num_digits

from lib.common import elapsed

total = 0
for n in count(1):
    powers = list((f"{i}**{n}", i**n) for i in range(1, 10) if num_digits(i**n) == n)
    if not powers:
        break
    total += len(powers)

print(total)
elapsed()
