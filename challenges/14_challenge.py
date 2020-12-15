from itertools import product
from pathlib import Path
from typing import List

import colorama
import numpy as np

# Prepare colorama to highlight printed solutions.
colorama.init(autoreset=True)
answer_highlight = colorama.Fore.BLUE + colorama.Style.BRIGHT


# Input data.
input_data_path = Path("data/day_14/input.txt")
input_data = []
with open(input_data_path, "r") as file:
    for l in file:
        input_data.append(l.rstrip())


class Mask:
    """A maks object used by the 'port' (in the puzzle)."""

    def __init__(self, str_bitmask):
        self.bitmask = str_bitmask.replace("mask = ", "")
        self.num_floats = self.bitmask.count("X")

    def __str__(self):
        return f"{self.bitmask} (num. floats: {self.num_floats})"


def dec_to_b36(d: int) -> str:
    """Convert decimal into 36b."""
    return "{:036b}".format(d)


def b36_to_dec(b):
    """Convert 36b into decimal."""
    return int(b, 2)


def split_memory_command(s: str) -> List[int]:
    """Split a memory command into location and value."""
    x = s.replace("mem", "").replace("[", "").replace("]", "").replace(" ", "")
    return [int(y) for y in x.split("=")]


def apply_mask_to_location(x: int, mask: Mask) -> str:
    """Augment a memory location using a mask."""
    x_b = dec_to_b36(x)
    y_b = []

    for a, b in zip(x_b, mask.bitmask):
        if b == "0":
            y_b.append(a)
        elif b == "1":
            y_b.append("1")
        elif b == "X":
            y_b.append("X")
        else:
            raise Exception(f"Unknown value in bitmask: {b}")

    y_b = "".join(y_b)
    return y_b


def get_all_possible_locations(loc: int, mask: Mask) -> List[str]:
    """Get all of the possible memory locations when augmented by a mask."""
    mask_loc = apply_mask_to_location(loc, mask)
    mask_loc_ary = np.array(list(mask_loc))
    possible_locs = []
    float_values = [[0, 1] for _ in range(mask.num_floats)]
    for float_value in product(*float_values):
        mask_loc_ary = np.array(list(mask_loc))
        mask_loc_ary[mask_loc_ary == "X"] = np.array(float_value)
        possible_locs.append("".join(list(mask_loc_ary)))
    return possible_locs


memory = {}  # The "memory" units.
mask = None  # The current mask.
for d in input_data:
    if "mask" in d:
        mask = Mask(d)
        print(f"current mask: {mask}", end="\r")
    else:
        loc, val = split_memory_command(d)
        all_locs = get_all_possible_locations(loc, mask)
        for l in all_locs:
            memory[l] = val

print("")
print(answer_highlight + f"sum of stored values: {sum(list(memory.values()))}")
