from collections import Counter
from pathlib import Path

import colorama
import numpy as np

# Prepare colorama to highlight printed solutions.
colorama.init(autoreset=True)
answer_highlight = colorama.Fore.BLUE + colorama.Style.BRIGHT

# Input data.
input_data_path = Path("data/day_10/input.txt")
adapters = [0]
with open(input_data_path, "r") as file:
    for l in file:
        adapters.append(int(l.rstrip()))

print(f"number of adapters: {len(adapters)}")


## Puzzle 1

adapters.sort()
adapters.append(max(adapters) + 3)
jolt_diff = []
for i in range(1, len(adapters)):
    jolt_diff.append(adapters[i] - adapters[i - 1])

jolt_diff_count = Counter(jolt_diff)
print(f"number of jolt differences:")
for i in (1, 3):
    print(f"  {i}: {jolt_diff_count[i]}")

print(answer_highlight + f"puzzle 1 answer: {jolt_diff_count[1] * jolt_diff_count[3]}")


## Puzzle 2

# Get boundaries for spliting the adapters where the
# difference in jolts is 3.
splits = list(np.where(np.asarray(jolt_diff) == 3)[0] + 1)
splits = [0] + splits + [len(adapters)]

# Count the number adapters in strings of 1
split_lengths = [b - a for a, b in zip(splits[:-1], splits[1:])]
split_counts = Counter(split_lengths)

# Table of the number of arrangements that can be made when removing
# 0, 1, or 2 adapters from a segment of 1s.
# > | length | 0 | 1 | 2 | total |
# > |--------|---|---|---|-------|
# > | 2      | 1 | 0 | 0 | 1     |
# > | 3      | 1 | 1 | 0 | 2     |
# > | 4      | 1 | 2 | 1 | 4     |
# > | 5      | 1 | 3 | 3 | 7     |

# Use the above table to calculate the number of combinations.
num_arrangements = 2 ** split_counts[3] * 4 ** split_counts[4] * 7 ** split_counts[5]
print(answer_highlight + f"number of different arrangements: {num_arrangements}")


## Puzzle 2 (with strings)
# I realized, after completing the second puzzle with the method above,
# that the splitting, subtracting, counting, etc could be easily done
# by converting the jolt difference array into a string and splitting
# by 3. This method is performed below and produces the same answer
# as above.

# Turn the array of jolt differences into a string and split at "3".
strings_of_ones = "".join([str(i) for i in jolt_diff]).split("3")
# Count the lengths of the split strings of "11...11" and offset by 1.
split_count_str = Counter([len(s) + 1 for s in strings_of_ones])
# Use the above table to calculate the number of combinations.
num_arrangements_str = (
    2 ** split_counts[3] * 4 ** split_counts[4] * 7 ** split_counts[5]
)
print(
    answer_highlight
    + f"number of different arrangements (str method): {num_arrangements_str}"
)
