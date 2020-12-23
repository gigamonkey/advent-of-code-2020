#!/usr/bin/env python

import fileinput
import re
from dataclasses import dataclass

pat = re.compile(r"^(\d+)-(\d+) (\w): (\w+)$")


def xor(a, b):
    return (not a and b) or (a and not b)


@dataclass
class Line:
    min: int
    max: int
    char: str
    password: str

    def ok(self):
        return self.min <= sum(self.char == c for c in self.password) <= self.max

    def ok2(self):
        return xor(
            self.char == self.password[self.min - 1],
            self.char == self.password[self.max - 1],
        )


def parse_file(lines):
    for line in lines:
        if m := pat.match(line):
            yield Line(int(m.group(1)), int(m.group(2)), m.group(3), m.group(4))
        else:
            print(f"No match: {line}")


if __name__ == "__main__":

    # print(sum(line.ok() for line in parse_file(fileinput.input())))
    print(sum(line.ok2() for line in parse_file(fileinput.input())))
