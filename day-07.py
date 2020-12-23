#!/usr/bin/env python

import fileinput
import re
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict

contains = re.compile("^(.*?) bags contain (.*)$")
contents = re.compile("(\d+) (.*?) bags?(?:(?:, )|\.$)")


@dataclass
class Rule:
    outer: str
    inner: Dict[str, int]


def parse(input):
    return [parse_rule(line[:-1]) for line in input]


def parse_rule(line):
    if m := contains.fullmatch(line):
        outer = m.group(1)
        inner = m.group(2)
        if inner == "no other bags.":
            return Rule(outer, {})
        else:
            if matches := contents.findall(inner):
                return Rule(outer, {c: int(n) for n, c in matches})
            else:
                raise Exception(f"{inner} doesn't match inner pattern.")

    else:
        raise Exception(f"{line} doesn't match line pattern")


def invert(rules):
    d = defaultdict(set)
    for r in rules:
        for c, n in r.inner.items():
            d[c].add(r.outer)
    return d


def to_dict(rules):
    return {r.outer: r.inner for r in rules}


def outers(color, inverted, seen=None):

    if seen is None:
        seen = set()

    for c in inverted[color] - seen:
        seen = seen | outers(c, inverted, seen | {c})

    return seen


def count_bags(color, tree):
    return 1 + sum(n * count_bags(c, tree) for c, n in tree[color].items())


if __name__ == "__main__":

    rules = parse(fileinput.input())

    # print(len(outers("shiny gold", invert(rules))))

    print(count_bags("shiny gold", to_dict(rules)) - 1)
