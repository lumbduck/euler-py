from functools import lru_cache
import math


@lru_cache(maxsize=None)
def num_digits(n, base=10):
    """Return number of digits in n."""
    assert n >= 0, "Must provide a non-negative integer"
    if n == 0:
        return 1
    else:
        return math.floor(math.log(n, base)) + 1


def incr(n, base=10, incr=1):
    """
    Return str representation of next sequential integer in the given base.

    NOTE: Params :n: and :incr: must be provided in the given base.
    """
    assert base <= 10, "Can only increment in base 10 or less"
    return to_str((int(str(n), base) + incr), base)


def is_palindrome(x):
    str_x = str(x)
    if list(str_x) == list(reversed(str_x)):
        return True


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
