#!/usr/bin/env python

import fileinput

# If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.

# If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.

# Otherwise, the seat's state does not change.


def parse(input):
    return [list(line[:-1]) for line in input]


def neighbors(i, j, x_range, y_range):
    d = (-1, 0, 1)
    for x in d:
        for y in d:
            if x != 0 or y != 0:
                n_i = i + x
                n_j = j + y
                if n_i in x_range and n_j in y_range:
                    yield (n_i, n_j)


def new_value(grid, current, neighbors):
    if current == "L" and all(grid[j][i] in {"L", "."} for i, j in neighbors):
        return "#"
    elif current == "#" and sum(grid[j][i] == "#" for i, j in neighbors) >= 4:
        return "L"
    else:
        return current


def next_grid(grid):
    x_range = range(len(grid[0]))
    y_range = range(len(grid))

    new_grid = [["."] * len(x_range) for _ in y_range]

    changes = False

    for j in y_range:
        for i in x_range:
            n = list(neighbors(i, j, x_range, y_range))
            current = grid[j][i]
            new = new_value(grid, current, n)
            new_grid[j][i] = new
            changes = changes or (current != new)

    return new_grid, changes


def occupied(grid):
    return sum(sum(c == "#" for c in row) for row in grid)


def fix_point(grid):
    changes = True
    while changes:
        grid, changes = next_grid(grid)
    return grid


if __name__ == "__main__":

    grid = parse(fileinput.input())

    end = fix_point(grid)

    print(f"{occupied(end)} occpupied seats.")
