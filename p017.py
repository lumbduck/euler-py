"""
If the numbers 1 to 5 are written out in words: one, two, three, four, five, then there are 3 + 3 + 5 + 4 + 4 = 19 letters used in total.

If all the numbers from 1 to 1000 (one thousand) inclusive were written out in words, how many letters would be used?


NOTE: Do not count spaces or hyphens. For example, 342 (three hundred and forty-two) contains 23 letters and 115 (one hundred and fifteen) contains 20 letters. The use of "and" when writing out numbers is in compliance with British usage.
"""
limit = 1000

ONES = {
    0: 'zero',
    1: 'one',
    2: 'two',
    3: 'three',
    4: 'four',
    5: 'five',
    6: 'six',
    7: 'seven',
    8: 'eight',
    9: 'nine',
}
TEENS = {
    10: 'ten',
    11: 'eleven',
    12: 'twelve',
    13: 'thirteen',
    14: 'fourteen',
    15: 'fifteen',
    16: 'sixteen',
    17: 'seventeen',
    18: 'eighteen',
    19: 'nineteen',
}
TENS = {
    20: 'twenty',
    30: 'thirty',
    40: 'forty',
    50: 'fifty',
    60: 'sixty',
    70: 'seventy',
    80: 'eighty',
    90: 'ninety',
}
POWERS = {
    100: 'hundred',
    1000: 'thousand',
}


def num_to_words(n):
    if n < 10:
        return ONES[n]
    elif n < 20:
        return TEENS[n]
    elif n < 100:
        tens, ones = divmod(n, 10)
        s_tens = TENS[tens * 10]
        s_ones = '-{}'.format(ONES[ones]) if ones else ''
        return s_tens + s_ones
    elif n < 1000:
        hundreds, tens = divmod(n, 100)
        s_tens = ' and {}'.format(num_to_words(tens)) if tens else ''
        s_hundreds = '{} {}'.format(ONES[hundreds], POWERS[100])
        return s_hundreds + s_tens
    elif n < 1000000 and n % 1000 == 0:
        return num_to_words(n / 1000) + ' ' + POWERS[1000]
    else:
        raise ValueError("Must enter a number between 0 and 1000 (inclusive)")


def count_letter_characters(s):
    return len(s.replace(' ', '').replace('-', ''))


character_count = 0
for i in range(1, limit + 1):
    character_count += count_letter_characters(num_to_words(i))

print(character_count)
