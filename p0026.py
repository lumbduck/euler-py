"""
A unit fraction contains 1 in the numerator. The decimal representation of the unit fractions with denominators 2 to 10 are given:

1/2	= 	0.5
1/3	= 	0.(3)
1/4	= 	0.25
1/5	= 	0.2
1/6	= 	0.1(6)
1/7	= 	0.(142857)
1/8	= 	0.125
1/9	= 	0.(1)
1/10	= 	0.1
Where 0.1(6) means 0.166666..., and has a 1-digit recurring cycle. It can be seen that 1/7 has a 6-digit recurring cycle.

Find the value of d < 1000 for which 1/d contains the longest recurring cycle in its decimal fraction part.
"""
from datetime import datetime

start_time = datetime.now()

dividend_limit = 1000


def generate_unit_fraction(n):
    """Returns (q, r), where q is the next digit in the unit fraction and r is the remainder of the previous long-division step."""
    assert n > 1, "n must be an integer greater than 1"

    r = 1
    while True:
        q, r = divmod(r * 10, n)
        yield q, r


longest = (0, 0)
for n in range(2, dividend_limit):
    encountered_quotients = []
    for q, r in generate_unit_fraction(n):
        if (q, r) in encountered_quotients:
            repeat_len = len(encountered_quotients) - encountered_quotients.index((q, r))
            if repeat_len > longest[1]:
                longest = (n, repeat_len)
                # print("Current winner: 1/{} has {} repeating digits".format(n, repeat_len))
            break
        else:
            encountered_quotients.append((q, r))

print(longest)
print("Execution time: {}".format(datetime.now() - start_time))
