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


def valid_ticket(rules, ticket):
    return all(valid(rules, n) for n in ticket)


def possible_field(rules, field, value):
    return any(value in r for r in rules[field])


def deduce_fields(notes):

    possible_fields = frozenset(notes.rules.keys())

    possibilities = [possible_fields] * len(notes.rules)

    # Search: For each ticket, for each position in the ticket check
    # the value against the rule for the fields that are still
    # possibilities for that field and eliminate any field that is
    # violated by the value. If any position gets whittled down to a
    # single possibile field, remove that field from all other
    # positions. A simple search since we don't need to worry about
    # backtracking.

    for ticket in notes.nearby:
        if valid_ticket(notes.rules, ticket):
            for i, v in enumerate(ticket):
                for field in possibilities[i]:
                    if not possible_field(notes.rules, field, v):
                        if eliminate(possibilities, i, field):
                            return [list(p)[0] for p in possibilities]

    raise Exception(f"No solution: {possibilities}")


def eliminate(possibilities, i, field):
    if field in possibilities[i]:
        possibilities[i] = possibilities[i] - {field}
        if len(possibilities[i]) == 1:
            for j in range(len(possibilities)):
                if j != i:
                    eliminate(possibilities, j, list(possibilities[i])[0])
    return all(len(p) == 1 for p in possibilities)


if __name__ == "__main__":

    notes = parse(fileinput.input())

    part = 2

    if part == 1:
        print(ticket_scanning_error_rate(notes.rules, notes.nearby))
    else:
        print(deduce_fields(notes))
