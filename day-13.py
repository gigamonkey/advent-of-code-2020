#!/usr/bin/env python

import fileinput


def parse(input):
    lines = list(input)
    return int(lines[0][:-1]), [int(n) for n in lines[1][:-1].split(",") if n != "x"]


def shortest_wait(start, buses):
    return min((b - (start % b), b) for b in buses)


if __name__ == "__main__":

    start, buses = parse(fileinput.input())

    wait, bus = shortest_wait(start, buses)

    # print((wait, bus))
    print(wait * bus)
