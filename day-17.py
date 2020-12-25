#!/usr/bin/env python

import fileinput
from itertools import product

d = (-1, 0, 1)

dims = {dim: tuple(product(d, repeat=dim)) for dim in (3, 4)}


def parse(input, dims=3):
    on = set()
    for y, row in enumerate(input):
        for x, c in enumerate(row):
            if c == "#":
                on.add((x, y) + (0,) * (dims - 2))
    return on


def at(coord):
    return {tuple(c + d for c, d in zip(coord, n)) for n in dims[len(coord)]}


def step(state):
    to_consider = {p for on in state for p in at(on)}
    return {p for p in to_consider if active_in_next(p, state)}


def active_in_next(coord, state):
    on = len(at(coord) & state)
    return on == 3 or (coord in state and on == 4)


def dump(state):
    # Only works for 3d
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

    initial = parse(fileinput.input(), dims=4)

    c = 0
    state = initial

    for i in range(6):
        c += 1
        state = step(state)

    print(len(state))
