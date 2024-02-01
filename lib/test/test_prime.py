from functools import update_wrapper
import lib.prime as prime
import pytest


# Pytest fixtures
@pytest.fixture()
def clear_prime_cache():
    """Clear module-level prime caching in prime.py before executing a test."""
    print("\nClearing prime cache")
    prime.clear_prime_cache()
    yield


# Clean up lru_cache wrappers so that introspection works during test reporting
update_wrapper(prime.lru_cache, prime.prime_factors)
update_wrapper(prime.lru_cache, prime.prime_factors_precomputed)
update_wrapper(prime.lru_cache, prime.sum_divisors)


########################
# Test data
########################

# First 100 primes, used for several tests
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541]

# Expected outcomes for reduce_by_factor test
reduce_by_factor_expected = [
    ((6, 4), (6, 0)),
    ((6, 6), (1, 1)),
    ((12, 2), (3, 2))
]


########################
# Tests
########################

def test_reduce_by_factor():
    for pair in reduce_by_factor_expected:
        assert prime.reduce_by_factor(*pair[0]) == pair[1], "Failed: reduce {} by {}".format(pair[0][0], pair[0][1])


def test_prime_factors_sync(clear_prime_cache):
    """
    Check that both prime factoring functions return the same results up to 10000.

    Both functions depend on :func prime.reduce_by_factor:. Thus this test only roughly ensures accuracy.
    """
    for i in range(2, 1000):
        assert prime.prime_factors(i) == prime.prime_factors_precomputed(i), "Prime factorizations out of sync"


def test_sieve_primes_max_6_lower_edge(clear_prime_cache):
    """Test whether :param max_prime: result does not exceed the given value."""
    assert prime.sieve_primes(max_prime=primes[6] - 1) == primes[:6]


def test_sieve_primes_max_6_upper_edge():
    """
    Test whether :param max_prime: result includes the given value.

    NOTE: Omitted clear_prime_cache teardown, which conflates two edge case tests due to result of previous test
        (:func test_sieve_primes_max_6_lower_edge:). I.e., before generating the expected 6th prime, sieve_primes
        must first recognize that the cache has not been sufficiently updated for the given value.
    """
    assert prime.sieve_primes(max_prime=primes[6]) == primes[:7]


def test_sieve_primes(clear_prime_cache):
    assert prime.sieve_primes(num_primes=100) == primes, "Failed to sieve first 100 primes."


def test_is_prime(clear_prime_cache):
    for p in primes:
        assert prime.is_prime(p), "False negative for primality test with :cache_primes:=True (p={})".format(p)


def test_is_prime_composite(clear_prime_cache):
    for c in filter(lambda x: x not in primes, range(primes[-1])):
        assert not prime.is_prime(c), "False positive for primality test with :cache_primes:=True (p={})".format(c)


def test_is_prime_no_cache(clear_prime_cache):
    for p in primes:
        assert prime.is_prime(p, cache_primes=False), "False negative for primality test with :cache_primes:=False (p={})".format(p)
        assert prime.CACHED_PRIMES_L == [2], "Erroneous cache generation during primality test"


def test_is_prime_no_cache_composite(clear_prime_cache):
    for c in filter(lambda x: x not in primes, range(primes[-1])):
        assert not prime.is_prime(c, cache_primes=False), "False positive for primality test with :cache_primes:=False (c={})".format(c)
        assert prime.CACHED_PRIMES_L == [2], "Erroneous cache generation during primality test"


def test_primes(clear_prime_cache):
    for step_size in range(3, 15):
        generated = list()
        for i, p in enumerate(prime.primes(step=step_size)):
            if i >= 100:
                break
            generated.append(p)

        assert generated == primes, "Failed prime generator. (:step_size:={})".format(step_size)


def test_primes_start_index(clear_prime_cache):
    step_size = 14
    for start_index in range(30):
        generated = list()
        for i, p in enumerate(prime.primes(start_index=start_index, step=step_size)):
            if i >= 100 - start_index:
                break
            generated.append(p)

        assert generated == primes[start_index:], "Failed prime generator with start_index {}. (:step_size:={})".format(start_index, step_size)


def test_primes_reverse(clear_prime_cache):
    for step_size in range(3, 15):
        generated = list()
        for i, p in enumerate(prime.primes(step=step_size, reverse=True)):
            if i >= 110:
                # NOTE: This test must retrieve a extra results since the iteration is not in numerical order.
                # Since the largest step_size is only 15 we just retrieve a few and then slice them out.
                break
            generated.append(p)

        assert sorted(generated)[:100] == primes, "Failed prime generator with :reverse:=True. (:step_size:={})".format(step_size)
