#!/usr/bin/env python
import fileinput
from dataclasses import dataclass


@dataclass
class BoardingPass:
    row: int
    col: int
    seat: int


def parse(input):
    return [boarding_pass(line[:-1]) for line in input]


def boarding_pass(line):
    row = int(line[:7].replace("F", "0").replace("B", "1"), 2)
    col = int(line[7:].replace("R", "1").replace("L", "0"), 2)
    return BoardingPass(row, col, row * 8 + col)


if __name__ == "__main__":

    passes = parse(fileinput.input())

    print(max(p.seat for p in passes))
