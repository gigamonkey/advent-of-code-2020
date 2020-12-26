#!/usr/bin/env python

# Rotations - 0, 90, 180, 270 degrees.
# Flips - horizontal, vertical, two diagonals (?)

# Search plan:
#
# - Make empty grid for the square.
#
# - Initially every position can hold any tile in any orientation.
#
# - Pick a starting position (say top left) and start searching
#   through the possible oriented tiles.
#
# - On each choice, eliminate from neighboring positions any oriented
#   tiles whose edges don't match. If any position gets down to one
#   possibility, propagate the consequences to its neighbors,
#   recursively.
#
# - Keep searching from the position with the fewest possibilites.
#
# - Backtrack if any position has its last possible tile eliminated.

import fileinput
import re
from dataclasses import dataclass
from dataclasses import replace
from functools import reduce
from itertools import product
from math import sqrt
from typing import Tuple

tile_pat = re.compile("^Tile (\d+):")


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


neighboring = {
    "top": (0, -1),
    "bottom": (0, 1),
    "left": (-1, 0),
    "right": (1, 0),
}

opposites = {
    "top": "bottom",
    "bottom": "top",
    "left": "right",
    "right": "left",
}


def neighbors(state, pos):
    x, y = pos

    for side, (dx, dy) in neighboring.items():
        n = (x + dx, y + dy)
        if n in state:
            yield n, side


@dataclass(frozen=True)
class Tile:

    num: int
    rows: Tuple[Tuple[str]]
    orientation: int = 0

    def orient(self, o):
        if o == self.orientation:
            return self
        else:
            return replace(
                self, rows=transform(self.rows, transforms[o]), orientation=o
            )

    def all_orientations(self):
        return {self.orient(o) for o in range(8)}

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


def search(state):
    if state is None:
        return None

    elif is_solved(state):
        return {k: list(v)[0] for k, v in state.items()}

    else:
        p = next_position(state)
        tiles = frozenset(state[p])
        for tile in tiles:
            if solution := search(assign(dict(state), p, tile)):
                return solution


def is_solved(state):
    return all(len(p) == 1 for p in state.values())


def next_position(state):
    return min((len(v), p) for p, v in state.items() if len(v) > 1)[1]


def assign(state, pos, tile):
    print(f"Assigning {tile.num} {tile.orientation} to {pos}")
    others = frozenset(t for t in state[pos] if t != tile)
    if others:
        return eliminate(state, pos, others)
    else:
        print(f"Already assigned.")
        return state


def eliminate(state, pos, tiles):

    # Bail quickly if this won't change anyhing.
    if not state[pos] & tiles:
        return state

    print(f"Eliminating {len(tiles)} tiles from {pos}")

    # Otherise we're actually removing tiles from this position. As a
    # consequence we will need to check our neighbors after we're done.
    state[pos] = state[pos] - tiles

    if not state[pos]:
        # Hit a dead end
        print(f"No tiles left in {pos}")
        return None

    else:
        unique_left = {t.num for t in state[pos]}

        if len(unique_left) == 1:

            print(f"Only one unique tile {unique_left} left in {pos}")

            # If this position is now down to one tile (by number) we
            # need to eliminate that tile from all other positions.
            to_remove = list(state[pos])[0].all_orientations()
            for p in state.keys():
                if p != pos:
                    if (state := eliminate(state, p, to_remove)) is None:
                        return None

        # Now we can check our neighbors for tiles that are no longer
        # possible given the changes to this position.
        for n, side in neighbors(state, pos):
            edges = {t.edge(side) for t in state[pos]}
            to_remove = {t for t in state[n] if t.edge(opposites[side]) not in edges}
            print(
                f"Eliminating {len(to_remove)} tiles with no common edge from neighbor {n} of {pos}"
            )
            if (state := eliminate(state, n, to_remove)) is None:
                return None

        return state


def show_tiles(tiles):
    for tile in tiles:
        print(f"Tile {tile.num}; orientations: {tile.orientation}:")
        for row in tile.rows:
            print("".join(row))
        print()


if __name__ == "__main__":

    tiles = parse(fileinput.input())

    all_orientations = {
        oriented for tile in tiles for oriented in tile.all_orientations()
    }

    # print(len(all_orientations))

    # show_tiles(all_orientations)

    image_size = round(sqrt(len(tiles)))

    state = {
        p: frozenset(all_orientations) for p in product(range(image_size), repeat=2)
    }

    print(len(state))

    solution = search(state)

    for k, v in solution.items():
        print(f"{k}: {v.num}")
