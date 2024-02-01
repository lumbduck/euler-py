"""
Prime Digit Replacements

By replacing the 1st digit of the 2-digit number *3, it turns out that six of the nine possible values: 13, 23, 43, 53, 73, and 83, are all prime.

By replacing the 3rd and 4th digits of 56**3 with the same digit, this 5-digit number is the first example having seven primes among the ten generated numbers, yielding the family: 56003, 56113, 56333, 56443, 56663, 56773, and 56993. Consequently 56003, being the first member of this family, is the smallest prime with this property.

Find the smallest prime which, by replacing part of the number (not necessarily adjacent digits) with the same digit, is part of an eight prime value family.
"""
from lib.prime import is_prime, primes
from lib.common import elapsed


def replace_digit(n, old, new):
    n_str = str(n)
    return int(n_str.replace(str(old), str(new)))


def generate_families(p):
    p_str = str(p)
    fams = []
    # We're going to replace each digit by all other possible digits to generate a family for testing
    for d in set(p_str):
        if p_str.find(d, p_str.find(d) + 1) == -1:
            # We only consider digits that are repeated more than once
            continue
        if p_str[-1] == d:
            # We can ignore the last digit since it will give at most 5 primes due to the even numbers being excluded
            continue
        elif p_str[0] == d:
            # Don't include 0 when replacing the first digit
            fams.append([replace_digit(p, d, i) for i in range(1, 10)])
        else:
            fams.append([replace_digit(p, d, i) for i in range(10)])

    return fams


def best_family(p):
    best = 0
    for fam in generate_families(p):
        prime_count = len(list(filter(None, (is_prime(n) for n in fam))))
        if prime_count > best:
            best = prime_count

    return best


limit = 8
best_prime = 56003
best_len = 5

for p in filter(lambda p: p > 99, primes()):
    p_best = best_family(p)
    if p_best > best_len:
        best_prime = p
        best_len = p_best
        if best_len >= limit:
            break

print("First family of {} prime: {}".format(limit, best_prime))
elapsed()
