"""
The nth term of the sequence of triangle numbers is given by, t_n = ½n(n+1); so the first ten triangle numbers are:

1, 3, 6, 10, 15, 21, 28, 36, 45, 55, ...

By converting each letter in a word to a number corresponding to its alphabetical position and adding these values we form a word value. For example, the word value for SKY is 19 + 11 + 25 = 55 = t_10. If the word value is a triangle number then we shall call the word a triangle word.

Using data/p42_words.txt, a 16K text file containing nearly two-thousand common English words, how many are triangle words?
"""
from lib.seq import which_triangle_num
from lib.words import word_value


with open('data/p42_words.txt') as fh:
    words = fh.read().strip().replace('"', '').split(',')

print(len(list(filter(which_triangle_num, map(word_value, words)))))
