import re
from itertools import product
from pathlib import Path

import colorama
import numpy as np

# Prepare colorama to highlight printed solutions.
colorama.init(autoreset=True)
answer_highlight = colorama.Fore.BLUE + colorama.Style.BRIGHT


# Input data.
input_data_file = Path("data", "day_19", "input.txt")
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


def compile_regex(x, n_times="+"):
    """Turn a list into a grouped regular expression."""
    y = "(" + "|".join(x) + ")" + n_times
    return y


def add_rule_at(i, rules, messages):
    rule = rules[i]
    new_messages = []

    if i == 8:
        new_messages = []
        regex_42 = compile_regex(add_rule_at(42, rules=rules, messages=[]))
        if len(messages) == 0:
            new_messages = [regex_42]
        else:
            new_messages = [message + regex_42 for message in messages]
        return new_messages
    elif i == 11:
        new_messages = []
        # Add '{N}' instead of '+' so can be replaced by actual numbers during matching.
        regex_42 = compile_regex(
            add_rule_at(42, rules=rules, messages=[]), n_times="{N}"
        )
        regex_31 = compile_regex(
            add_rule_at(31, rules=rules, messages=[]), n_times="{N}"
        )

        if len(messages) == 0:
            new_messages = [regex_42 + regex_31]
        else:
            new_messages = [regex_42 + m + regex_31 for m in messages]
        return new_messages

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

# Add in start and end regex indicators.
all_possible_messages = ["^" + m + "$" for m in all_possible_messages]

valid_messages = []
for message in messages:
    for possible_message in all_possible_messages:
        for N in range(1, 10):
            possible_message_N = possible_message.replace("N", str(N))
            if bool(re.match(possible_message_N, message)):
                valid_messages.append(message)
                break

print(answer_highlight + f"number of valid messages: {len(valid_messages)}")
