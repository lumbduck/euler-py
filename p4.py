######
# A palindromic number reads the same both ways. The largest palindrome made from the product of two 2-digit numbers is 9009 = 91 × 99.
#
# Find the largest palindrome made from the product of two 3-digit numbers.
######

digit_limit = 3
factor_upper_limit = sum([9 * (10 ** i) for i in range(digit_limit)])
factor_lower_limit = sum([9 * (10 ** i) for i in range(digit_limit - 1)])
print("Max possible factor: {}".format(factor_upper_limit))


def is_palindrome(x):
    str_x = str(x)
    if list(str_x) == list(reversed(str_x)):
        return True


def factor(x, upper_limit=factor_upper_limit, lower_limit=factor_lower_limit):
    for a in range(upper_limit, lower_limit, -1):
        for b in range(upper_limit, lower_limit, -1):
            if a * b == x:
                return [a, b]


def gen_palindromes(upper_limit=factor_upper_limit**2, lower_limit=(factor_lower_limit + 1)**2):
    for a in range(upper_limit, lower_limit - 1, -1):
        if is_palindrome(a):
            yield a


def main():
    for p in gen_palindromes():
        factors = factor(p)
        if factors:
            print("Palindrome: {} (given by {} * {})".format(p, *factors))
            break


main()
