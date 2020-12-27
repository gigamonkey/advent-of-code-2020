#!/usr/bin/env python

from functools import reduce
from operator import add
import fileinput

def parse(input):
    decks = [[],[]]

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

def score(decks):
    winner = decks[0] or decks[1]
    return reduce(add, ((i + 1) * card for i, card in enumerate(reversed(winner))))


if __name__ == "__main__":

    decks = parse(fileinput.input())

    print(score(play(decks)))
