#!/usr/bin/env python3

from dataclasses import dataclass
from typing import List

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

@dataclass
class Coord:
    x: int
    y: int

@dataclass
class Line:
    a: Coord
    b: Coord

    @classmethod
    def from_input_line(cls, line: str) -> 'Line':
        a, _, b = line.strip().split(' ')
        return cls(
            Coord(*[int(n) for n in a.split(',')]),
            Coord(*[int(n) for n in b.split(',')]),
        )

lines: List[Line] = []
max_x: int = 0
max_y: int = 0
grid: List[List[int]]

with open(INPUT_FILE_NAME, "r") as input_file:
    for input_line in input_file:
        line = Line.from_input_line(input_line)
        # if (line.a.x - line.b.x) * (line.a.y - line.b.y) != 0:
        #     continue
        max_x = max(max_x, line.a.x, line.b.x)
        max_y = max(max_y, line.a.y, line.b.y)
        lines.append(line)

grid = [[0] * (max_x + 1) for _ in range(max_y + 1)]
for line in lines:
    dx = int((line.b.x - line.a.x) / abs(line.b.x - line.a.x) if line.b.x - line.a.x != 0 else 0)
    dy = int((line.b.y - line.a.y) / abs(line.b.y - line.a.y) if line.b.y - line.a.y != 0 else 0)
    ix = line.a.x
    iy = line.a.y
    while ix != line.b.x or iy != line.b.y:
        grid[iy][ix] += 1
        ix += dx
        iy += dy
    grid[iy][ix] += 1

# for line in grid:
#     print(line)

count = sum(
    sum(1 if cell > 1 else 0 for cell in line)
    for line in grid
)
print(count)
