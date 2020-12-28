#!/usr/bin/env python

import fileinput
from functools import reduce
from operator import add

verbose_recursive = False

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


def recursive(decks):

    seen = set()

    i = 0

    while decks[0] and decks[1]:

        s = snapshot(decks)
        if s in seen:
            #print(f"Infinite loop: {decks}")
            decks[0] = decks[0] + decks[1]
            decks[1] = []
            break
        else:
            seen.add(s)

        p1 = decks[0].pop(0)
        p2 = decks[1].pop(0)
        i += 1

        if p1 <= len(decks[0]) and p2 <= len(decks[1]):
            mp1 = max(decks[0])
            mp2 = max(decks[1])
            winner = 0 if max(decks[0]) > max(decks[1]) else 1
            if verbose_recursive:
                print(f"FAST: recursive game {i} 0: {p1} vs 1: {p2} ({len(decks[0])} and {len(decks[1])}; maxes {mp1} and {mp2}) winner is {winner}: {decks}")
        else:
            winner = 0 if p1 > p2 else 1
            # print(f"Normal game 0: {p1} vs 1: {p2} winner is {winner}")

        if winner == 0:
            order = [p1, p2]
        else:
            order = [p2, p1]

        decks[winner].extend(order)
        #print(f"Adding cards {order} to deck {winner}: {decks}")

    return decks


def old_recursive(decks):

    memo = dict()

    def loop(decks, level=0):

        seen = set()

        if 10 < level:
            print(f"{[level]} {len(seen)}")

        entry_snapshot = snapshot(decks)
        if entry_snapshot in memo:
            return memo[entry_snapshot]

        count = 0

        i = 0

        while decks[0] and decks[1]:

            count += 1

            s = snapshot(decks)
            if s in seen:
                memo[entry_snapshot] = [decks[0] + decks[1], []]
                return memo[entry_snapshot]
            else:
                seen.add(s)

            p1 = decks[0].pop(0)
            p2 = decks[1].pop(0)
            i += 1

            if p1 <= len(decks[0]) and p2 <= len(decks[1]):

                r_deck = [decks[0][:p1], decks[1][:p2]]

                r = loop(r_deck, level + 1)

                if r[0] and not r[1]:
                    winner = 0
                elif not r[0] and r[1]:
                    winner = 1
                else:
                    print(f"Huh, loop returned an incomplete game: {r}")

                if verbose_recursive and level == 0:
                    print(f"SLOW: recursive game {i} 0: {p1} vs 1: {p2} ({len(decks[0])} and {len(decks[1])}) winner is {winner}: {decks}")

                if winner == 0:
                    decks[0].append(p1)
                    decks[0].append(p2)
                else:
                    decks[1].append(p2)
                    decks[1].append(p1)

            else:
                decks[p2 > p1].extend(sorted([p1, p2], reverse=True))


        memo[entry_snapshot] = decks
        return memo[entry_snapshot]

    return loop(decks)

def copy(decks):
    return [decks[0][:], decks[1][:]]


def score(decks):
    winner = decks[0] or decks[1]
    #print(f"Scoring winner {winner}")
    return reduce(add, ((i + 1) * card for i, card in enumerate(reversed(winner))))


if __name__ == "__main__":

    decks = parse(fileinput.input())

    import sys
    import random

    #per = int(sys.argv[1])

    # print(score(play(copy(decks))))
    print(score(old_recursive(copy(decks))))

    def deal(per):
        deck = list(range(1, (per * 2) + 1))
        random.shuffle(deck)

        decks = [deck[:per], deck[per:]]

        if (per * 2) in decks[1]:
            return [decks[1],decks[0]]
        else:
            return decks

    def compare(decks):
        fast = recursive(copy(decks))
        slow = old_recursive(copy(decks))

        fast_score = score(fast)
        slow_score = score(slow)

        if fast_score != slow_score:
            print(decks)
            print(f"Fast: {fast}")
            print(f"Slow: {slow}")
            print()


    # decks = [[3, 14, 19, 18, 10, 6, 2, 15, 13, 8], [20, 7, 9, 12, 1, 17, 5, 4, 16, 11]]

    # Infinite loop
    # decks = [[17, 14, 15, 6, 13, 10, 19, 7, 12, 1], [20, 18, 16, 11, 4, 2, 9, 8]]

    #for i in range(1000):
    #    compare(deal(per))
