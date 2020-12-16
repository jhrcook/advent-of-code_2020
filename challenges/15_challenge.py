from pathlib import Path
from time import time

import colorama
import numpy as np

# Prepare colorama to highlight printed solutions.
colorama.init(autoreset=True)
answer_highlight = colorama.Fore.BLUE + colorama.Style.BRIGHT

# Input data.
input_data = "12,1,16,3,11,0"
values = [int(x) for x in input_data.split(",")]

n_turns = 30000000
starting_turn = len(values) + 1

# Dictionary to hold at what index a value was previously used.
previous_idx = {}  # [value: idx]
# Dictionary to hold at what index a value was last used.
last_idx = {val: idx + 1 for idx, val in enumerate(values)}  # [value: idx]
# The value used in the previous turn. (updated each turn)
previous_value = values[-1]

# Start timer.
start_time = time()

for turn in range(starting_turn, n_turns + 1):
    try:
        new_value = last_idx[previous_value] - previous_idx[previous_value]
    except:
        new_value = 0

    try:
        previous_idx[new_value] = last_idx[new_value]
    except:
        None

    last_idx[new_value] = turn
    previous_value = new_value

# End timer.
finish_time = time()

print("")
print(f"operation took {(finish_time - start_time) / 60:.2f} min.")
print(answer_highlight + f"{n_turns}th answer: {previous_value}")
