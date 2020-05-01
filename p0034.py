"""
145 is a curious number, as 1! + 4! + 5! = 1 + 24 + 120 = 145.

Find the sum of all numbers which are equal to the sum of the factorial of their digits.

Note: as 1! = 1 and 2! = 2 are not sums they are not included.
"""
from itertools import count
from math import factorial
import time


def digital_factorials(n):
    return [factorial(int(d)) for d in str(n)]


start_time = time.time()

lower_bound = 10  # Must be a sum of at least 2 factorials


# Similar to problem #30, looks for the first instance of a number composed of all 9s where the factorial exceeds that number.
upper_bound_order = next(filter(lambda i: factorial(9) * i <= sum(9 * 10**j for j in range(i)), count(2)))
upper_bound = factorial(9) * upper_bound_order

# NOTE: A somewhat tighter bound can be achieved here. 7 * 9! = 2540160, which means the most signicant digit can be at most 2. This limits the bound to 2! + 6 * 9! = 2177282
print("Upper bound: {}".format(upper_bound))

total = 0
for n in range(lower_bound, upper_bound):
    sequence = digital_factorials(n)

    if n == sum(sequence):
        print("Found match: {} = {}".format(n, ' + '.join(str(d) for d in sequence)))
        total += n

print("Sum of matches: {}".format(total))
print("Execution time: {}".format(time.time() - start_time))


p = 2199999
print(sum(digital_factorials(p)))
