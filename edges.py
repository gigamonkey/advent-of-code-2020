#!/usr/bin/env python

from operator import mul
from functools import reduce
from collections import defaultdict
import fileinput
import re
from dataclasses import dataclass
from dataclasses import field
from functools import reduce
from itertools import product
from math import sqrt
from typing import Tuple

verbose = False

tile_pat = re.compile("^Tile (\d+):")

sides = ['top', 'bottom', 'left', 'right']


def flipper(fn):
    def flip(square):
        size = len(square)
        new_square = [[None] * size for _ in range(size)]
        for x, y in product(range(size), repeat=2):
            new_x, new_y = fn(size - 1, x, y)
            new_square[new_y][new_x] = square[y][x]
        return tuple(tuple(row) for row in new_square)

    return flip


flips = [
    flipper(fn)
    for fn in (
        lambda n, x, y: (x, (n - y)),
        lambda n, x, y: ((n - x), y),
        lambda n, x, y: (y, x),
        lambda n, x, y: ((n - y), (n - x)),
    )
]

transforms = [(), (0,), (1,), (2,), (3,), (0, 1), (0, 2), (0, 3)]


def transform(sq, ts):
    return reduce(lambda s, t: flips[t](s), ts, sq)


@dataclass(frozen=True)
class Tile:

    num: int
    bits: Tuple[Tuple[str]] = field(compare=False, repr=False)
    orientation: int = 0

    rows: Tuple[Tuple[str]] = field(compare=False, repr=False, init=False)

    def __post_init__(self):
        oriented = transform(self.bits, transforms[self.orientation])
        object.__setattr__(self, "rows", oriented)

    def orient(self, o):
        return self if o == self.orientation else Tile(self.num, self.bits, o)

    def all_orientations(self):
        return {self.orient(o) for o in range(8)}

    def all_edges(self):
        return {o.edge(side) for side in sides for o in self.all_orientations()}

    def edge(self, side):
        if side == "top":
            return "".join(self.rows[0])
        elif side == "bottom":
            return "".join(self.rows[-1])
        elif side == "left":
            return "".join(row[0] for row in self.rows)
        elif side == "right":
            return "".join(row[-1] for row in self.rows)
        else:
            raise Exception(f"Uknown side: {side}")


def parse(input):
    def g():
        for line in input:
            text = line[:-1]
            if m := tile_pat.match(text):
                num = int(m.group(1))
                rows = []
                for line in input:
                    if text := line[:-1]:
                        rows.append(tuple(text))
                    else:
                        break
                yield Tile(num, tuple(rows))

    return list(g())


if __name__ == "__main__":

    tiles = parse(fileinput.input())

    d = defaultdict(set)

    for tile in tiles:
        for e in tile.all_edges():
            d[e].add(tile)

    outer = {tile for edge, tiles in d.items() for tile in tiles if len(tiles) == 1}

    corners = {tile for tile in outer if sum(len(d[e]) == 1 for e in tile.all_edges()) == 4}

    print(reduce(mul, (tile.num for tile in corners)))
