#!/usr/bin/env python

import fileinput


def parse(input):
    return list(stanzas(input))


def stanzas(input):
    buf = ""
    for line in input:
        if line[:-1]:
            buf += line[:-1]
        else:
            yield buf
            buf = ""
    if buf:
        yield buf


def total(answers):
    return sum(len(set(x)) for x in answers)


if __name__ == "__main__":

    answers = parse(fileinput.input())

    print(total(answers))
