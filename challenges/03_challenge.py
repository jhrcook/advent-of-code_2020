from pathlib import Path

import numpy as np

# Import data and convert to numpy array.
input_data_path = Path("data/day_03/input.txt")
data = []
with open(input_data_path, "r") as file:
    for l in file:
        data.append(list(l.rstrip()))

data = np.asarray(data)
print(data)


def count_trees_encountered(m, dx, dy):
    """
    Count the number of trees encountered on a hill when following
    the provided slope (dx, dy).
    """
    x = 0
    tree_count = 0
    for y in range(0, m.shape[0], dy):
        _x = x % m.shape[1]
        if m[y, _x] == "#":
            tree_count += 1
        x += dx
    return tree_count


# Get solution to various slopes.
all_trees_hit = 1
for dx, dy in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
    trees_hit = count_trees_encountered(data, dx, dy)
    print(f"slope: ({dx}, {dy}) -> {trees_hit} trees")
    all_trees_hit *= trees_hit

# The solution to the second puzzle is the product of all the
# trees encountered when following the above slopes.
print(f"solution: {all_trees_hit}")
