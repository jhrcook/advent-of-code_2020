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

    def __str__(self):
        return self.bitmask


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


def augment_value(x: int, mask: Mask) -> str:
    """Augment a value using a mask."""
    x_b = dec_to_b36(x)
    y_b = [a if b == "X" else b for a, b in zip(x_b, mask.bitmask)]
    y_b = "".join(y_b)
    y = b36_to_dec(y_b)
    return y


memory = {}
mask = None
for d in input_data:
    if "mask" in d:
        mask = Mask(d)
        print(f"current mask: {mask}", end="\r")
    else:
        loc, val = split_memory_command(d)
        memory[loc] = augment_value(val, mask)

print("")
print(answer_highlight + f"sum of stored values: {sum(list(memory.values()))}")
