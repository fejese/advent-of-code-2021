#!/usr/bin/env python3

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple

# INPUT_FILE_NAME: str = "test-input-3"
INPUT_FILE_NAME: str = "input"

GRID_MIN: int = -50
GRID_MAX: int = 50
INPUT_LINE_PATTERN: re.Pattern = re.compile(
    r"^(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)$"
)


class ActionIDGenerator:
    def __init__(self) -> None:
        self.next_id: int = 0

    def gen(self) -> int:
        id: int = self.next_id
        self.next_id += 1
        return id


ACTION_ID_GENERATOR: ActionIDGenerator = ActionIDGenerator()


@dataclass
class Action:
    action: str
    x_min: int
    x_max: int
    y_min: int
    y_max: int
    z_min: int
    z_max: int
    id: int = field(default_factory=ACTION_ID_GENERATOR.gen)

    @property
    def size(self) -> int:
        return (
            (self.x_max - self.x_min + 1)
            * (self.y_max - self.y_min + 1)
            * (self.z_max - self.z_min + 1)
        )


def parse_input() -> List[Action]:
    actions: List[Action] = []
    with open(INPUT_FILE_NAME, "r") as input_file:
        for line_no, line in enumerate(input_file):
            match: Optional[re.Match] = INPUT_LINE_PATTERN.match(line)
            if not match:
                raise Exception(f"Can not parse linen {line_no}: [{line}]")
            action: str = match.group(1)
            x_min, x_max = sorted(int(match.group(i)) for i in [2, 3])
            y_min, y_max = sorted(int(match.group(i)) for i in [4, 5])
            z_min, z_max = sorted(int(match.group(i)) for i in [6, 7])
            actions.append(Action(action, x_min, x_max, y_min, y_max, z_min, z_max))
    return actions


# INTERSECT_CACHE: Dict[Tuple[int, int], bool] = {}


def intersect(a: Action, b: Action) -> bool:
    # global INTERSECT_CACHE
    # cache_key: Tuple[int, int] = tuple(sorted([a.id, b.id]))
    # if cache_key in INTERSECT_CACHE:
    #     return INTERSECT_CACHE[cache_key]

    result: bool = True
    if a.x_max < b.x_min or a.x_min > b.x_max:
        result = False
    elif a.y_max < b.y_min or a.y_min > b.y_max:
        result = False
    elif a.z_max < b.z_min or a.z_min > b.z_max:
        result = False

    # INTERSECT_CACHE[cache_key] = result
    return result


def gen_intersection_actions(a: Action, b: Action) -> List[Action]:
    intersection: Action = Action(
        action=b.action,
        x_min=max(a.x_min, b.x_min),
        x_max=min(a.x_max, b.x_max),
        y_min=max(a.y_min, b.y_min),
        y_max=min(a.y_max, b.y_max),
        z_min=max(a.z_min, b.z_min),
        z_max=min(a.z_max, b.z_max),
    )
    # print("Intersection:", intersection)
    actions: List[Action] = []
    if intersection.x_min > a.x_min:
        # print("1")
        actions.append(
            Action(
                action=a.action,
                x_min=a.x_min,
                x_max=intersection.x_min - 1,
                y_min=a.y_min,
                y_max=a.y_max,
                z_min=a.z_min,
                z_max=a.z_max,
            )
        )
    if intersection.x_max < a.x_max:
        # print("2")
        actions.append(
            Action(
                action=a.action,
                x_min=intersection.x_max + 1,
                x_max=a.x_max,
                y_min=a.y_min,
                y_max=a.y_max,
                z_min=a.z_min,
                z_max=a.z_max,
            )
        )
    if intersection.y_min > a.y_min:
        # print("3")
        actions.append(
            Action(
                action=a.action,
                x_min=intersection.x_min,
                x_max=intersection.x_max,
                y_min=a.y_min,
                y_max=intersection.y_min - 1,
                z_min=a.z_min,
                z_max=a.z_max,
            )
        )
    if intersection.y_max < a.y_max:
        # print("4")
        actions.append(
            Action(
                action=a.action,
                x_min=intersection.x_min,
                x_max=intersection.x_max,
                y_min=intersection.y_max + 1,
                y_max=a.y_max,
                z_min=a.z_min,
                z_max=a.z_max,
            )
        )
    if intersection.z_min > a.z_min:
        # print("5")
        actions.append(
            Action(
                action=a.action,
                x_min=intersection.x_min,
                x_max=intersection.x_max,
                y_min=intersection.y_min,
                y_max=intersection.y_max,
                z_min=a.z_min,
                z_max=intersection.z_min - 1,
            )
        )
    if intersection.z_max < a.z_max:
        # print("6")
        actions.append(
            Action(
                action=a.action,
                x_min=intersection.x_min,
                x_max=intersection.x_max,
                y_min=intersection.y_min,
                y_max=intersection.y_max,
                z_min=intersection.z_max + 1,
                z_max=a.z_max,
            )
        )
    actions.append(b)
    return actions


SIMPLIFICATION_COUNT: int = 0


def simplify(actions: List[Action]) -> Tuple[List[Action], bool]:
    global SIMPLIFICATION_COUNT
    print(f"Simplification round {SIMPLIFICATION_COUNT}")
    SIMPLIFICATION_COUNT += 1
    print(f"  action count: {len(actions)}")

    simplified_actions: List[Action] = []
    change: bool = False
    ai: int
    for ai, action in enumerate(actions):
        intersection_with_simplified_action: Optional[int] = None
        for sai, simplified_action in enumerate(simplified_actions):
            if intersect(action, simplified_action):
                intersection_with_simplified_action = sai
                break
        if intersection_with_simplified_action is None:
            if action.action == "on":
                simplified_actions.append(action)
            else:
                change = True
            continue

        change = True
        simplified_action = simplified_actions[sai]
        simplified_actions.remove(simplified_action)
        intersection_actions = gen_intersection_actions(simplified_action, action)
        need_break: bool = True
        # need_break: bool = False
        # for intersection_action in intersection_actions:
        #     for simplified_action in simplified_actions:
        #         if intersect(intersection_action, simplified_action):
        #             need_break = True
        #             break
        #     if need_break:
        #         break
        simplified_actions += intersection_actions
        simplified_actions += actions[ai + 1 :]
        if need_break:
            break
    print(f"  last action: {ai}")
    print(f"  actions left: {len(simplified_actions) - ai}")

    return (simplified_actions, change)


actions: List[Action] = parse_input()
while True:
    change: bool
    actions, change = simplify(actions)
    if not change:
        break

on_count: int = sum(a.size for a in actions)

print(on_count)
