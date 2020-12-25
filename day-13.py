#!/usr/bin/env python

import fileinput
from functools import reduce


def parse(input):
    lines = list(input)
    return int(lines[0][:-1]), [int(n) for n in lines[1][:-1].split(",") if n != "x"]


def shortest_wait(start, buses):
    return min((b - (start % b), b) for b in buses)


def parse2(input):
    lines = list(input)
    return [(i, int(n)) for i, n in enumerate(lines[1][:-1].split(",")) if n != "x"]


def solve(problem):
    return next(reduce(common, [candidates(o, b) for o, b in problem]))


def candidates(offset, bus):
    i = -offset
    while True:
        i += bus
        yield i


def common(g1, g2):
    x1 = next(g1)
    x2 = next(g2)

    while True:
        if x1 == x2:
            yield x1
            x1 = next(g1)
            x2 = next(g2)
        elif x1 > x2:
            x2 = next(g2)
        else:
            x1 = next(g1)


def solve2(problem):

    a = [p[1] - p[0] for p in problem]
    n = [p[1] for p in problem]

    return simultaneous_congruences(a, n)


def simultaneous_congruences(a, n):
    """ "
    Based on Cameron's answer at https://www.khanacademy.org/computing/computer-science/cryptography/modarithmetic/a/congruence-modulo
    """

    M = reduce(lambda a, b: a * b, n)

    def Mi(i):
        return M // n[i]

    def Mi_inverse(i):
        return modular_inverse(Mi(i), n[i])

    return sum(a[i] * Mi(i) * Mi_inverse(i) for i in range(len(a))) % M


def extended_euclidian(a, b):
    """
    Based on code from: https://www.techiedelight.com/extended-euclidean-algorithm-implementation/
    """
    if a == 0:
        return (b, 0, 1)
    else:
        gcd, x, y = extended_euclidian(b % a, a)
        print(f"extended_euclidian({a}, {b}) => {(gcd, y - (b // a) * x, x)}")
        return (gcd, y - (b // a) * x, x)


def modular_inverse(a, b):
    print(f"modular_inverse({a}, {b})")
    gcd, x, y = extended_euclidian(a, b)
    if gcd == 1:
        return x % b
    else:
        raise Exception(f"Not co-prime {a} and {b}!")


if __name__ == "__main__":

    part = 2

    if part == 1:
        start, buses = parse(fileinput.input())
        wait, bus = shortest_wait(start, buses)
        print(wait * bus)

    else:

        problem = parse2(fileinput.input())
        print(solve2(problem))
