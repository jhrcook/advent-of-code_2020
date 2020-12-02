import re
from pathlib import Path

# Input data.
input_data_path = Path("data/day_02/input.txt")


def split_password(p):
    """Split a line of the password database into its four components."""
    p_split = p.rstrip().replace(":", "").split(" ")
    n_first, n_second = [int(x) for x in p_split[0].split("-")]
    p_letter = p_split[1]
    password = p_split[2]
    return (n_first, n_second, p_letter, password)


def password_is_valid_policy1(p):
    """Validate a password against the first policy."""
    n_min, n_max, p_letter, password = split_password(p)
    count_letter = len(re.findall(p_letter, password))
    return n_min <= count_letter <= n_max


def password_is_valid_policy2(p):
    """Validate a password against the second policy."""
    n_first, n_second, p_letter, password = split_password(p)
    letter_1 = password[n_first - 1] == p_letter
    letter_2 = password[n_second - 1] == p_letter
    if (letter_1 and letter_2) or (not letter_1 and not letter_2):
        return False
    return True


def count_passwords_against_policy(file, password_policy):
    """Count the number of valid passwords in a file with a given policy."""
    number_of_valid_passwords = 0
    with open(file, "r") as data:
        for l in data:
            if password_policy(l):
                number_of_valid_passwords += 1
    return number_of_valid_passwords


# Answers to the challenge.
print(
    f"number of valid passwords with policy 1: {count_passwords_against_policy(input_data_path, password_is_valid_policy1)}"
)
print(
    f"number of valid passwords with policy 2: {count_passwords_against_policy(input_data_path, password_is_valid_policy2)}"
)
