#!/usr/bin/env python

import fileinput
from dataclasses import dataclass

# North, East, South, West
directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]


@dataclass
class Ship:
    direction: int = 1
    x: int = 0
    y: int = 0

    def execute(self, code, arg):
        if code == "N":
            self.y += arg
        elif code == "E":
            self.x += arg
        elif code == "S":
            self.y -= arg
        elif code == "W":
            self.x -= arg
        elif code == "F":
            dx, dy = directions[self.direction]
            self.x += arg * dx
            self.y += arg * dy
        elif code == "L":
            turn = arg // 90
            self.direction = (self.direction - turn) % 4
        elif code == "R":
            turn = arg // 90
            self.direction = (self.direction + turn) % 4


def parse(input):
    return [(line[0], int(line[1:-1])) for line in input]


if __name__ == "__main__":

    program = parse(fileinput.input())

    s = Ship()

    for code, arg in program:
        s.execute(code, arg)

    print(abs(s.x) + abs(s.y))
