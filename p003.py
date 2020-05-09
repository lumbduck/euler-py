"""
The prime factors of 13195 are 5, 7, 13 and 29.

What is the largest prime factor of the number 600851475143 ?
"""
target = 600851475143

max_prime_factor = target
end = False


def reduce_max(max_fact, new_fact):
    check = divmod(max_fact, new_fact)
    if check[1]:
        return max_fact
    else:
        return check[0]


while end is False:
    new_max = reduce_max(max_prime_factor, 2)
    if max_prime_factor == new_max:
        break
    elif new_max == 1:
        end = True
    else:
        max_prime_factor = new_max

if end is False:
    for i in range(3, target, 2):
        if end is True:
            break

        while True:
            new_max = reduce_max(max_prime_factor, i)
            if max_prime_factor == new_max:
                break
            elif new_max == 1:
                end = True
                break
            else:
                max_prime_factor = new_max

# Solution
print(max_prime_factor)
