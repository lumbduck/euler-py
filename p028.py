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
import time

start_time = time.time()

side_limit = 1001

diagonal_sum = 1
square_count = 1  # How many squares have been built
square_side = 3  # Num elements in side of current square
square_origin = 2  # Where did the last square start
corner = 1  # How many corners have been assigned to the current square

n = 3  # Start from a corner and increment by the current square's side length (-1)
while n <= side_limit ** 2:
    diagonal_sum += n

    if corner == 4:
        square_count += 1
        square_side = square_count * 2 + 1
        square_origin = n + 1
        corner = 1
    else:
        corner += 1
    n += square_side - 1


print("Sum of diagonals for {}x{} spiral: {}".format(side_limit, side_limit, diagonal_sum))
print("Execution time: {}".format(time.time() - start_time))
