import re
from pathlib import Path

import colorama as clr

# Prepare colorama to highlight printed solutions.
clr.init(autoreset=True)
answer_highlight = clr.Fore.BLUE + clr.Style.BRIGHT

# Input data.
input_data_path = Path("data/day_07/input.txt")


## Read in rules


def parse_bag_rule(r):
    r_split = r.rstrip().split(" contain ")
    bag = r_split[0].replace(" bags", "")
    contains = r_split[1].split(", ")
    contains = set(
        [x.replace(" bags", "").replace(" bag", "").replace(".", "") for x in contains]
    )

    if contains == set(["no other"]):
        contains = set([])

    return (bag, contains)


bag_rules = {}
with open(input_data_path, "r") as file:
    for rule in file:
        bag, contains = parse_bag_rule(rule)
        try:
            bag_rules[bag] = bag_rules[bag].union(contains)
        except:
            bag_rules[bag] = contains

print(f"There are {len(bag_rules.keys())} rules.")

## Create graph of rules.


def remove_digits(x):
    return re.sub("[0-9]", "", x).strip()


bag_graph = {}  # [bag] -> bags that can contain the bag
for outside_bag, contained_bags in bag_rules.items():
    contained_bags = [remove_digits(x) for x in contained_bags]
    for contained_bag in contained_bags:
        try:
            bag_graph[contained_bag].add(outside_bag)
        except:
            bag_graph[contained_bag] = set([outside_bag])


def get_containing_bags(gr, bag, bag_list):
    """Append all of the bags that can contain a given bag to the `bag_list`. (recursive)"""
    try:
        containing_bags = gr[bag]
        for containing_bag in containing_bags:
            bag_list.append(containing_bag)
            get_containing_bags(gr, containing_bag, bag_list)
    except:
        return None


bags_containing_shinygold = []
get_containing_bags(bag_graph, "shiny gold", bags_containing_shinygold)
# Solution to puzzle 1.
print(
    answer_highlight
    + f"Number of bags that can contain a shiny gold bag: {len(set(bags_containing_shinygold))}"
)


def count_bags_in_bag(d, bag):
    """Count the number of bags within some bag. (recursive)"""
    count = 0
    try:
        for contained_bag in d[bag]:
            num = int("".join(filter(lambda i: i.isdigit(), contained_bag)))
            contained_bag = remove_digits(contained_bag)
            for b in [contained_bag] * num:
                count += 1 + count_bags_in_bag(d, b)
        return count
    except:
        return 0


print(
    answer_highlight
    + f"Number of bags contained within one shiny gold bag: {count_bags_in_bag(bag_rules, 'shiny gold')}"
)
