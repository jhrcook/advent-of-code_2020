from collections import Counter
from pathlib import Path

import colorama as clr

# Prepare colorama to highlight printed solutions.
clr.init(autoreset=True)
answer_highlight = clr.Fore.BLUE + clr.Style.BRIGHT

# Input data.
input_data_path = Path("data/day_10/input.txt")
adapters = [0]
with open(input_data_path, "r") as file:
    for l in file:
        adapters.append(int(l.rstrip()))

adapters.sort()
adapters.append(max(adapters) + 3)
jolt_diff = []
for i in range(1, len(adapters)):
    jolt_diff.append(adapters[i] - adapters[i - 1])

print(jolt_diff[:5])
jolt_diff_count = Counter(jolt_diff)
print(f"number of jolt differences:")
for i in (1, 3):
    print(f"  {i}: {jolt_diff_count[i]}")

print(answer_highlight + f"puzzle 1 answer: {jolt_diff_count[1] * jolt_diff_count[3]}")
