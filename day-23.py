#!/usr/bin/env python

test = "389125467"
test_result = "67384529"

puzzle = "583976241"
part1_answer = "24987653"


def rotate_to_end(current, cups):
    i = cups.index(current)
    return cups[i + 1 :] + cups[: i + 1]


def dest(current, maximum, missing):
    d = current
    while True:
        d = ((d - 2) % maximum) + 1
        if d not in missing:
            return d


def step(current, cups):

    x = " ".join(f"({c})" if c == current else str(c) for c in cups)
    print(f"cups: {x}")
    s = rotate_to_end(current, cups)
    pickup = s[:3]
    print(f"pick up: {' '.join(str(c) for c in pickup)}")
    s = s[3:]
    d = dest(current, max(s), pickup)
    print(f"destination: {d}")
    print()
    return rotate_to_end(d, s) + pickup


def solve(start):
    cups = [int(c) for c in start]
    current = cups[0]
    for i in range(100):
        print(f"-- move {i + 1} --")
        cups = step(current, cups)
        current = cups[(cups.index(current) + 1) % len(cups)]
    return "".join(str(c) for c in rotate_to_end(1, cups)[:-1])


if __name__ == "__main__":

    assert solve(test) == test_result
    assert solve(puzzle) == part1_answer

    print("ok")
