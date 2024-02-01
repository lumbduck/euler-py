"""
Prime Pair Sets

The primes 3, 7, 109, and 673, are quite remarkable. By taking any two primes and concatenating them in any order the result will always be prime. For example, taking 7 and 109, both 7109 and 1097 are prime. The sum of these four primes, 792, represents the lowest sum for a set of four primes with this property.

Find the lowest sum for a set of five primes for which any two primes concatenate to produce another prime.
"""
from collections import defaultdict
from itertools import chain

from lib.prime import is_prime, primes, sieve_primes
from lib.common import elapsed, split_timer

target_set_size = 5

# For each prime, p, keep a set of primes, q with p > q, for which (p, q) satisfy the pair_primality test.
prime_pairs = defaultdict(set)


def populate_prime_pairs(p, q):
    """Return True if concatening m and n in both orders produces two primes."""
    if p in prime_pairs and q in prime_pairs[p]:
        return True

    elif is_prime(int(str(p) + str(q))) and is_prime(int(str(q) + str(p))):
        prime_pairs[p].add(q)
        return True


def get_connected_set(p_pairs, n):
    """Return a set of n primes from the set p_pairs for which all pairs satisfy pair primality with each other, if such a set exists."""
    if len(p_pairs) >= n:
        if n == 1:
            # Done
            return p_pairs

        # Starting from large prime in p_pairs, start checking for pair primes all the way down
        #   stopping only if there are not enough primes left to reach n,
        #   or if we have found n pairwise connected primes
        p_pairs = sorted(p_pairs, reverse=True)
        for i in range(len(p_pairs) - n + 1):
            q = p_pairs[i]
            if q in prime_pairs:
                # Recurse
                q_set = get_connected_set(prime_pairs[q].intersection(p_pairs[i + 1:]), n - 1)

                if q_set:
                    q_set.add(q)
                    return q_set

            elif q == 3 and n == 2:
                # Backup base case, since 3 will never be added to prime_pairs dict
                return {3}

    return set()


def solve_by_pairing(target_size=target_set_size):
    # This algorithm will populate prime_pairs with each prime (key) pointing to a set of all
    #   smaller primes that form a valid prime pair with it.
    # Each of these is then checked by get_connected_set to see if there are enough pairwise
    #   connections to complete the problem.

    # NOTE: prime index starts from 3 to avoid primes 2 and 5, which cannot be part of any prime pair.
    # 3 is chained into the inner loop, but not the outer loop because no valid primes are less than 3.
    log_step = 1000
    next_step = 0

    for p in primes(step=10000, start_index=3):
        for q in chain(reversed(sieve_primes(max_prime=p)[3:-1]), [3]):
            populate_prime_pairs(p, q)

        if p > next_step:
            split_timer()
            print(f"Reached p > {next_step} -- {p}: {prime_pairs.get(p)}")
            next_step += log_step

        if p in prime_pairs:
            p_set = get_connected_set(prime_pairs[p], target_size - 1)
            if p_set:
                p_set.add(p)
                return sorted(p_set)[:target_size]


print(solve_by_pairing(5))
elapsed()  # Around 20 minutes!
