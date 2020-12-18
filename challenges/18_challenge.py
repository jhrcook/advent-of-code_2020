from pathlib import Path

import colorama
import numpy as np

# Prepare colorama to highlight printed solutions.
colorama.init(autoreset=True)
answer_highlight = colorama.Fore.BLUE + colorama.Style.BRIGHT

DEBUG = False
if DEBUG:
    input_data_file = Path("data", "day_18", "input_test.txt")
    n_cycles = 6
else:
    input_data_file = Path("data", "day_18", "input.txt")
    n_cycles = 6

# Input data.
equations = []
with open(input_data_file, "r") as file:
    for line in file:
        equations.append(line.rstrip())


class Noomber:
    """Custom number where division is actually addition..."""

    def __init__(self, x):
        self.x = int(x)

    def __truediv__(self, other):
        return Noomber(self.x + other.x)

    def __mul__(self, other):
        return Noomber(self.x * other.x)

    def __str__(self):
        return f"{self.x}"


class Equation:
    """An equation of Noombers."""

    def __init__(self, str_equation):
        self.equation = Equation.parse_equation(str_equation)

    def evaluate(self):
        return eval(self.equation)

    def parse_equation(eq):
        parsed_eq = [f"Noomber({x})" if x.isdigit() else x for x in eq]
        parsed_eq = "".join(parsed_eq)
        parsed_eq = parsed_eq.replace("+", "/")
        return parsed_eq


answers = []
for equation in equations:
    answer = Equation(equation).evaluate()
    answers.append(answer.x)

print(answer_highlight + f"sum of all answers: {np.sum(answers)}")
