"""
The sum of the squares of the first ten natural numbers is,

1^2+2^2+...+10^2 = 385

The square of the sum of the first ten natural numbers is,

(1+2+...+10)^2 = 55^2 = 3025

Hence the difference between the sum of the squares of the first ten natural numbers and the square of the sum is 3025−385=2640.

Find the difference between the sum of the squares of the first one hundred natural numbers and the square of the sum.
"""
from functools import reduce
from operator import add

limit = 100

sum_of_squares = reduce(add, (i**2 for i in range(1, limit + 1)))
square_of_sum = sum(range(1, limit + 1))**2

print("Square of sum ({}) - Sum of squares ({}) for numbers 1 to {} = {} ".format(
    square_of_sum, sum_of_squares, limit, square_of_sum - sum_of_squares
))
