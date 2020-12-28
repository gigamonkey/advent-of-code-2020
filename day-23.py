#!/usr/bin/env python

test = "389125467"
test_result = "67384529"

puzzle = "583976241"

def rotate_to_end(current, cups):
    i = cups.index(current)
    return cups[i + 1 :] + cups[: i + 1]


def dest(current, cups):
    d = current - 1
    while d not in cups:
        d -= 1
        d %= max(cups) + 1
    return d


def step(current, cups):

    x = " ".join(f"({c})" if c == current else str(c) for c in cups)
    print(f"cups: {x}")
    s = rotate_to_end(current, cups)
    pickup = s[:3]
    print(f"pick up: {' '.join(str(c) for c in pickup)}")
    s = s[3:]
    d = dest(current, s)
    print(f"destination: {d}")
    print()
    return rotate_to_end(d, s) + pickup


def solve(cups):
    current = cups[0]
    for i in range(100):
        print(f"-- move {i + 1} --")
        cups = step(current, cups)
        current = cups[(cups.index(current) + 1) % len(cups)]
    return "".join(str(c) for c in rotate_to_end(1, cups)[:-1])


if __name__ == "__main__":

    start = [int(c) for c in puzzle]

    print(start)
    print()
    print(solve(start))
    print()
    # print('92658374')
    # print(test_result)
