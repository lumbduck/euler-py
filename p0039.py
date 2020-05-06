"""
If p is the perimeter of a right angle triangle with integral length sides, {a,b,c}, there are exactly three solutions for p = 120.

{20,48,52}, {24,45,51}, {30,40,50}

For which value of p ≤ 1000, is the number of solutions maximised?
"""
from collections import defaultdict
from math import sqrt
import time

start_time = time.time()

limit = 1000


def is_right(a, b, c):
    return a**2 + b**2 == c**2


def get_triples(max_perim):
    tris = defaultdict(list)  # perimeter: [(a1, b1, c1), (a2, b2, c2)...]
    for a in range(1, limit // 3):
        for b in range(a + 1, limit // 2):
            c = sqrt(a**2 + b**2)
            if a + b + c > max_perim:
                break
            else:
                c = int(c)
                if is_right(a, b, c):
                    tris[a + b + c].append((a, b, c))

    return tris


best_perim = 0
num_tris = 0
perims = get_triples(limit)
for p in perims:
    if len(perims[p]) > num_tris:
        best_perim = p
        num_tris = len(perims[p])

print("Best perimeter {} ({} unqiue triples): {}".format(best_perim, num_tris, perims[best_perim]))
print("Additional observations:")
print("\tLongest short leg: {}".format(max(x for x in (max(a for (a, b, c) in perims[p]) for p in perims))))
print("\tLongest long leg: {}".format(max(x for x in (max(b for (a, b, c) in perims[p]) for p in perims))))
print("\tLongest hypotenuse: {}".format(max(x for x in (max(c for (a, b, c) in perims[p]) for p in perims))))
print("Execution time: {}".format(time.time() - start_time))
