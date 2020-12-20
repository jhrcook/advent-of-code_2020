from itertools import product
from pathlib import Path

import colorama
import numpy as np
from numpy.core.defchararray import array
from numpy.lib.function_base import rot90
from numpy.lib.twodim_base import flipud
from numpy.random import uniform as u

# Prepare colorama to highlight printed solutions.
colorama.init(autoreset=True)
answer_highlight = colorama.Fore.BLUE + colorama.Style.BRIGHT


# Input data.
DEBUG = False
if DEBUG:
    input_data_file = Path("data", "day_20", "input_test.txt")
else:
    input_data_file = Path("data", "day_20", "input.txt")


class Tile:
    """An individual tile of the full image."""

    def __init__(self, name, array):
        self.name = name
        self.array = array
        self.assemble_possible_sides()

    def assemble_possible_sides(self):
        """Make an array of all possible sides of the tile."""
        all_sides = []
        for side in (
            self.array[0, :],
            self.array[-1, :],
            self.array[:, 0],
            self.array[:, -1],
        ):
            all_sides.append(side)
            all_sides.append(np.flip(side))
        self.possible_sides = all_sides


tiles = {}


def replace_with_numeric_list(line):
    return [1 if x == "#" else 0 for x in list(line)]


CURRENT_TILE_NAME = None
CURRENT_TILE = None
with open(input_data_file, "r") as file:
    for line in file:
        line = line.rstrip()
        if "Tile" in line:
            CURRENT_TILE_NAME = int(line.replace("Tile ", "").replace(":", ""))
        elif line == "":
            tiles[CURRENT_TILE_NAME] = Tile(name=CURRENT_TILE_NAME, array=CURRENT_TILE)
            CURRENT_TILE = None
        else:
            if CURRENT_TILE is None:
                CURRENT_TILE = np.array(replace_with_numeric_list(line))
            else:
                CURRENT_TILE = np.vstack(
                    [CURRENT_TILE, replace_with_numeric_list(line)]
                )

tiles_names = list(tiles.keys())

TILE_WIDTH = tiles[tiles_names[0]].array.shape[0]
print(f"number of tiles: {len(tiles_names)}")
print(f"tile width: {TILE_WIDTH}")

# Mapping of connections between tiles.
tile_graph = {tile: set([]) for tile in tiles_names}

# Compare all tiles to build tile graph.
for t1, t2 in product(tiles_names, tiles_names):
    if t1 == t2:
        continue
    for side1, side2 in product(tiles[t1].possible_sides, tiles[t2].possible_sides):
        if np.all(side1 == side2):
            tile_graph[t1] = tile_graph[t1].union([t2])
            tile_graph[t2] = tile_graph[t2].union([t1])
            break

if DEBUG:
    print(tile_graph)

# Puzzle 1 answer is the product of the tile IDs in the corners.
answer = 1
for tile, connections in tile_graph.items():
    if len(connections) == 2:
        answer *= tile

print(answer_highlight + f"product of corder tile IDs: {answer}")
