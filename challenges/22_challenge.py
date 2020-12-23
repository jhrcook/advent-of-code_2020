import time
from pathlib import Path

import colorama

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

print(f"length of deck 1: {len(deck1)}")
print(f"length of deck 2: {len(deck2)}")

if DEBUG:
    print("Starting state of decks:")
    print(deck1)
    print(deck2)
    print("-" * 30)


def decks_to_string(d1, d2):
    """A simple 'hash' for the two decks."""
    return (
        "D1:"
        + ",".join([str(x) for x in d1])
        + "; D2:"
        + ",".join([str(x) for x in d2])
    )


tic = time.time()


def play_recursive_combat(d1, d2):
    game_memory = set([])  # Memory of all previous decks.
    while len(d1) > 0 and len(d2) > 0:
        deck_hash = decks_to_string(d1, d2)
        if deck_hash in game_memory:
            # If the same round has already been played, break with 1 as winner.
            winner = 1
            break
        else:
            game_memory = game_memory.union({deck_hash})
            c1 = d1.pop()
            c2 = d2.pop()

            if len(d1) >= c1 and len(d2) >= c2:
                new_d1 = d1.copy()[-c1:]
                new_d2 = d2.copy()[-c2:]
                winner = play_recursive_combat(new_d1, new_d2)
            elif c1 > c2:
                winner = 1
            else:
                winner = 2

        if winner == 1:
            d1.insert(0, c1)
            d1.insert(0, c2)
        else:
            d2.insert(0, c2)
            d2.insert(0, c1)

    return winner


# Play the main game.
play_recursive_combat(deck1, deck2)

toc = time.time()
print(f"total game time: {(toc - tic):.2f} sec.")

if DEBUG:
    print("Final state of decks:")
    print(deck1)
    print(deck2)
    print("-" * 30)


def calculate_score(d):
    return sum([(i + 1) * c for i, c, in enumerate(d)])


score = 0
if len(deck1) > 0:
    score = calculate_score(deck1)
else:
    score = calculate_score(deck2)

print(answer_highlight + f"winner's score: {score}")
