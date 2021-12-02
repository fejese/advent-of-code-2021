#!/usr/bin/env python3

from typing import Optional

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

with open(INPUT_FILE_NAME, "r") as input_file:
    prev: Optional[int] = None
    increase_count: int = 0
    for line in input_file:
        current: int = int(line.strip())
        if prev is not None and current > prev:
            increase_count += 1
        prev = current

    print(increase_count)
