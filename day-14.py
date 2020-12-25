#!/usr/bin/env python

import fileinput
import re
from dataclasses import dataclass
from dataclasses import field
from functools import reduce
from itertools import combinations
from typing import Dict
from typing import List
from typing import Optional

mask_inst = re.compile(r"mask = (.*)\n")
store_instr = re.compile(r"mem\[(\d+)\] = (\d+)\n")


@dataclass
class Mask:
    keep: int
    on: int

    def execute(self, cpu):
        cpu.mask = self


@dataclass
class Store:
    address: int
    value: int

    def execute(self, cpu):
        cpu.memory[self.address] = (self.value & cpu.mask.keep) | cpu.mask.on


@dataclass
class FloatingMask:
    keep: int
    on: int
    floating: List[int]

    def execute(self, cpu):
        cpu.mask = self


@dataclass
class FloatingStore(Store):
    def execute(self, cpu):
        base = (self.address & cpu.mask.keep) | cpu.mask.on
        for f in cpu.mask.floating:
            cpu.memory[base | f] = self.value


@dataclass
class CPU:
    memory: Dict[int, int] = field(default_factory=dict)
    mask: Optional[Mask] = None

    def sum(self):
        return sum(self.memory.values())


def parse(input, mask_decoder, store):
    for line in input:
        if m := mask_inst.fullmatch(line):
            yield mask_decoder(m.group(1))
        elif m := store_instr.fullmatch(line):
            yield store(int(m.group(1)), int(m.group(2)))
        else:
            raise Exception(f"No match: {line[:-1]}")


def decode(mask):
    keep = int(mask.replace("1", "0").replace("X", "1"), 2)
    on = int(mask.replace("X", "0"), 2)
    return Mask(keep, on)


def floating_masks(mask):

    # And this to pass through all the bits that are 0 in the mask
    k_d = {"1": "0", "0": "1", "X": "0"}
    keep = int("".join(k_d[c] for c in mask), 2)

    # Or this to turn on all the bits that are 1 in the mask.
    on = int(mask.replace("X", "0"), 2)

    # Floats
    bits = [2 ** (35 - i) for i, c in enumerate(mask) if c == "X"]
    floating = [
        reduce(lambda a, b: a | b, c, 0)
        for i in range(len(bits) + 1)
        for c in combinations(bits, i)
    ]

    return FloatingMask(keep, on, floating)


if __name__ == "__main__":

    part = 2

    if part == 1:
        mask = decode
        store = Store

    else:
        mask = floating_masks
        store = FloatingStore

    cpu = CPU()

    for op in parse(fileinput.input(), mask, store):
        op.execute(cpu)

    print(cpu.sum())
