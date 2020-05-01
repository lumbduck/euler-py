"""
Surprisingly there are only three numbers that can be written as the sum of fourth powers of their digits:

1634 = 1^4 + 6^4 + 3^4 + 4^4
8208 = 8^4 + 2^4 + 0^4 + 8^4
9474 = 9^4 + 4^4 + 7^4 + 4^4
As 1 = 1^4 is not a sum it is not included.

The sum of these numbers is 1634 + 8208 + 9474 = 19316.

Find the sum of all the numbers that can be written as the sum of fifth powers of their digits.
"""
import time

start_time = time.time()

power = 5
lower_bound = 10
upper_bound = 1000000
# Better lower bounds can probably be achieved
# Upper bound can be seen by examining this table, which shows that 6 digits are possible but not 7:
#              largest    sum of raised nines   smallest
# 2 digits:         99 <= 118098 = 2 * 59049  >  11
# 3 digits:        999 <= 177147 = 3 * 59049  >  111
# 4 digits:       9999 <= 236196 = 4 * 59049  >  1111
# 5 digits:      99999 <= 295245 = 5 * 59049  >  11111
# 6 digits:     999999 >  354294 = 6 * 59049  >  111111
# 7 digits:    9999999 >  413343 = 7 * 59049  <  1111111
# 8 digits:   99999999 >  472392 = 8 * 59049  <  11111111
# 9 digits:  999999999 >  531441 = 9 * 59049  <  111111111


def raise_digits(n, p):
    assert isinstance(n, int) and isinstance(p, int) and n >= 0 and p > 0, "Inputs must be positive integers"

    n_digits_raised_to_p = [int(d)**p for d in list(str(n))]
    return n_digits_raised_to_p


total = 0
for n in range(lower_bound, upper_bound):
    sequence = raise_digits(n, power)

    d_sum_terms_str = ' + '.join([str(k) for k in sequence])
    d_sum = sum(sequence)

    if n == d_sum:
        print("Found match: {} = {}".format(n, d_sum_terms_str))
        total += n

print("Sum of matches: {}".format(total))
print("Execution time: {}".format(time.time() - start_time))
