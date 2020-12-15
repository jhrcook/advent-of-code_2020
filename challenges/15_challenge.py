from itertools import product
from pathlib import Path
from typing import List

import colorama
import numpy as np

# Prepare colorama to highlight printed solutions.
colorama.init(autoreset=True)
answer_highlight = colorama.Fore.BLUE + colorama.Style.BRIGHT


# Input data.
input_data = "12,1,16,3,11,0"
values = np.array([int(x) for x in input_data.split(",")])

for turn in range(len(values) + 1, 2020 + 1):
    print(f"turn: {turn}", end="\r")
    previous_val = values[turn - 2]
    locs = np.where(values == previous_val)[0]
    if locs.shape[0] == 1:
        values = np.append(values, 0)
    else:
        locs = locs - 1
        next_val = locs[-1] - locs[-2]
        values = np.append(values, next_val)

print(answer_highlight + f"2020th answer: {values[-1]}")
