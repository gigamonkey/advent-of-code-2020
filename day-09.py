#!/usr/bin/env python

import fileinput
from itertools import combinations


def parse(input):
    return [int(line[:-1]) for line in input]


def check(numbers, i, prefix):
    n = numbers[i]
    for a, b in combinations(numbers[i - prefix : i], 2):
        if a + b == n:
            return True, (a, b)
    return False


def find_problem(numbers, prefix):
    for i in range(prefix, len(numbers)):
        if not check(numbers, i, prefix):
            return numbers[i]


def find_range(numbers, target):

    start = 0
    end = 0
    total = 0

    while end < len(numbers):
        if total < target:
            total += numbers[end]
            end += 1
        elif total > target:
            total -= numbers[start]
            start += 1
        else:
            return start, end


if __name__ == "__main__":

    numbers = parse(fileinput.input())

    odd = find_problem(numbers, 25)

    a, b = find_range(numbers, odd)

    r = numbers[a:b]

    print(min(r) + max(r))
