#!/usr/bin/env python

from dataclasses import dataclass
from typing import Optional

test = "389125467"
short_test_result = "92658374"
test_result = "67384529"
test_part_2_result = 149245887792

puzzle = "583976241"
part1_answer = "24987653"


@dataclass
class Link:

    value: int
    next: Optional["Link"] = None

    def take(self, n):
        buf = []
        x = self
        for _ in range(n):
            buf.append(x.value)
            x = x.next
        return buf

    def end(self):
        n = self
        while n.next is not None:
            n = n.next
        return n


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
    # print(f"cups: {x}")
    s = rotate_to_end(current, cups)
    pickup = s[:3]
    # print(f"pick up: {' '.join(str(c) for c in pickup)}")
    s = s[3:]
    d = dest(current, max(s), pickup)
    # print(f"destination: {d}")
    # print()
    return rotate_to_end(d, s) + pickup


def solve(start):
    cups = [int(c) for c in start]
    current = cups[0]
    for i in range(100):
        # print(f"-- move {i + 1} --")
        cups = step(current, cups)
        current = cups[(cups.index(current) + 1) % len(cups)]
    return "".join(str(c) for c in rotate_to_end(1, cups)[:-1])


#
# Linked list version
#


def solve_2(start, steps, maximum=9):
    circle = make_circle(start, maximum)
    index = index_links(circle, maximum)

    current = circle
    for i in range(steps):

        if i % 10_000 == 0:
            print(".", end="", flush=True)
        if i % 1_000_000 == 0:
            print("", flush=True)

        # print(f"-- move {i + 1} --")
        # print(f"cups: {cups(current)}")
        current = step_2(current, index, maximum)
    print()
    return index[1]


def part_1_solution(one):
    return "".join(str(v) for v in one.next.take(8))


def part_2_solution(one):
    return one.next.value * one.next.next.value


def cups(current):
    values = current.take(9)
    return " ".join(str(v) if v != current.value else f"({v})" for v in values)


def step_2(current, index, maximum):

    pickup_tail = current
    pickup_values = set()

    for _ in range(3):
        pickup_tail = pickup_tail.next
        pickup_values.add(pickup_tail.value)

    # Splice out the three picked up cups
    pickup_head = current.next
    current.next = pickup_tail.next

    dest_index = dest(current.value, maximum, pickup_values)
    # print(f"pick up: {' '.join(str(c) for c in pickup_head.take(3))}")
    # print(f"dest: {dest_index}")

    d = index[dest_index]
    insert_point = d.next
    d.next = pickup_head
    pickup_tail.next = insert_point
    return current.next


def check_invariants(current):
    in_circle = set(current.take(1_000_000))

    assert in_circle == set(range(1, 1_000_001)), f"{len(in_circle)}"


def make_circle(start, maximum):
    "Make the circle of Links."
    if maximum > 9:
        head, tail = to_links(range(10, maximum + 1))
        head, _ = to_links([int(c) for c in start], head)
    else:
        head, tail = to_links([int(c) for c in start])

    tail.next = head
    return head


def index_links(head, maximum):
    "Make an index from the value of the Link to the Link object."
    index = [None] * (maximum + 1)
    link = head
    for i in range(1, maximum + 1):
        index[link.value] = link
        link = link.next
    return index


def to_links(xs, head=None):
    tail = None
    for x in reversed(xs):
        head = Link(x, head)
        if tail is None:
            tail = head
    return head, tail


if __name__ == "__main__":

    check = False

    if check:
        assert solve(test) == test_result
        assert solve(puzzle) == part1_answer
        assert part_1_solution(solve_2(test, 10)) == short_test_result
        assert part_1_solution(solve_2(test, 100)) == test_result
        assert part_1_solution(solve_2(puzzle, 100)) == part1_answer
        assert (
            part_2_solution(solve_2(test, 10_000_000, 1_000_000)) == test_part_2_result
        )
        print("ok")

    print(part_2_solution(solve_2(puzzle, 10_000_000, 1_000_000)))
