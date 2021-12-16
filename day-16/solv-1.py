#!/usr/bin/env python3

import re
from typing import List, Optional, Tuple

# INPUT_FILE_NAME: str = "test-input"
# INPUT_FILE_NAME: str = "test-input-2"
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

top level:
"""


def process_packets(
    bin_str: str,
    num_sub_packets: Optional[int] = None,
    length_sub_packets: Optional[int] = None,
) -> Tuple[List[int], str]:
    versions: List[int] = []
    length: int = 0
    assert num_sub_packets is not None or length_sub_packets is not None

    if num_sub_packets:
        for _ in range(num_sub_packets):
            version: int = int(bin_str[length : length + 3], 2)
            type_id: int = int(bin_str[length + 3 : length + 6], 2)
            versions.append(version)
            length += 6

            if type_id == 4:
                payload: str = LITERAL_PATTERN.match(bin_str[length:]).group(0)
                length += len(payload)
            else:
                length_type_id: int = int(bin_str[length], 2)
                length += 1
                if length_type_id == 0:
                    sub_length: int = int(bin_str[length : length + 15], 2)
                    length += 15
                    sub_versions, _ = process_packets(
                        bin_str[length : length + sub_length],
                        length_sub_packets=sub_length,
                    )
                    versions += sub_versions
                    length += sub_length
                else:
                    sub_num: int = int(bin_str[length : length + 11], 2)
                    length += 11
                    sub_versions, remainder = process_packets(
                        bin_str[length:], num_sub_packets=sub_num
                    )
                    versions += sub_versions
                    length = len(bin_str) - len(remainder)
    else:
        # length_sub_packets
        while length < length_sub_packets:
            version: int = int(bin_str[length : length + 3], 2)
            type_id: int = int(bin_str[length + 3 : length + 6], 2)
            versions.append(version)
            length += 6

            if type_id == 4:
                payload: str = LITERAL_PATTERN.match(bin_str[length:]).group(0)
                length += len(payload)
            else:
                length_type_id: int = int(bin_str[length], 2)
                length += 1
                if length_type_id == 0:
                    sub_length: int = int(bin_str[length : length + 15], 2)
                    length += 15
                    sub_versions, _ = process_packets(
                        bin_str[length : length + sub_length],
                        length_sub_packets=sub_length,
                    )
                    versions += sub_versions
                    length += sub_length
                else:
                    sub_num: int = int(bin_str[length : length + 11], 2)
                    length += 11
                    sub_versions, remainder = process_packets(
                        bin_str[length:], num_sub_packets=sub_num
                    )
                    versions += sub_versions
                    length = len(bin_str) - len(remainder)
    return (versions, bin_str[length:])


def process(hex_str: str) -> None:
    bin_str: str = "".join(f"{int(ch, 16):04b}" for ch in hex_str)

    versions, remainder = process_packets(bin_str, num_sub_packets=1)
    print(versions, sum(versions), remainder)


with open(INPUT_FILE_NAME, "r") as input_file:
    for line in input_file:
        process(line.strip())
