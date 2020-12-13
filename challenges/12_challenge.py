import re
from copy import copy
from itertools import product
from pathlib import Path

import colorama
import numpy as np

# Prepare colorama to highlight printed solutions.
colorama.init(autoreset=True)
answer_highlight = colorama.Fore.BLUE + colorama.Style.BRIGHT


class Direction:
    """A direction for moving a cruise ship"""

    def __init__(self, s):
        self.action = re.sub("[0-9]+", "", s)
        self.value = int(re.sub("[A-Z]+", "", s))

    def __str__(self):
        return f"{self.action} - {self.value}"


# Input data.
input_data_path = Path("data/day_12/input.txt")
directions = []
with open(input_data_path, "r") as file:
    for l in file:
        directions.append(Direction(l.rstrip()))

print(f"number of directions: {len(directions)}")


class Waypoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({round(self.x, 2)}, {round(self.y, 2)})"

    def __copy__(self):
        return Waypoint(self.x, self.y)

    def cartesian_to_polar(self):
        r = np.sqrt(self.x ** 2 + self.y ** 2)
        theta = np.arctan2(self.y, self.x)
        return r, theta

    def polar_to_cartesian(self, r, theta):
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        return x, y

    def rotate(self, angle):
        """Rotate the waypoint by an angle. (relative to the ship)"""
        r, theta = self.cartesian_to_polar()
        theta += angle * np.pi / 180.0
        self.x, self.y = self.polar_to_cartesian(r, theta)

    def move(self, direction):
        """Move the waypoint by a direction."""
        if direction.action == "N":
            self.y += direction.value
        elif direction.action == "S":
            self.y -= direction.value
        elif direction.action == "E":
            self.x += direction.value
        elif direction.action == "W":
            self.x -= direction.value
        elif direction.action == "L":
            self.rotate(direction.value)
        elif direction.action == "R":
            self.rotate(-1 * direction.value)
        else:
            raise Exception(f"Unknown direction: {direction}")


class Ship:
    """The position of a cruise ship."""

    def __init__(self, x, y, waypoint):
        self.start_x = x
        self.x = x
        self.start_y = y
        self.y = y
        self.waypoint = waypoint

    def __str__(self):
        return (
            f"position: ({round(self.x, 2)}, {round(self.y, 2)}) - waypoint: {waypoint}"
        )

    def __copy__(self):
        return Position(self.x, self.y, copy(self.waypoint))

    def move(self, direction):
        """Move the ship or waypoint by a given direction."""
        if direction.action == "F":
            self.x += self.waypoint.x * direction.value
            self.y += self.waypoint.y * direction.value
        else:
            waypoint.move(direction)

    def manhattan_dist(self):
        return abs(self.start_x - self.x) + abs(self.start_y - self.y)


# Move one direction at a time. (solve puzzle 2)
waypoint = Waypoint(10, 1)
ship = Ship(0, 0, waypoint)
for d in directions:
    ship.move(d)

print(answer_highlight + f"Manhattan distance: {round(ship.manhattan_dist())}")
