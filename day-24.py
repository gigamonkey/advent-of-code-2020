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


def neighbors(tile):
    x, y = tile
    return [(x + dx, y + dy) for dx, dy in directions.values()]


def start(instructions):
    c = flips(instructions)
    return {tile for tile, v in c.items() if v % 2 == 1}


def step(black):
    to_consider = {n for b in black for n in neighbors(b)}
    return {tile for tile in to_consider if is_black_next(tile, black)}


def is_black_next(tile, black):
    black_neighbors = sum(n in black for n in neighbors(tile))
    return black_neighbors in {1, 2} if tile in black else black_neighbors == 2


if __name__ == "__main__":

    instructions = parse(fileinput.input())

    state = start(instructions)

    for i in range(101):
        if i < 10 or i % 10 == 0:
            print(f"Day {i}: {len(state)}")
        if i == 10:
            print()
        state = step(state)
