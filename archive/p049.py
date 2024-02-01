"""
Prime Permutations

The arithmetic sequence, 1487, 4817, 8147, in which each of the terms increases by 3330, is unusual in two ways: (i) each of the three terms are prime, and, (ii) each of the 4-digit numbers are permutations of one another.

There are no arithmetic sequences made up of three 1-, 2-, or 3-digit primes, exhibiting this property, but there is one other 4-digit increasing sequence.

What 12-digit number do you form by concatenating the three terms in this sequence?
"""
from itertools import takewhile
from time import time

from lib.numb import perm
from lib.prime import is_prime, primes


def primes_four():
    """Return generator of 4-digit primes, largest first."""
    return takewhile(lambda x: x > 1000, primes(reverse=True, step=10000))


def get_triples(p):
    perms = sorted(filter(lambda x: x < p, perm(p)))
    if not perms:
        return []

    candidate_triples = []
    for i, k in enumerate(perms):
        if (p + k) / 2 in perms[i + 1:]:
            candidate_triples.append(sorted((k, (p + k) // 2, p)))
    return candidate_triples


start_time = time()

for p in primes_four():
    arithm_triples = get_triples(p)
    for triple in arithm_triples:
        if all([is_prime(x) for x in triple]):
            print("Found triple: {} (Concatenated: {})".format(triple, ''.join(map(str, triple))))

print("Execution time: {}".format(time() - start_time))
