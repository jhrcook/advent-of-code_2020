from itertools import product
from pathlib import Path

import numpy as np

# Read in data file as a list of integers.
input_file = Path("data", "day_01", "input.txt")
data = []
with open(input_file, "r") as input_data:
    for line in input_data:
        data.append(int(line))


def challenge1(data, num_values=2, target_value=2020):
    """General solver for challenge 1."""
    data_array = [data for _ in range(num_values)]
    for values in product(*data_array):
        if np.sum(values) == target_value:
            print("Solution found.")
            return np.product(values)


# Solve challenge 1.
sol1 = challenge1(data, 2, 2020)
print(f"solution 1: {sol1}")
sol2 = challenge1(data, 3, 2020)
print(f"solution 2: {sol2}")
