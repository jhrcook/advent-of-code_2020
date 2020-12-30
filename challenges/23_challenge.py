import pickle
from pathlib import Path
from time import time

import colorama
import numpy as np

# Prepare colorama to highlight printed solutions.
colorama.init(autoreset=True)
answer_highlight = colorama.Fore.BLUE + colorama.Style.BRIGHT


# Input data.
DEBUG = False
if DEBUG:
    input_data = "389125467"
else:
    input_data = "589174263"

cups = np.array([int(x) for x in input_data])
print(f"number of cups: {len(cups)}")
print(f"starting state of cups: {cups}")

# Add on additional cups by the crab.
cups = np.append(cups, np.arange(max(cups) + 1, 1000000 + 1))
print(f"new number of cups: {len(cups)}")


def get_next_3_cups(cups, start):
    """'Pick up' the next three cups."""
    js = np.mod((np.arange(1, 4, dtype="int") + start), len(cups))
    sub_cups = cups[js]
    cups = np.delete(cups, js)
    return cups, np.array(sub_cups, dtype="int")


def get_destination(cups, current_v):
    """Get the next destination."""
    min_cups = np.min(cups)
    v = current_v - 1
    while True:
        if v < min_cups:
            v = np.max(cups)
            break
        elif v in cups:
            break
        v -= 1
    return v, np.where(cups == v)[0][0]


def place_cups_at(cups, sub_cups, at):
    """Place the picked-up cups back at a specific position."""
    return np.insert(cups, at, sub_cups)


CACHE_DIR = Path("cache", "day_23")


def get_cache_path(move_i):
    p = CACHE_DIR / f"move-{move_i}-cache.pkl"
    return p


def cache_cups(cups, move_i):
    with open(get_cache_path(move_i), "wb") as c:
        pickle.dump(cups, c)
    return None


cache_files = [p for p in CACHE_DIR.iterdir() if p.is_file() and "cache" in p.name]
if len(cache_files) > 0:
    largest_cache = np.max([int(p.name.split("-")[1]) for p in cache_files])
    print(f"loading cache from move {largest_cache}")
    START = largest_cache
    with open(get_cache_path(largest_cache), "rb") as f:
        cups = pickle.load(f)
else:
    START = 0

N_MOVES = 10000000
for move in range(START, N_MOVES):
    if move % 100000 == 0:
        print(f"caching move: {move}")
        cache_cups(cups, move)
    cups, picked_up_cups = get_next_3_cups(cups, 0)
    _, destination = get_destination(cups, cups[0])
    cups = place_cups_at(cups, picked_up_cups, destination + 1)
    cups = np.roll(cups, -1)

if DEBUG:
    print(f"final state of cups: {cups}")


def get_answer(cups):
    cups = np.roll(cups, -np.where(cups == 1)[0][0])
    return cups[1] * cups[2]


print(answer_highlight + f"answer: {get_answer(cups)}")
