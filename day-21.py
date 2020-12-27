#!/usr/bin/env python

import fileinput
import re
from collections import defaultdict
from functools import reduce
from operator import or_

pat = re.compile(r"(.*?) \(contains (.*)\)")


def parse(input):
    def g():
        for line in input:
            if m := pat.fullmatch(line[:-1]):
                ingredients = set(m.group(1).split(" "))
                allergens = set(m.group(2).split(", "))
                yield ingredients, allergens

    return list(g())


def solve(foods):
    no_known = no_known_allergens(foods)
    return sum(len(ingredients & no_known) for ingredients, _ in foods)


def no_known_allergens(foods):
    d = match(foods)
    all_ingredients = reduce(or_, (i for i, _ in foods))
    known = reduce(or_, (i for i in d.values()))
    return all_ingredients - known


def match(foods):

    all_ingredients = reduce(or_, (i for i, _ in foods))

    d = defaultdict(lambda: all_ingredients)

    for ingredients, allergens in foods:
        for a in allergens:
            d[a] = d[a] & ingredients
            propagate(d, a)

    return d


def propagate(d, k):
    if len(d[k]) == 1:
        for k2 in d:
            if k2 != k:
                if d[k] & d[k2]:
                    d[k2] = d[k2] - d[k]
                    propagate(d, k2)


if __name__ == "__main__":

    foods = parse(fileinput.input())

    print(solve(foods))
