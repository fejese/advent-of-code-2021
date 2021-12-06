#!/usr/bin/env python3

from typing import List

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

fish_per_age: List[int] = [0] * 9
with open(INPUT_FILE_NAME, "r") as input_file:
    ages: List[int] = [int(n) for n in input_file.read().strip().split(",")]
    for age in ages:
        fish_per_age[age] += 1

for _ in range(256):
    # print(fish_per_age)
    zeroes: int = fish_per_age[0]
    for age in range(8):
        fish_per_age[age] = fish_per_age[age+1]
    fish_per_age[8] = zeroes
    fish_per_age[6] += zeroes

# print(fish_per_age)
print(sum(fish_per_age))
