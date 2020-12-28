from itertools import product
from pathlib import Path

import colorama
import numpy as np

np.random.seed(0)

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
print("Building tile graph... ", end="")
for t1, t2 in product(tiles_names, tiles_names):
    if t1 == t2:
        continue
    for side1, side2 in product(tiles[t1].possible_sides, tiles[t2].possible_sides):
        if np.all(side1 == side2):
            tile_graph[t1] = tile_graph[t1].union([t2])
            tile_graph[t2] = tile_graph[t2].union([t1])
            break
print("done")

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


# Iterate over edges
print("Iterating over edge tiles to assemble tile grid... ", end="")
for i, j in product(range(width), range(width)):
    if tile_grid[i, j] == 0:
        neighbors = get_neighbors(tile_grid, i, j)
        neighbors = [x for x in neighbors if x != 0]
        if i == 0 or j == 0 or i == width - 1 or j == width - 1:
            next_tile = [
                t for t, ns in tile_graph.items() if appears_atleast(ns, neighbors, 1)
            ]
            next_tile = [t for t in next_tile if t in edge_tiles]
            tile_grid[i, j] = next_tile[0]
            edge_tiles = [x for x in edge_tiles if x != next_tile[0]]
print("done")

# Iterate through insides
print("Iterating over inner tiles to assemble tile grid... ", end="")
for i, j in product(range(1, width - 1), range(1, width - 1)):
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
print("done")

if DEBUG:
    print(tile_grid)


tile = tiles[1951]
tile_width = tile.array.shape[0]

transformed_tiles = {}


def identity(a):
    """A function that returns the input array."""
    return a


def random_transform(a):
    """Randomly transform a tile."""
    transforms = [np.fliplr, np.flipud, np.rot90, identity]
    return np.random.choice(transforms)(a)


def random_flip(a):
    """Randomly flip a tile."""
    transforms = [np.fliplr, np.flipud, identity]
    return np.random.choice(transforms)(a)


def random_flip_lr(a):
    """Randomly flip a tile (left/right only)."""
    transforms = [np.fliplr, identity]
    return np.random.choice(transforms)(a)


def check_tile_row(m, width):
    """Check that a row of tiles fits."""
    b = []
    for k in range(width - 1, m.shape[1] - 1, width):
        b.append(np.all(m[:, k] == m[:, k + 1]))
    return np.all(b)


print("Assembling rows of ordered tiles... ", end="")
sorted_tile_rows = []
for i in range(width):
    print(f"{i} ", end="")
    sorted_tile_row = []
    for j in range(0, tile_grid.shape[1], 2):
        row_tiles = [tiles[t].array for t in tile_grid[i, j : j + 2]]
        while True:
            row_tiles = [random_transform(t) for t in row_tiles]
            tile_row = np.hstack(row_tiles)
            if check_tile_row(tile_row, tile_width):
                sorted_tile_row.append(tile_row)
                break
    while True:
        sorted_tile_row = [random_flip(t) for t in sorted_tile_row]
        tile_row = np.hstack(sorted_tile_row)
        if check_tile_row(tile_row, tile_width):
            sorted_tile_rows.append(tile_row)
            break
print("done")

print("Stacking sorted rows to build full image... ", end="")
sorted_tile_rows = [a.transpose() for a in sorted_tile_rows]
while True:
    sorted_tile_rows = [random_flip_lr(t) for t in sorted_tile_rows]
    tile_image = np.hstack(sorted_tile_rows)
    if check_tile_row(tile_image, tile_width):
        full_image = tile_image
        break
print("done")

if DEBUG:
    print(full_image)

# Remove duplicate rows and columns
idx = []
for i in range(tile_grid.shape[0]):
    idx += [x + (i * tile_width) for x in [0, tile_width - 1]]
full_image = np.delete(full_image, idx, axis=0)
full_image = np.delete(full_image, idx, axis=1)

if DEBUG:
    full_image = np.rot90(full_image)
    full_image = np.flipud(full_image)
    string_image = full_image.copy()
    string_image = string_image.astype("str")
    string_image[string_image == "0"] = "."
    string_image[string_image == "1"] = "#"

    string_image_rows = []
    for i in range(string_image.shape[0]):
        string_image_rows.append("".join(string_image[i, :]))
    print("\n".join(string_image_rows))

SEA_MONSTER = [
    "                  # ",
    "#    ##    ##    ###",
    " #  #  #  #  #  #   ",
]
SEA_MONSTER = [x.replace(" ", "0") for x in SEA_MONSTER]
SEA_MONSTER = [x.replace("#", "1") for x in SEA_MONSTER]
SEA_MONSTER = [list(x) for x in SEA_MONSTER]
SEA_MONSTER = [np.array(x, dtype=int) for x in SEA_MONSTER]
SEA_MONSTER = np.array(SEA_MONSTER)
if DEBUG:
    print(SEA_MONSTER)

INVERSE_SEA_MONSTER = (SEA_MONSTER.copy() - 1) * -1
if DEBUG:
    print(INVERSE_SEA_MONSTER)


def detect_and_remove_sea_monster(m, verbose=True):
    if np.sum(m * SEA_MONSTER) == np.sum(SEA_MONSTER):
        if verbose:
            print("Detected sea monster!")
        return m * INVERSE_SEA_MONSTER
    else:
        return m


if DEBUG:
    print("(test seamonster):")
    TEST_MONSTER = [
        [0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1],
        [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1],
        [0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
    ]
    print(detect_and_remove_sea_monster(TEST_MONSTER))


starting_sum = np.sum(full_image)
monster_height, monster_width = SEA_MONSTER.shape
num_of_checks = 0

print("Searching for monsters... ", end="")
for _ in range(2):
    full_image = np.fliplr(full_image)
    for _ in range(2):
        full_image = np.flipud(full_image)
        for _ in range(4):
            full_image = np.rot90(full_image)
            for i in range(0, full_image.shape[0] - monster_height):
                for j in range(0, full_image.shape[1] - monster_width):
                    m = full_image[i : i + monster_height, j : j + monster_width]
                    if not np.all(m.shape == SEA_MONSTER.shape):
                        raise Exception("In correct sub-matrix dimensions.")
                    full_image[
                        i : i + monster_height, j : j + monster_width
                    ] = detect_and_remove_sea_monster(m, verbose=False)
                    num_of_checks += 1
print("done")
print(f"checked {num_of_checks} sub-matrices")
final_sum = np.sum(full_image)
print(f"started with {starting_sum} 1's and finished with {final_sum}.")
print(answer_highlight + f"the habitat's water roughness: {final_sum}")
