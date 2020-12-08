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


def run_code(code):
    code_finished = True
    current_line = 0
    total_accumulated = 0

    while True:
        # Check the line of code.
        if current_line == len(code):
            code_finished = True
            break
        elif current_line > len(code):
            code_finished = False
            break

        line = code[current_line]

        # Game loop.
        if line.has_been_executed:
            # Stop if the code has been run before.
            code_finished = False
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

    return (total_accumulated, current_line, code_finished)


def swap_operation(l):
    """Swap the operation from 'jmp' <--> 'nop' for a line of code."""
    if l.op == "jmp":
        l.op = "nop"
    elif l.op == "nop":
        l.op = "jmp"
    else:
        return False
    return True


# Try changing each line of code and seeing if the program finishes.
for change_line_i in range(len(code)):

    # Reset the `has_been_executed` attribute for each line.
    for l in code:
        l.has_been_executed = False

    # Change the line of code if it is "jmp" or "op".
    # (returns whether or not the code was changed)
    code_did_change = swap_operation(code[change_line_i])

    if code_did_change:
        res = run_code(code)
        swap_operation(code[change_line_i])
        if res[2]:
            print(
                answer_highlight
                + f"changed line {change_line_i} to finish with total: {res[0]}"
            )
