from itertools import permutations
from math import sqrt

from numb import incr, POSITIVE_DIGITS, reverse, to_base, to_str


# Generators

def collatz(n=None):
    """Return generator for the terms of the collatz sequence for n."""
    while True:
        yield n
        if n == 1:
            return
        halved, is_odd = divmod(n, 2)
        if is_odd:
            n = 3 * n + 1
        else:
            n = halved


def fib(n=None):
    """Return generator for the first n Fibonnaci numbers, (or leave n=None for infinite iteration)."""
    prev = 0
    curr = 1
    if n is not None and n >= 0:
        for i in range(0, n):
            yield curr
            new = curr + prev
            prev = curr
            curr = new
    else:
        while True:
            yield curr
            new = curr + prev
            prev = curr
            curr = new


def pair_iter(start=1, asymmetric=True, strategy='descending'):
    """
    Return a generator which iterates over pairs of integers (i, j) in a regular pattern.

    Parameters:
        :bool asymmetric: If True, i < j for all pairs. Otherwise all possible 2 tuples are traversed.
        :str strategy: Allows `ascending`, `descending`, or `alternating`. This determines if the first term is
            incremented or decremented as the second term increases. For `alternating`, they both alternate direction.
    """
    i = j = start
    if asymmetric:
        if strategy == 'alternating':
            while True:
                j += 1
                while i < j:
                    yield i, j
                    i += 1
                j += 1
                while i > 1:
                    yield i, j
                    i -= 1

        elif strategy == 'ascending':
            while True:
                j += 1
                while i < j:
                    yield i, j
                    i += 1
                i = start

        elif strategy == 'descending':
            while True:
                j += 1
                while i >= start:
                    yield i, j
                    i -= 1
                i = j

        else:
            raise ValueError("Specify a valid strategy.")

    else:
        if strategy == 'alternating':
            while True:
                yield i, j
                j += 1
                while j > start:
                    yield i, j
                    i += 1
                    j -= 1
                yield i, j
                i += 1
                while i > start:
                    yield i, j
                    i -= 1
                    j += 1

        if strategy == 'ascending':
            while True:
                yield i, j
                j += 1
                i = start
                while i < j:
                    yield i, j
                    i += 1

        if strategy == 'descending':
            while True:
                yield i, j
                j += 1
                i = j
                while i > start:
                    yield i, j
                    i -= 1

        else:
            raise ValueError("Specify a valid strategy.")


def palindromes(lower=None, upper=None, base=10):
    """
    Return generator of str representations of palindromic numbers.

    NOTE: lower and upper bounds should be given in base 10, regardless of :param base:
    """
    assert base > 0 and base <= 10, "Base must be an integer between 1 and 10, inclusive."
    if not lower:
        lower = 0

    curr_pal = to_base(lower, base)  # Except here, this is guaranteed to be palindromic during generation
    rollover_digit = str(base - 1)  # Used to check if an integer is about to rollover a new digit

    # Generate 1-digit palindromes if necessary
    len_lower = len(to_str(lower, base))
    if len_lower == 1:
        temp_upper = min(base, upper) if upper else base
        while int(curr_pal, base) < temp_upper:
            yield curr_pal
            curr_pal = incr(curr_pal, base)

    # Some defaults
    pal_prefix = '1'
    middle_digit = ''
    len_pal_prefix = 1

    # Set up the palindrome prefix and middle digit, starting from the lower limit if necessary
    if lower >= base:
        # We can ignore lower limits below the base since those numbers have already been yielded
        len_pal_prefix, is_odd_len = divmod(len_lower, 2)
        pal_prefix = to_str(lower, base)[:len_pal_prefix]

        if is_odd_len:
            middle_digit = to_str(lower, base)[len_pal_prefix]

    # We will generate palindromes by reflecting the prefix over itself (inserting a middle digit when necessary.)
    # E.g., consider lower = 500, which gives us pal_prefix = 5, and middle_digit = 0 (in base 10).
    # From there, we repeatedly increment the middle_digit and roll it over in the base numeral system.
    # We increment pal_prefix each time middle_digit rolls over:
    # 505, 515, 525,...,595, 606, 616,..., 696, 707,...,999
    # From here we ignore the middle digit and increment pal_prefix until all of its digits roll over:
    # 1001, 1111, 1221,..., 1991,..., 9999
    # From here, we put the middle_digit back in and start the process over with pal_prefix = 10 and middle_digit = 0
    # Note how pal prefix must restart from 10 when middle_digit is put back in.
    # The next elements will include 10001, 10101,...,19991,...,99999, at which point pal_prefix becomes 100.
    curr_pal = pal_prefix + middle_digit + reverse(pal_prefix)
    while not upper or int(curr_pal, base) < upper:
        if int(curr_pal, base) >= lower:
            yield curr_pal

        if middle_digit:
            if middle_digit == rollover_digit:
                # When the base number is all 9s we have to turn over a new digit and remove the middle digit
                pal_prefix = incr(pal_prefix, base)
                if len(pal_prefix) == len_pal_prefix:
                    middle_digit = '0'
                else:
                    len_pal_prefix += 1
                    middle_digit = ''

            else:
                middle_digit = incr(middle_digit, base)

        else:
            pal_prefix = incr(pal_prefix, base)
            if len(pal_prefix) > len_pal_prefix:
                middle_digit = '0'
                pal_prefix = pal_prefix[:-1]

        curr_pal = pal_prefix + middle_digit + pal_prefix[::-1]


