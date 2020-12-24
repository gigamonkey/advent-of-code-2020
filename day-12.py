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


@dataclass
class Waypoint:
    north: int = 1
    east: int = 10

    def execute(self, code, arg):
        if code == "N":
            self.north += arg
        elif code == "E":
            self.east += arg
        elif code == "S":
            self.north -= arg
        elif code == "W":
            self.east -= arg
        elif code == "L":  # Counter clockwise:
            for _ in range(arg // 90):
                tmp = self.east
                self.east = -self.north
                self.north = tmp
        elif code == "R":  # Clockwise
            for _ in range(arg // 90):
                tmp = self.east
                self.east = self.north
                self.north = -tmp


@dataclass
class WaypointShip:
    waypoint: Waypoint
    x: int = 0
    y: int = 0

    def execute(self, code, arg):
        if code in "NSEWLR":
            self.waypoint.execute(code, arg)
        elif code == "F":
            self.x += self.waypoint.north * arg
            self.y += self.waypoint.east * arg


def parse(input):
    return [(line[0], int(line[1:-1])) for line in input]


if __name__ == "__main__":

    program = parse(fileinput.input())

    s = WaypointShip(Waypoint(1, 10))

    for code, arg in program:
        s.execute(code, arg)

    print(abs(s.x) + abs(s.y))
