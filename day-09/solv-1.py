#!/usr/bin/env python3

from typing import List, Set, Tuple

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

with open(INPUT_FILE_NAME, "r") as input_file:
    map: List[str] = [l.strip() for l in input_file]

ROW_COUNT = len(map)
COL_COUNT = len(map[0])


def get_neighbours(x: int, y: int) -> Set[Tuple[int, int]]:
    neighbours: Set[Tuple[int, int]] = set()
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                # no self
                continue
            if dx != 0 and dy != 0:
                # no diagonals
                continue
            if 0 <= x + dx < COL_COUNT and 0 <= y + dy < ROW_COUNT:
                neighbours.add((x + dx, y + dy))
    return neighbours


low_points: List[int] = []
for x in range(COL_COUNT):
    for y in range(ROW_COUNT):
        neighbours = get_neighbours(x, y)
        current = int(map[y][x])
        low_point = True
        for neighbour in neighbours:
            if int(map[neighbour[1]][neighbour[0]]) <= current:
                low_point = False
                break

        if low_point:
            low_points.append(current)

print(low_points)
print(sum(low_points) + len(low_points))
