#!/usr/bin/env python3

from typing import List

# INPUT_FILE_NAME: str = "test-input-basic"
# INPUT_FILE_NAME: str = "test-input-basic-2"
# INPUT_FILE_NAME: str = "test-input-basic-3"
# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

sea: List[List[str]]
with open(INPUT_FILE_NAME, "r") as input_file:
    sea = [[ch for ch in line.strip()] for line in input_file]

WIDTH: int = len(sea[0])
HEIGHT: int = len(sea)

step: int = 0
movement: bool = True
[print("".join(line)) for line in sea + [""]]
while movement:
    step += 1
    # print(step)
    movement = False
    new_sea: List[List[str]] = [["."] * WIDTH for _ in range(HEIGHT)]
    for y, line in enumerate(sea):
        for x, ch in enumerate(line):
            left: str = line[(x - 1) % WIDTH]
            right: str = line[(x + 1) % WIDTH]
            if ch == "." and left == ">":
                new_sea[y][x] = ">"
                movement = True
            elif ch == ">" and right == ".":
                new_sea[y][x] = "."
                movement = True
            else:
                new_sea[y][x] = sea[y][x]
    sea = new_sea
    new_sea: List[List[str]] = [["."] * WIDTH for _ in range(HEIGHT)]
    # [print("".join(line)) for line in sea + [""]]
    for y, line in enumerate(sea):
        for x, ch in enumerate(line):
            up: str = sea[(y - 1) % HEIGHT][x]
            down: str = sea[(y + 1) % HEIGHT][x]
            if ch == "." and up == "v":
                new_sea[y][x] = "v"
                movement = True
            elif ch == "v" and down == ".":
                new_sea[y][x] = "."
                movement = True
            else:
                new_sea[y][x] = sea[y][x]
    sea = new_sea
    # [print("".join(line)) for line in sea + [""]]

[print("".join(line)) for line in sea + [""]]
print(step)
