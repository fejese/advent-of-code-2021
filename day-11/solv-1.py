#!/usr/bin/env python3

from typing import List, Set, Tuple

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

MAP_SIZE: int = 10


def get_neighbours(x: int, y: int) -> Set[Tuple[int, int]]:
    neighbours: Set[Tuple[int, int]] = set()
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                # no self
                continue
            if 0 <= x + dx < MAP_SIZE and 0 <= y + dy < MAP_SIZE:
                neighbours.add((x + dx, y + dy))
    return neighbours


def flash(
    map: List[List[int]], flashed: Set[Tuple[int, int]], x: int, y: int
) -> Set[Tuple[int, int]]:
    neighbours = get_neighbours(x, y)
    for n in neighbours:
        if n in flashed:
            continue
        map[n[1]][n[0]] += 1
        if map[n[1]][n[0]] > 9:
            flashed.add(n)
            map[n[1]][n[0]] = 0
            flashed = flashed.union(flash(map, flashed, n[0], n[1]))
    return flashed


def step(map: List[List[int]]) -> int:
    flashed: Set[Tuple[int, int]] = set()
    for x in range(MAP_SIZE):
        for y in range(MAP_SIZE):
            if (x, y) in flashed:
                continue
            map[y][x] += 1
            if map[y][x] > 9:
                flashed.add((x, y))
                map[y][x] = 0
                flashed = flashed.union(flash(map, flashed, x, y))
    return len(flashed)


map: List[List[int]]
with open(INPUT_FILE_NAME, "r") as input_file:
    map = [[int(n) for n in line.strip()] for line in input_file]


total_flashes: int = 0
for i in range(100):
    flashes = step(map)
    total_flashes += flashes
    # print(f"After step {i+1}:")
    # print("flashes:", flashes)
    # [print(line) for line in map]
    # print()

print("total flashes:", total_flashes)
