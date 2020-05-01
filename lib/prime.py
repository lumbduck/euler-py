from collections import defaultdict
from functools import reduce, lru_cache
from itertools import takewhile, product
from math import sqrt
from operator import mul


# A cache of sequential primes for avoiding multiple runs of :func sieve_primes:
CACHED_PRIMES = [2]


def sieve_primes(max_prime=None, num_primes=None):
    if (not max_prime and not num_primes):
        # TODO: Is there some way to take advantage of type hints (`import typing`)
        raise TypeError("Must provide an integer for at least one of :max_prime: or :num_primes:")

    # Check cache before calculating
    global CACHED_PRIMES
    if max_prime and max_prime <= CACHED_PRIMES[-1]:
        return takewhile(lambda x: x <= max_prime, CACHED_PRIMES)
    elif num_primes and num_primes <= len(CACHED_PRIMES):
        return CACHED_PRIMES[:num_primes + 1]

    # Special case for 2 since we don't want to deal with even numbers
    elif max_prime == 2 or num_primes == 1:
        return [2]

    # Set starting conditions
    if CACHED_PRIMES and len(CACHED_PRIMES) > 1:
        primes = CACHED_PRIMES[1:]  # Will reinsert 2 at end
        test_num = primes[-1] + 2
    else:
        primes = [3]  # Will insert 2 at index 0 later
        test_num = 5

    # Conditions for controlling the loop
    # Note that for the :num_primes: case, since 2 is left out of the primes, we need one less in the limit
    condition_basis = test_num if max_prime else len(primes)
    condition_limit = max_prime + 1 if max_prime else num_primes - 1

    while condition_basis < condition_limit:
        sqrt_test_num = sqrt(test_num)
        is_composite = False
        for p in takewhile(lambda x: x <= sqrt_test_num, primes):
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
    CACHED_PRIMES = primes

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


@lru_cache(maxsize=None)
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


def cancel_common_factors(i_fact, j_fact):
    min_factors = {p: min(i_fact.get(p, 0), j_fact.get(p, 0)) for p in set(i_fact).union(j_fact)}
    return {p: i_fact[p] - min_factors[p] for p in i_fact}, {p: j_fact[p] - min_factors[p] for p in j_fact}


def reduce_factorization(factorization):
    return reduce(mul, (p**k for p, k in factorization.items()))


def generate_divisors(factorization):
    raised_factors = []
    for k, v in factorization.items():
        raised_factors.append([k**i for i in range(v + 1)])

    # Generate all possible products of prime factors to get all proper divisors
    product_components = product(*raised_factors)
    divisors = [reduce(mul, components) for components in product_components]
    # Remove original number from divisor list
    divisors = divisors[:-1]
    return divisors


def sum_raised_primes(p, power_of_p):
    return int((p**(power_of_p + 1) - 1) / (p - 1))


@lru_cache(maxsize=None)
def sum_divisors(n):
    if n == 1:
        return 0
    factorization = prime_factors(n)
    return reduce(mul, (sum_raised_primes(p, k) for p, k in factorization.items())) - n


@lru_cache(maxsize=None)
def is_prime(n):
    # NOTE: Due to generation of :global CACHED_PRIMES:, if you plan on testing many primes then performance is improved by testing large primes first.
    if n < 2:
        return False

    global CACHED_PRIMES
    if n in CACHED_PRIMES or n in sieve_primes(max_prime=n):
        return True
    else:
        return False


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
