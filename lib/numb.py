from collections import Counter
from functools import lru_cache, reduce
from itertools import permutations
import math
from operator import mul
from string import digits

POSITIVE_DIGITS = digits[1:]


@lru_cache(maxsize=None)
def num_digits(n, base=10):
    """Return number of digits in n."""
    assert n >= 0, "Must provide a non-negative integer"
    if n == 0:
        return 1
    else:
        if base == 10:
            this_log = math.log10
        elif base == 2:
            this_log = math.log2
        else:
            return math.floor(math.log(n, base)) + 1
        return math.floor(this_log(n)) + 1


def same_digits(n, digits):
    """Return True if n has exactly the digits in :param digits: (any iterable of digits)."""
    return sorted(str(n)) == sorted(digits)


def comb(n, k):
    """Return nCr (n-choose-k)."""
    # This is available as math.comb in python 3.8+
    k = min(n - k, k)
    if k <= 0:
        return 1
    elif k == 1:
        return n

    p = reduce(mul, range(n, n - k, -1), 1)
    q = reduce(mul, range(1, k + 1), 1)

    return p // q


def perm(n, preserve_length=True):
    """Return set of numbers that are permutations of the digits of n."""
    if preserve_length:
        # Throw away any permutations that begin with a zero
        return set(map(lambda x: int(''.join(x)), filter(lambda x: x[0] != '0', permutations(str(n)))))
    else:
        return set(map(lambda x: int(''.join(x)), permutations(str(n))))


def incr(n, base=10, incr=1):
    """
    Return str representation of next sequential integer in the given base.

    NOTE: Params :n: and :incr: must be provided in the given base.
    """
    assert base <= 10, "Can only increment in base 10 or less"
    return to_str((int(str(n), base) + incr), base)


def reverse(n):
    "Return string in reverse (converts numbers to strings)"
    # For some reason this is slightly faster than str(s)[::-1]
    return str(n)[::-1]


def is_palindrome(x):
    str_x = str(x)
    if tuple(str_x) == tuple(reversed(str_x)):
        return True


def is_pandigital(n, pandigits):
    return num_digits(n) == len(pandigits) and set(str(n)) == set(pandigits)


def is_permutation(m, n, base=10):
    "Return True if the digits of m and n are a permutation of each other."
    return Counter(to_str(m, base=base)) == Counter(to_str(n, base=base))


def to_base(n, base=10):
    """
    Return a str representation of the decimal number n in the given base.

    NOTE: Only works for :base: <= 10.
    """
    if n == 0:
        return '0'
    elif base == 2:
        if int(n) < 0:
            return '-' + bin(-int(n))[2:]
        else:
            return bin(int(n))[2:]
    elif n < 0:
        return -to_base(-int(n), base)
    else:
        p, r = divmod(int(n), base)
        if p:
            return to_base(p, base) + str(r)
        else:
            return str(r)


def to_str(n, base=10):
    """Return decimal integer n as a str in the given base."""
    if base == 10:
        return str(n)
    else:
        return to_base(n, base=base)
