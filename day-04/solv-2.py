#!/usr/bin/env python3

from typing import List, Set

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"


class Board:
    def __init__(self, nums: List[List[int]]) -> None:
        self.all_nums: Set[int] = set()
        for row in nums:
            for num in row:
                self.all_nums.add(num)
        self.sets: List[Set[int]] = [set(row) for row in nums] + [
            set([row[c] for row in nums]) for c in range(len(nums[0]))
        ]
        # print(self.all_nums, self.sets)

    def mark(self, num: int) -> bool:
        try:
            self.all_nums.remove(num)
        except KeyError:
            pass
        won: bool = False
        for aset in self.sets:
            try:
                aset.remove(num)
                if len(aset) == 0:
                    won = True
            except KeyError:
                pass

        return won


with open(INPUT_FILE_NAME, "r") as input_file:
    parts: List[str] = input_file.read().strip().split("\n\n")

series = [int(n) for n in parts[0].strip().split(",")]
boards = [
    Board(
        [
            [int(n) for n in line.strip().replace("  ", " ").split(" ")]
            for line in part.split("\n")
        ]
    )
    for part in parts[1:]
]

won = False
boards_won: Set[Board] = set()
for num in series:
    for board in boards:
        if board in boards_won:
            continue
        won = board.mark(num)
        if won:
            print(sum(board.all_nums) * num)
            boards_won.add(board)
