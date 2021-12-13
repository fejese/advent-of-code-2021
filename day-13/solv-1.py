#!/usr/bin/env python3

from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Set, Tuple

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"


def dot_from_input_line(line: str) -> Tuple[int, int]:
    return tuple(int(c) for c in line.strip().split(","))


class FoldDirection(Enum):
    VERTICAL = auto()
    HORIZONTAL = auto()


@dataclass
class Fold:
    direction: FoldDirection
    position: int

    @classmethod
    def from_input_line(cls, line: str) -> "Fold":
        parts: List[str] = line.strip().split(" ")[2].split("=")
        direction: FoldDirection = FoldDirection.VERTICAL if parts[
            0
        ] == "x" else FoldDirection.HORIZONTAL
        return cls(direction, int(parts[1]))


dots: Set[Tuple[int, int]]
folds: List[Fold]
with open(INPUT_FILE_NAME, "r") as input_file:
    parts: List[str] = input_file.read().split("\n\n")
    dots = set(dot_from_input_line(line) for line in parts[0].strip().split("\n"))
    folds = [Fold.from_input_line(line) for line in parts[1].strip().split("\n")]

for fold in folds[:1]:
    new_dots: Set[Tuple[int, int]] = set()
    for dot in dots:
        if fold.direction == FoldDirection.HORIZONTAL:
            if dot[1] < fold.position:
                new_dots.add(dot)
            else:
                new_dots.add((dot[0], 2 * fold.position - dot[1]))
        else:
            if dot[0] < fold.position:
                new_dots.add(dot)
            else:
                new_dots.add((2 * fold.position - dot[0], dot[1]))
    dots = new_dots

print(len(dots))
