from pathlib import Path
from time import time

_data = 'data'  # relative base path for data files
_start = time()
_split = None


def data(filename):
    d_path = Path(_data)
    return d_path.joinpath(filename)


def elapsed():
    """Print elapsed time in seconds since this module was loaded."""
    print("Elapsed time: {} seconds".format(round(time() - _start, 6)))


def split_timer():
    """Set split timer and, if this is not the first call to split_timer, print time since it was last set."""
    global _split
    if _split:
        print("Split time: {} seconds".format(round(time() - _split, 6)))
    _split = time()
