#!/usr/bin/env python3

from copy import copy
from functools import partial
from typing import Callable, Dict, List, Optional, Tuple, Union

INPUT_FILE_NAME: str = "input"


class InputProvider:
    def __init__(self, input: int) -> None:
        self.input = [int(x) for x in str(input)]
        self.index = 0
        self.len = len(self.input)

    def read(self) -> int:
        if self.index >= self.len:
            raise Exception(f"Out of data for {self.input}")
        ret_val = self.input[self.index]
        self.index += 1
        return ret_val


Instruction = Callable[[InputProvider, Dict[str, int]], None]


def inp(
    register: str, input_provider: InputProvider, registers: Dict[str, int],
) -> None:
    # print(f"[inp] register: {register}")
    registers[register] = input_provider.read()


def add(
    register_a: str,
    b: Union[str, int],
    input_provider: InputProvider,
    registers: Dict[str, int],
) -> None:
    b_val: int = b if isinstance(b, int) else registers[b]
    # print(f"[add] register_a: {register_a}, b: {b}, b_val: {b_val}")
    registers[register_a] += b_val


def mul(
    register_a: str,
    b: Union[str, int],
    input_provider: InputProvider,
    registers: Dict[str, int],
) -> None:
    b_val: int = b if isinstance(b, int) else registers[b]
    # print(f"[mul] register_a: {register_a}, b: {b}, b_val: {b_val}")
    registers[register_a] *= b_val


def div(
    register_a: str,
    b: Union[str, int],
    input_provider: InputProvider,
    registers: Dict[str, int],
) -> None:
    b_val: int = b if isinstance(b, int) else registers[b]
    # print(f"[div] register_a: {register_a}, b: {b}, b_val: {b_val}")
    registers[register_a] //= b_val


def mod(
    register_a: str,
    b: Union[str, int],
    input_provider: InputProvider,
    registers: Dict[str, int],
) -> None:
    b_val: int = b if isinstance(b, int) else registers[b]
    # print(f"[mod] register_a: {register_a}, b: {b}, b_val: {b_val}")
    registers[register_a] %= b_val


def eql(
    register_a: str,
    b: Union[str, int],
    input_provider: InputProvider,
    registers: Dict[str, int],
) -> None:
    b_val: int = b if isinstance(b, int) else registers[b]
    # print(f"[eql] register_a: {register_a}, b: {b}, b_val: {b_val}")
    registers[register_a] = 1 if registers[register_a] == b_val else 0


def parse_input() -> List[List[Instruction]]:
    instructions: List[List[Instruction]] = []
    with open(INPUT_FILE_NAME, "r") as input_file:
        for line in input_file:
            parts: List[str] = line.strip().split(" ")
            op: str = parts[0]
            a: str = parts[1]
            b: Optional[Union[str, int]] = None
            if len(parts) > 2:
                try:
                    b: int = int(parts[2])
                except ValueError:
                    b: str = parts[2]
            if op == "inp":
                instructions.append([partial(inp, a)])
            elif op == "add":
                instructions[-1].append(partial(add, a, b))
            elif op == "mul":
                instructions[-1].append(partial(mul, a, b))
            elif op == "div":
                instructions[-1].append(partial(div, a, b))
            elif op == "mod":
                instructions[-1].append(partial(mod, a, b))
            elif op == "eql":
                instructions[-1].append(partial(eql, a, b))
            else:
                raise Exception(f"Unknown op: {op} (from {line})")
    return instructions


RegisterCacheKey = Tuple[str, int]
CacheKey = Tuple[
    int, Tuple[RegisterCacheKey, RegisterCacheKey, RegisterCacheKey, RegisterCacheKey]
]


CACHE: Dict[CacheKey, Optional[int]] = {}
CACHE_HIT: int = 0
CACHE_TOTAL: int = 0


def get_min_valid(
    instructions: List[List[Instruction]],
    length: int,
    instruction_set_idx: int = 0,
    initial_registers: Dict[str, int] = None,
    prefix: int = 0,
) -> Optional[int]:
    if initial_registers is None:
        initial_registers = {register: 0 for register in "xyzw"}

    global CACHE
    global CACHE_HIT
    global CACHE_TOTAL
    CACHE_TOTAL += 1
    cache_miss: int = CACHE_TOTAL - CACHE_HIT
    if CACHE_TOTAL % 10000 == 0:
        cache_ratio: float = 0 if CACHE_HIT == 0 else CACHE_HIT / (CACHE_TOTAL)
        print(
            f"trying prefix: {str(prefix):14s}",
            f"CACHE total: {CACHE_TOTAL:10d}",
            f"hit: {CACHE_HIT:10d}",
            f"miss: {cache_miss:10d}",
            f"ratio: {cache_ratio:2.4%}",
        )
    cache_key: CacheKey = tuple([length, *initial_registers.items()])
    if cache_key in CACHE:
        CACHE_HIT += 1
        return CACHE[cache_key]

    for input in range(1, 10):
        registers: Dict[str, int] = copy(initial_registers)
        input_provider: InputProvider = InputProvider(input)
        for instruction in instructions[instruction_set_idx]:
            instruction(input_provider, registers)

        if length == 1:
            if registers["z"] == 0:
                # print(f"VALID: {input}")
                CACHE[cache_key] = input
                return input
        else:
            sub_min_valid: Optional[int] = get_min_valid(
                instructions=instructions,
                length=length - 1,
                instruction_set_idx=instruction_set_idx + 1,
                initial_registers=registers,
                prefix=10 * prefix + input,
            )
            if sub_min_valid is not None:
                min_valid: int = 10 ** (length - 1) * input + sub_min_valid
                # print(f"VALID: {min_valid}")
                CACHE[cache_key] = min_valid
                return min_valid

    CACHE[cache_key] = None
    return None


instructions: List[List[Instruction]] = parse_input()
print(get_min_valid(instructions, 14))
