from collections import Counter
from pathlib import Path

import colorama
import numpy as np

# Prepare colorama to highlight printed solutions.
colorama.init(autoreset=True)
answer_highlight = colorama.Fore.BLUE + colorama.Style.BRIGHT

# Input data.
input_data = []
DEBUG = False
if DEBUG:
    input_data_file = Path("data", "day_16", "input_test2.txt")
else:
    input_data_file = Path("data", "day_16", "input.txt")
with open(input_data_file, "r") as file:
    for line in file:
        if line.rstrip() != "":
            input_data.append(line.rstrip())


class Rule:

    """A rule for a field of a ticket."""

    def __init__(self, txt):
        self.name = txt.split(": ")[0]
        self.values = Rule.extract_values(txt.split(": ")[1])
        self.possible_positions = np.array([])

    def extract_values(txt):
        values = np.array([])
        for val_range in txt.split(" or "):
            a, b = [int(x) for x in val_range.split("-")]
            values = np.append(values, np.arange(a, b + 1))
        return values

    def find_possible_positions(self, tickets):
        """Given a list of tickets, what possible positions could this rule have."""
        ticket_value_matrix = np.stack([t.values for t in tickets])
        pos = []
        for c in range(ticket_value_matrix.shape[1]):
            check = [v in self.values for v in ticket_value_matrix[:, c]]
            if np.all(check):
                pos.append(c)
        self.possible_positions = np.array(pos)

    def __str__(self):
        return f"{self.name}\n\tvalues: {list(self.values)}\n\tpositions: {list(self.possible_positions)}"

    def is_valid(self, x):
        """Does a value satisfy the rule."""
        return x in self.values


class Ticket:

    """A train ticket with values with unknown labels."""

    def __init__(self, values):
        self.values = np.array([int(x) for x in values.split(",")])

    def __str__(self):
        return f"{self.values.shape[0]} values: {list(self.values)}"


## Parse input data from a single text file.
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


def remove_from_list(l, idx):
    """For each `i` in `idx`, remove the value at `i` in list `l`."""
    idx.sort(reverse=True)
    for i in idx:
        l.pop(i)


# Remove invalid tickets.
bad_tickets_idx = []
all_rule_values = np.concatenate([r.values for r in rules])
for idx, ticket in enumerate(nearby_tickets):
    for t_val in ticket.values:
        if t_val not in all_rule_values:
            bad_tickets_idx.append(idx)
            break

# Remove the bad tickets from my list of nearby tickets.
remove_from_list(nearby_tickets, bad_tickets_idx)

# Consider all tickets, including mine.
all_tickets = nearby_tickets + [my_ticket]

# Get all possible positions for a rule based on the tickets.
rules = np.array(rules)
for rule in rules:
    rule.find_possible_positions(all_tickets)


def get_num_positions(rs):
    """The number of possible positions per rule."""
    return np.array([len(r.possible_positions) for r in rs])


def remove_pos(p, rs):
    """Remove a position from all rules."""
    for r in rs:
        if r.possible_positions.shape[0] > 1:
            r.possible_positions = r.possible_positions[r.possible_positions != p]


def count_positions(rs):
    """Count the number of rules that have each position."""
    all_pos = []
    for r in rs:
        all_pos += list(r.possible_positions)
    return Counter(all_pos)


def remove_all_pos_except(p, rs):
    """Remove all positions except for p in the rule has p as an option."""
    for r in rs:
        if p in r.possible_positions:
            r.possible_positions = np.array([p])


# Continue until each rule has a single position.
n_positions = get_num_positions(rules)
while not np.all(n_positions == 1):
    # If a rule has 1 position, remove the position from all other rules.
    pos_in_one_rule = [r.possible_positions[0] for r in rules[n_positions == 1]]
    for pos in pos_in_one_rule:
        remove_pos(pos, rules)

    # If a position is only available in one rule, remove it from the others.
    pos_count = count_positions(rules)
    for pos, count in pos_count.items():
        if count == 1:
            remove_all_pos_except(pos, rules)

    n_positions = get_num_positions(rules)

# Answer to puzzle is product of all values on my ticket for rules
# that start with 'departure'.
answer = 1
for r in rules:
    if r.name.startswith("departure"):
        answer *= my_ticket.values[r.possible_positions[0]]

print(answer_highlight + f"answer: {answer}")
