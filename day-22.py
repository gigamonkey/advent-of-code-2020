#!/usr/bin/env python

from functools import reduce
from operator import add


def parse(input):
    decks = [[], []]

    for line in input:
        text = line[:-1]
        if text == "Player 1:":
            p = 0
        elif text == "Player 2:":
            p = 1
        elif text:
            decks[p].append(int(text))

    return decks


def play(decks):

    while decks[0] and decks[1]:
        p1 = decks[0].pop(0)
        p2 = decks[1].pop(0)
        decks[p2 > p1].extend(sorted([p1, p2], reverse=True))

    return decks


def snapshot(decks):
    return tuple(tuple(d) for d in decks)


def copy(decks):
    return [decks[0][:], decks[1][:]]


verbose_loop = False

max_count = 2750


def recursive(decks):

    memo = dict()

    def loop(decks, level=0):
        global verbose_loop

        seen = set()

        if 10 < level:
            print(f"{[level]} {len(seen)}")

        entry_snapshot = snapshot(decks)
        if entry_snapshot in memo:
            return memo[entry_snapshot]

        # verbose_loop = True

        count = 0

        while decks[0] and decks[1]:

            count += 1

            if count > max_count:
                print(f"{count}: ({len(decks[0])} vs {len(decks[1])}) {decks}")

            if verbose_loop:
                print(f"[{level}]: In loop: {len(decks[0])}, {len(decks[1])}")

            s = snapshot(decks)
            if s in seen:
                # if count > max_count:
                # print(f"{count}: Player 1 wins by loop {decks}")
                memo[entry_snapshot] = [decks[0] + decks[1], []]
                return memo[entry_snapshot]
            else:
                seen.add(s)

            p1 = decks[0].pop(0)
            p2 = decks[1].pop(0)

            # if verbose_loop: print(f"[{level}]: Deciding kind of game: {len(decks[0])}, {len(decks[1])}")
            if p1 <= len(decks[0]) and p2 <= len(decks[1]):
                if verbose_loop or count > max_count:
                    print(f"[{level}]: Recursive game")

                r = loop(copy(decks), level + 1)

                # assert set(r[0]) | set(r[1]) == set(decks[0]) | set(decks[1])

                if verbose_loop:
                    print(f"[{level}]: Back from recursive call {decks}")

                if r[0] and not r[1]:
                    winner = 0
                elif not r[0] and r[1]:
                    winner = 1
                else:
                    print(f"Huh, loop returned an incomplete game: {r}")

                if winner == 0:
                    decks[0].append(p1)
                    decks[0].append(p2)
                else:
                    decks[1].append(p2)
                    decks[1].append(p1)

            else:
                if verbose_loop or count > max_count:
                    print(f"[{level}]: Regular game")
                decks[p2 > p1].extend(sorted([p1, p2], reverse=True))

            if verbose_loop:
                print(f"[{level}] End of loop: {len(decks[0])}, {len(decks[1])}")

        if verbose_loop:
            print(f"[{level}] Out of loop: {len(decks[0])}, {len(decks[1])}")
        memo[entry_snapshot] = decks
        return memo[entry_snapshot]

    r = loop(decks)
    print(f"{len(memo):,d} total unique decks.")
    return r


def score(decks):
    winner = decks[0] or decks[1]
    return reduce(add, ((i + 1) * card for i, card in enumerate(reversed(winner))))


if __name__ == "__main__":

    # decks = parse(fileinput.input())

    # x = 19
    # decks[0] = decks[0][:x]
    # decks[1] = decks[1][:x]

    # swaps = [-2]
    # for s in swaps:
    #    decks[0][s], decks[1][s] = decks[1][s], decks[0][s]

    import sys

    per = int(sys.argv[1])

    deck = list(range(1, (per * 2) + 1))
    import random

    random.shuffle(deck)

    decks = [deck[:per], deck[per:]]

    print(score(play(copy(decks))))
    print(score(recursive(copy(decks))))
