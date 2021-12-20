#!/usr/bin/env python3

from typing import List

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

PADDING: int = 100

algo: List[int]
image: List[List[int]]

with open(INPUT_FILE_NAME, "r") as input_file:
    parts: List[str] = input_file.read().strip().split("\n\n")
    algo = [1 if ch == "#" else 0 for ch in parts[0].replace("\n", "")]
    image = [
        [1 if ch == "#" else 0 for ch in line] for line in parts[1].strip().split("\n")
    ]

image = (
    [[0] * len(image[0]) for _ in range(PADDING)]
    + image
    + [[0] * len(image[0]) for _ in range(PADDING)]
)
image = [[0] * PADDING + line + [0] * PADDING for line in image]


def enhance(
    image: List[List[int]], algo: List[int], default_pixel: int,
) -> List[List[int]]:
    width: int = len(image[0])
    height: int = len(image)
    enhanced: List[List[int]] = [[0] * width for _ in range(height)]
    for xi in range(width):
        for yi in range(height):
            index: int = 0
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    bit: int
                    if 0 <= xi + dx < width and 0 <= yi + dy < height:
                        bit = image[yi + dy][xi + dx]
                    else:
                        bit = default_pixel
                    index = (index << 1) + bit
            enhanced[yi][xi] = algo[index]
    return enhanced


def print_image(image: List[List[int]]) -> None:
    for line in image:
        print("".join(["#" if bit == 1 else "." for bit in line]))
    print()


for i in range(50):
    print(f"Enhance round #{i+1}")
    image = enhance(image, algo, default_pixel=i % 2)

print_image(image)
count = sum(sum(line) for line in image)
print(count)
