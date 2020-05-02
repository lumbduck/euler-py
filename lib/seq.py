from lib.numb import incr, to_base, to_str


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
    """Generates n Fibonnaci numbers, (or leave n=None for infinite iteration)."""
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


def palindromes(lower=None, upper=None, base=10):
    """
    Return generator of str representations of palindromic numbers.

    NOTE: lower and upper bounds should be given in base 10, regardless of :param base:
    """
    assert base > 0 and base <= 10, "Base must be an integer between 1 and 10, inclusive."
    if not lower:
        lower = 0

    curr_pal = to_base(lower, base)  # Except here, this is guaranteed to be palindromic during generation
    rollover_digit = str(base - 1)  # Used to check if an integer is about to rollover a new digit

    # Generate 1-digit palindromes if necessary
    len_lower = len(to_str(lower, base))
    if len_lower == 1:
        temp_upper = min(base, upper) if upper else base
        while int(curr_pal, base) < temp_upper:
            yield curr_pal
            curr_pal = incr(curr_pal, base)

    # Some defaults
    pal_prefix = '1'
    middle_digit = ''
    len_pal_prefix = 1

    # Set up the palindrome prefix and middle digit, starting from the lower limit if necessary
    if lower >= base:
        # We can ignore lower limits below the base since those numbers have already been yielded
        len_pal_prefix, is_odd_len = divmod(len_lower, 2)
        pal_prefix = to_str(lower, base)[:len_pal_prefix]

        if is_odd_len:
            middle_digit = to_str(lower, base)[len_pal_prefix]

    # We will generate palindromes by reflecting the prefix over itself (inserting a middle digit when necessary.)
    # E.g., consider lower = 500, which gives us pal_prefix = 5, and middle_digit = 0 (in base 10).
    # From there, we repeatedly increment the middle_digit and roll it over in the base numeral system.
    # We increment pal_prefix each time middle_digit rolls over:
    # 505, 515, 525,...,595, 606, 616,..., 696, 707,...,999
    # From here we ignore the middle digit and increment pal_prefix until all of its digits roll over:
    # 1001, 1111, 1221,..., 1991,..., 9999
    # From here, we put the middle_digit back in and start the process over with pal_prefix = 10 and middle_digit = 0
    # Note how pal prefix must restart from 10 when middle_digit is put back in.
    # The next elements will include 10001, 10101,...,19991,...,99999, at which point pal_prefix becomes 100.
    curr_pal = pal_prefix + middle_digit + pal_prefix[::-1]
    while not upper or int(curr_pal, base) < upper:
        if int(curr_pal, base) >= lower:
            yield curr_pal

        if middle_digit:
            if middle_digit == rollover_digit:
                # When the base number is all 9s we have to turn over a new digit and remove the middle digit
                pal_prefix = incr(pal_prefix, base)
                if len(pal_prefix) == len_pal_prefix:
                    middle_digit = '0'
                else:
                    len_pal_prefix += 1
                    middle_digit = ''

            else:
                middle_digit = incr(middle_digit, base)

        else:
            pal_prefix = incr(pal_prefix, base)
            if len(pal_prefix) > len_pal_prefix:
                middle_digit = '0'
                pal_prefix = pal_prefix[:-1]

        curr_pal = pal_prefix + middle_digit + pal_prefix[::-1]
