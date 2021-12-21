#!/usr/bin/env python3

from dataclasses import dataclass
from typing import Dict, List, Tuple

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

WINNING_SCORE: int = 21
ROLL_SUMS: List[int] = sorted(
    [sum([r1, r2, r3]) for r1 in [1, 2, 3] for r2 in [1, 2, 3] for r3 in [1, 2, 3]]
)


@dataclass
class Game:
    positions: Tuple[int, int]
    scores: Tuple[int, int] = (0, 0)
    active_player: int = 0

    def __hash__(self) -> int:
        return tuple([self.positions, self.scores, self.active_player]).__hash__()


WIN_CACHE: Dict[Game, List[int]] = {}
WIN_CACHE_HIT: int = 0
WIN_CACHE_MISS: int = 0


def gen_win_counts(game: Game) -> List[int]:
    global WIN_CACHE_HIT
    global WIN_CACHE_MISS
    # cache_hit_rate: float = WIN_CACHE_HIT/(WIN_CACHE_HIT + WIN_CACHE_MISS) if WIN_CACHE_HIT > 0 else 0
    # print(
    #     f"[Cache info] size: {len(WIN_CACHE)},",
    #     f"hit: {WIN_CACHE_HIT},",
    #     f"miss: {WIN_CACHE_MISS},",
    #     f"hit ratio: {cache_hit_rate:4f}",
    # )

    if game in WIN_CACHE:
        WIN_CACHE_HIT += 1
        return WIN_CACHE[game]
    WIN_CACHE_MISS += 1

    for player in range(2):
        if game.scores[player] >= WINNING_SCORE:
            result: List[int] = [player == 0, player == 1]
            WIN_CACHE[game] = result
            return result

    active_player: int = game.active_player
    sub_games: List[Game] = []
    for roll_sum in ROLL_SUMS:
        new_positions: List[int] = list(game.positions)
        new_positions[active_player] = new_positions[active_player] + roll_sum
        if new_positions[active_player] > 10:
            new_positions[active_player] -= 10
        new_scores: List[int] = list(game.scores)
        new_scores[active_player] += new_positions[active_player]
        sub_games.append(
            Game(
                positions=tuple(new_positions),
                scores=tuple(new_scores),
                active_player=(active_player + 1) % 2,
            )
        )

    win_counts: List[int] = [0, 0]
    for sub_game in sub_games:
        win_counts = [wc + swc for wc, swc in zip(win_counts, gen_win_counts(sub_game))]

    WIN_CACHE[game] = win_counts
    return win_counts


with open(INPUT_FILE_NAME, "r") as input_file:
    start_positions: List[int] = [
        int(line.split(" ")[-1].strip()) for line in input_file
    ]

win_counts = gen_win_counts(Game(positions=tuple(start_positions)))
print(win_counts)
print(max(win_counts))
