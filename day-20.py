#!/usr/bin/env python

import fileinput
import re
from collections import defaultdict
from dataclasses import dataclass
from dataclasses import field
from functools import reduce
from itertools import product
from math import sqrt
from operator import mul
from typing import Tuple

verbose = False

sea_monster = [
    "                  #",
    "#    ##    ##    ###",
    " #  #  #  #  #  #",
]


tile_pat = re.compile("^Tile (\d+):")

sides = ["top", "bottom", "left", "right"]

opposite = {
    "top": "bottom",
    "bottom": "top",
    "left": "right",
    "right": "left",
}


def flipper(fn, diag):
    def flip(rect):
        height = len(rect)
        width = len(rect[0])
        new_width, new_height = (width, height) if not diag else (height, width)
        new_rect = [[None] * new_width for _ in range(new_height)]
        for x, y in product(range(width), range(height)):
            new_x, new_y = fn(width - 1, height - 1, x, y)
            new_rect[new_y][new_x] = rect[y][x]
        return tuple(tuple(row) for row in new_rect)

    return flip


flips = [
    flipper(fn, diag)
    for fn, diag in (
        # Vertical
        (lambda w, h, x, y: (x, (h - y)), False),
        # Horizontal
        (lambda w, h, x, y: ((w - x), y), False),
        # Diagonal 1
        (lambda w, h, x, y: (y, x), True),
        # Diagonal 2
        (lambda w, h, x, y: ((h - y), (w - x)), True),
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


def tiles_for_edges(tiles):
    """
    Map all the possible edges for all the tiles (in all orientations)
    to the base tiles that can have that edge.
    """
    d = defaultdict(set)
    for tile in tiles:
        for e in tile.all_edges():
            d[e].add(tile)
    return d


def categorized_tiles(tiles):

    d = tiles_for_edges(tiles)

    # For each edge, if there's only one tile with that edge, it must be an outer tile.
    outer = {tile for edge, tiles in d.items() for tile in tiles if len(tiles) == 1}

    # Corner tiles have four edges (two actually, times two
    # orientations) that aren't shared with any other tile.

    def is_corner(tile):
        return sum(len(d[e]) == 1 for e in tile.all_edges()) == 4

    corners = {tile for tile in outer if is_corner(tile)}

    return {"corners": corners, "outer": outer - corners, "inner": set(tiles) - outer}


def solve(tiles):

    size = round(sqrt(len(tiles)))

    d = tiles_for_edges(tiles)

    categorized = categorized_tiles(tiles)

    corners = categorized["corners"]

    image = [[None] * size for _ in range(size)]

    image[0][0] = list(corners)[0]

    def other(neighbor, direction):
        edge = neighbor.edge(opposite[direction])
        tiles = {t for t in d[edge] if t.num != neighbor.num}
        assert len(tiles) == 1, f"neighbor: {neighbor} tiles: {tiles}"
        for t in list(tiles)[0].all_orientations():
            if t.edge(direction) == edge:
                return t

    for y in range(size):
        for x in range(size):
            if x == 0:
                if y == 0:
                    image[y][x] = list(corners)[0]
                else:
                    image[y][x] = other(image[y - 1][x], "top")
            else:
                image[y][x] = other(image[y][x - 1], "left")

    return image


def combine(image):
    def g():
        for row in image:
            tile_height = len(row[0].rows)
            for y in range(1, tile_height - 1):
                yield tuple(c for tile in row for c in tile.rows[y][1:-1])

    return tuple(g())


def show(bits):
    for line in bits:
        print("".join(line))


def on_bits(image):
    return {
        (x, y) for y, row in enumerate(image) for x, c in enumerate(row) if c == "#"
    }


def find_monster(monster, image):
    image_bits = on_bits(image)
    monster_bits = on_bits(monster)

    all_monsters = set()

    found = 0

    for bx, by in product(range(len(image[0])), range(len(image))):
        translated = {(x + bx, y + by) for (x, y) in monster_bits}
        if (translated & image_bits) == translated:
            all_monsters |= translated
            found += 1

    roughness = len(image_bits - all_monsters)

    return (found, roughness)


if __name__ == "__main__":

    tiles = parse(fileinput.input())

    image = combine(solve(tiles))

    for t in transforms:
        x = transform(image, t)
        m, r = find_monster(sea_monster, x)
        if m > 0:
            print(f"{m} monsters; roughness = {r}")

    d = defaultdict(set)
    for tile in tiles:
        for e in tile.all_edges():
            d[e].add(tile)

    outer = {tile for edge, tiles in d.items() for tile in tiles if len(tiles) == 1}

    corners = {
        tile for tile in outer if sum(len(d[e]) == 1 for e in tile.all_edges()) == 4
    }

    if reduce(mul, (tile.num for tile in corners)) == 21599955909991:
        print("ok")
