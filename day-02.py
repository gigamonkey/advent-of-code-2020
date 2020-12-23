#!/usr/bin/env python

import fileinput
from dataclasses import dataclass

import re

pat = re.compile(r"^(\d+)-(\d+) (\w): (\w+)$")

@dataclass
class Line:
    min: int
    max: int
    char: str
    password: str

    def ok(self):
        return self.min <= sum(self.char == c for c in self.password) <= self.max



def parse_file(lines):
    for line in lines:
        if m := pat.match(line):
            yield Line(int(m.group(1)), int(m.group(2)), m.group(3), m.group(4))


if __name__ == "__main__":

    print(sum(line.ok() for line in parse_file(fileinput.input())))
