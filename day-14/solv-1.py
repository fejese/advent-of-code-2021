#!/usr/bin/env python3

from collections import defaultdict
from typing import Dict, List, Tuple

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

template: str
rules: Dict[str, str]


def step(template: str, rules: Dict[str, str]) -> str:
    new_template: str = template[0]
    for i in range(1, len(template)):
        new_template += rules.get(template[i - 1 : i + 1], "")
        new_template += template[i]

    return new_template


def get_dist(template: str) -> Dict[str, int]:
    dist: Dict[str, int] = defaultdict(int)
    for ch in template:
        dist[ch] += 1

    return dist


def get_minmax(dist: Dict[str, int]) -> Tuple[int, int]:
    min_val: int = min(dist.values())
    max_val: int = max(dist.values())
    return (min_val, max_val)


def get_sol(minmax: Tuple[int, int]) -> int:
    return minmax[1] - minmax[0]


with open(INPUT_FILE_NAME, "r") as input_file:
    parts: List[str] = input_file.read().split("\n\n")
    template = parts[0]
    rules = {
        line.split(" ")[0]: line.split(" ")[2] for line in parts[1].strip().split("\n")
    }

# print(template)
for _ in range(10):
    template = step(template, rules)
    # print(template)

dist = get_dist(template)
minmax = get_minmax(dist)
sol = get_sol(minmax)

print(dist)
print(minmax)
print(sol)
