from pathlib import Path

import numpy as np

# Read in data file as a list of integers.
input_file = Path("data", "day_01", "input.txt")
data = []
with open(input_file, "r") as input_data:
    for line in input_data:
        data.append(int(line))

# Loop over all possible combinations to find solution.
sum_to_2020 = []
for i in range(0, len(data)):
    for j in range(i, len(data)):
        if data[i] + data[j] == 2020:
            sum_to_2020 = [data[i], data[j]]
            print(f"values found: {sum_to_2020[0]} + {sum_to_2020[1]} = 2020")

answer = sum_to_2020[0] * sum_to_2020[1]
print(f"Solution: {answer}")
