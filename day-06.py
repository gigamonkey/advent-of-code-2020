#!/usr/bin/env python

import fileinput
from functools import reduce


def parse(input):
    return list(stanzas(input))


def stanzas(input):
    buf = []
    for line in input:
        if line[:-1]:
            buf.append(set(line[:-1]))
        else:
            yield buf
            buf = []
    if buf:
        yield buf


def anyone(x):
    return len(reduce(lambda a, b: a | b, x))


def everyone(x):
    return len(reduce(lambda a, b: a & b, x))


def total(answers, fn=anyone):
    return sum(fn(x) for x in answers)


if __name__ == "__main__":

    answers = parse(fileinput.input())

    print(total(answers))
    print(total(answers, everyone))
