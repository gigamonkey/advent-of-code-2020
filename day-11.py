#!/usr/bin/env python

import fileinput

# If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.

# If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.

# Otherwise, the seat's state does not change.


directions = [(x, y) for x in (-1, 0, 1) for y in (-1, 0, 1) if x != 0 or y != 0]


def parse(input):
    return [list(line[:-1]) for line in input]


#
# Part 1
#


def visible_neighbors(grid, x, y):
    x_range = range(len(grid[0]))
    y_range = range(len(grid))
    return [grid[y][x] for x, y in neighbors(x, y, x_range, y_range)]


def neighbors(x, y, x_range, y_range):
    for d_x, d_y in directions:
        n_x = x + d_x
        n_y = y + d_y
        if n_x in x_range and n_y in y_range:
            yield (n_x, n_y)


#
# Part 2
#


def visible_in_all_directions(grid, x, y):
    return [in_direction(grid, x, y, d) for d in directions]


def in_direction(grid, x, y, d):
    x_range = range(len(grid[0]))
    y_range = range(len(grid))
    d_x, d_y = d
    while True:
        x += d_x
        y += d_y
        if x in x_range and y in y_range:
            value = grid[y][x]
            if value != ".":
                return value
        else:
            break

    return None


def rule(current, visible, too_crowded):
    if current == "L" and all(v != "#" for v in visible):
        return "#"
    elif current == "#" and sum(v == "#" for v in visible) >= too_crowded:
        return "L"
    else:
        return current


def next_grid(grid, visible_fn, too_crowded):
    x_range = range(len(grid[0]))
    y_range = range(len(grid))

    new_grid = [["."] * len(x_range) for _ in y_range]

    changes = False

    for j in y_range:
        for i in x_range:
            new_grid[j][i] = rule(grid[j][i], visible_fn(grid, i, j), too_crowded)
            changes |= grid[j][i] != new_grid[j][i]

    return new_grid, changes


def occupied(grid):
    return sum(sum(c == "#" for c in row) for row in grid)


def fix_point(grid, next_grid):
    changes = True
    while changes:
        grid, changes = next_grid(grid)
    return grid


def dump(grid):
    for row in grid:
        print("".join(row))
    print()


if __name__ == "__main__":

    grid = parse(fileinput.input())

    end = fix_point(grid, lambda grid: next_grid(grid, visible_in_all_directions, 5))

    print(f"{occupied(end)} occpupied seats.")
