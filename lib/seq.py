def triangle_num(n):
    return int(n * (n + 1) / 2)


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
