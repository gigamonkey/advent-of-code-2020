#!/usr/bin/env python

import fileinput
import re
from dataclasses import dataclass
from dataclasses import field
from typing import Dict
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
class CPU:
    memory: Dict[int, int] = field(default_factory=dict)
    mask: Optional[Mask] = None

    def sum(self):
        return sum(self.memory.values())


def parse(input):
    for line in input:
        if m := mask_inst.fullmatch(line):
            keep, on = decode(m.group(1))
            yield Mask(keep, on)
        elif m := store_instr.fullmatch(line):
            yield Store(int(m.group(1)), int(m.group(2)))
        else:
            raise Exception(f"No match: {line[:-1]}")


def decode(mask):
    keep = int(mask.replace("1", "0").replace("X", "1"), 2)
    on = int(mask.replace("X", "0"), 2)
    return keep, on


if __name__ == "__main__":

    cpu = CPU()

    for op in parse(fileinput.input()):
        op.execute(cpu)

    print(cpu.sum())
