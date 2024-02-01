"""
By starting at the top of the triangle below and moving to adjacent numbers on the row below, the maximum total from top to bottom is 23.

'3'
'7' 4
2 '4' 6
8 5 '9' 3
(should be formatted as center-justified)

That is, 3 + 7 + 4 + 9 = 23.

Find the maximum total from top to bottom in data/p67_triangle.txt, a 15K text file containing a triangle with one-hundred rows.

NOTE: This is a much more difficult version of Problem 18. It is not possible to try every route to solve this problem, as there are 299 altogether! If you could check one trillion (1012) routes every second it would take over twenty billion years to check them all. There is an efficient algorithm to solve it. ;o)

"""
f_path = 'data/p67_triangle.txt'
data = []
with open(f_path) as f:
    for line in f:
        data.append([int(x) for x in line.split()])

# initialize lists for storing intermediate path lengths
path_lengths = [[0] * len(line) for line in data]


def get_parents(row, column):
    parent1 = path_lengths[row - 1][column - 1] if column > 0 else 0
    parent2 = path_lengths[row - 1][column] if column < len(data[row - 1]) else 0

    return parent1, parent2


for i, l in enumerate(data):
    for j, v in enumerate(l):
        if i == 0:
            path_lengths[i][j] = v
        else:
            path_lengths[i][j] = v + max(get_parents(i, j))
    # print("Path lengths on line {}: {}".format(i, path_lengths[i]))

print(max(path_lengths[-1]))
