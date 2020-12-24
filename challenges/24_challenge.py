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

# Flip tiles.
for instruction in instructions:
    pos = ORIGIN.copy()
    for i in instruction:
        pos += directions[i]
    if tile_grid[pos[0], pos[1]] == 0:
        tile_grid[pos[0], pos[1]] = 1
    else:
        tile_grid[pos[0], pos[1]] = 0


print(answer_highlight + f"number of black tiles: {int(np.sum(tile_grid))}")
