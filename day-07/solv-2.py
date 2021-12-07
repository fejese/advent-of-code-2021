#!/usr/bin/env python3

from typing import List, Optional

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

with open(INPUT_FILE_NAME, "r") as input_file:
    positions = [int(p) for p in input_file.read().strip().split(",")]


def sum1n(n: int) -> int:
    return int((n * (n + 1)) / 2)


min_cost: Optional[int] = None
for aligned_pos in range(min(positions), max(positions)):
    cost = sum(sum1n(abs(p - aligned_pos)) for p in positions)
    if min_cost is None or cost < min_cost:
        min_cost = cost

print(min_cost)
