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


def answer(g, turn=2020):
    return next(islice(g, turn - 1, turn))


if __name__ == "__main__":

    start = [int(x) for x in sys.argv[1].split(",")]
    turn = int(sys.argv[2])
    print(answer(game(start), turn))
