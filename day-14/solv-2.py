#!/usr/bin/env python3

from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Tuple

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

dist: Dict[str, int] = defaultdict(int)
rules: Dict[str, Tuple[str, str]]


def step(dist: Dict[str, int], rules: Dict[str, Tuple[str, str]]) -> Dict[str, int]:
    new_dist: Dict[str, int] = defaultdict(int)

    for match, replacements in rules.items():
        for replacement in replacements:
            new_dist[replacement] += dist[match]

    return new_dist


def get_chdist(dist: Dict[str, int], template: str) -> Dict[str, int]:
    chdist: Dict[str, int] = defaultdict(int)
    chdist[template[0]] += 1
    chdist[template[-1]] += 1

    for pair, count in dist.items():
        chdist[pair[0]] += count
        chdist[pair[1]] += count

    for ch, count in chdist.items():
        chdist[ch] = int(chdist[ch] / 2)

    return chdist


def get_minmax(dist: Dict[str, int]) -> Tuple[int, int]:
    min_val: int = min(dist.values())
    max_val: int = max(dist.values())
    return (min_val, max_val)


def get_sol(minmax: Tuple[int, int]) -> int:
    return minmax[1] - minmax[0]


with open(INPUT_FILE_NAME, "r") as input_file:
    parts: List[str] = input_file.read().split("\n\n")
    template: str = parts[0]
    for i in range(len(template) - 1):
        dist[template[i : i + 2]] += 1
    rules = {
        line.split(" ")[0]: (
            f"{line.split(' ')[0][0]}{line.split(' ')[2]}",
            f"{line.split(' ')[2]}{line.split(' ')[0][1]}",
        )
        for line in parts[1].strip().split("\n")
    }

print(dist)
for i in range(40):
    start = datetime.now()
    print(f"{start} Calculating step {i}")
    dist = step(dist, rules)
    end = datetime.now()
    # print(template)
    print(f"Took {end - start}\n")


chdist = get_chdist(dist, template)
minmax = get_minmax(chdist)
sol = get_sol(minmax)

print(dist)
print(chdist)
print(minmax)
print(sol)
