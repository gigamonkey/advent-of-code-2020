#!/usr/bin/env python

import fileinput

def parse(input):
    lines = list(input)
    return int(lines[0][:-1]), [int(n) for n in lines[1][:-1].split(",") if n != "x"]


if __name__ == "__main__":

    sched = parse(fileinput.input())

    print(sched)
