import lib.prime as prime


primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541]

reduce_by_factor_expected_results = [
    ((6, 4), (6, 0)),
    ((6, 6), (1, 1)),
    ((12, 2), (3, 2))
]


def test_reduce_by_factor():
    for pair in reduce_by_factor_expected_results:
        assert prime.reduce_by_factor(*pair[0]) == pair[1], "Failed: reduce {} by {}".format(pair[0][0], pair[0][1])


def test_prime_factors_sync():
    """
    Check that both prime factoring functions return the same results up to 10000.

    Both functions depend on :func prime.reduce_by_factor:. Thus this test only roughly ensures accuracy.
    """
    for i in range(2, 10000):
        assert prime.prime_factors(i) == prime.prime_factors_precomputed(i), "Prime factorizations out of sync"


def test_is_prime():
    for p in primes:
        assert prime.is_prime(p), "Failed primality test with :cache_primes:=True (p={})".format(p)


def test_is_prime_no_cache():
    for p in primes:
        assert prime.is_prime(p, False), "Failed primality test with :cache_primes:=False (p={})".format(p)
