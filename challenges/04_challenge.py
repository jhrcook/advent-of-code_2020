from pathlib import Path

# Passport file.
input_data_path = Path("data/day_04/input.txt")

# Required fields.
passport_required_fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"]
npcred_required_fields = passport_required_fields[:-1]


## Read in and merge raw data.

# Read in each line of the data file.
data_lines = []
with open(input_data_path, "r") as file:
    for l in file:
        data_lines.append(l)

# Some entries are split on multiple lines and they need to be merged.
raw_data = []
buffer = ""
for line in data_lines:
    if line == "\n":
        raw_data.append(buffer)
        buffer = ""
    else:
        buffer = buffer + " " + line


## Create a dictionary for each passport entry and validate.


def split_passport_field(x):
    """Split a single entry of a passport into the key and value pair."""
    return x.split(":")


def process_passport_data(x):
    """Process a single passport entry into a dict."""
    y = [split_passport_field(i) for i in x.split()]
    d = {a: b for a, b in y}
    return d


def is_valid_passport(x, required_fields):
    """Check that a passport has all required fields."""
    fields_set = set(required_fields)
    keys_set = set(x.keys())
    return len(fields_set.intersection(keys_set)) == len(fields_set)


# Make a list of passports.
passports = [process_passport_data(x) for x in raw_data]
# Check if each passport is valid.
passport_is_valid = [is_valid_passport(p, npcred_required_fields) for p in passports]

# Solution to puzzle 1.
print(f"number of valid passports: {sum(passport_is_valid)}")
