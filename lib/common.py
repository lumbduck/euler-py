import time

_start = time.time()
_split = None


def elapsed():
    """Print elapsed time in seconds since this module was loaded."""
    print("Elapsed time: {} seconds".format(round(time.time() - _start, 6)))


def split_timer():
    """Set split timer and, if this is not the first call to split_timer, print time since it was last set."""
    global _split
    if _split:
        print("Split time: {} seconds".format(round(time.time() - _split, 6)))
    _split = time.time()
