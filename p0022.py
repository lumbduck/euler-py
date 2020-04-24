"""
Using data/p22_names.txt, a 46K text file containing over five-thousand first names, begin by sorting it into alphabetical order. Then working out the alphabetical value for each name, multiply this value by its alphabetical position in the list to obtain a name score.

For example, when the list is sorted into alphabetical order, COLIN, which is worth 3 + 15 + 12 + 9 + 14 = 53, is the 938th name in the list. So, COLIN would obtain a score of 938 × 53 = 49714.

What is the total of all the name scores in the file?
"""
from string import ascii_uppercase

# Generate a dictionary mapping letters to sequential values
letter_values = {}
for i, x in enumerate(ascii_uppercase):
    letter_values[x] = i + 1

# Extract and sort names
sorted_names = None
names_path = 'data/p22_names.txt'
with open(names_path) as f:
    sorted_names = f.read().replace('"', '').split(',')

sorted_names.sort()


def score_letters(name):
    return sum(letter_values[l] for l in name)


print(sum(score_letters(name) * (i + 1) for i, name in enumerate(sorted_names)))
