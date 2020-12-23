#!/usr/bin/env python

import fileinput


def parse(input):
    return list(stanzas(input))


def stanzas(input):
    buf = []
    for line in input:
        if line[:-1]:
            buf += line[:-1].split(" ")
        else:
            yield to_dict(buf)
            buf = []
    if buf:
        yield to_dict(buf)


def to_dict(x):
    return dict(p.split(":") for p in x)


if __name__ == "__main__":

    x = parse(fileinput.input())
    print(x)
