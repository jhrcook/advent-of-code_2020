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
invalid_number = None
for i in range(25, len(xmas_code)):
    preamble = xmas_code[i - 25 : i]
    if not sum_does_exist(preamble, target=xmas_code[i]):
        invalid_number = xmas_code[i]
        break


# Print solution to puzzle 1.
if invalid_number is None:
    print("No invalid number found 😔")
else:
    print(answer_highlight + f"Invalid number:{xmas_code[i]}")


def find_weakness(code, L, target):
    """
    Find the contiguous array that sums to the target value.
    Returns the calculated weakness value.
    """
    for i in range(L, len(code)):
        a = xmas_code[i - L : i]
        if sum(a) == target:
            return calc_encryption_weakness(a)
    return None


def calc_encryption_weakness(a):
    """Calculate the encryption weakness from the contiguous array."""
    return min(a) + max(a)


# Loop through all possible sizes of array to find the weakness
min_len = 2
max_len = len(xmas_code) - 1
weakness = None
for L in range(min_len, max_len):
    print(f"size of array: {L}", end="\r")
    weakness = find_weakness(code=xmas_code, L=L, target=invalid_number)
    if weakness is not None:
        break

# Print solution to puzzle 2.
print("")
if weakness is None:
    print(answer_highlight + f"No encryption weakness found 😔")
else:
    print(answer_highlight + f"Encryption weakness: {weakness}")
