"""
Totient Maximum

Euler's totient function, phi(n) [sometimes called the phi function], is defined as the number of positive integers not exceeding `n` which are relatively prime to `n`. For example, as 1, 2, 4, 5, 7, and 8, are all less than or equal to nine and relatively prime to nine, phi(9) = 6.

n   Relatively Prime        phi(n)  n / phi(n)
2	1	                    1	    2
3	1,2	                    2	    1.5
4	1,3	                    2	    2
5	1,2,3,4	                4	    1.25
6	1,5	                    2	    3
7	1,2,3,4,5,6	            6	    1.1666...
8	1,3,5,7	                4	    2
9	1,2,4,5,7,8	            6	    1.5
10	1,3,7,9	                4	    2.5
It can be seen that n = 6 produces a maximum n / phi(n) for n <= 10.

Find the value of n <= 1 000 000 for which n / phi(n) is a maximum.
"""
from collections import defaultdict
from math import sqrt

from pandas import DataFrame

from lib.common import elapsed, split_timer
from lib.prime import gcd, prime_factors_precomputed, primes

MAX_RANGE = 10 ** 6
REPORT_RANGE = set(range(50, 1000, 50)) if MAX_RANGE <= 1000 else set(range(1000, MAX_RANGE, 1000))
REPORT_LEVEL = 1

# Initialize split timer
split_timer()


# For detailed report level, stuff some results into a dataframe for reporting output/inspection
if REPORT_LEVEL > 1:
    def assign_default_df_data() -> dict[str, int | float]:
        return {
            'gcd_phi': -1,
            'gcd_ratio': -1,
            'factor_phi': -1,
            'factor_ratio': -1,
        }

    df_data: dict[int, dict[str, int | float]] = defaultdict(assign_default_df_data)


# Method 1: use GCD to directly calculate phi
def phi_by_gcd(n: int) -> float:
    phi = 2  # assume 1 and n - 1 to start
    if n % 2 == 0:
        # reduce tests for even numbers
        test_range = (n - 3, 2, -2)
    else:
        phi += 1  # since 2 is coprime
        test_range = (n - 2, 2, -1)

    for i in range(*test_range):
        if gcd(i, n) == 1:
            phi += 1
    return phi


def find_largest_ratio_by_gcd(maximum: int = MAX_RANGE, report_level=REPORT_LEVEL):
    print("\nUsing direct GCD calculation...")
    largest_ratio = 3.0
    best_n = 6

    for n in range(maximum, 10, -1):
        phi = phi_by_gcd(n)
        ratio = n / phi

        if report_level:
            if n in REPORT_RANGE:
                print(f"Reporting: phi({n})={phi}")

            if report_level > 1:
                df_data[n].update({
                    'gcd_phi': phi,
                    'gcd_ratio': ratio,
                })

        if ratio > largest_ratio:
            largest_ratio = ratio
            best_n = n
            print(f"New largest: {n} (ratio={largest_ratio})")

    print(f"\nLargest ratio: {largest_ratio} for n={best_n}")


# Method 2: compare prime factors to calculate phi indirectly
def find_largest_ratio_by_prime_factors(maximum: int = MAX_RANGE, report_level=REPORT_LEVEL):
    print("\nUsing prime factors comparison...")
    print("Precomputing prime factors...")
    factors = {
        # Prime factorization (without powers) keyed to each composite integer
        # NOTE: Order of range is reversed to kick lib.prime caching into gear
        n: set(prime_factors_precomputed(n))
        for n in range(maximum, 1, -1)
    }

    # Sort so we can compare slices
    factors_list = sorted(list(factors))

    # How long did prime factorization take?
    split_timer()

    largest_ratio = 3.0
    best_n = 6

    # We compare each set of prime factors to determine which numbers are coprime
    for i, n in enumerate(factors_list):
        # contra_phi is the sum of numbers less than n which are not coprime to n
        contra_phi = sum(any(factors[n].intersection(factors[m])) for m in factors_list[:i])
        phi = n - contra_phi - 1
        ratio = n / phi

        if ratio > largest_ratio:
            largest_ratio = ratio
            best_n = n
            print(f"New largest: {n} (ratio={largest_ratio})")

        if report_level:
            if n in REPORT_RANGE:
                print(f"Reporting: phi({n})={phi}")

            if report_level > 1:
                df_data[n].update({
                    'factor_phi': phi,
                    'factor_ratio': ratio,
                })

    print(f"\nLargest ratio: {largest_ratio} for n={best_n}")


# Method 3: The right way, by direct construction
# There's no need to do anything other than take the product of unique primes until we exceed the upper limit
# This ensures the maximum number of divisors (and fewest coprimes)
def construct_largest_ratio_n(maximum: int = MAX_RANGE):
    print("\nUsing direct construction...")
    n = 1
    for p in primes(step=sqrt(maximum) // 1):
        n *= p
        if n > maximum:
            print(f"Largest ratio phi(n)/n given by n={n}")
            return


print(f"\nDetermining largest ratio of n to phi(n) for n <= {MAX_RANGE}.")


if __name__ == '__main__':
    for f in (
        construct_largest_ratio_n,
        # find_largest_ratio_by_prime_factors,
        # find_largest_ratio_by_gcd
    ):
        f()
        split_timer()

    print("\n")
    if REPORT_LEVEL > 1:
        df = DataFrame.from_dict(df_data, orient="index")
        print(df[(df['gcd_phi'] != df['factor_phi']) & (df['gcd_phi'] > -1)])

    elapsed()
