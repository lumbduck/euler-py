"""
Triangle, pentagonal, and hexagonal numbers are generated by the following formulae:

Triangle	 	Tn=n(n+1)/2	 	1, 3, 6, 10, 15, ...
Pentagonal	 	Pn=n(3n−1)/2	 	1, 5, 12, 22, 35, ...
Hexagonal	 	Hn=n(2n−1)	 	1, 6, 15, 28, 45, ...
It can be verified that T285 = P165 = H143 = 40755.

Find the next triangle number that is also pentagonal and hexagonal.
"""
from itertools import count
import time

from lib.seq import is_hexagonal, is_pentagonal, triangle_num

initial_value = 285
assert is_hexagonal(triangle_num(initial_value)) and is_pentagonal(triangle_num(initial_value)), "Invalid."

start_time = time.time()

for i in count(initial_value + 1):
    t = triangle_num(i)
    if is_hexagonal(t) and is_pentagonal(t):
        print(t)
        break

print("Execution time: {}".format(time.time() - start_time))
