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
DEBUG = True
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
    print("Tile connections:")
    for tile, connections in tile_graph.items():
        print(f"{tile} -> {connections}")
    print("=" * 30)

# Puzzle 1 answer is the product of the tile IDs in the corners.
corner_tiles = []
for tile, connections in tile_graph.items():
    if len(connections) == 2:
        corner_tiles.append(tile)

print(answer_highlight + f"product of corner tile IDs: {np.product(corner_tiles)}")

## Puzzle 2 ##

tile_graph = {tile: list(neighbors) for tile, neighbors in tile_graph.items()}

width = int(np.sqrt(len(tiles_names)))
tile_grid = np.zeros((width, width))

# 1. place the first corner
first_corner = corner_tiles[0]
tile_grid[0, 0] = first_corner

# 2. randomly place neighbors of the corner
first_neighbors = tile_graph[first_corner]
tile_grid[0, 1] = first_neighbors[0]
tile_grid[1, 0] = first_neighbors[1]

# 3. list of edge and inner tiles
edge_tiles = [tile for tile, values in tile_graph.items() if len(values) in [2, 3]]
inner_tiles = [x for x in tiles_names if x not in edge_tiles]
# remove edges already placed
edge_tiles = [x for x in edge_tiles if x not in tile_grid]


def get_neighbors(m, i, j):
    """Get the neighbors of (i,j) in matrix `m`."""
    max_i, max_j = m.shape
    neighbors = []
    if i - 1 >= 0:
        neighbors.append(m[i - 1, j])
    if i + 1 < max_i:
        neighbors.append(m[i + 1, j])
    if j - 1 >= 0:
        neighbors.append(m[i, j - 1])
    if j + 1 < max_j:
        neighbors.append(m[i, j + 1])
    return neighbors


def appears_exactly(xs, ary, num):
    """Do the values in `xs` appear in `ary` exactly `num` times."""
    count = sum([1 for x in xs if x in ary])
    return count == num


def appears_atleast(xs, ary, num):
    count = sum([1 for x in xs if x in ary])
    return count >= num


for i, j in product(range(width), range(width)):
    if tile_grid[i, j] == 0:
        neighbors = get_neighbors(tile_grid, i, j)
        neighbors = [x for x in neighbors if x != 0]
        if i == 0 or j == 0 or i == width - 1 or j == width - 1:
            next_tile = [
                t for t, ns in tile_graph.items() if appears_atleast(ns, neighbors, 1)
            ]
            print(next_tile)
            next_tile = [t for t in next_tile if t in edge_tiles]
            tile_grid[i, j] = next_tile[0]
            edge_tiles = [x for x in edge_tiles if x != next_tile[0]]

for i, j in product(range(width), range(width)):
    if tile_grid[i, j] == 0:
        neighbors = get_neighbors(tile_grid, i, j)
        neighbors = [x for x in neighbors if x != 0]
        if len(inner_tiles) > 0:
            next_tile = [
                t for t, ns in tile_graph.items() if appears_atleast(ns, neighbors, 2)
            ]
            next_tile = [t for t in next_tile if t in inner_tiles]
            tile_grid[i, j] = next_tile[0]
            inner_tiles = [x for x in inner_tiles if x != next_tile[0]]

print(tile_grid)
