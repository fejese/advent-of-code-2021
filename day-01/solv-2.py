#!/usr/bin/env python3

from typing import List, Optional

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

levels: List[int]
with open(INPUT_FILE_NAME, "r") as input_file:
    levels = [int(line.strip()) for line in input_file]

agg_levels: List[int] = [
    sum(levels[i:i+3]) for i in range(len(levels) - 2)
]

# print(agg_levels)

prev: Optional[int] = None
increase_count: int = 0
for level in agg_levels:
    if prev is not None and level > prev:
        increase_count += 1
    prev = level

print(increase_count)
