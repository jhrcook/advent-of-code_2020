from itertools import product
from pathlib import Path

import colorama
import numpy as np

# Prepare colorama to highlight printed solutions.
colorama.init(autoreset=True)
answer_highlight = colorama.Fore.BLUE + colorama.Style.BRIGHT

DEBUG = False
if DEBUG:
    input_data_file = Path("data", "day_17", "input_test.txt")
    n_cycles = 6
else:
    input_data_file = Path("data", "day_17", "input.txt")
    n_cycles = 6

# Input data.
input_data = []
with open(input_data_file, "r") as file:
    for line in file:
        d = line.rstrip().replace(".", "0").replace("#", "1")
        d = [int(x) for x in d]
        input_data.append(d)

# Create initial array  with 2 more axes for `z` and `w`.
conway_cubes = np.array(input_data)
conway_cubes = np.expand_dims(conway_cubes, axis=0)
conway_cubes = np.expand_dims(conway_cubes, axis=0)
conway_cubes = np.pad(conway_cubes, 1)

print("Starting cubes")
print(conway_cubes[1, :, :, :])
print("=" * 30)


def is_activated(ary, x, y, z, w):
    """Return the next state of a cube at (x,y,z,w)."""
    inital_val = ary[x, y, z, w]
    cube = ary[
        (x - 1) : (x + 2), (y - 1) : (y + 2), (z - 1) : (z + 2), (w - 1) : (w + 2)
    ]
    cube[1, 1, 1, 1] = 0
    total = np.sum(cube)

    if inital_val == 1 and (total < 2 or total > 3):
        return 0
    elif inital_val == 0 and total == 3:
        return 1
    else:
        return inital_val


# Simulate 6 cycles of the Conway Cubes start-up.
for i in range(n_cycles):
    previous_shape = conway_cubes.shape
    padded_cubes = conway_cubes.copy()
    padded_cubes = np.pad(padded_cubes, 1)

    index_ranges = []
    for i in previous_shape:
        index_ranges.append(range(0, i))

    for x, y, z, w in product(*index_ranges):
        conway_cubes[x, y, z, w] = is_activated(
            padded_cubes.copy(), x + 1, y + 1, z + 1, w + 1
        )

    conway_cubes = np.pad(conway_cubes, 1)

print(f"Final shape: {conway_cubes.shape}")
print(
    answer_highlight
    + f"number of active cubes after {n_cycles} cycles: {np.sum(conway_cubes)}"
)
