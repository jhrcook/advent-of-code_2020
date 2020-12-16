from pathlib import Path
from time import time

import colorama
import numpy as np

# Prepare colorama to highlight printed solutions.
colorama.init(autoreset=True)
answer_highlight = colorama.Fore.BLUE + colorama.Style.BRIGHT

# Input data.
input_data = []
input_data_file = Path("data", "day_16", "input.txt")
with open(input_data_file, "r") as file:
    for line in file:
        if line.rstrip() != "":
            input_data.append(line.rstrip())


class Rule:
    def __init__(self, txt):
        self.name = txt.split(": ")[0]
        self.values = Rule.extract_values(txt.split(": ")[1])

    def extract_values(txt):
        values = np.array([])
        for val_range in txt.split(" or "):
            a, b = [int(x) for x in val_range.split("-")]
            values = np.append(values, np.arange(a, b + 1))
        return values

    def __str__(self):
        return f"{self.name}; values: {list(self.values)}"

    def is_valid(self, x):
        return x in self.values


class Ticket:
    def __init__(self, values):
        self.values = np.array([int(x) for x in values.split(",")])

    def __str__(self):
        return f"{self.values.shape[0]} values: {list(self.values)}"


rules = []
my_ticket = None
nearby_tickets = []

my_ticket_next = False
parsing_nearby_tickets = False
for line in input_data:
    if line == "your ticket:":
        my_ticket_next = True
    elif line == "nearby tickets:":
        parsing_nearby_tickets = True
    elif not parsing_nearby_tickets and not my_ticket_next:
        rules.append(Rule(line))
    elif my_ticket_next and my_ticket is None:
        my_ticket = Ticket(line)
        my_ticket_next = False
    elif parsing_nearby_tickets:
        nearby_tickets.append(Ticket(line))

if False:
    print("RULES")
    for rule in rules:
        print(rule)

    print("\nMY TICKET")
    print(my_ticket)

    print("\nNEARBY TICKETS")
    for ticket in nearby_tickets:
        print(ticket)

    print("-" * 30)


def get_invalid_fields(t, r):
    t_set = set(t.values)
    r_set = set(r.values)
    d = t_set.difference(r_set)
    return list(d)


scanning_error_rate = 0
all_rule_values = np.concatenate([r.values for r in rules])
for ticket in nearby_tickets:
    for t_val in ticket.values:
        if t_val not in all_rule_values:
            scanning_error_rate += t_val

print(answer_highlight + f"ticket scanning error rate: {scanning_error_rate}")
