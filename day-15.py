#!/usr/bin/env python

import sys
from itertools import islice


def game(start):
    seen = dict()

    turn = 1
    for number in start[:-1]:
        seen[number] = turn
        turn += 1
        yield number

    last = start[-1]
    yield last

    while True:
        if last in seen:
            prev = seen[last]
            seen[last] = turn
            last = turn - prev
            yield last
        else:
            seen[last] = turn
            last = 0
            yield last
        turn += 1


def answer(g):
    return next(islice(g, 2019, 2020))


if __name__ == "__main__":

    start = [int(x) for x in sys.argv[1].split(",")]
    print(answer(game(start)))
