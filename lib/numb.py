from functools import lru_cache
import math


@lru_cache(maxsize=None)
def num_digits(n, base=10):
    """Return number of digits in n."""
    assert n >= 0, "Must provide a non-negative integer"
    return math.floor(math.log(n, base)) + 1
