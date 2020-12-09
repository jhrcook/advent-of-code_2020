from pathlib import Path

import colorama as clr

# Prepare colorama to highlight printed solutions.
clr.init(autoreset=True)
answer_highlight = clr.Fore.BLUE + clr.Style.BRIGHT

# Input data.
input_data_path = Path("data/day_09/input.txt")
xmas_code = []
with open(input_data_path, "r") as file:
    for l in file:
        xmas_code.append(int(l.rstrip()))


print(f"num of values: {len(xmas_code)}")


def sum_does_exist(v, target):
    """Are there two different numbers in `v` that sum to `target`?"""
    u = list(set(v))
    for idx, i in enumerate(u):
        for j in u[idx:]:
            if i != j and i + j == target:
                return True
    return False


# Check each value to find the sum in the preamble.
for i in range(25, len(xmas_code)):
    preamble = xmas_code[i - 25 : i]
    if not sum_does_exist(preamble, target=xmas_code[i]):
        print(
            answer_highlight
            + f"first number to not have sum in the preamble:{xmas_code[i]}"
        )
        break
