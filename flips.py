#!/usr/bin/env python

from collections import defaultdict
from functools import reduce
from itertools import count
from itertools import product


def flip(square, fn):
    size = len(square)
    new_square = [[None] * size for _ in range(size)]
    for x, y in product(range(size), repeat=2):
        new_x, new_y = fn(size - 1, x, y)
        new_square[new_y][new_x] = square[y][x]
    return new_square

def flip_horizontal(square):
    return flip(square, lambda n, x, y: (x, (n - y)))

def flip_vertical(square):
    return flip(square, lambda n, x, y: ((n - x), y))

def flip_diagonal_1(square):
    return flip(square, lambda n, x, y: (y, x))

def flip_diagonal_2(square):
    return flip(square, lambda n, x, y: ((n - y), (n - x)))


def to_string(sq):
    return "".join("".join(row) for row in sq)


transformations = [
    flip_horizontal,
    flip_vertical,
    flip_diagonal_2,
    flip_diagonal_1,
]


def transform(sq, ts):
    return reduce(lambda s, t: transformations[t](s), ts, sq)


def transforms():
    r = range(4)
    for n in count(0):
        for p in product(r, repeat=n):
            yield p


if __name__ == "__main__":

    square = [["A", "B"], ["D", "C"]]

    results = defaultdict(set)


    for i, t in enumerate(transforms()):
        x = to_string(transform(square, t))
        results[x].add(t)
        if i == 100000:
            break


    print(len(results.keys()))
    for r, ts in results.items():
        print(f"{r}: {min(ts, key=lambda x: (len(x), x))}")
