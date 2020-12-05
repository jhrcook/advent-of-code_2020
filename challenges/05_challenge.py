import re
from pathlib import Path

import colorama as clr
import numpy as np

# Prepare colorama to highlight printed solutions.
clr.init(autoreset=True)
answer_highlight = clr.Fore.BLUE + clr.Style.BRIGHT

# Read in data.
input_data_path = Path("data/day_05/input.txt")
boarding_passes = []
with open(input_data_path, "r") as file:
    boarding_passes = list(file)

boarding_passes = [x.rstrip() for x in boarding_passes]


def parse_binary_space_partitioning_system(x, max_n):
    """Perform the binary space partitioning algorithm to locate a single value."""
    if not bool(re.match("^[a-b]+$", x)):
        # Check that all characters in `x` are either 'a' or 'b'.
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
    """Replace the existing code with a standard one for first or second have or binary partition."""
    return bp.replace(lower_char, "a").replace(upper_char, "b")


def parse_row(x, max_row):
    """Parse row information."""
    mod_x = modify_boarding_pass_characters(x, "F", "B")
    return parse_binary_space_partitioning_system(mod_x, max_row)


def parse_col(x, max_col):
    """Parse column information."""
    mod_x = modify_boarding_pass_characters(x, "L", "R")
    return parse_binary_space_partitioning_system(mod_x, max_col)


def get_seat_location(bp, max_rows, max_cols):
    """Find a seat location of a boarding pass."""
    return (parse_row(bp[:7], max_rows), parse_col(bp[7:], max_cols))


# Get all seat locations: [(row, col)]
seat_locations = [get_seat_location(bp, 128, 8) for bp in boarding_passes]


def calculate_seat_id(r, c):
    """From the seat's location, calculate the seat ID."""
    return r * 8 + c


# List of all seat IDs.
seat_ids = [calculate_seat_id(*bp) for bp in seat_locations]

# Solution to first puzzle.
print(answer_highlight + f"highest seat id: {max(seat_ids)}")

# Create a seating chart with 0 = empty, 1 = occupied.
seating_chart = np.zeros((128, 8))
for r, c in seat_locations:
    seating_chart[r, c] = 1

# Locate my seat as unoccupied but with neighboring seat IDs occupied.
my_seat = -1
for r, c in zip(*np.where(seating_chart == 0)):
    seat_id = calculate_seat_id(r, c)
    if seat_id + 1 in seat_ids and seat_id - 1 in seat_ids:
        # Solution to second puzzle.
        print(
            answer_highlight
            + f"my seat is located at row {r}, column {c} with seat id {seat_id}"
        )
        my_seat = seat_id

# Print sad message if my seat is not located.
if my_seat == -1:
    print("I didn't find my seat 😔")
