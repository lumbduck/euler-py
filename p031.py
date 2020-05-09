"""
In the United Kingdom the currency is made up of pound (£) and pence (p). There are eight coins in general circulation:

1p, 2p, 5p, 10p, 20p, 50p, £1 (100p), and £2 (200p).
It is possible to make £2 in the following way:

1×£1 + 1×50p + 2×20p + 1×5p + 1×2p + 3×1p
How many different ways can £2 be made using any number of coins?
"""
from functools import lru_cache
import time

start_time = time.time()

target = 200

# numeric labels for each coin mapped to their value in pence, sorted largest to smallest in both label and value.
# This just makes it a little easier than a list to visualize what's happening in the recursion below.
coins = {
    8: 200,
    7: 100,
    6: 50,
    5: 20,
    4: 10,
    3: 5,
    2: 2,
    1: 1,
}


@lru_cache(maxsize=None)
def count_fill_combos(coin_key, fill_amount):
    """Recurses down from the given coin key until it has counted all possible combinations."""
    if coin_key < 1 or fill_amount < 1:
        return 0

    value = coins[coin_key]
    possible = fill_amount // value

    if possible == 0:
        return count_fill_combos(coin_key - 1, fill_amount)

    elif coin_key > 1:
        # Count all possible combinations which can add up to the remainder for each possible coin count
        fill_combos = 0
        for i in range(possible + 1):
            remainder = fill_amount - value * i
            if remainder > 0:
                fill_combos += count_fill_combos(coin_key - 1, remainder)
            else:
                fill_combos += 1

        return fill_combos

    elif possible == fill_amount:
        # The last coin has only one way to fill in the remainder
        return 1

    else:
        # This is a failure to fill the total fill_amount space, due to granularity of the fill_amount denominations
        # This should not happen if there is a coin of value 1
        raise ValueError("Failed to fill fill_amount space")


print("Valid combinations: {}".format(count_fill_combos(max(coins), target)))
print("Execution time: {}".format(time.time() - start_time))
