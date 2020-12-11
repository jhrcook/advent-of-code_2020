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


def get_plausible_range(a, min_a, max_a):
    return list(range(max(min_a, a - 1), min(max_a, a + 2)))


def get_neighbors(i, j, ary):
    """Get the neighbors for seat a (i, j)."""
    neighbors = []
    i_range = get_plausible_range(i, 0, ary.shape[0])
    j_range = get_plausible_range(j, 0, ary.shape[1])
    for a, b in product(i_range, j_range):
        if i != a or j != b:
            neighbors.append(ary[a, b])
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
            elif seats_0[i, j] == "#" and n_neighbors >= 4:
                # Seat becomes empty.
                seats_1[i, j] = "L"

print(f"seats converged at step: {count}")  # 98
num_seats_occupied = np.sum(seats_0 == "#")
print(
    answer_highlight + f"number of seats occupied at equilibrium: {num_seats_occupied}"
)
