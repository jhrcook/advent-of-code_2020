from operator import inv
from pathlib import Path
from time import perf_counter

import colorama
import numpy as np

# Prepare colorama to highlight printed solutions.
colorama.init(autoreset=True)
answer_highlight = colorama.Fore.BLUE + colorama.Style.BRIGHT


# Input data.
input_data_path = Path("data/day_13/input.txt")
input_data = []
with open(input_data_path, "r") as file:
    for l in file:
        input_data.append(l.rstrip())

timept = int(input_data[0])
buses = [int(x) for x in input_data[1].split(",") if x != "x"]
print(f"time: {timept}")
print(f"buses: {buses}")


# Puzzle 1.


def check_for_bus(buses, at_time):
    """If it exists, return the bus that would arrive at a time."""
    for bus in buses:
        if at_time % bus == 0:
            return bus
    return None


target_bus = None
for t_i in range(timept, timept + 10000):
    target_bus = check_for_bus(buses, at_time=t_i)
    if target_bus is not None:
        print(f"bus {target_bus} at {t_i}")
        print(answer_highlight + f"answer: {target_bus * (t_i - timept)}")
        break


# Puzzle 2.

print("-" * 20)

buses = [int(x) if x != "x" else np.nan for x in input_data[1].split(",")]
buses = np.array(buses)
n_buses = buses.shape[0]
nan_idx = ~np.isnan(buses)

max_bus = int(max(buses))
max_idx = int(np.where(buses == max_bus)[0][0])


MIN = 100000000000000
MAX = np.product(buses[nan_idx]).astype("int")
print(f"max value: {MAX}")

bus_order = np.argsort(buses[nan_idx])
ordered_buses = np.flip(buses[nan_idx][bus_order]).astype("int")
ordered_idx = np.flip(np.arange(n_buses)[nan_idx][bus_order]).astype("int")

m0 = {bus: MIN - (MIN % bus) - idx for idx, bus in zip(ordered_idx, ordered_buses)}

print(ordered_buses)
print(ordered_idx)


for m1 in range(MIN, MAX, min(1000000000000, MAX - 1)):
    print(f"top of range: {m1}", end="\n")
    range_set = None
    for i, bus in zip(ordered_idx, ordered_buses):

        if range_set is None:
            range_set = np.arange(m0[bus], m1, bus, dtype="int")
            m0[bus] = max(range_set)
        else:
            range_set = range_set[np.mod(range_set + i, bus) == 0]

        if range_set.shape[0] == 0:
            break

    if range_set.shape[0] > 0:
        print("")
        print(answer_highlight + f"soln: {min(range_set)}")
        break
