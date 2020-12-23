#!/usr/bin/env python

import fileinput
import re
from dataclasses import dataclass

op = re.compile("(\w+) ([-+]\d+)")


@dataclass
class Op:
    code: str
    num: int


def parse(input):
    return [parse_op(line[:-1]) for line in input]


def parse_op(line):
    if m := op.fullmatch(line):
        return Op(m.group(1), int(m.group(2)))
    else:
        raise Exception(f"{line} doesn't match line pattern")


if __name__ == "__main__":

    instructions = parse(fileinput.input())

    print(instructions)
