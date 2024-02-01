"""
Cyclical Figurate Numbers

Triangle, square, pentagonal, hexagonal, heptagonal, and octagonal numbers are all figurate (polygonal) numbers and are generated by the following formulae:

Triangle            P_3,n=n(n+1)/2	 	1, 3, 6, 10, 15, ...
Square              P_4,n=n^2	 	    1, 4, 9, 16, 25, ...
Pentagonal          P_5,n=n(3n−1)/2	 	1, 5, 12, 22, 35, ...
Hexagonal           P_6,n=n(2n−1)	 	1, 6, 15, 28, 45, ...
Heptagonal          P_7,n=n(5n−3)/2	 	1, 7, 18, 34, 55, ...
Octagonal           P_8,n=n(3n−2)	 	1, 8, 21, 40, 65, ...
The ordered set of three 4-digit numbers: 8128, 2882, 8281, has three interesting properties.

The set is cyclic, in that the last two digits of each number is the first two digits of the next number (including the last number with the first).
Each polygonal type: triangle (P_3,127=8128), square (P_4,91=8281), and pentagonal (P_5,44=2882), is represented by a different number in the set.
This is the only set of 4-digit numbers with this property.
Find the sum of the only ordered set of six cyclic 4-digit numbers for which each polygonal type: triangle, square, pentagonal, hexagonal, heptagonal, and octagonal, is represented by a different number in the set.
"""
from functools import lru_cache
from itertools import count

from lib.seq import triangle_num, square_num, pentagonal_num, hexagonal_num, heptagonal_num, octagonal_num

from lib.common import elapsed

f_count = 6
f_funcs = (triangle_num, square_num, pentagonal_num, hexagonal_num, heptagonal_num, octagonal_num)
f_names = tuple(f.__name__[:-4] for f in f_funcs)

# A tuple diagonal matrix for filtering
base_masks = tuple(tuple(True if j == i else False for j in range(f_count)) for i in range(f_count))


def get_polygonal_nums():
    nums = {}

    for i, f in enumerate(f_funcs[:f_count]):
        for k in count(5):
            n = f(k)
            if n > 9999:
                break
            elif n > 999:
                if r_digits(n) < 10:
                    # The number has a zero in the tens place and cannot be part of a cycle
                    continue
                elif n not in nums:
                    nums[n] = [0] * f_count

                nums[n][i] = 1

    return nums


@lru_cache(maxsize=None)
def l_digits(n):
    return int(str(n)[:2])


@lru_cache(maxsize=None)
def r_digits(n):
    return int(str(n)[2:])


def gather_cycle_from_seed(seed, r_digs, nums):
    """Recurse from n-tuple seed (n-tuple of numbers identified with figurate function index) to find n-tuple solution."""
    if None not in seed:
        if r_digs == l_digits(seed[0]):
            return seed
        else:
            return None

    r_candidates = frozenset(n for n in nums if n not in seed and l_digits(n) == r_digs)

    if not r_candidates:
        return

    for n in r_candidates:
        next_r_digs = r_digits(n)
        for j in (j for j in range(f_count) if (not seed[j] and nums[n][j])):
            next_seed = tuple(n if j == k else seed[k] for k in range(f_count))
            extended = gather_cycle_from_seed(next_seed, next_r_digs, nums)
            if extended:
                # Done
                return extended


def run():
    nums = get_polygonal_nums()

    for n, f_types in nums.items():
        if not f_types[0]:
            continue

        # seed = [n] + [None] * (f_count - 1)
        seed = tuple(n if i == 0 else None for i in range(f_count))
        c = gather_cycle_from_seed(seed, r_digits(n), nums)

        if c:
            total = sum(c)
            print(' + '.join((str(m) for m in c)), '=', total)
            return c, total

    print("Failed to find cycle")


run()
elapsed()
