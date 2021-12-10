#!/usr/bin/env python3

from typing import Dict, List

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

SCORES: Dict[str, int] = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}
PAIRS: Dict[str, str] = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}
PAIRS.update({v: k for k, v in PAIRS.items()})

lines: List[str]
with open(INPUT_FILE_NAME, "r") as input_file:
    lines = [l.strip() for l in input_file]

score: int = 0
for line in lines:
    stack: List[str] = []
    corrupted: bool = False
    pos: int = 0
    for ch in line:
        if ch in "([{<":
            stack.append(ch)
        elif PAIRS[ch] == stack[-1]:
            stack.pop()
        else:
            print(f"Line corrupted with {ch} at {pos}. Stack: {stack}")
            score += SCORES[ch]
            corrupted = True
            break
        pos += 1
    if not corrupted:
        if stack:
            print("Line incomplete")
        else:
            print("Line is ok")

print("score: ", score)
