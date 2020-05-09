"""
A permutation is an ordered arrangement of objects. For example, 3124 is one possible permutation of the digits 1, 2, 3 and 4. If all of the permutations are listed numerically or alphabetically, we call it lexicographic order. The lexicographic permutations of 0, 1 and 2 are:

012   021   102   120   201   210

What is the millionth lexicographic permutation of the digits 0, 1, 2, 3, 4, 5, 6, 7, 8 and 9?
"""
from math import factorial

limit = 1000000
unused_digits = list(range(0, 10))

res_digits = []

# Not sure how to do this other than decrementing the target before starting.
# Otherwise we end up with one extra step in the lexicographic permutation and would have to backtrack.
# Perhaps this can be thought of as indexing our lexicographic ordering from 0.
limit -= 1

# Essentially, this alogrithm relies on the observation that for k distinct digits there are k! permutations.
# The last of these permutations, in lexicographic order, is: [k-1, k-2, ..., 1, 0].
# Thus, to find the nth permutation, we need to find the largest k! (with k <= length of our available list of digits)
#   that does not exceed n and then divide the target by this number giving q, r (quotient with remainder).
# q is the index of an available digit, which is removed. This is repeated using the remainder as the new target.
# The removed digits form the correct permutation.
for i in range(len(unused_digits)):
    digit, limit = divmod(limit, factorial(len(unused_digits) - 1))
    res_digits.append(unused_digits[digit])
    del unused_digits[digit]

print(''.join([str(x) for x in res_digits]))
