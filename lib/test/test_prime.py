import lib.prime as prime

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
