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

oxygen_nums = [num for num in nums]
co2_nums = [num for num in nums]

i: int = 0
while len(oxygen_nums) > 1:
    # print(oxygen_nums)
    zeroes, ones = get_distribution(oxygen_nums, i)
    bit = "0" if zeroes > ones else "1"
    oxygen_nums = [num for num in oxygen_nums if num[i] == bit]
    i = i + 1
oxygen_num = oxygen_nums[0]

i: int = 0
while len(co2_nums) > 1:
    zeroes, ones = get_distribution(co2_nums, i)
    bit = "1" if ones < zeroes else "0"
    co2_nums = [num for num in co2_nums if num[i] == bit]
    i = i + 1
co2_nums = co2_nums[0]

print(oxygen_num, co2_nums)
print(int(oxygen_num, 2), int(co2_nums, 2))
print(int(oxygen_num, 2) * int(co2_nums, 2))
