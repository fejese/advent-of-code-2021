#!/usr/bin/env python3

import re
from dataclasses import dataclass
from typing import List, Optional


# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

NUM_PATTERN: re.Pattern = re.compile(r"^\d+$")


class Node:
    def __init__(
        self,
        parent: Optional["Node"] = None,
        num: Optional[int] = None,
        left: Optional["Node"] = None,
        right: Optional["Node"] = None,
    ) -> None:
        self.parent: Optional["Node"] = parent
        self.num: Optional[int] = num
        self.left: Optional["Node"] = left
        self.right: Optional["Node"] = right
        self.level = 1 if parent is None else parent.level + 1

    @classmethod
    def from_string(cls, string: str, parent: Optional["Node"] = None) -> "Node":
        if NUM_PATTERN.match(string):
            return cls(parent=parent, num=int(string))

        node = cls(parent=parent)
        parts: List[str]

        string = string[1:-1]
        if string[0] == "[":
            open_bracket: int = 1
            idx: int = 1
            while open_bracket > 0:
                if string[idx] == "[":
                    open_bracket += 1
                elif string[idx] == "]":
                    open_bracket -= 1
                idx += 1
            parts = [string[:idx], string[idx + 1 :]]
        else:
            parts = string.split(",", 1)

        node.left = cls.from_string(parts[0], node)
        node.right = cls.from_string(parts[1], node)
        return node

    @property
    def magnitude(self) -> int:
        if self.num is not None:
            return self.num
        return self.left.magnitude * 3 + self.right.magnitude * 2

    def reduce(self) -> bool:
        if self.explode():
            # print("exploded")
            return True
        if self.split():
            # print("split")
            return True
        return False

    def split(self) -> bool:
        if self.num is not None and self.num >= 10:
            # print("splitting: ", self, " from ", self.parent)
            self.left = Node(parent=self, num=self.num // 2)
            self.right = Node(parent=self, num=self.num - self.left.num)
            self.num = None
            return True
        if self.left and self.left.split():
            return True
        if self.right and self.right.split():
            return True
        return False

    def explode(self) -> bool:
        if self.num is not None:
            return False

        if self.left and self.left.explode():
            return True

        if self.right and self.right.explode():
            return True

        if self.level <= 4:
            return False

        if self.left.num is None:
            return False

        if self.right.num is None:
            return False

        # print("Exploding: ", self, " from ", self.parent)

        child: Node = self
        parent: Node = child.parent
        while parent and parent.left == child:
            child = parent
            parent = child.parent
        if parent and parent.left:
            child = parent.left
            while child and child.right:
                child = child.right
            if child:
                child.num += self.left.num

        child = self
        parent = child.parent
        while parent and parent.right == child:
            child = parent
            parent = child.parent
        if parent and parent.right:
            child = parent.right
            while child and child.left:
                child = child.left
            if child:
                child.num += self.right.num

        self.left = None
        self.right = None
        self.num = 0
        return True

    def fix_levels(self) -> None:
        self.level = (self.parent.level + 1) if self.parent else 1
        if self.left:
            self.left.fix_levels()
        if self.right:
            self.right.fix_levels()

    def add(self, other: "Node") -> "Node":
        new_root = Node(left=self, right=other)
        self.parent = new_root
        other.parent = new_root
        new_root.fix_levels()
        return new_root

    def __str__(self) -> str:
        if self.num is not None:
            return str(self.num)
        return f"[{str(self.left)},{str(self.right)}]"


with open(INPUT_FILE_NAME, "r") as input_file:
    parts: List[str] = input_file.read().strip().split("\n\n")
    for part in parts:
        lines: List[str] = part.strip().split("\n")
        tree: Optional[Node] = None

        max_magnitude: int = 0
        for left_line in lines:
            for right_line in lines:
                if left_line == right_line:
                    continue
                left: Node = Node.from_string(left_line)
                right: Node = Node.from_string(right_line)
                total: Node = left.add(right)
                while total.reduce():
                    pass

                max_magnitude = max(max_magnitude, total.magnitude)

        print(max_magnitude)
        print()
