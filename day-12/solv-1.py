#!/usr/bin/env python3

from collections import defaultdict
from typing import Dict, List, Set


# INPUT_FILE_NAME: str = "test-input"
# INPUT_FILE_NAME: str = "test-input-2"
# INPUT_FILE_NAME: str = "test-input-3"
INPUT_FILE_NAME: str = "input"


START_CAVE: str = "start"
END_CAVE: str = "end"


def is_small(cave: str) -> bool:
    return cave == cave.lower()


connections: Dict[str, Set[str]] = defaultdict(set)
small_caves: Set[str] = set()
with open(INPUT_FILE_NAME, "r") as input_file:
    for line in input_file:
        caves = line.strip().split("-")
        connections[caves[0]].add(caves[1])
        connections[caves[1]].add(caves[0])
        if is_small(caves[0]):
            small_caves.add(caves[0])
        if is_small(caves[1]):
            small_caves.add(caves[1])

path_count: int = 0
paths: List[List[str]] = [[START_CAVE]]
while paths:
    new_paths: List[List[str]] = []
    for path in paths:
        for next_cave in connections[path[-1]]:
            if next_cave == END_CAVE:
                path_count += 1
                continue
            if next_cave in path and next_cave in small_caves:
                continue
            new_paths.append(path + [next_cave])
    paths = new_paths

print(path_count)
