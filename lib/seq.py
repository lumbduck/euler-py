def collatz(n):
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
    """Generator for n Fibonnaci numbers, (or n can be left as none for infinite iteration)."""
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


def triangle_num(n):
    return int(n * (n + 1) / 2)
