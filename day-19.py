#!/usr/bin/env python

import fileinput
import re
from dataclasses import dataclass
from typing import List

rule_pat = re.compile(r"(\d+): (.*)")

# Part 2 patch
# 8: 42 | 42 8
# 11: 42 31 | 42 11 31


@dataclass
class Rule:
    pass


@dataclass
class CharRule:
    char: str

    def compile(self, rules):
        return self.char

    def matcher(self, rules):
        return CharMatcher(self.char)


@dataclass
class RefRule:
    refs: List[str]

    def compile(self, rules):
        return "".join(rules[r].compile(rules) for r in self.refs)

    def matcher(self, rules):
        return SequenceMatcher([rules[r].matcher(rules) for r in self.refs])


@dataclass
class OrRule:
    parts: List[RefRule]

    def compile(self, rules):
        return f"({'|'.join(p.compile(rules) for p in self.parts)})"

    def matcher(self, rules):
        return OrMatcher([p.matcher(rules) for p in self.parts])


#
# Build our own matchers since we can't do the new Rule 11 with regexps.
#


@dataclass
class Matcher:
    def match(self, s, pos):
        pass


@dataclass
class CharMatcher(Matcher):
    char: str

    def match(self, s, pos):
        if pos < len(s) and s[pos] == self.char:
            return True, pos + 1
        else:
            return False, pos


@dataclass
class SequenceMatcher(Matcher):
    parts: List[Matcher]

    def match(self, s, pos):
        new_pos = pos
        for p in self.parts:
            ok, new_pos = p.match(s, new_pos)
            if not ok:
                return False, pos
        return True, new_pos


@dataclass
class OrMatcher(Matcher):
    options: List[Matcher]

    def match(self, s, pos):
        new_pos = pos
        for o in self.options:
            ok, new_pos = o.match(s, new_pos)
            if ok:
                return ok, new_pos
        return False, pos


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
    p = re.compile(rules["0"].compile(rules))
    return lambda s: p.fullmatch(s) is not None


def root_matcher(rules):
    m = rules["0"].matcher(rules)

    def f(s):
        ok, pos = m.match(s, 0)
        return ok if pos == len(s) else False

    return f


if __name__ == "__main__":

    rules, entries = parse(fileinput.input())

    r = compile(rules)
    m = root_matcher(rules)

    print(sum(r(e) for e in entries))
    print(sum(m(e) for e in entries))
