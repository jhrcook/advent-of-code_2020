from itertools import product
from pathlib import Path

import colorama
import numpy as np

# Prepare colorama to highlight printed solutions.
colorama.init(autoreset=True)
answer_highlight = colorama.Fore.BLUE + colorama.Style.BRIGHT


# Input data.
DEBUG = False
data_dir = Path("data", "day_24")
if DEBUG:
    input_data_file = data_dir / "input_test.txt"
else:
    input_data_file = data_dir / "input.txt"

instructions = []
with open(input_data_file, "r") as file:
    for line in file:
        instructions.append(line.rstrip())


def parse_instruction(instruction):
    """Parse the non-deliminated instruction into a list of individual moves."""
    parsed_instruction = []
    current_instruction = ""
    for i in instruction:
        if i == "n" or i == "s":
            current_instruction = i
        else:
            parsed_instruction.append(current_instruction + i)
            current_instruction = ""
    return parsed_instruction


instructions = [parse_instruction(x) for x in instructions]
print(f"there are {len(instructions)} instructions")

if DEBUG:
    print("tile flipping instructions")
    for instruction in instructions:
        print("  " + " ".join(instruction))
    print("=" * 40)

# Make a grid with plenty of space.
max_dim = np.max([len(i) for i in instructions]) * 2
grid_width = (max_dim * 2) + 1
tile_grid = np.zeros((grid_width, grid_width))
print(f"grid  dim: {tile_grid.shape}")

# The origin to start from each time.
ORIGIN = np.array([max_dim, max_dim])
print(f"origin: {ORIGIN}")


# Map cardinal directions to 2D array.
directions = {
    "e": np.array([2, 0]),
    "se": np.array([1, -1]),
    "sw": np.array([-1, -1]),
    "w": np.array([-2, 0]),
    "nw": np.array([-1, 1]),
    "ne": np.array([1, 1]),
}

#### Puzzle 1 ####

# Flip tiles.
for instruction in instructions:
    pos = ORIGIN.copy()
    for i in instruction:
        pos += directions[i]
    if tile_grid[pos[0], pos[1]] == 0:
        tile_grid[pos[0], pos[1]] = 1
    else:
        tile_grid[pos[0], pos[1]] = 0


def total_black_tiles(g):
    return int(np.sum(g))


print(answer_highlight + f"number of black tiles: {total_black_tiles(tile_grid)}")


#### Puzzle 2 ####


def count_black_neighbors(m, i, j):
    current_value = m[i, j]
    sum_neighbors = np.sum([m[i + x[0], j + x[1]] for x in directions.values()])
    return current_value, sum_neighbors


N_DAYS = 100

for day in range(1, N_DAYS + 1):
    tile_grid_padded = np.pad(tile_grid, pad_width=2)
    for i, j in product(range(tile_grid.shape[0]), range(tile_grid.shape[1])):
        current_color, num_blacks = count_black_neighbors(
            tile_grid_padded, i + 2, j + 2
        )
        if current_color == 1 and (num_blacks == 0 or num_blacks > 2):
            tile_grid[i, j] = 0
        elif current_color == 0 and num_blacks == 2:
            tile_grid[i, j] = 1
    tile_grid = np.pad(tile_grid, pad_width=2)
    if day % 10 == 0:
        print(f"day {day}: {total_black_tiles(tile_grid)}")


print(answer_highlight + f"number of black tiles: {total_black_tiles(tile_grid)}")
