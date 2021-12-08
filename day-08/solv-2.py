#!/usr/bin/env python3

from copy import copy
from typing import List, Optional, Set

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

# 2 char => 1
# 3 char => 7
# 4 char => 4
# 5 char => 2, 3, 5
# 6 char => 0, 6, 9
# 7 char => 8

#  aaaa
# b    c
# b    c
#  dddd
# e    f
# e    f
#  gggg


def get_output(digits: List[str]) -> int:
    nums: List[Set[str]] = [set(ch for ch in d) for d in digits]

    known: List[Optional[Set[str]]] = [None] * 10
    for num in nums:
        if len(num) == 2:
            known[1] = num
        elif len(num) == 3:
            known[7] = num
        elif len(num) == 4:
            known[4] = num
        elif len(num) == 7:
            known[8] = num

    for num in nums:
        if len(num) == 5:
            if len(num.intersection(known[1])) == 2:
                known[3] = num
            elif len(num.intersection(known[4])) == 2:
                known[2] = num
            else:
                known[5] = num
        elif len(num) == 6:
            if len(num.intersection(known[1])) == 1:
                known[6] = num
            elif len(num.intersection(known[4])) == 3:
                known[0] = num
            else:
                known[9] = num

    output_num = 0
    for output in nums[-4:]:
        output_num = output_num * 10 + known.index(output)

    return output_num


output_total: int = 0
with open(INPUT_FILE_NAME, "r") as input_file:
    for line in input_file:
        output = get_output(line.replace(" |", "").strip().split(" "))
        # print(output)
        output_total += output

print(output_total)
