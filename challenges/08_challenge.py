from pathlib import Path

import colorama as clr

# Prepare colorama to highlight printed solutions.
clr.init(autoreset=True)
answer_highlight = clr.Fore.BLUE + clr.Style.BRIGHT


class Code:
    """A line of code."""

    def __init__(self, text):
        self.text = text
        self.op, self.arg = Code.parse_text(text)
        self.has_been_executed = False

    def parse_text(text):
        split_text = text.split(" ")
        return (split_text[0], int(split_text[1]))

    def __str__(self):
        has_run = "has" if self.has_been_executed else "has not"
        res = f"`{self.op}`: {self.arg} ({has_run} run)"
        return res


# Input data.
input_data_path = Path("data/day_08/input.txt")
code = []
with open(input_data_path, "r") as file:
    for l in file:
        code.append(Code(l.rstrip()))


current_line = 0
total_accumulated = 0

# Game loop
while True:
    line = code[current_line]

    if line.has_been_executed:
        # Stop if the code has been run before.
        break
    elif line.op == "nop":
        # No operation.
        current_line += 1
    elif line.op == "acc":
        # Add value to to accumulate.
        total_accumulated += line.arg
        current_line += 1
    elif line.op:
        # Jump.
        current_line += line.arg

    line.has_been_executed = True

print(answer_highlight + f"Final aggregate: {total_accumulated}")
