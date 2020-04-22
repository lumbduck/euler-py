"""
The following iterative sequence is defined for the set of positive integers:

n → n/2 (n is even)
n → 3n + 1 (n is odd)

Using the rule above and starting with 13, we generate the following sequence:

13 → 40 → 20 → 10 → 5 → 16 → 8 → 4 → 2 → 1
It can be seen that this sequence (starting at 13 and finishing at 1) contains 10 terms. Although it has not been proved yet (Collatz Problem), it is thought that all starting numbers finish at 1.

Which starting number, under one million, produces the longest chain?

NOTE: Once the chain starts the terms are allowed to go above one million.
"""
from lib.seq import collatz
from datetime import datetime

start_time = datetime.now()

test_limit = 1000000
collatz_cache = {}


def collatz_run(n):
    "Return then length of a Collatz sequence for n"
    curr_len = 0
    for c in collatz(n):
        if c in collatz_cache:
            collatz_cache[n] = curr_len + collatz_cache[c]
            return collatz_cache[n]
        else:
            curr_len += 1

    collatz_cache[n] = curr_len
    return collatz_cache[n]


leader = None
seq_len = 0
for n in range(1, test_limit + 1):
    curr_len = collatz_run(n)
    if curr_len > seq_len:
        seq_len = curr_len
        leader = n
        print("New leader {} ({} elements)".format(n, curr_len))

print("Longest sequence from {} ({} elements)".format(leader, seq_len))
print("Execution time: {}".format(datetime.now() - start_time))