def pandigitals(d, reverse_order=False, include_zero=True):
    """Return generator for d-digit pandigital numbers (or d+1 digits if :param include_zero:=True)."""
    assert d < 10, "Pandigitals can be generated with at most 9 nonzero digits"

    pandigits = POSITIVE_DIGITS[:d] if not reverse_order else reverse(POSITIVE_DIGITS[:d])

    if include_zero:
        if reverse_order:
            pandigits += '0'
        else:
            pandigits = '0' + pandigits
        for n in filter(lambda x: x[0] != '0', permutations(pandigits)):
            yield int(''.join(n))
    else:
        for n in permutations(pandigits):
            yield int(''.join(n))


# Closed form values from geometric sequences (along with inverse lookups and tests)

def hexagonal_num(n):
    """Return the nth hexagonal number."""
    assert n > 0 and int(n) == n, "Must provide a positive integer."
    return int(n * (2 * n - 1))


def pentagonal_num(n):
    """Return the nth pentagonal number."""
    assert n > 0 and int(n) == n, "Must provide a positive integer."
    return int(n * (3 * n - 1) / 2)


def triangle_num(n):
    """Return the nth triangle number."""
    assert n > 0 and int(n) == n, "Must provide a positive integer."
    return int(n * (n + 1) / 2)


def is_hexagonal(h):
    """Return a positive integer n, such that `t` is the nth hexagonal number, if such an n exists."""
    test_n = (1 + sqrt(1 + 8 * h)) / 4
    return test_n.is_integer()


def is_pentagonal(p):
    """Return a positive integer n, such that `p` is the nth pentagonal number, if such an n exists."""
    test_n = (1 + sqrt(1 + 24 * p)) / 6
    return test_n.is_integer()


def is_triangular(t):
    """Return a positive integer n, such that `t` is the nth triangle number, if such an n exists."""
    test_n = (-1 + sqrt(1 + 8 * t)) / 2
    return test_n.is_integer()


def which_hexagonal_num(h):
    """Return a positive integer n, such that `t` is the nth hexagonal number, if such an n exists."""
    test_n = (1 + sqrt(1 + 8 * h)) / 4
    if test_n.is_integer():
        return int(test_n)


def which_pentagonal_num(p):
    """Return a positive integer n, such that `p` is the nth pentagonal number, if such an n exists."""
    test_n = (1 + sqrt(1 + 24 * p)) / 6
    if test_n.is_integer():
        return int(test_n)


def which_triangle_num(t):
    """Return a positive integer n, such that `t` is the nth triangle number, if such an n exists."""
    test_n = (-1 + sqrt(1 + 8 * t)) / 2
    if test_n.is_integer():
        return int(test_n)


for i in range(1, 100):
    assert is_hexagonal(hexagonal_num(i)), "FAIL {}".format(i)
