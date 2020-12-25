#!/usr/bin/env python

import fileinput
import re
from dataclasses import dataclass
from typing import Dict
from typing import List

rule_pat = re.compile(r"^(.*?): (.*)$")


@dataclass
class Notes:
    rules: Dict[str, List[range]]
    ticket: List[int]
    nearby: List[List[int]]


def parse(input):
    rules = dict()
    ticket = None
    nearby = []

    state = "rules"

    for line in input:
        line = line[:-1]
        if not line:
            state = None
        elif state is None:
            if line == "your ticket:":
                state = "yours"
            elif line == "nearby tickets:":
                state = "nearby"

        elif state == "rules":
            if m := rule_pat.match(line):
                rules[m.group(1)] = parse_rule(m.group(2))
            else:
                raise Exception("Expecting rule.")

        elif state == "yours":
            ticket = line.split(",")
        elif state == "nearby":
            nearby.append(line.split(","))

    return Notes(rules, ticket, nearby)


def parse_rule(s):
    def to_range(r):
        a, b = r.split("-")
        return range(int(a), int(b) + 1)

    return [to_range(r) for r in s.split(" or ")]


if __name__ == "__main__":

    print(parse(fileinput.input()))
