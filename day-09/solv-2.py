#!/usr/bin/env python3

from typing import List, Optional, Set, Tuple

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

with open(INPUT_FILE_NAME, "r") as input_file:
    map: List[List[int]] = [[int(n) for n in l.strip()] for l in input_file]

ROW_COUNT = len(map)
COL_COUNT = len(map[0])


def get_neighbours(pos: Tuple[int, int]) -> Set[Tuple[int, int]]:
    x, y = pos
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


RIDGE: int = -1
UNKNOWN_BASIN: int = -2
KNOWN_BASIN: int = -3


def find_next_unknown(basin_map: List[List[int]]) -> Optional[Tuple[int, int]]:
    for x in range(COL_COUNT):
        for y in range(ROW_COUNT):
            if basin_map[y][x] == UNKNOWN_BASIN:
                return (x, y)
    return None


def fill_basin(basin_map: List[List[int]], basin_starting_point: Tuple[int, int]):
    size: int = 1
    basin_map[basin_starting_point[1]][basin_starting_point[0]] = KNOWN_BASIN
    neighbours: Set[Tuple[int, int]] = get_neighbours(basin_starting_point)
    for neighbour in neighbours:
        neighbour_val = basin_map[neighbour[1]][neighbour[0]]
        if neighbour_val == RIDGE or neighbour_val == KNOWN_BASIN:
            continue
        neighbour_size: int = fill_basin(basin_map, neighbour)
        size += neighbour_size
    return size


basin_map: List[List[int]] = [
    [RIDGE if h == 9 else UNKNOWN_BASIN for h in row] for row in map
]

basin_sizes: List[int] = []
while True:
    basin_starting_point: Optional[Tuple[int, int]] = find_next_unknown(basin_map)
    if basin_starting_point is None:
        break
    basin_size = fill_basin(basin_map, basin_starting_point)
    basin_sizes.append(basin_size)

basin_sizes = sorted(basin_sizes)
top3 = basin_sizes[-3:]
print(top3, top3[0] * top3[1] * top3[2])
