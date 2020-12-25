#!/usr/bin/env python

import fileinput
from itertools import product

d = (-1, 0, 1)

cube = tuple(product(d, d, d))


def parse(input):
    on = set()
    for y, row in enumerate(input):
        for x, c in enumerate(row):
            if c == "#":
                on.add((x, y, 0))
    return on


def cube_at(coord):
    return {tuple(c + d for c, d in zip(coord, n)) for n in cube}


def step(state):
    to_consider = {p for on in state for p in cube_at(on)}
    return {p for p in to_consider if active_in_next(p, state)}


def active_in_next(coord, state):
    on = len(cube_at(coord) & state)
    return on == 3 or (coord in state and on == 4)


def dump(state):
    xs = [p[0] for p in state]
    ys = [p[1] for p in state]
    zs = [p[2] for p in state]

    for z in range(min(zs), max(zs) + 1):
        print(f"Z = {z}; {len(state)} active.")
        for y in range(min(ys), max(ys) + 1):
            for x in range(min(xs), max(xs) + 1):
                c = (x, y, z)
                print("#" if c in state else ".", end="")
            print()
        print()


if __name__ == "__main__":

    initial = parse(fileinput.input())

    print(initial)

    c = 0
    print(f"After {c} cycle(s)")
    state = initial
    dump(state)

    for i in range(6):
        c += 1
        state = step(state)
        print(f"After {c} cycle(s)")
        dump(state)

    print(len(state))
