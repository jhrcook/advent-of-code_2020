from pathlib import Path

import colorama as clr
import numpy as np

# Prepare colorama to highlight printed solutions.
clr.init(autoreset=True)
answer_highlight = clr.Fore.BLUE + clr.Style.BRIGHT

# Read in data.
input_data_path = Path("data/day_06/input.txt")
customs_answers = []
answer = set([])
with open(input_data_path, "r") as file:
    for x in file:
        if x == "\n":
            customs_answers.append(answer)
            answer = set([])
        else:
            answer = answer.union(set(x.rstrip()))
# Add on the last one.
customs_answers.append(answer)

print(f"number of groups: {len(customs_answers)}")
print(
    answer_highlight
    + f"total number of 'yes' answers: {sum([len(x) for x in customs_answers])}"
)
