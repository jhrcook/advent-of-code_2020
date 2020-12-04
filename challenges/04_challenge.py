import re
from pathlib import Path

# Passport file.
input_data_path = Path("data/day_04/input.txt")

# Required fields.
passport_required_fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"]
npcred_required_fields = passport_required_fields[:-1]


# Valid eye colors.
valid_eyecolors = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]

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


## Create a dictionary for each passport entry.


def split_passport_field(x):
    """Split a single entry of a passport into the key and value pair."""
    return x.split(":")


def process_passport_data(x):
    """Process a single passport entry into a dict."""
    y = [split_passport_field(i) for i in x.split()]
    d = {a: b for a, b in y}
    return d


# Make a list of passports.
passports = [process_passport_data(x) for x in raw_data]


## Passport validation.


def has_all_required_fields(x, required_fields):
    """Check that a passport has all required fields."""
    fields_set = set(required_fields)
    keys_set = set(x.keys())
    return len(fields_set.intersection(keys_set)) == len(fields_set)


def is_valid_birthyear(passport, min, max):
    """Check that a passport has a valid birth year."""
    return min <= int(passport["byr"]) <= max


def is_valid_issueyear(passport, min, max):
    """Check that a passport has a valid issue year."""
    return min <= int(passport["iyr"]) <= max


def is_valid_exprirationyear(passport, min, max):
    """Check that a passport has a valid expiration year."""
    return min <= int(passport["eyr"]) <= max


def is_valid_height(passport, min_cm, max_cm, min_in, max_in):
    """Check that a passport has a valid height value."""
    height = passport["hgt"]
    if "cm" in height:
        return min_cm <= int(height[:-2]) <= max_cm
    elif "in" in height:
        return min_in <= int(height[:-2]) <= max_in
    return False


def is_valid_haircolor(passport):
    """Check that a passport has a valid hair color."""
    clr = passport["hcl"]
    if not clr[0] == "#":
        return False
    clr = clr[1:]
    return len(clr) == 6 and bool(re.match("^[a-zA-Z0-9]+$", clr))


def is_valid_eyecolor(passport, valid_eyecolors):
    """Check that a passport has a valid eye color."""
    clr = passport["ecl"]
    return type(clr) == str and clr in valid_eyecolors


def is_valid_passportid(passport):
    """Check that a passport has a valid passport ID number."""
    pid = passport["pid"]
    return len(pid) == 9 and bool(re.match("^[0-9]+$", pid))


def is_valid_passport(passport, validation_functions, fxn_args):
    """Check that a passport is valid."""
    for f, kwargs in zip(validation_functions, fxn_args):
        if not f(passport, **kwargs):
            return False
    return True


# List of functions that check different required attributes of the passport.
passport_validation_functions = [
    has_all_required_fields,
    is_valid_birthyear,
    is_valid_issueyear,
    is_valid_exprirationyear,
    is_valid_height,
    is_valid_haircolor,
    is_valid_eyecolor,
    is_valid_passportid,
]
# Arguments to the above functions.
passport_validation_info = [
    {"required_fields": npcred_required_fields},
    {"min": 1920, "max": 2002},
    {"min": 2010, "max": 2020},
    {"min": 2020, "max": 2030},
    {"min_cm": 150, "max_cm": 193, "min_in": 59, "max_in": 76},
    {},
    {"valid_eyecolors": valid_eyecolors},
    {},
]

# Check all passports.
passport_is_valid = [
    is_valid_passport(p, passport_validation_functions, passport_validation_info)
    for p in passports
]
# Solution to puzzle 2.
print(f"number of valid passports: {sum(passport_is_valid)}")
