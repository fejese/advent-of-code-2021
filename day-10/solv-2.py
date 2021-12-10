#!/usr/bin/env python3

from typing import Dict, List

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

SCORES: Dict[str, int] = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
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

scores: List[int] = []
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
            corrupted = True
            break
        pos += 1
    if not corrupted:
        if stack:
            fix: str = ""
            fscore: int = 0
            while stack:
                fix_ch = PAIRS[stack.pop()]
                fscore = fscore * 5 + SCORES[fix_ch]
                fix += fix_ch
            print(f"Line incomplete. Fixed with {fix} with score {fscore}")
            scores.append(fscore)
        else:
            print("Line is ok")

scores = sorted(scores)
score = scores[int((len(scores) - 1) / 2)]
print("score: ", score)
