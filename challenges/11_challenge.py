from itertools import product
from pathlib import Path

import colorama
import numpy as np

# Prepare colorama to highlight printed solutions.
colorama.init(autoreset=True)
answer_highlight = colorama.Fore.BLUE + colorama.Style.BRIGHT

# Input data.
input_data_path = Path("data/day_11/input.txt")
seats = []
with open(input_data_path, "r") as file:
    for l in file:
        seats.append(list(l.rstrip()))

seats = np.asarray(seats)


def get_above(i, j, ary):
    return np.flip(ary[:i, j])


def get_below(i, j, ary):
    return ary[i + 1 :, j]


def get_left(i, j, ary):
    return np.flip(ary[i, :j])


def get_right(i, j, ary):
    return ary[i, (j + 1) :]


def get_lr_diag_values(i, j, ary):
    """Get the values along the left-right (standard) diagonal."""
    rows, cols = np.indices(ary.shape)
    row_idx = np.diag(rows, k=j - i)
    col_idx = np.diag(cols, k=j - i)
    return ary[row_idx, col_idx]


def get_upleft(i, j, ary):
    return np.flip(get_lr_diag_values(i, j, ary)[: min(i, j)])


def get_dnright(i, j, ary):
    return get_lr_diag_values(i, j, ary)[(min(i, j) + 1) :]


def get_rl_diag_values(i, j, ary):
    """Get the values along the right-left diagonal."""
    new_j = (ary.shape[1] - 1) - j
    rows, cols = np.indices(ary.shape)
    row_idx = np.diag(rows, k=new_j - i)
    col_idx = np.diag(cols, k=new_j - i)
    return np.flip(np.fliplr(ary)[row_idx, col_idx])


def get_dnleft(i, j, ary):
    return np.flip(get_rl_diag_values(i, j, ary)[: min(j, ary.shape[0] - 1 - i)])


def get_upright(i, j, ary):
    return get_rl_diag_values(i, j, ary)[(min(j, ary.shape[0] - 1 - i) + 1) :]


def get_neighbors(i, j, ary):
    """Get the neighbors for seat a (i, j)."""
    neighbors = []

    for f in [
        get_above,
        get_below,
        get_left,
        get_right,
        get_upleft,
        get_upright,
        get_dnleft,
        get_dnright,
    ]:
        s = f(i, j, ary)
        s = s[s != "."]
        if len(s) > 0:
            neighbors.append(s[0])

    return np.array(neighbors)


def count_occupied_neighbors(neighbors):
    """Count the number of occupied neighboring seats."""
    return sum(neighbors == "#")


seats_0 = seats.copy()
seats_1 = seats.copy()
seats_1[seats_1 == "L"] = "#"
count = 1
while not np.all(seats_0 == seats_1):

    seats_0 = seats_1.copy()
    count += 1
    print(f"loop number: {count}", end="\r")

    for i in range(seats.shape[0]):
        for j in range(seats.shape[1]):
            if seats[i, j] == ".":
                # Skip if no seat.
                next
            n_neighbors = count_occupied_neighbors(get_neighbors(i, j, seats_0))
            if seats_0[i, j] == "L" and n_neighbors == 0:
                # Seat becomes taken.
                seats_1[i, j] = "#"
            elif seats_0[i, j] == "#" and n_neighbors >= 5:
                # Seat becomes empty.
                seats_1[i, j] = "L"

print(f"seats converged at step: {count}")  # takes 86 steps
num_seats_occupied = np.sum(seats_0 == "#")
print(
    answer_highlight + f"number of seats occupied at equilibrium: {num_seats_occupied}"
)
