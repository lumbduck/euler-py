"""
An irrational decimal fraction is created by concatenating the positive integers:

0.123456789101112131415161718192021...

It can be seen that the 12th digit of the fractional part is 1.

If dn represents the nth digit of the fractional part, find the value of the following expression.

d1 × d10 × d100 × d1000 × d10000 × d100000 × d1000000
"""
import time

start_time = time.time()

ordinal_limit = 6


####
# This is a slow version that runs brute force generation of all Champernowne digits
####
# def champernowne_digits():
#     for i in itertools.count():
#         for dig in str(i):
#             yield int(dig)
#
#
# digit_locations = [10**j for j in range(ordinal_limit + 1)]
# last_digit = digit_locations[-1]
#
# print("Finding nth digits of Champernowne's constant for n in {}".format(digit_locations))
#
# target = 1
# for i, d in enumerate(champernowne_digits()):
#     if i in digit_locations:
#         target *= d
#     if i == last_digit:
#         break
####


# The fast version: this counts the number of digits generated at each order of magnitude for integers, i.
# Then you can directly choose the appropriate integer that gives the next target digit.
digit_locations = [10**j - 1 for j in range(ordinal_limit + 1)]
j = 1
total = 1
num_digits = 0
next_num_digits = 9
for find_index in digit_locations:
    # We need to seek forward to see if we would exceed our target digit location
    while next_num_digits <= find_index:
        num_digits = next_num_digits

        j += 1
        next_num_digits += j * (10**j - 10**(j - 1))

    # Now we know that num_digits is less than the target index.
    # We also know that all additional integers required to get to find_index have the same order of magnitude
    #   i.e., they all have j digits.
    # This gives us enough info to simply start from 10**(j-1) and count out to the appropriate integer.
    relative_int, relative_digit = divmod(find_index - num_digits, j)
    i = 10**(j - 1) + relative_int
    total *= int(str(i)[relative_digit])

print("Total: {}".format(total))
print("Execution time: {}".format(time.time() - start_time))
