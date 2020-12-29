#!/usr/bin/env python

import fileinput
import re
from collections import Counter

# e, se, sw, w, nw, and ne

pat = re.compile("(?:[ns][ew])|(?:[ew])")

directions = {
    "e": (1, 0),
    "w": (-1, 0),
    "se": (1 / 2, -1),
    "sw": (-1 / 2, -1),
    "ne": (1 / 2, 1),
    "nw": (-1 / 2, 1),
}


def parse(input):
    return [parse_moves(line[:-1]) for line in input]


def parse_moves(text):
    return pat.findall(text)


def eval(moves):
    x, y = 0, 0
    for m in moves:
        dx, dy = directions[m]
        x += dx
        y += dy
    return x, y


def flips(all_moves):
    c = Counter()
    for moves in all_moves:
        c[eval(moves)] += 1
    return c


def black(all_moves):
    c = flips(all_moves)
    return sum(v % 2 == 1 for v in c.values())


if __name__ == "__main__":

    instructions = parse(fileinput.input())

    print(black(instructions))
