#!/usr/bin/env python

# Rotations - 0, 90, 180, 270 degrees.
# Flips - horizontal, vertical, two diagonals (?)

import re
import fileinput

tile_pat = re.compile("^Tile (\d+):")

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
            tiles[num] = rows

    return tiles



if __name__ == "__main__":

    tiles = parse(fileinput.input())

    for num, tile in tiles.items():
        print(f"Tile {num}:")
        for row in tile:
            print(row)
        print()
