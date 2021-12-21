#!/usr/bin/env python3

from typing import List, Tuple

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"


class Dice:
    def __init__(self) -> None:
        self.val: int = 0
        self.roll_count: int = 0

    def roll(self) -> int:
        ret: int = self.val + 1
        self.val = ret % 100
        self.roll_count += 1
        return ret

    def __str__(self) -> str:
        return f"[val: {self.val + 1}, roll count: {self.roll_count}]"

    def __repr__(self) -> str:
        return self.__str__()


class Player:
    def __init__(self, start_position: int) -> None:
        self._position = start_position - 1
        self.score = 0

    @property
    def position(self) -> int:
        return self._position + 1

    def step(self, steps: int) -> None:
        self._position = (self._position + steps) % 10
        self.score += self.position

    def won(self) -> bool:
        return self.score >= 1000

    def __str__(self) -> str:
        return f"[pos: {self.position}, score: {self.score}]"

    def __repr__(self) -> str:
        return self.__str__()


dice: Dice = Dice()
players: Tuple[Player, Player]

with open(INPUT_FILE_NAME, "r") as input_file:
    players = tuple(
        Player(start_position=int(line.split(" ")[-1].strip())) for line in input_file
    )

print(players, dice)

round_no: int = -1
while not players[0].won() and not players[1].won():
    round_no = (round_no + 1) % 2
    rolls: List[int] = [dice.roll() for _ in range(3)]
    active_player = players[round_no]
    active_player.step(sum(rolls))
    print(players, dice)

loser_score = min(players[0].score, players[1].score)
roll_count = dice.roll_count
print(loser_score, roll_count)
print(loser_score * roll_count)
