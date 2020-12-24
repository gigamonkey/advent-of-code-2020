#!/usr/bin/env python

import fileinput
from collections import Counter


def parse(input):
    return [int(line[:-1]) for line in input]


def part_one(numbers):
    s = sorted(numbers + [0, max(numbers) + 3])
    c = Counter()
    for i in range(1, len(s)):
        c[s[i] - s[i - 1]] += 1
    return c[1] * c[3]


if __name__ == "__main__":

    numbers = parse(fileinput.input())

    print(part_one(numbers))
