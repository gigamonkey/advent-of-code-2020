#!/usr/bin/env python

import fileinput
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


def recursive(decks):
    def loop(decks, level=0):

        seen = set()

        while decks[0] and decks[1]:

            s = snapshot(decks)
            if s in seen:
                return [decks[0] + decks[1], []]
            else:
                seen.add(s)

            p1 = decks[0].pop(0)
            p2 = decks[1].pop(0)

            if p1 <= len(decks[0]) and p2 <= len(decks[1]):
                r = loop([decks[0][:p1], decks[1][:p2]], level + 1)

                if r[0] and not r[1]:
                    winner = 0
                elif not r[0] and r[1]:
                    winner = 1
                else:
                    print(f"Huh, loop returned an incomplete game: {r}")

            else:
                winner = 0 if p1 > p2 else 1

            decks[winner].extend((p1, p2) if winner == 0 else (p2, p1))

        return decks

    return loop(decks)


def snapshot(decks):
    return tuple(tuple(d) for d in decks)


def copy(decks):
    return [decks[0][:], decks[1][:]]


def score(decks):
    winner = decks[0] or decks[1]
    return reduce(add, ((i + 1) * card for i, card in enumerate(reversed(winner))))


if __name__ == "__main__":

    decks = parse(fileinput.input())

    print(score(play(copy(decks))))
    print(score(recursive(copy(decks))))
