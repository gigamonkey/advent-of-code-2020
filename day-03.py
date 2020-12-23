#!/usr/bin/env python

import fileinput


def count_trees(grid, right=3, down=1):
    width = len(grid[0])
    x = 0
    count = 0
    for row in grid[1:]:
        x += 3
        if row[x % width] == "#":
            count += 1
    return count


if __name__ == "__main__":

    print(count_trees([line[:-1] for line in fileinput.input()]))
