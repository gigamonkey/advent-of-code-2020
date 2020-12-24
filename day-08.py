#!/usr/bin/env python

import fileinput
import re
from dataclasses import dataclass
from dataclasses import field
from dataclasses import replace
from typing import FrozenSet
from typing import List
from typing import Optional

op = re.compile("(\w+) ([-+]\d+)")


@dataclass
class Op:
    code: str
    num: int


@dataclass
class VM:
    ops: List[Op]
    pc: int = 0
    acc: int = 0
    done: bool = False
    looped: bool = False
    patch: Optional[int] = None
    seen: FrozenSet[int] = field(default_factory=lambda: frozenset(set()))

    def execute(self):

        if self.pc in self.seen:
            self.done = True
            self.looped = True
            return

        if self.pc == len(self.ops):
            self.done = True
            return

        self.seen |= {self.pc}

        op = self.ops[self.pc]

        if self.patch == self.pc:
            self.execute_patched(op)
        else:
            if op.code == "acc":
                self.acc += op.num
                self.pc += 1
            elif op.code == "jmp":
                self.pc += op.num
            elif op.code == "nop":
                self.pc += 1

    def execute_patched(self, op):
        if op.code == "acc":
            raise Exception(f"Can't patch at acc pc: {self.pc}")
        elif op.code == "jmp":
            self.pc += 1
        elif op.code == "nop":
            self.pc += op.num

    def patched(self):
        return replace(self, patch=self.pc)


def parse(input):
    return [parse_op(line[:-1]) for line in input]


def parse_op(line):
    if m := op.fullmatch(line):
        return Op(m.group(1), int(m.group(2)))
    else:
        raise Exception(f"{line} doesn't match line pattern")


def run(vm):
    while not vm.done:
        vm.execute()
    return vm.acc, vm.looped


def find_patch(ops):
    vm = VM(ops)

    while not vm.looped:
        vm.execute()
        if ops[vm.pc].code in {"jmp", "nop"}:
            p = vm.patched()
            acc, looped = run(p)
            if not looped:
                return acc
    return None


if __name__ == "__main__":

    ops = parse(fileinput.input())

    # print(run(VM(ops)))
    print(find_patch(ops))
