#!/usr/bin/env python

import fileinput
import re
from dataclasses import dataclass
from typing import List

rule_pat = re.compile(r"(\d+): (.*)")


@dataclass
class Rule:
    pass


@dataclass
class CharRule:
    char: str

    def compile(self, rules):
        return self.char


@dataclass
class RefRule:
    refs: List[str]

    def compile(self, rules):
        return "".join(rules[r].compile(rules) for r in self.refs)


@dataclass
class OrRule:
    parts: List[RefRule]

    def compile(self, rules):
        return f"({'|'.join(p.compile(rules) for p in self.parts)})"


def parse(input):

    rules = {}

    # Read rules
    for line in input:
        text = line[:-1]
        if m := rule_pat.fullmatch(text):
            rules[m.group(1)] = parse_rule(m.group(2))
        elif not text:
            break

    # Read entries
    return rules, [line[:-1] for line in input]


def parse_rule(text):
    if text[0] == '"':
        return CharRule(text[1])
    else:
        parts = text.split(" | ")
        if len(parts) == 1:
            return RefRule(parts[0].split(" "))
        else:
            return OrRule([RefRule(p.split(" ")) for p in parts])


def compile(rules):
    return re.compile(rules["0"].compile(rules))


if __name__ == "__main__":

    rules, entries = parse(fileinput.input())

    r = compile(rules)

    print(sum(r.fullmatch(e) is not None for e in entries))
