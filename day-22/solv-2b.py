#!/usr/bin/env python3

import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple

# INPUT_FILE_NAME: str = "test-input-3"
INPUT_FILE_NAME: str = "input"

INPUT_LINE_PATTERN: re.Pattern = re.compile(
    r"^(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)$"
)


@dataclass
class Action:
    action: str
    x_min: int
    x_max: int
    y_min: int
    y_max: int
    z_min: int
    z_max: int

    @property
    def size(self) -> int:
        return (
            (self.x_max - self.x_min + 1)
            * (self.y_max - self.y_min + 1)
            * (self.z_max - self.z_min + 1)
        )

    def intersect(self, other: "Action") -> bool:
        if self.x_max < other.x_min or self.x_min > other.x_max:
            return False
        if self.y_max < other.y_min or self.y_min > other.y_max:
            return False
        if self.z_max < other.z_min or self.z_min > other.z_max:
            return False

        return True


def parse_input() -> List[Action]:
    actions: List[Action] = []
    with open(INPUT_FILE_NAME, "r") as input_file:
        for line_no, line in enumerate(input_file):
            match: Optional[re.Match] = INPUT_LINE_PATTERN.match(line)
            if not match:
                raise Exception(f"Can not parse line {line_no}: [{line}]")
            action: str = match.group(1)
            x_min, x_max = sorted(int(match.group(i)) for i in [2, 3])
            y_min, y_max = sorted(int(match.group(i)) for i in [4, 5])
            z_min, z_max = sorted(int(match.group(i)) for i in [6, 7])
            actions.append(Action(action, x_min, x_max, y_min, y_max, z_min, z_max))
    return actions


def gen_sub_actions(a: Action, b: Action) -> List[Action]:
    intersection: Action = Action(
        action=b.action,
        x_min=max(a.x_min, b.x_min),
        x_max=min(a.x_max, b.x_max),
        y_min=max(a.y_min, b.y_min),
        y_max=min(a.y_max, b.y_max),
        z_min=max(a.z_min, b.z_min),
        z_max=min(a.z_max, b.z_max),
    )
    actions: List[Action] = []
    if intersection.x_min > a.x_min:
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
    return actions


def simplify(actions: List[Action]) -> List[Action]:
    simplified_actions: List[Action] = []
    for action in actions:
        new_simplified_actions: List[Action] = []
        for sai, simplified_action in enumerate(simplified_actions):
            if action.intersect(simplified_action):
                new_simplified_actions += gen_sub_actions(simplified_action, action)
            else:
                new_simplified_actions.append(simplified_action)
        simplified_actions = new_simplified_actions

        if action.action == "on":
            simplified_actions.append(action)

    return simplified_actions


actions: List[Action] = parse_input()
actions = simplify(actions)
on_count: int = sum(a.size for a in actions)

print(on_count)
