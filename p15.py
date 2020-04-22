"""
Starting in the top left corner of a 2×2 grid, and only being able to move to the right and down, there are exactly 6 routes to the bottom right corner.

(see diagram at https://projecteuler.net/problem=15)

How many such routes are there through a 20×20 grid?
"""
from sympy import summation, symbols

a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t =\
    symbols('a b c d e f g h i j k l m n o p q r s t', integer=True)

# "Closed form" solution based on analyzing the possible routes on arbitrary nxm rectangles
#    where the solution is given by Σ(0,n) . . . Σ(0,i)(1), where the sum is repeated m times
# Note: The choice to sum only the value "1" is aesthetic. Shifting indeces and/or using
#    triangle numbers can be employed to vary the expression or change the number of summations.
routes_for_20x20 = summation(1,
                             (a, 0, b), (b, 0, c), (c, 0, d), (d, 0, e), (e, 0, f), (f, 0, g),
                             (g, 0, h), (h, 0, i), (i, 0, j), (j, 0, k), (k, 0, l), (l, 0, m),
                             (m, 0, n), (n, 0, o), (o, 0, p), (p, 0, q), (q, 0, r), (r, 0, s),
                             (s, 0, t), (t, 0, 20))

print(routes_for_20x20)
