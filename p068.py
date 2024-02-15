"""
Consider the following "magic" 3-gon ring, filled with the numbers 1 to 6, and each line adding to nine.

  4
   \
    3
   / \
  1---2--6
 /
5


Working clockwise, and starting from the group of three with the numerically lowest external node (4,3,2 in this example), each solution can be described uniquely. For example, the above solution can be described by the set: 4,3,2; 6,2,1; 5,1,3.

It is possible to complete the ring with four different totals: 9, 10, 11, and 12. There are eight solutions in total.

Total	Solution Set
9	4,2,3; 5,3,1; 6,1,2
9	4,3,2; 6,2,1; 5,1,3
10	2,3,5; 4,5,1; 6,1,3
10	2,5,3; 6,3,1; 4,1,5
11	1,4,6; 3,6,2; 5,2,4
11	1,6,4; 5,4,2; 3,2,6
12	1,5,6; 2,6,4; 3,4,5
12	1,6,5; 3,5,4; 2,4,6
By concatenating each group it is possible to form 9-digit strings; the maximum string for a 3-gon ring is 432621513.

Using the numbers 1 to 10, and depending on arrangements, it is possible to form 16- and 17-digit strings. What is the maximum 16-digit string for a "magic" 5-gon ring?

[IMAGE OMITTED: Note that each "spoke" still only has 3 elements, comprised to form a single side of the 5-gon]
"""
from lib.common import elapsed

import numpy as np
import numpy.typing as npt

from collections import defaultdict
from itertools import permutations
from typing import Annotated, Self

SIZE: int = 5  # >= 3
MAX_DIGIT: int = 10  # >= 2 * SIZE, where we treat numbers greater than 10 as "digits"
DIGITS: Annotated[tuple[int], MAX_DIGIT] = tuple(range(1, MAX_DIGIT + 1))
LOWER_LIMIT = DIGITS[0] + DIGITS[1] + DIGITS[-1]
UPPER_LIMIT = sum(DIGITS[-4:-1])

print(f"Constructing {SIZE}-gons with elements {DIGITS}")


class Ngon:
    def __init__(self, n: int) -> None:
        self.matrix: npt.NDArray[npt.NDArray[int]] = np.array([np.array(3 * (0,)) for i in range(n)], dtype=int)  # type: ignore

    def validate(self, target: int = 0) -> bool:
        previous_row = self.matrix[-1]
        if target < 1:
            target = np.sum(previous_row)
        for row in self.matrix:
            if target != np.sum(row):
                print(f"Target sum failed on {row}")
                return False
            elif previous_row[-1] != row[1]:
                print(f"Overlap failed on {previous_row} -> {row}")
                return False
            previous_row = row

        print(self.matrix)
        return True

    def duplicate(self) -> Self:
        dupe: npt.NDArray[npt.NDArray[int]] = np.array([self.matrix[i] for i in range(len(self.matrix))], dtype=int)  # type: ignore
        return dupe

    def to_number(self) -> int:
        stringified_rows = [''.join(map(str, row)) for row in self.matrix]
        return int(''.join(stringified_rows))

    def get_signature(self) -> Annotated[tuple[int], SIZE + 1]:
        vertices = [row[1] for row in self.matrix]
        start_at = vertices.index(min(vertices))
        vertices = vertices[start_at:] + vertices[:start_at]
        return tuple([sum(self.matrix[0])] + vertices)

    def from_signature(self, target, vertices: Annotated[tuple[int], SIZE + 1]) -> int | None:
        all_values = set()
        for i, v in enumerate(vertices):
            last_value = vertices[i + 1] if i < SIZE - 1 else vertices[0]
            self.matrix[i] = [target - last_value - v, v, last_value]
            if any(val < 1 or val not in DIGITS for val in self.matrix[i]):
                return
            else:
                all_values.update(self.matrix[i])

        if not set(DIGITS).issubset(all_values):
            return

        # Reorder matrix by lowest spoke end
        first_column = [row[0] for row in self.matrix]
        start_at = first_column.index(min(first_column))
        self.matrix = np.concatenate((self.matrix[start_at:], self.matrix[:start_at]))

        # NOTE: validation is skipped, since construction rules have been verified for accuracy
        # if self.validate(target):
        #     return self.to_number()
        return self.to_number()


ngon = Ngon(SIZE)

# *Magic* ngons are unique up to a properly order tuple of the polygon's vertices for a given target sum.
# We use this fact to cache them to a dict keyed off the target values, with each target containing a set of tuples for previously seen vertices.
# Note that we must rotate to the lowest vertex of each tuple to ensure uniqueness, which will be a different order than the solution.
cache: defaultdict[int, set[Annotated[tuple[int], SIZE]]] = defaultdict(set)

# We'll construct vertex sets and attempt to verify whether they form magic ngons with the larget numeric representation
largest_num = 0
# largest_ngon = ngon

# Note that for the final answer we restrict the digits of the inner vertices so that 10 must be on a spoke end
# (otherwise we would get a 17-digit numeric represenation, which is outside the specified solution set)
for signature in permutations(DIGITS[:-1] if MAX_DIGIT == 10 else DIGITS, r=SIZE):
    # Check for previous attempt by rotating to the lowest vertex:
    start_at = signature.index(min(signature))
    cache_sig = signature[start_at:] + signature[:start_at]

    for target in range(LOWER_LIMIT, UPPER_LIMIT + 1):
        if cache_sig in cache[target]:
            continue
        else:
            cache[target].add(cache_sig)

        val = ngon.from_signature(target, signature)
        if val and val > largest_num:
            largest_num = val
            # largest_ngon = ngon.duplicate()

print(f"Largest constructed magic Ngon value: {largest_num}")
# print(largest_ngon)
elapsed()
