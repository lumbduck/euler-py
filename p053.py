"""
Combinatoric Selections

There are exactly ten ways of selecting three from five, 12345:

123, 124, 125, 134, 135, 145, 234, 235, 245, and 345

We will denote this number of combinations by comb(5, 3)=10.

In general, comb(n, r)=n! / r!(n−r)!, where r≤n, n!=n×(n−1)×...×3×2×1, and 0!=1.

It is not until n=23, that a value exceeds one-million: comb(23, 10)=1144066.

How many, not necessarily distinct, values of comb(n, r) for 1≤n≤100, are greater than one-million?
"""
from numpy import array, convolve, float64

from numb import comb
from common import elapsed

lower_bound = 1000000
n_limit = 100


def combinatorial_solution():
    total = 0

    for n in range(n_limit, 0, -1):
        midpoint, is_odd = divmod(n, 2)

        # Test middle value if n is even (symmetry about this point since there are equal choices for 0 items as for n)
        if not is_odd:
            if comb(n, midpoint) > lower_bound:
                total += 1
            else:
                # Since this process is working down from 100 and this is the largest remaining binomial coefficient, we are done
                break

        for k in range(midpoint - (not is_odd), 0, -1):
            if comb(n, k) > lower_bound:
                # Except for the midpoint handled above, there are always two symmetric binomial coefficients,
                #   comb(n, k) and comb(n, n-k)
                total += 2
            else:
                # Working from the middle outward ensures that no other value for n can exceed the limit
                break

    return total


def combinatorial_solution_inverted():
    total = 0

    for n in range(23, n_limit + 1):
        # Starting from the edge of the triangle, at comb(n, 1), we work toward the middle until exceeding the lower_bound
        # At that point, all further values for that row (up to symmetry) will exceed the same bound.
        # Thus we can simply count how many values are left from that point and ignore comb(n, k).
        for k in range(n):
            if comb(n, k) > lower_bound:
                # NOTE: We know that n=23 gives 4 values over the 1000000. All subsequent rows have more.
                # Thus we never have to worry about the middle value, comb(n, n/2) being miscounted when n is even.
                total += n + 1 - 2 * k
                break

    return total


def dynamic_solution_with_convolutions():
    """Use convolutions of [1, 1] to generate rows of Pascal's triangle (i.e., binomial coefficients)."""
    total = 0

    row_n = array((1,), dtype=float64)  # Row 0 of Pascal's triangle, to be updated in place using convolutions of [1, 1]
    conv_kernel = array((1, 1), dtype=float64)

    for n in range(1, n_limit + 1):
        row_n = convolve(row_n, conv_kernel)
        total += len(row_n[row_n > lower_bound])

    return total


def dynamic_solution():
    """Directly compute the values of Pascal's triangle."""
    total = 0

    # Keeping one (symmetric) half of Pascal's triangle, starting from row n=1 and updating in place
    row_n = [1]  # In this format, rows 2-4 will look like [1, 2], [1, 3], [1, 4, 6], respectively.

    for n in range(2, n_limit + 1):
        half_n, is_odd = divmod(n, 2)
        is_even = not is_odd

        if is_even:
            # Get middle value of row and check against bound
            mid_value = 2 * row_n[0]
            if mid_value > lower_bound:
                total += 1

        # Sum other terms and check against bound
        # NOTE: there are two of each value due to symmetry
        for k in range(half_n - is_even):
            val = row_n[k] + row_n[k + 1]
            row_n[k] = val
            if val > lower_bound:
                total += 2

        if is_even:
            # Append middle value
            row_n.insert(0, mid_value)

    return total


print(f"There are {dynamic_solution_with_convolutions()} values of comb(n, r) that exceed {lower_bound} for natural numbers, n, up to {n_limit}")
elapsed()

##################
# Performance Testing
##################
# from timeit import timeit
#
# A lot of variation here, especially with numpy, but these the rough results
# ~4.6s:
# print(timeit(dynamic_solution, number=10000))
#
# ~5.5s:
# print(timeit(combinatorial_solution_inverted, number=10000))
#
# ~4.4s
# print(timeit(dynamic_solution_with_convolutions, number=10000))
