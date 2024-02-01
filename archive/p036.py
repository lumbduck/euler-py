"""
The decimal number, 585 = 1001001001_(2) (binary), is palindromic in both bases.

Find the sum of all numbers, less than one million, which are palindromic in base 10 and base 2.

(Please note that the palindromic number, in either base, may not include leading zeros.)
"""
from lib.numb import is_palindrome
from lib.seq import palindromes
import time

start_time = time.time()

limit = 1000000

sum_shared = 0
count_shared = 0
total_count = 0
for p in palindromes(upper=limit, base=10):
    total_count += 1
    if is_palindrome(bin(int(p))[2:]):
        sum_shared += int(p)
        count_shared += 1

print("{} shared palindromes (from {} decimal palindromes), with sum {}".format(count_shared, total_count, sum_shared))
print("Execution time: {}".format(time.time() - start_time))
