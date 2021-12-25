#!/usr/bin/env python3

import re
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

Coord = Tuple[int, int]
TRANSIENT_CORR_POS: Set[int] = {2, 4, 6, 8}


@dataclass
class Game:
    rooms: List[str]
    corridor: str
    cost: int = 0
    parent: Optional["Game"] = None

    _cache_key: Optional[str] = None

    @property
    def cache_key(self) -> str:
        if not self._cache_key:
            cache_parts: List[str] = [self.corridor] + self.rooms
            self._cache_key = "|".join(cache_parts)
        return self._cache_key

    @property
    def done(self) -> bool:
        return all(
            all(pos == expected for pos in room)
            for room, expected in zip(self.rooms, "ABCD")
        )

    def print_no_parent(self) -> None:
        print(f"Game(rooms={self.rooms}, corridor={self.corridor}, cost={self.cost})")

    def print_stack(self) -> None:
        if self.parent:
            self.parent.print_stack()
        self.print_no_parent()


def read_input() -> Game:
    with open(INPUT_FILE_NAME, "r") as input_file:
        lines: List[str] = input_file.readlines()
        rooms: List[List[str]] = [
            "".join(lines[y][x] for y in [2, 3]) for x in [3, 5, 7, 9]
        ]
    return Game(rooms=rooms, corridor="." * 11)


def get_min_cost(game: Game) -> int:
    games_to_process: List[Game] = deque([game])
    games_processed: Dict[str, int] = {}
    min_cost: Optional[int] = None
    hit_count: Dict[str, int] = defaultdict(int)

    process_iteration: int = 0
    while games_to_process:
        hit_count[game.cache_key] += 1

        if len(games_to_process) == 1:
            print(
                f"iteration (total processed): {process_iteration:7d},",
                f"processed: {len(games_processed):6d},",
                f"to process: {len(games_to_process):5d},",
                f"min cost: {min_cost or -1:6d},",
                f"key: {game.cache_key},",
                f"hits: {hit_count[game.cache_key]},",
            )
        process_iteration += 1
        game: Game = games_to_process.popleft()

        if game.cache_key in games_processed:
            if games_processed[game.cache_key] <= game.cost:
                continue
            games_processed[game.cache_key] = game.cost
        else:
            games_processed[game.cache_key] = game.cost
        if game.done:
            if min_cost is None or min_cost > game.cost:
                print("New min cost:")
                game.print_stack()
                min_cost = game.cost
            continue

        if min_cost is not None and game.cost >= min_cost:
            continue

        corr: str = game.corridor
        new_games: List[Game] = []

        for room_no, letter in enumerate("ABCD"):
            step_cost = 10 ** room_no
            room_pos = room_no * 2 + 2

            if letter in corr and game.rooms[room_no].strip(f".{letter}") == "":
                new_room: str
                room_steps: int

                if game.rooms[room_no] == "..":
                    new_room = f".{letter}"
                    room_steps = 2
                else:
                    new_room = letter * 2
                    room_steps = 1

                new_rooms: List[str] = [
                    new_room if i == room_no else room
                    for i, room in enumerate(game.rooms)
                ]

                try:
                    corr_pos: int = corr.rindex(letter, 0, room_pos)
                    if corr[corr_pos + 1 : room_pos].strip(".") == "":
                        corr_steps: int = room_pos - corr_pos
                        new_corridor: str = corr[:corr_pos] + "." + corr[corr_pos + 1 :]
                        new_games.append(
                            Game(
                                rooms=new_rooms,
                                corridor=new_corridor,
                                cost=game.cost + step_cost * (corr_steps + room_steps),
                                parent=game,
                            )
                        )
                except ValueError:
                    pass

                try:
                    corr_pos: int = corr.index(letter, room_pos)
                    if corr[room_pos:corr_pos].strip(".") == "":
                        corr_steps: int = corr_pos - room_pos
                        new_corridor: str = corr[:corr_pos] + "." + corr[corr_pos + 1 :]
                        new_games.append(
                            Game(
                                rooms=new_rooms,
                                corridor=new_corridor,
                                cost=game.cost + step_cost * (corr_steps + room_steps),
                                parent=game,
                            )
                        )
                except ValueError:
                    pass

            if game.rooms[room_no].strip(f".{letter}") != "":
                new_room: str
                room_steps: int
                found_letter: str

                if game.rooms[room_no][0] == ".":
                    new_room = ".."
                    room_steps = 2
                    found_letter = game.rooms[room_no][1]
                else:
                    new_room = "." + game.rooms[room_no][1]
                    room_steps = 1
                    found_letter = game.rooms[room_no][0]

                new_rooms: List[str] = [
                    new_room if i == room_no else room
                    for i, room in enumerate(game.rooms)
                ]
                found_step_cost: int = 10 ** "ABCD".index(found_letter)

                min_valid_corr_pos: int = room_pos
                max_valid_corr_pos: int = room_pos
                for corr_pos in range(len(corr)):
                    if corr_pos in TRANSIENT_CORR_POS:
                        continue
                    if corr_pos < room_pos:
                        if corr[corr_pos] == ".":
                            if min_valid_corr_pos == room_pos:
                                min_valid_corr_pos = corr_pos
                        else:
                            min_valid_corr_pos = room_pos
                    else:
                        if corr[corr_pos] == ".":
                            max_valid_corr_pos = corr_pos
                        else:
                            break

                for corr_pos in range(min_valid_corr_pos, max_valid_corr_pos + 1, 1):
                    if corr_pos in TRANSIENT_CORR_POS:
                        continue
                    corr_steps: int = abs(corr_pos - room_pos)
                    new_corridor: str = corr[:corr_pos] + found_letter + corr[
                        corr_pos + 1 :
                    ]

                    new_games.append(
                        Game(
                            rooms=new_rooms,
                            corridor=new_corridor,
                            cost=game.cost
                            + found_step_cost * (corr_steps + room_steps),
                            parent=game,
                        )
                    )

        # if game.cache_key in [
        #     "...B.......|BA|CD|.C|DA"
        # ]:
        #     print(f"new games for {game.cache_key}")
        #     [g.print_no_parent() for g in new_games]
        games_to_process += new_games

    return min_cost


initial_game: Game = read_input()
min_cost = get_min_cost(initial_game)
print(min_cost)
