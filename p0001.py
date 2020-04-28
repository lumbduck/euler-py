"""
If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6 and 9. The sum of these multiples is 23.

Find the sum of all the multiples of 3 or 5 below 1000.
"""
target_max = 1000
total = 0

# Keep track of multiples of 3 and 5
a = 3
b = 5

while a < target_max or b < target_max:
    if a < b:
        total += a
        a += 3
    elif a == b:
        total += a
        a += 3
        b += 5
    else:
        total += b
        b += 5

print(total)
