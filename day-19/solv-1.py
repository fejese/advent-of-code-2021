#!/usr/bin/env python3

from copy import copy
from typing import List, Set, Tuple

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

COS: List[int] = [1.0, 0.0, -1.0, -0.0]
SIN: List[int] = [0.0, 1.0, 0.0, -1.0]

M = List[List[int]]
P = Tuple[int, int, int]
Scan = Set[P]


class FoundOne(Exception):
    pass


"""
Rx(i) = [
    [1, 0, 0],
    [0, cos i, -sin i],
    [0, sin i, cos i],
]
Ry(i) = [
    [cos i, 0, sin i],
    [0, 1, 0],
    [-sin i, 0 , cos i],
]
Rz(i) = [
    [cos i, -sin i, 0],
    [sin i, cos i, 0],
    [0, 0, 1],
]
"""


def get_rx(quarter_turns: int) -> M:
    quarter_turns = quarter_turns % 4
    return [
        [1, 0, 0],
        [0, COS[quarter_turns], -SIN[quarter_turns]],
        [0, SIN[quarter_turns], COS[quarter_turns]],
    ]


def get_ry(quarter_turns: int) -> M:
    quarter_turns = quarter_turns % 4
    return [
        [COS[quarter_turns], 0, SIN[quarter_turns]],
        [0, 1, 0],
        [-SIN[quarter_turns], 0, COS[quarter_turns]],
    ]


def get_rz(quarter_turns: int) -> M:
    quarter_turns = quarter_turns % 4
    return [
        [COS[quarter_turns], -SIN[quarter_turns], 0],
        [SIN[quarter_turns], COS[quarter_turns], 0],
        [0, 0, 1],
    ]


ROTATIONS: List[List[M]] = [
    *[[get_rx(rxi), get_ry(ryi)] for ryi in range(4) for rxi in range(4)],
    *[[get_rx(rxi), get_rz(rzi)] for rzi in [1, 3] for rxi in range(4)],
]


def rotate(point: P, rotations: List[M]) -> P:
    new_point: P = copy(point)
    for rotation in rotations:
        new_point = tuple(
            sum(new_point[i] * rotation[i][j] for i in range(3)) for j in range(3)
        )
    return new_point


def set_o(point: P, origo: P) -> P:
    return tuple(pc - oc for pc, oc in zip(point, origo))


scans: List[Scan]

with open(INPUT_FILE_NAME, "r") as input_file:
    scans = [
        set(
            tuple(int(n) for n in point_data.strip().split(","))
            for point_data in scan_data.strip().split("\n")[1:]
        )
        for scan_data in input_file.read().strip().split("\n\n")
    ]

ROTATION_CACHE: List[List[Scan]] = [
    [set(rotate(p, rotation) for p in scan) for rotation in ROTATIONS] for scan in scans
]

beacons: Set[P] = scans[0]
matched: List[int] = [0]
checked_pairs: Set[Tuple[int, int]] = set()

while len(matched) < len(scans):
    try:
        for lidx, left in enumerate(scans):
            if lidx not in matched:
                continue
            for ridx, right in enumerate(scans):
                if (min(lidx, ridx), max(lidx, ridx)) in checked_pairs:
                    continue
                if lidx == ridx or ridx in matched:
                    continue
                for rotation_id in range(len(ROTATIONS)):
                    rotated_right: Scan = ROTATION_CACHE[ridx][rotation_id]
                    for o_left in left:
                        for o_right in rotated_right:
                            o_diff: P = tuple(
                                roc - loc for loc, roc in zip(o_left, o_right)
                            )
                            shifted_right: Scan = set(
                                set_o(p, o_diff) for p in rotated_right
                            )
                            intersection: Set[P] = left.intersection(shifted_right)
                            if len(intersection) >= 12:
                                beacons = beacons.union(shifted_right)
                                scans[ridx] = shifted_right
                                matched.append(ridx)
                                print(f"Matched {ridx} with {lidx}")
                                raise FoundOne()
                checked_pairs.add((min(lidx, ridx), max(lidx, ridx)))
    except FoundOne:
        pass


print(len(beacons))
