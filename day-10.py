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


def part_two(numbers):
    def g(s):
        if len(s) == 1:
            yield s
        else:
            first, *rest = s
            for i in range(len(rest)):
                if rest[i] - first <= 3:
                    for tail in g(rest[i:]):
                        yield [first, *tail]

    s = [0] + sorted(numbers) + [max(numbers) + 3]
    return g(s)


def count(g):
    c = 0
    for _ in g:
        c += 1
    return c


if __name__ == "__main__":

    numbers = parse(fileinput.input())

    print(count(part_two(numbers)))
