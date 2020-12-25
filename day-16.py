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
            ticket = parse_ticket(line)
        elif state == "nearby":
            nearby.append(parse_ticket(line))

    return Notes(rules, ticket, nearby)


def parse_rule(s):
    def to_range(r):
        a, b = r.split("-")
        return range(int(a), int(b) + 1)

    return [to_range(r) for r in s.split(" or ")]


def parse_ticket(s):
    return [int(x) for x in s.split(",")]


def ticket_scanning_error_rate(rules, tickets):
    return sum(n for t in tickets for n in t if not valid(rules, n))


def valid(rules, n):
    return any(n in r for rule in rules.values() for r in rule)


if __name__ == "__main__":

    notes = parse(fileinput.input())

    print(ticket_scanning_error_rate(notes.rules, notes.nearby))
