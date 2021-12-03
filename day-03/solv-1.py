#!/usr/bin/env python3

from typing import List, Tuple

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

nums: List[str]
with open(INPUT_FILE_NAME, "r") as input_file:
    nums = [line.strip() for line in input_file]

num_length: int = len(nums[0])

gamma_rate: int = 0
epsilon_rate: int = 0

def get_distribution(nums: List[str], pos: int) -> Tuple[int, int]:
    zeroes: int = len([num for num in nums if num[i] == "0"])
    ones: int = len(nums) - zeroes
    return (zeroes, ones)

for i in range(num_length):
    zeroes, ones = get_distribution(nums, i)
    bit = 1 if zeroes > ones else 0
    nbit = 1 - bit
    gamma_rate = gamma_rate * 2 + bit
    epsilon_rate = epsilon_rate * 2 + nbit

print(gamma_rate * epsilon_rate)
