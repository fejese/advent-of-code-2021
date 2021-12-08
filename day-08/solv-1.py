#!/usr/bin/env python3

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

# 2 char => 1
# 3 char => 7
# 4 char => 4
# 5 char => 2, 3, 5
# 6 char => 0, 6, 9
# 7 char => 8

with open(INPUT_FILE_NAME, "r") as input_file:
    print(
        sum(
            sum(
                1 if len(enc) in [2, 3, 4, 7] else 0
                for enc in line.strip().split("|")[1].split(" ")
            )
            for line in input_file
        )
    )
