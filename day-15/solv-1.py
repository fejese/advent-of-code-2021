#!/usr/bin/env python3

from typing import List

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

risk_map: List[List[int]]
with open(INPUT_FILE_NAME, "r") as input_file:
    risk_map = [[int(ch) for ch in line.strip()] for line in input_file]

WIDTH: int = len(risk_map[0])
HEIGHT: int = len(risk_map)

agg_map: List[List[int]] = [[WIDTH * HEIGHT * 9] * WIDTH for _ in range(HEIGHT)]
agg_map[0][0] = 0

changes: bool = True
rounds: int = 1
while changes:
    print(f"Round #{rounds}")
    changes = False
    for y in range(len(risk_map)):
        for x in range(len(risk_map[0])):
            options: List[int] = []
            if y > 0:
                options.append(agg_map[y - 1][x])
            if x > 0:
                options.append(agg_map[y][x - 1])
            if y < HEIGHT - 1:
                options.append(agg_map[y + 1][x])
            if x < WIDTH - 1:
                options.append(agg_map[y][x + 1])

            if options:
                new = min(options) + risk_map[y][x]
                if new < agg_map[y][x]:
                    agg_map[y][x] = new
                    changes = True
    rounds += 1

print(agg_map[-1][-1])
