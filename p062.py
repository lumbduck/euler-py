"""
Cubic Permutations

The cube, 41063625 (345^3), can be permuted to produce two other cubes: 56623104 (384^3) and 66430125 (405^3). In fact, 41063625 is the smallest cube which has exactly three permutations of its digits which are also cube.

Find the smallest cube for which exactly five permutations of its digits are cube.
"""
from collections import defaultdict
from itertools import count
from math import ceil, factorial

from lib.numb import same_digits

from lib.common import elapsed, split_timer

target = 5


def get_cubes(start, stop):
    return set(k**3 for k in range(start, stop))


def get_start_order(target=target):
    return next(filter(lambda x: x[1] >= target, ((i, factorial(i)) for i in count(1))))[0]


def sorted_digits(n):
    return tuple(sorted(str(n)))


#  ~6s
def solve_w_set_manipulation(target=target):
    # Cubes will be checked in chunks by limiting the domain of f(x) = x^(1/3) to a given order of magnitude.
    # This allows precomputation of all cubes in a given range of permutations.
    order = get_start_order()
    start = ceil(10**((order - 1) / 3))

    for i in count(order):
        stop = ceil(10**(i / 3))
        cubes = get_cubes(start, stop)
        cube_count = len(cubes)

        split_timer()
        print(f"Checking {len(cubes)} cubes between {start:,}^3 = {start**3:,} and {stop:,}^3 = {stop**3:,}")
        while cubes:
            # Remove a random element
            c = cubes.pop()
            c_digits = str(c)

            # And then remove permutations of that element
            c_perms = [p for p in cubes if same_digits(p, c_digits)]
            cubes.difference_update(c_perms)

            # If the set length has changed by exactly our target amount then we're done
            if cube_count - len(cubes) == target:
                return min(c_perms)
            else:
                cube_count = len(cubes)

        start = stop


#  ~0.0218s
def solve_w_counter(target=target):
    """Much faster than solve_w_set_manipulation, this simply keys the cubes off their sorted digits so they can be counted quickly."""
    # Cubes will be checked in chunks by limiting the domain of f(x) = x^(1/3) to a given order of magnitude.
    # This allows precomputation of all cubes in a given range of permutations.
    order = get_start_order()
    start = ceil(10**((order - 1) / 3))

    for i in count(order):
        stop = ceil(10**(i / 3))

        cube_gen = (k**3 for k in range(start, stop))
        cubes = defaultdict(list)

        # Store cubes in a dict keyed by the sorted digits
        for c in cube_gen:
            cubes[sorted_digits(c)].append(c)

        split_timer()
        print(f"Checking {len(cubes)} cubes between {start:,}^3 = {start**3:,} and {stop:,}^3 = {stop**3:,}")

        for c, v in cubes.items():
            if len(v) == target:
                return min(v)

        start = stop


print(f"{solve_w_counter()} is the smallest cube which has exactly {target} cubes among the permutations of its digits")
elapsed()
