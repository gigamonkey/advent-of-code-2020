#!/usr/bin/env python

# Rotations - 0, 90, 180, 270 degrees.
# Flips - horizontal, vertical, two diagonals (?)

import fileinput
import re
from dataclasses import dataclass
from typing import List

tile_pat = re.compile("^Tile (\d+):")


@dataclass
class Tile:

    num: int
    rows: List[str]

    @property
    def top(self):
        return self.rows[0]

    @property
    def bottom(self):
        return self.rows[-1]

    @property
    def left(self):
        return "".join(row[0] for row in self.rows)

    @property
    def right(self):
        return "".join(row[-1] for row in self.rows)


def parse(input):
    tiles = {}

    for line in input:
        text = line[:-1]
        if m := tile_pat.match(text):
            num = int(m.group(1))
            rows = []
            for line in input:
                if text := line[:-1]:
                    rows.append(text)
                else:
                    break
            tiles[num] = Tile(num, rows)

    return tiles


if __name__ == "__main__":

    tiles = parse(fileinput.input())

    for tile in tiles.values():
        print(f"Tile {tile.num}:")
        for row in tile.rows:
            print(row)
        print()
        print(f"Top: {tile.top}")
        print(f"Bottom: {tile.bottom}")
        print(f"Left: {tile.left}")
        print(f"Right: {tile.right}")
        print()
