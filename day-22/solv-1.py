#!/usr/bin/env python3

import re
from typing import List, Optional, Set, Tuple

# INPUT_FILE_NAME: str = "test-input"
# INPUT_FILE_NAME: str = "test-input-2"
INPUT_FILE_NAME: str = "input"

GRID_MIN: int = -50
GRID_MAX: int = 50
INPUT_LINE_PATTERN: re.Pattern = re.compile(
    r"^(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)$"
)

grid: Set[Tuple[int, int, int]] = set()

with open(INPUT_FILE_NAME, "r") as input_file:
    for line_no, line in enumerate(input_file):
        match: Optional[re.Match] = INPUT_LINE_PATTERN.match(line)
        if not match:
            raise Exception(f"Can not parse linen {line_no}: [{line}]")
        action: str = match.group(1)
        x_min, x_max = sorted(int(match.group(i)) for i in [2, 3])
        y_min, y_max = sorted(int(match.group(i)) for i in [4, 5])
        z_min, z_max = sorted(int(match.group(i)) for i in [6, 7])
        for x in range(max(-50, x_min), min(50, x_max) + 1, 1):
            for y in range(max(-50, y_min), min(50, y_max) + 1, 1):
                for z in range(max(-50, z_min), min(50, z_max) + 1, 1):
                    coord: Tuple[int, int, int] = (x, y, z)
                    # print(f"  Setting {x} {y} {z} to {action}")
                    if action == "on":
                        grid.add(coord)
                    elif coord in grid:
                        grid.remove(coord)


print(len(grid))
