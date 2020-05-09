"""
Self Powers

The series, 1^1 + 2^2 + 3^3 + ... + 10^10 = 10405071317.

Find the last ten digits of the series, 11 + 22 + 33 + ... + 10001000.
"""
from time import time
from timeit import timeit

limit = 1000
digit_limit = 10


def get_slice(n, digits):
    return int(str(n)[-digits:])


def run(digits=digit_limit, limit=limit, use_compr=False, use_slice=False):
    if use_compr:
        if digits:
            if use_slice:
                total = sum(get_slice(x**x, digits) for x in range(1, 1001))
                total = total % digits
            else:
                total = sum(x**x % (10 * digits) for x in range(1, 1001))
                total = total % (10 * digits)
        else:
            total = sum(x**x for x in range(1, 1001))

    else:
        total = 0

        if digits:
            if use_slice:
                for x in range(1, limit + 1):
                    total += get_slice(x**x, digits)
                    total = get_slice(total, digits)
            else:
                for x in range(1, limit + 1):
                    total += x**x % (10 * digits)
                    total = total % (10 * digits)

        else:
            for x in range(1, limit + 1):
                total += x**x

    return total


def test():
    x = 0
    for i in range(100):
        x += i


start_time = time()
print(run(use_slice=True))
print("Execution time: {}".format(time() - start_time))


print("\ntimeit: performance tests with various looping and truncation methodologies\n")

print("Simple loop with mod", timeit('run()', globals={'run': run}, number=1000))
print("Simple loop with all digits", timeit('run(digits=None)', globals={'run': run}, number=1000))
print("List comprehension with mod", timeit('run(use_compr=True)', globals={'run': run}, number=1000))
print("List comprehension with all digits", timeit('run(digits=None, use_compr=True)', globals={'run': run}, number=1000))

# These are very slow
# print("Simple loop with slicing", timeit('run(use_slice=True)', globals={'run': run}, number=1000))
# print("List comprehension with slicing", timeit('run(use_compr=True, use_slice=True)', globals={'run': run}, number=1000))
