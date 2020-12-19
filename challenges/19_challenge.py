from itertools import product
from pathlib import Path

import colorama
import numpy as np

# Prepare colorama to highlight printed solutions.
colorama.init(autoreset=True)
answer_highlight = colorama.Fore.BLUE + colorama.Style.BRIGHT

DEBUG = False
if DEBUG:
    input_data_file = Path("data", "day_19", "input_test.txt")
    n_cycles = 6
else:
    input_data_file = Path("data", "day_19", "input.txt")
    n_cycles = 6


# Input data.
rules = []
messages = []
collecting_rules = True

with open(input_data_file, "r") as file:
    for line in file:
        if line == "\n":
            collecting_rules = False
        elif collecting_rules:
            rules.append(line.rstrip())
        else:
            messages.append(line.rstrip())


def parse_rule(r):
    num = int(r.split(":")[0])
    values = r.split(": ")[1].rstrip().split(" | ")
    values = [v.split(" ") for v in values]
    for i, v in enumerate(values):
        for j, a in enumerate(v):
            if a.isdigit():
                v[j] = int(a)
            else:
                v[j] = a.replace('"', "")
    return (num, values)


rules_list = [parse_rule(r) for r in rules]
rules = {i: v for i, v in rules_list}


print(f"number of rules: {len(rules)}")
print(f"number of messages: {len(messages)}")


def add_rule_at(i, rules, messages):
    rule = rules[i]
    new_messages = []
    for values in rule:
        messages_copy = messages.copy()
        if values == ["a"] or values == ["b"]:
            if len(messages_copy) == 0:
                messages_copy = values
            else:
                messages_copy = [message + values[0] for message in messages_copy]
        else:
            for value in values:
                messages_copy = add_rule_at(value, rules=rules, messages=messages_copy)
        new_messages += messages_copy
    return new_messages


all_possible_messages = add_rule_at(0, rules=rules, messages=[])
print(f"num possibles: {len(set(all_possible_messages))}")

valid_messages = set(messages).intersection(set(all_possible_messages))
print(answer_highlight + f"number of valid messages: {len(valid_messages)}")
