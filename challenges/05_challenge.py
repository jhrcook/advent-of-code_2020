import re
from pathlib import Path

import numpy as np

# Read in data.
input_data_path = Path("data/day_05/input.txt")
boarding_passes = []
with open(input_data_path, "r") as file:
    boarding_passes = list(file)

boarding_passes = [x.rstrip() for x in boarding_passes]


def parse_binary_space_partitioning_system(x, max_n):
    # Check that all characters in `x` are either 'a' or 'b'.
    if not bool(re.match("^[a-b]+$", x)):
        raise Exception(f"Unrecognized characters in input x: {x}")

    ary = np.arange(start=0, stop=max_n, step=1, dtype="int")

    for c in x:
        half = int(len(ary) / 2)
        if c == "a":
            ary = ary[:half]
        else:
            ary = ary[half:]

    if ary.shape[0] != 1:
        raise Exception(f"Length of final array is not 1: {ary}")
    return ary[0]


def modify_boarding_pass_characters(bp, lower_char, upper_char):
    return bp.replace(lower_char, "a").replace(upper_char, "b")


def parse_row(x, max_row):
    mod_x = modify_boarding_pass_characters(x, "F", "B")
    return parse_binary_space_partitioning_system(mod_x, max_row)


def parse_col(x, max_col):
    mod_x = modify_boarding_pass_characters(x, "L", "R")
    return parse_binary_space_partitioning_system(mod_x, max_col)


def get_seat_location(bp, max_rows, max_cols):
    return (parse_row(bp[:7], max_rows), parse_col(bp[7:], max_cols))


seat_locations = [get_seat_location(bp, 128, 8) for bp in boarding_passes]


def calculate_seat_id(r, c):
    return r * 8 + c


seat_ids = [calculate_seat_id(*bp) for bp in seat_locations]

# Solution to first puzzle.
print(f"highest seat id: {max(seat_ids)}")
