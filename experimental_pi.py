from numpy.random import randint
from numpy import sqrt

sample_sz = 1000
upper_lim = 1000000
rs = zip(randint(upper_lim, size=sample_sz), randint(upper_lim, size=sample_sz))


def is_coprime(x, y):
    for a in range(2, min(x, y) + 1):
        if x % a == 0 and y % a == 0:
            # print("Factor found: {}".format(a))  # debug
            return 0
    return 1


coprime_total = 0
i = 0
print("Example output:")
try:
    for r in rs:
        r_0, r_1 = r
        if is_coprime(r_0, r_1):
            coprime_total += 1

        # Print 10 example pairs
        if i < 10:
            print("\t{}, {}".format(r_0, r_1))
        i += 1

except(KeyboardInterrupt):
    print("Interrupted...")

print("Total coprime of {} random whole numbers (up to {}): {}".format(i, upper_lim, coprime_total))
coprime_prob = coprime_total / i
print("Prob of coprime: {}".format(coprime_prob))
pi_exp = sqrt(6 / coprime_prob)

print("Experimental value of pi: {}".format(pi_exp))
