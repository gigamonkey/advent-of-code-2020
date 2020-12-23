#!/usr/bin/env python

import fileinput


def part_1(numbers):

    d = {}

    for n in numbers:
        if n in d:
            print(f"{n} * {d[n]} = {n * d[n]}")
        else:
            d[2020 - n] = n


def part_2(numbers, target, n):
    def g(target, n, numbers, acc):
        if target == 0 and n == 0:
            yield acc
        elif target > 0 and n > 0 and numbers:
            yield from g(target - numbers[0], n - 1, numbers[1:], acc + [numbers[0]])
            yield from g(target, n, numbers[1:], acc)

    return next(g(target, n, numbers, []))


if __name__ == "__main__":

    numbers = [int(line) for line in fileinput.input()]

    a, b = part_2(numbers, 2020, 2)
    print(f"{a} * {b} = {a * b}")

    a, b, c = part_2(numbers, 2020, 3)
    print(f"{a} * {b} * {c} = {a * b * c}")
