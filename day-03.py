#!/usr/bin/env python

import fileinput
from functools import reduce
from operator import mul


def parse(input):
    return [line[:-1] for line in input]


def count_trees(grid, right=3, down=1):
    width = len(grid[0])
    x = 0
    count = 0
    for row in grid[0::down][1:]:
        x += right
        if row[x % width] == "#":
            count += 1
    return count


def part2(grid):
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    return reduce(mul, [count_trees(grid, *s) for s in slopes])


if __name__ == "__main__":

    grid = parse(fileinput.input())
    print(count_trees(grid))

    print(part2(grid))
