#!/usr/bin/env python

import fileinput
import re
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


if __name__ == "__main__":

    rules = parse(fileinput.input())

    for r in rules:
        print(r)
