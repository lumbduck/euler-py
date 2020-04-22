from collections import defaultdict
from math import sqrt
from itertools import takewhile


def prime_factors_old(n):
    factors = defaultdict(int)

    trial_factor = 2
    while n > 1:
        q, r = divmod(n, trial_factor)
        if r == 0:
            n = q
            factors[trial_factor] += 1
        else:
            trial_factor += 1

    return factors


def sieve_primes(max_prime=None, num_primes=None):
    if (not max_prime and not num_primes):
        # TODO: Is there some way to take advantage of type hints (`import typing`)
        raise TypeError("Must provide an integer for at least one of :max_prime: or :num_primes:")

    if max_prime == 2 or num_primes == 1:
        return [2]

    primes = [3]  # ignoring 2 because we won't be testing even numbers

    test_num = 5
    # Conditions for controlling the loop
    # Note that for the :num_primes: case, since 2 is left out of the primes, we need one less in the limit
    condition_basis = test_num if max_prime else len(primes)
    condition_limit = max_prime + 1 if max_prime else num_primes - 1

    while condition_basis < condition_limit:
        is_composite = False
        for p in takewhile(lambda x: x <= sqrt(test_num), primes):
            if test_num % p == 0:
                is_composite = True
                break
        if not is_composite:
            primes.append(test_num)

        # XXX: WHY DOES THIS RUN 3 TIMES SLOWER?! (Possibility that python 3.8 might fix it)
        # filtered_primes = takewhile(lambda x: x <= sqrt(i), primes)
        # if not any(i % p == 0 for p in filtered_primes):
        #     primes.append(i)

        test_num += 2
        condition_basis = test_num if max_prime else len(primes)
        condition_limit = max_prime + 1 if max_prime else num_primes - 1

    primes.insert(0, 2)
    return primes


def reduce_by_factor(n, reduct):
    n_reduced = n
    reduct_count = 0
    n_div_reduct, n_mod_reduct = divmod(n_reduced, reduct)
    while n_mod_reduct == 0:
        reduct_count += 1
        n_reduced = n_div_reduct
        n_div_reduct, n_mod_reduct = divmod(n_reduced, reduct)

    return (n_reduced, reduct_count)


def prime_factors(n):
    factors = dict()
    n_reduced, factor_count = reduce_by_factor(n, 2)
    if factor_count:
        factors[2] = factor_count
    n_reduced, factor_count = reduce_by_factor(n_reduced, 3)
    if factor_count:
        factors[3] = factor_count

    k = 1
    while n_reduced > 1:
        for test_factor in (6 * k - 1, 6 * k + 1):
            n_reduced, factor_count = reduce_by_factor(n_reduced, test_factor)
            if factor_count:
                factors[test_factor] = factor_count
        k += 1

    return factors


# XXX: The following code supports a variation of prime_factors() that relies on precomputed primes
# cached_primes = sieve_primes(max_prime=65500)


# def prime_factors_cached(n):
#     factors = dict()
#     for p in cached_primes:
#         n, factor_count = reduce_by_factor(n, p)
#         if factor_count:
#             factors[p] = factor_count
#         if n <= 1:
#             break

#     return factors
