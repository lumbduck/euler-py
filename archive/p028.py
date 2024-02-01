"""
Starting with the number 1 and moving to the right in a clockwise direction a 5 by 5 spiral is formed as follows:

21 22 23 24 25
20  7  8  9 10
19  6  1  2 11
18  5  4  3 12
17 16 15 14 13

It can be verified that the sum of the numbers on the diagonals is 101.

What is the sum of the numbers on the diagonals in a 1001 by 1001 spiral formed in the same way?
"""
from itertools import count

from lib.common import elapsed

side_limit = 1001


def gen_corners(max_width):
    yield 1  # Central element

    for i in count(1):
        side_len = 2 * i  # 1 less than actual dimensions of square

        if side_len + 1 > max_width:
            return

        # Yield four corners
        last_corner = (side_len + 1)**2  # Easiest one to calculate
        for j in range(3, -1, -1):
            yield last_corner - j * side_len


print(sum(gen_corners(side_limit)))
elapsed()
