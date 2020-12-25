from itertools import product
from pathlib import Path

import colorama
import numpy as np

# Prepare colorama to highlight printed solutions.
colorama.init(autoreset=True)
answer_highlight = colorama.Fore.BLUE + colorama.Style.BRIGHT


# Input data.
DEBUG = False
data_dir = Path("data", "day_25")
if DEBUG:
    input_data_file = data_dir / "input_test.txt"
else:
    input_data_file = data_dir / "input.txt"

public_keys = []
with open(input_data_file, "r") as file:
    for line in file:
        public_keys.append(int(line.rstrip()))

print(f"public keys: {public_keys[0]}, {public_keys[1]}")


def find_loop_size(subject_number, target_val, max_loop_size=100):
    value = 1
    for loop_size in range(max_loop_size):
        value = (value * subject_number) % 20201227
        if value == target_val:
            return loop_size + 1
    return None


def transform_subject_number(subject_number, loop_size):
    value = 1
    for _ in range(loop_size):
        value = (value * subject_number) % 20201227
    return value


loop_sizes = [find_loop_size(7, x, max_loop_size=10000000000) for x in public_keys]
if loop_sizes[0] is None or loop_sizes[1] is None:
    raise Exception("Loop sizes not found 😢")

print(f"loop sizes: {loop_sizes[0]}, {loop_sizes[1]}")

encryption_key = transform_subject_number(public_keys[0], loop_sizes[1])
print(answer_highlight + f"encryption key: {encryption_key}")
