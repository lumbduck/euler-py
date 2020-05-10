"""
Consecutive Prime Sum

The prime 41, can be written as the sum of six consecutive primes:

41 = 2 + 3 + 5 + 7 + 11 + 13
This is the longest sum of consecutive primes that adds to a prime below one-hundred.

The longest sum of consecutive primes below one-thousand that adds to a prime, contains 21 terms, and is equal to 953.

Which prime, below one-million, can be written as the sum of the most consecutive primes?
"""
from itertools import takewhile
from operator import itemgetter
from time import time

from prime import is_prime, primes

limit = 1000000


# ~4 seconds
def dynamic_solution(limit=limit):
    """Keeps a running total of sums of primes and returns value of longest sum that is prime and less than limit."""
    start_time = time()

    # Accumlate attributes for sums starting from each prime in prime_sums.
    # Indexed by the position of the starting prime, attributes of prime_sums will be like:
    #   (start, total, best, length), where `start` is this tuple's index (for convenience),
    #   `total` is the running sum, `best` is the last total which was prime, and `length`
    #   is the length of the best sum starting from this prime
    prime_sums = []
    best_run = 1  # Just keep track of the length for optimizing stopping condition

    def update_sum(i, p, total, best, start, length, limit=limit):
        total += p
        if total > limit:
            return (None, best, start, length)  # Indicates this sum can stop accumulating

        elif is_prime(total):
            best = total
            length = i - start + 1

        return (total, best, start, length)

    for i, p in enumerate(primes()):
        for j, tally in enumerate(prime_sums):
            # Updating a cummulative total
            if tally[0]:
                prime_sums[j] = update_sum(i, p, *tally)
                if tally[3] > best_run:
                    best_run = tally[3]

            elif tally[3] < best_run:
                # This sum is no longer relevant, so we can remove it
                del prime_sums[j]

        # Create an entry for the current prime's cummulative total
        if p <= limit / best_run:
            prime_sums.append((p, p, i, i))

        # Check if we can stop (if all totals have exceeded the limit)
        elif not any(x[0] for x in prime_sums):
            res = sorted(prime_sums, key=itemgetter(3))[-1][1:]
            print("Best sum under {}: total={} ({} terms)".format(limit, res[0], res[2]))
            print("Execution time: {}".format(time() - start_time))
            return res[0]


# ~260 seconds
def slow_solution():
    """For each prime, p (starting from 2), finds the longest valid sum ending in p and returns the longest of these over all primes."""
    def sum_to_p(p, limit=limit):
        """
        Return a 2-tuple containing the largest possible prime that is a sum of consecutive primes
            ending in p, and the number of terms in the sum.
        """
        res = (p, 1)

        total = p

        # This generator will ensure that we are always list primes smallest to largest, starting 1 below p
        for i, q in enumerate(filter(lambda x: x < p, primes(reverse=True, step=p)), start=2):
            total += q

            if total > limit:
                return res

            elif is_prime(total):
                res = (total, i)

            if q == 2:
                return res

        return res

    start_time = time()
    best = (2, 1, 2)  # The sum, the number of terms in the sum, and the last prime in the sum

    for p in takewhile(lambda x: x <= limit, primes(start_index=2)):
        curr = sum_to_p(p)

        # Compare current best to the length of the longest sum ending in p
        if curr[1] > best[1]:
            best = (*curr, p)

    print("Best sum under {}: total={} ({} terms, ending in {})".format(limit, *best))
    print("Execution time: {}".format(time() - start_time))
    return best[0]


dynamic_solution()
