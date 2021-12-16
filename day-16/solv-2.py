#!/usr/bin/env python3

import re
from typing import List, Optional, Tuple

# INPUT_FILE_NAME: str = "test-input-3"
INPUT_FILE_NAME: str = "input"

LITERAL_PATTERN: re.Pattern = re.compile(r"^(1[01]{4})*0[01]{4}")

"""
000 - version
000 - type id
    4 => literal value
        (1[01]{4})*0[01]{4}

    !4 => operator
        0 - length type id
            0 => [01]{15} = length
            1 => [01]{11} = # sub-packets
    0 => sum
    1 => product
    2 => min
    3 => max
    5 => gt (a > b ? 1 : 0)
    6 => lt (a < b ? 1 : 0)
    7 => eq (a = b ? 1 : 0)


top level:
"""


def process_packets(
    bin_str: str,
    num_sub_packets: Optional[int] = None,
    length_sub_packets: Optional[int] = None,
) -> Tuple[List[int], str]:
    values: List[int] = []
    length: int = 0
    assert num_sub_packets is not None or length_sub_packets is not None

    if num_sub_packets:
        for _ in range(num_sub_packets):
            type_id: int = int(bin_str[length + 3 : length + 6], 2)
            length += 6

            if type_id == 4:
                payload: str = LITERAL_PATTERN.match(bin_str[length:]).group(0)
                length += len(payload)
                value: int = 0
                for _ in range(int(len(payload) / 3)):
                    if not payload:
                        break
                    value = value * 16 + int(payload[1:5], 2)
                    payload = payload[5:]
                values.append(value)
            else:
                length_type_id: int = int(bin_str[length], 2)
                length += 1
                sub_values: List[int]
                if length_type_id == 0:
                    sub_length: int = int(bin_str[length : length + 15], 2)
                    length += 15
                    sub_values, _ = process_packets(
                        bin_str[length : length + sub_length],
                        length_sub_packets=sub_length,
                    )
                    length += sub_length
                else:
                    sub_num: int = int(bin_str[length : length + 11], 2)
                    length += 11
                    sub_values, remainder = process_packets(
                        bin_str[length:], num_sub_packets=sub_num
                    )
                    length = len(bin_str) - len(remainder)
                value: int
                if type_id == 0:
                    value = sum(sub_values)
                elif type_id == 1:
                    value: int = 1
                    for sub_val in sub_values:
                        value *= sub_val
                elif type_id == 2:
                    value = min(sub_values)
                elif type_id == 3:
                    value = max(sub_values)
                elif type_id == 5:
                    assert len(sub_values) == 2
                    value = 1 if sub_values[0] > sub_values[1] else 0
                elif type_id == 6:
                    assert len(sub_values) == 2
                    value = 1 if sub_values[0] < sub_values[1] else 0
                elif type_id == 7:
                    assert len(sub_values) == 2
                    value = 1 if sub_values[0] == sub_values[1] else 0
                else:
                    assert f"unknown operator: {type_id}"
                values.append(value)
    else:
        # length_sub_packets
        while length < length_sub_packets:
            type_id: int = int(bin_str[length + 3 : length + 6], 2)
            length += 6

            if type_id == 4:
                payload: str = LITERAL_PATTERN.match(bin_str[length:]).group(0)
                length += len(payload)
                value: int = 0
                for _ in range(int(len(payload) / 3)):
                    if not payload:
                        break
                    value = value * 16 + int(payload[1:5], 2)
                    payload = payload[5:]
                values.append(value)
            else:
                length_type_id: int = int(bin_str[length], 2)
                length += 1
                sub_values: List[int]
                if length_type_id == 0:
                    sub_length: int = int(bin_str[length : length + 15], 2)
                    length += 15
                    sub_values, _ = process_packets(
                        bin_str[length : length + sub_length],
                        length_sub_packets=sub_length,
                    )
                    length += sub_length
                else:
                    sub_num: int = int(bin_str[length : length + 11], 2)
                    length += 11
                    sub_values, remainder = process_packets(
                        bin_str[length:], num_sub_packets=sub_num
                    )
                    length = len(bin_str) - len(remainder)
                value: int
                if type_id == 0:
                    value = sum(sub_values)
                elif type_id == 1:
                    value: int = 1
                    for sub_val in sub_values:
                        value *= sub_val
                elif type_id == 2:
                    value = min(sub_values)
                elif type_id == 3:
                    value = max(sub_values)
                elif type_id == 5:
                    assert len(sub_values) == 2
                    value = 1 if sub_values[0] > sub_values[1] else 0
                elif type_id == 6:
                    assert len(sub_values) == 2
                    value = 1 if sub_values[0] < sub_values[1] else 0
                elif type_id == 7:
                    assert len(sub_values) == 2
                    value = 1 if sub_values[0] == sub_values[1] else 0
                else:
                    assert f"unknown operator: {type_id}"
                values.append(value)
    return (values, bin_str[length:])


def process(hex_str: str) -> None:
    bin_str: str = "".join(f"{int(ch, 16):04b}" for ch in hex_str)

    values, remainder = process_packets(bin_str, num_sub_packets=1)
    print(values, remainder)


with open(INPUT_FILE_NAME, "r") as input_file:
    for line in input_file:
        process(line.strip())
