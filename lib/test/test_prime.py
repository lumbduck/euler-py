import lib.prime as prime


def test_prime_factors_sync():
    for i in range(2, 10000):
        assert prime.prime_factors(i) == prime.prime_factors_precomputed(i), "Prime factorizations out of sync"
