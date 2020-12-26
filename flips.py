#!/usr/bin/env python

from collections import defaultdict
from functools import reduce
from itertools import count
from itertools import product





def flip_horizontal(sq):
    return list(reversed(square))

def flip_vertical(sq):
    return [list(reversed(row)) for row in sq]


def flip_diagonal_1(sq):
    return [[sq[1][1], sq[0][1]], [sq[1][0], sq[0][0]]]


def flip_diagonal_2(sq):
    return [[sq[0][0], sq[1][0]], [sq[0][1], sq[1][1]]]


def transform(square, fn):
    size = len(square)
    new_square = [[None] * size for _ in range(size)]
    for x, y in product(range(n), repeat=2):
        new_x, new_y = fn(size - 1, x, y)
        new_square[new_y][new_x] = square[y][x]
    return new_square

def new_flip_horizontal(square):
    return transform(square, lambda n, x, y: ((n - y), x))

def new_flip_vertical(square):
    return transform(square, lambda n, x, y: (y, (n - x)))

def new_flip_diagonal_1(square):
    return transform(square, lambda n, x, y: (y, x))

def new_flip_diagonal_2(square):
    return transform(square, lambda n, x, y: ((n - y), (n - x)))



def to_string(sq):
    return "".join("".join(row) for row in sq)


transformations = [
    flip_horizontal,
    flip_vertical,
    flip_diagonal_1,
    flip_diagonal_2,
]

new_transformations = [
    new_flip_horizontal,
    new_flip_vertical,
    new_flip_diagonal_1,
    new_flip_diagonal_2,
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
