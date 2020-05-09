"""
Take the number 192 and multiply it by each of 1, 2, and 3:

192 × 1 = 192
192 × 2 = 384
192 × 3 = 576
By concatenating each product we get the 1 to 9 pandigital, 192384576. We will call 192384576 the concatenated product of 192 and (1,2,3)

The same can be achieved by starting with 9 and multiplying by 1, 2, 3, 4, and 5, giving the pandigital, 918273645, which is the concatenated product of 9 and (1,2,3,4,5).

What is the largest 1 to 9 pandigital 9-digit number that can be formed as the concatenated product of an integer with (1,2, ... , n) where n > 1?
"""
from functools import reduce
from operator import concat
from string import digits
import time


def is_pandigital(n, dig):
    return set(str(n)) == set(dig)


def pandigital_multiple(i, j):
    return int(reduce(concat, map(lambda x: str(x * i), range(1, j + 1))))


start_time = time.time()

pos_digits = digits[1:]
limit = int(pos_digits[::-1])

best_multiple = None
best_val = 0

done = False
i_lim = int(str(limit)[:4]) + 1
for i in range(1, i_lim):
    if done:
        break
    for j in range(2, 10):
        val = pandigital_multiple(i, j)
        if val <= limit:
            if is_pandigital(val, pos_digits) and val > best_val:
                best_val = val
                best_multiple = (i, j)
        else:
            if j == 2:
                done = True
                break
            else:
                break

print("Best combo i={} with {} terms: {}".format(*best_multiple, best_val))
print("Execution time: {}".format(time.time() - start_time))
