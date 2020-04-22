"""
Starting in the top left corner of a 2×2 grid, and only being able to move to the right and down, there are exactly 6 routes to the bottom right corner.

(see diagram at https://projecteuler.net/problem=15)

How many such routes are there through a 20×20 grid?
"""
from functools import lru_cache

from datetime import datetime

start_time = datetime.now()

grid_size = 20

# This is the most efficient summation solution, due primarily to the caching.
# The commented out solutions below this are illustrative of the actual process being modeled.
# For a dynamic programming solution, see problem_15.py at https://repl.it/@tifojo/ProjectEuler
@lru_cache(maxsize=None, typed=False)
def recursive_sum(depth, terms):
    if depth == 0:
        return 1
    else:
        sum = 0
        for term in range(0, terms + 1):
            sum += recursive_sum(depth - 1, term)
        return sum


print(recursive_sum(grid_size, grid_size))


##################################################################
# "Closed form" solution based on analyzing the possible routes on arbitrary nxm rectangles
#    where the solution is given by Σ(0,n) . . . Σ(0,i)(1), where the sum is repeated m times
# NOTE: The choice to sum only the value "1" is aesthetic. Shifting indeces and/or using
#    triangle numbers can be employed to vary the expression or change the number of summations.
##################################################################
# from sympy import summation, symbols
# a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t =\
#     symbols('a b c d e f g h i j k l m n o p q r s t', integer=True)
# routes_for_20x20 = summation(1,
#                              (a, 0, b), (b, 0, c), (c, 0, d), (d, 0, e), (e, 0, f), (f, 0, g),
#                              (g, 0, h), (h, 0, i), (i, 0, j), (j, 0, k), (k, 0, l), (l, 0, m),
#                              (m, 0, n), (n, 0, o), (o, 0, p), (p, 0, q), (q, 0, r), (r, 0, s),
#                              (s, 0, t), (t, 0, 20))

# print(routes_for_20x20)

##################################################################
# Alternatively, generate the sympy code given above and execute with `exec`
# NOTE: Obviously a bad practice, but convenient for the above solution
##################################################################
# from sympy import summation, symbols
# summation_ranges = ''
# prev_symbol = None
# for i in range(grid_size):
#     new_symbol = 'j{}'.format(i)
#     exec("{} = symbols('{}', integer=True)".format(new_symbol, new_symbol))
#     if prev_symbol:
#         new_summation_range = '({}, 0, {}), '.format(prev_symbol, new_symbol)
#         summation_ranges += new_summation_range
#     if i == grid_size - 1:
#         summation_ranges += '({}, 0, {})'.format(new_symbol, grid_size)

#     prev_symbol = new_symbol

# num_routes = None
# exec_num_expr = "num_routes = summation(1, {})".format(summation_ranges)
# exec(exec_num_expr)
# print("Number of routes through {}x{} square: {}".format(grid_size, grid_size, num_routes))

print("Execution time: {}".format(datetime.now() - start_time))
