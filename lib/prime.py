from functools import lru_cache, reduce
from itertools import count, product, takewhile
from math import sqrt
from operator import mul


# A cache of sequential primes for avoiding multiple runs of :func sieve_primes:
CACHED_PRIMES_L = [2]
CACHED_PRIMES = set(CACHED_PRIMES_L)


# Generation and cache tools
def update_prime_cache(sorted_cache):
    global CACHED_PRIMES, CACHED_PRIMES_L
    CACHED_PRIMES_L = sorted_cache
    CACHED_PRIMES = set(CACHED_PRIMES_L)


def clear_prime_cache():
    update_prime_cache([2])


def sieve_primes(max_prime=None, num_primes=None):
    if (not max_prime and not num_primes):
        raise TypeError("Must provide an integer for at least one of :max_prime: or :num_primes:")

    # Check cache before calculating
    if max_prime and max_prime <= CACHED_PRIMES_L[-1]:
        return [p for p in CACHED_PRIMES_L if p <= max_prime]
    elif num_primes and num_primes <= len(CACHED_PRIMES):
        return CACHED_PRIMES_L[:num_primes + 1]

    # Special case for 2 since we don't want to deal with even numbers
    elif max_prime == 2 or num_primes == 1:
        return [2]

    # Set starting conditions
    if CACHED_PRIMES and len(CACHED_PRIMES) > 1:
        primes = CACHED_PRIMES_L[1:]  # Will reinsert 2 at end
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
    update_prime_cache(primes)

    return primes


def primes(step=10000, reverse=False):
    """Return infinite generator of primes, where :param step: indicates how to compromise performance by looking ahead."""
    assert step >= 3, ":param step: must be at least 3"

    low_index = 0

    for i in count(1):
        # Update cache while getting upper index for this step
        high_index = len(sieve_primes(step * i))

        # # XXX
        # print("INDECES: {}, {}".format(low_index, high_index))
        # if high_index > 10:
        #     break

        if high_index == low_index:
            # The step was too small to find another prime

            # TODO: Test and deploy warning feature
            # step_failures += 1
            # if step_failures % 100 == 0:
            #     warn("step size failing to generate primes in :func primes: with :step:={} ({} skipped steps so far)".format(step, step_failures))
            continue

        if reverse:
            # Start at the top of each step range
            # NOTE: For reverse order slicing of the prime cache, the high_index is off by one
            high_index -= 1
            if not low_index:
                for p in CACHED_PRIMES_L[high_index::-1]:
                    yield p

            else:
                for p in CACHED_PRIMES_L[high_index:low_index:-1]:
                    yield p

        else:
            for p in CACHED_PRIMES_L[low_index:high_index]:
                yield p
                low_index = p

        low_index = high_index


# Factoring tools
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
    """Return dict of prime factorization of n, in the form {prime_i: power_i} for primes [prime_1, prime_2,...]."""
    if n < 2:
        return {}

    factors = dict()

    # Special case 2
    n_reduced, factor_count = reduce_by_factor(n, 2)
    if factor_count:
        factors[2] = factor_count
    # Special case 3
    n_reduced, factor_count = reduce_by_factor(n_reduced, 3)
    if factor_count:
        factors[3] = factor_count

    # Remaining primes are all of the form 6*k +/- 1
    k = 1
    while n_reduced > 1:
        for test_factor in (6 * k - 1, 6 * k + 1):
            n_reduced, factor_count = reduce_by_factor(n_reduced, test_factor)
            if factor_count:
                factors[test_factor] = factor_count
        k += 1

    return factors


@lru_cache(maxsize=None)
def prime_factors_precomputed(n):
    """
    Return dict of prime factorization of n, in the form {prime_i: power_i} for primes [prime_1, prime_2,...].

    Precomputes primes, which improves performance over :func prime_factors: when iterating over many factorizations.
    """
    if n < 2:
        return {}

    factors = dict()
    for p in sieve_primes(max_prime=sqrt(n) + 1):
        n, factor_count = reduce_by_factor(n, p)
        if factor_count:
            factors[p] = factor_count
        if n <= 1:
            break

    if n > 1:
        # After dividing out all primes up to sqrt(n), if n is still not 1 then the remainder is prime
        factors[n] = 1

    return factors


# Factorization tools that take parameters in format returned by :func prime_factors:
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


# Miscellaneous
def is_prime(n, cache_primes=True):
    """Return True if n is prime, and otherwise False.

    Parameters:
        :int n: integer to test for primality
        :bool cache_primes: If True, generates all primes up `n` to test primality. If you plan on testing many primes then this can be exploited for performance gains by testing large primes first.
    """
    if n < 2:
        return False
    elif cache_primes:
        if n <= CACHED_PRIMES_L[-1]:
            if n in CACHED_PRIMES:
                return True
            else:
                return False
        elif n in sieve_primes(max_prime=n):
            return True
        else:
            return False
    else:
        # Special case 2 and 3
        if n in (2, 3):
            return True
        elif n % 2 == 0 or n % 3 == 0:
            return False
        else:
            # Remaining primes are all of the form 6*k +/- 1
            for k in range(1, int(sqrt(n) + 1) // 6 + 1):
                for test_factor in (6 * k - 1, 6 * k + 1):
                    if n % test_factor == 0:
                        return False

    return True


def sum_raised_primes(p, power_of_p):
    """Return sum of p raised to each power k, for 1 <= k <= power_of_p."""
    # Given by a closed form expression
    return int((p**(power_of_p + 1) - 1) / (p - 1))


@lru_cache(maxsize=None)
def sum_divisors(n):
    """Return sum of all proper divisors of n (excludes n itself)."""
    if n == 1:
        return 0
    # Return value is given by a closed form based on prime factorization
    factorization = prime_factors(n)
    return reduce(mul, (sum_raised_primes(p, k) for p, k in factorization.items())) - n
