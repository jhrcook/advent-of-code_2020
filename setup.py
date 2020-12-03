#!/bin/env python

# Set-up the scripts and data directories for each day.
# The Markdown for the README is also printed.

import os
from pathlib import Path

for i in range(4, 26):
    if i < 10:
        pad_i = "0" + str(i)
    else:
        pad_i = str(i)
    print(f"{i}. [Day {i}](challenges/{pad_i}_challenge.py)")
    Path(f"challenges/{pad_i}_challenge.py").touch()
    data_dir = Path(f"data/day_{pad_i}")
    if not data_dir.is_dir():
        os.mkdir(data_dir)
