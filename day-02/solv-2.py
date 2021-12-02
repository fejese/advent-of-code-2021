#!/usr/bin/env python3

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

with open(INPUT_FILE_NAME, "r") as input_file:
    x: int = 0
    depth: int = 0
    aim: int = 0
    for instruction in input_file:
        direction, amount_str = instruction.split(" ")
        amount: int = int(amount_str)
        if direction == "forward":
            x += amount
            depth += aim * amount
        elif direction == "down":
            aim += amount
        elif direction == "up":
            aim -= amount
        else:
            raise Exception(f"Can't parse instruction: {instruction}")

    print(x * depth)
