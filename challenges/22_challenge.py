from collections import Counter
from itertools import product
from pathlib import Path

import colorama
import numpy as np

# Prepare colorama to highlight printed solutions.
colorama.init(autoreset=True)
answer_highlight = colorama.Fore.BLUE + colorama.Style.BRIGHT


# Input data.
DEBUG = False
if DEBUG:
    input_data_file = Path("data", "day_22", "input_test.txt")
else:
    input_data_file = Path("data", "day_22", "input.txt")

deck1 = []
deck2 = []

current_deck = deck1
with open(input_data_file, "r") as file:
    for line in file:
        if line.rstrip() == "":
            next
        elif "Player 1" in line:
            current_deck = deck1
        elif "Player 2" in line:
            current_deck = deck2
        else:
            current_deck.append(int(line.rstrip()))

deck1.reverse()
deck2.reverse()

if DEBUG:
    print(deck1)
    print(deck2)

while len(deck1) > 0 and len(deck2) > 0:
    card1 = deck1.pop()
    card2 = deck2.pop()
    if card1 > card2:
        deck1.insert(0, card1)
        deck1.insert(0, card2)
    else:
        deck2.insert(0, card2)
        deck2.insert(0, card1)

if DEBUG:
    print(deck1)
    print(deck2)


def calculate_score(d):
    return sum([(i + 1) * c for i, c, in enumerate(d)])


score = 0
if len(deck1) > 0:
    score = calculate_score(deck1)
else:
    score = calculate_score(deck2)

print(answer_highlight + f"winner's score: {score}")
