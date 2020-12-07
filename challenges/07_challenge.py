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
    return (bag, contains)


bag_rules = {}
with open(input_data_path, "r") as file:
    for rule in file:
        bag, contains = parse_bag_rule(rule)
        try:
            bag_rules[bag] = bag_rules[bag].union(contains)
        except:
            bag_rules[bag] = contains


## Create graph of rules.
bag_graph = {}  # [bag] -> bags that can contain the bag
for outside_bag, contained_bags in bag_rules.items():
    contained_bags = [re.sub("[0-9]", "", x) for x in contained_bags]
    contained_bags = [x.strip() for x in contained_bags]
    for contained_bag in contained_bags:
        try:
            bag_graph[contained_bag].add(outside_bag)
        except:
            bag_graph[contained_bag] = set([outside_bag])


def get_containing_bags(gr, bag, bag_list):
    try:
        containing_bags = gr[bag]
        for containing_bag in containing_bags:
            bag_list.append(containing_bag)
            get_containing_bags(gr, containing_bag, bag_list)
    except:
        return None


bags_containing_shinygold = []
get_containing_bags(bag_graph, "shiny gold", bags_containing_shinygold)
print(
    answer_highlight
    + f"number of bags that can contain a shiny gold bag: {len(set(bags_containing_shinygold))}"
)
