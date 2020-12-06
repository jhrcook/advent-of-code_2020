from pathlib import Path

import colorama as clr

# Prepare colorama to highlight printed solutions.
clr.init(autoreset=True)
answer_highlight = clr.Fore.BLUE + clr.Style.BRIGHT

# Read in data.
input_data_path = Path("data/day_06/input.txt")
customs_answers = []  # List of all answers.
answer = set([])  # One groups answers.
is_new_group = True  # Track if there is a new group.
with open(input_data_path, "r") as file:
    for x in file:
        if x == "\n":
            # Reset for the next group.
            customs_answers.append(answer)
            answer = set([])
            is_new_group = True
        else:
            # Add new person's answers to the current group's answer.
            if is_new_group:
                answer = set(x.rstrip())
                is_new_group = False
            else:
                answer = answer.intersection(set(x.rstrip()))

# Add on the last one.
customs_answers.append(answer)

# Print results.
print(f"number of groups: {len(customs_answers)}")
print(
    answer_highlight
    + f"total number of 'yes' answers: {sum([len(x) for x in customs_answers])}"
)
