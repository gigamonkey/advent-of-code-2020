#!/usr/bin/env python

import fileinput
from itertools import combinations


def parse(input):
    return [int(line[:-1]) for line in input]


def check(numbers, i):
    n = numbers[i]
    for a, b in combinations(numbers[i - 5 : i], 2):
        if a + b == n:
            return True, (a, b)
    return False


def find_problem(numbers, prefix):
    for i in range(prefix, len(numbers)):
        if not check(numbers, i):
            return numbers[i]


if __name__ == "__main__":

    numbers = parse(fileinput.input())

    print(find_problem(numbers, 5))
