#!/usr/bin/env python3

import re
from dataclasses import dataclass
from typing import List

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

INPUT_PATTERN: re.Pattern = re.compile(
    r".*x=(-?\d+)\.\.(-?\d+).*y=(-?\d+)\.\.(-?\d+).*"
)


@dataclass
class Target:
    min_x: int
    min_y: int
    max_x: int
    max_y: int


target: Target
with open(INPUT_FILE_NAME, "r") as input_file:
    match: re.Match = INPUT_PATTERN.match(input_file.read())
    assert match
    parts: List[int] = [int(match.group(i)) for i in range(1, 5)]
    target = Target(
        min_x=min(parts[:2]),
        min_y=min(parts[2:]),
        max_x=max(parts[:2]),
        max_y=max(parts[2:]),
    )


max_start_y: int
for start_y in range(
    min(target.min_y, target.max_y) - 1, max(abs(target.min_y), abs(target.max_y)) + 1
):
    for start_x in range(0, max(target.min_x, target.max_x) + 1):
        posx: int = 0
        posy: int = 0
        vx: int = start_x
        vy: int = start_y
        while posy >= target.min_y and posx <= target.max_x:
            if target.min_x <= posx <= target.max_x:
                if target.min_y <= posy <= target.max_y:
                    max_start_y = start_y
            posx += vx
            posy += vy
            vx = 0 if vx == 0 else vx - 1
            vy -= 1

print(max_start_y, int(max_start_y * (max_start_y + 1) / 2))
