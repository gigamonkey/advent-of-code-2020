#!/usr/bin/env python

import fileinput
import re
from dataclasses import dataclass

op = re.compile("(\w+) ([-+]\d+)")


@dataclass
class Op:
    code: str
    num: int


@dataclass
class VM:
    pc: int = 0
    acc: int = 0

    def execute(self, op):
        if op.code == "acc":
            self.acc += op.num
            self.pc += 1
        elif op.code == "jmp":
            self.pc += op.num
        elif op.code == "nop":
            self.pc += 1


def parse(input):
    return [parse_op(line[:-1]) for line in input]


def parse_op(line):
    if m := op.fullmatch(line):
        return Op(m.group(1), int(m.group(2)))
    else:
        raise Exception(f"{line} doesn't match line pattern")


def run(ops):
    vm = VM()
    seen = set()
    while vm.pc not in seen:
        seen.add(vm.pc)
        vm.execute(ops[vm.pc])
    return vm.acc


if __name__ == "__main__":

    ops = parse(fileinput.input())

    print(run(ops))
