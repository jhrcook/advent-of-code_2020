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


def get_next_3_cups(cups, start):
    """'Pick up' the next three cups."""
    sub_cups = []
    js = []
    for j in range(1, 4):
        j = (j + start) % len(cups)
        sub_cups.append(cups[j])
        js.append(j)

    cups = np.delete(cups, js)
    return cups, np.array(sub_cups)


# cups, subtracted_cups = get_next_3_cups(cups, 6)


def get_destination(cups, current_v):
    """Get the next destination."""
    v = current_v - 1
    while True:
        if v < min(cups):
            v = max(cups)
            break
        if v in cups:
            break
        v -= 1
    return v, np.where(cups == v)[0][0]


# print(get_destination(cups, 3))


def place_cups_at(cups, sub_cups, at):
    """Place the picked-up cups back at a specific position."""
    return np.insert(cups, at, sub_cups)


# print(place_cups_at(cups, np.array([20, 21, 22]), 4))


N_MOVES = 100
for move in range(N_MOVES):
    cups, picked_up_cups = get_next_3_cups(cups, 0)
    _, destination = get_destination(cups, cups[0])
    cups = place_cups_at(cups, picked_up_cups, destination + 1)
    cups = np.roll(cups, -1)


print(f"   final state of cups: {cups}")


def get_answer(cups):
    cups_copy = cups.copy()
    while cups_copy[0] != 1:
        cups_copy = np.roll(cups_copy, -1)
    cups_copy = cups_copy[1:]
    return "".join([str(x) for x in cups_copy])


print(answer_highlight + f"answer: {get_answer(cups)}")

# > incorrect: 85674932
