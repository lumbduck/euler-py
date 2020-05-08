from string import ascii_uppercase

CHAR_VALUES = {}

for i, a in enumerate(ascii_uppercase, start=1):
    CHAR_VALUES[a] = i


def letter_value(a):
    return CHAR_VALUES[a]


def word_value(word):
    return sum(map(letter_value, word.upper()))
