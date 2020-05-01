"""
We shall say that an n-digit number is pandigital if it makes use of all the digits 1 to n exactly once; for example, the 5-digit number, 15234, is 1 through 5 pandigital.

The product 7254 is unusual, as the identity, 39 × 186 = 7254, containing multiplicand, multiplier, and product is 1 through 9 pandigital.

Find the sum of all products whose multiplicand/multiplier/product identity can be written as a 1 through 9 pandigital.

HINT: Some products can be obtained in more than one way so be sure to only include it once in your sum.
"""
from functools import lru_cache
from string import digits
import time

from lib.numb import num_digits

start_time = time.time()


# To maximize lru_cache effectiveness, all :param available: values for the functions below should be sorted strings
# whose digits are a subset of the following characters (this is format returned by :func reduce_digits:):
positive_digits = digits[1:]
base = 10


def reverse(s):
    "Return string in reverse (converts numbers to strings)"
    # For some reason this is slightly faster than str(s)[::-1]
    return ''.join(reversed(str(s)))


@lru_cache(maxsize=None)
def are_digits_equal(n, available):
    return available and num_digits(n) == len(available) and set(str(n)) == set(available)


@lru_cache(maxsize=None)
def is_available(n, available):
    n_set = set(str(n))
    return available and num_digits(n) == len(n_set) and n_set.issubset(available)


@lru_cache(maxsize=None)
def reduce_digits(used, available):
    used = set(str(used))
    available = set(str(available))
    return ''.join(sorted(available.difference(used)))


@lru_cache(maxsize=None)
def upper_bound_order(len_i, all_digits=positive_digits):
    """Return upper bound on the number of digits for inner loop."""
    # This was determined analytically using the available set of digits
    return (len(all_digits) + 1) // 2 - len_i


def inner_range(i, available):
    """Return iterator over appropriate bounds of inner loop, based on the first term of the product and remaining digits."""
    len_i = num_digits(i)
    len_j_max = upper_bound_order(len_i, available)

    j_max_str = reverse(available)[:len_j_max + 1]
    if j_max_str:
        j_max = int(j_max_str) + 1
    else:
        return []

    return filter(lambda x: is_available(x, available), range(i + 1, j_max))


res_set = set()
upper_limit = 10**3

for i in range(1, upper_limit):
    if not is_available(i, positive_digits):
        continue

    remaining_digits = reduce_digits(i, positive_digits)

    for j in inner_range(i, remaining_digits):
        res_remaining_digits = reduce_digits(j, remaining_digits)
        res = i * j

        if are_digits_equal(res, res_remaining_digits):
            print("{} x {} = {} ({}){}".format(
                i, j, i * j,
                res_remaining_digits,
                "\tDUPE" if res in res_set else '')
            )
            res_set.add(res)


print("Total: {}".format(sum(res_set)))
print("Execution time: {}".format(time.time() - start_time))
