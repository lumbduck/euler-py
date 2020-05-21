"""
Lychrel Numbers

If we take 47, reverse and add, 47 + 74 = 121, which is palindromic.

Not all numbers produce palindromes so quickly. For example,

349 + 943 = 1292,
1292 + 2921 = 4213
4213 + 3124 = 7337

That is, 349 took three iterations to arrive at a palindrome.

Although no one has proved it yet, it is thought that some numbers, like 196, never produce a palindrome. A number that never forms a palindrome through the reverse and add process is called a Lychrel number. Due to the theoretical nature of these numbers, and for the purpose of this problem, we shall assume that a number is Lychrel until proven otherwise. In addition you are given that for every number below ten-thousand, it will either (i) become a palindrome in less than fifty iterations, or, (ii) no one, with all the computing power that exists, has managed so far to map it to a palindrome. In fact, 10677 is the first number to be shown to require over fifty iterations before producing a palindrome: 4668731596684224866951378664 (53 iterations, 28-digits).

Surprisingly, there are palindromic numbers that are themselves Lychrel numbers; the first example is 4994.

How many Lychrel numbers are there below ten-thousand?
"""
from numb import is_palindrome, reverse
from common import elapsed

limit = 10000
iter_limit = 50

# Caching for known non-Lychrel numbers (this cuts the runtime almost in half)
known_false = set()


def is_lychrel(n, iter_limit=iter_limit):
    """Return True if n is a Lychrel number (up to number of 50 iterations)."""
    # Will add to cache if non-Lychrel
    seen = {n}

    for i in range(iter_limit):
        n = n + int(reverse(n))

        if is_palindrome(n) or n in known_false:
            known_false.update(seen)
            return False
        else:
            seen.add(n)

    return True


def run(limit=limit):
    print(f"Found {sum(is_lychrel(n) for n in range(limit))} Lychrel numbers (up to {limit}, tested by {iter_limit} iterations)")


run()
elapsed()
