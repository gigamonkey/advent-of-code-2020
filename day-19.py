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
class CharRule(Rule):
    char: str

    def matcher(self, rules):
        return CharMatcher(self.char)


@dataclass
class RefRule(Rule):
    refs: List[str]

    def matcher(self, rules):
        return SequenceMatcher([rules[r].matcher(rules) for r in self.refs])


@dataclass
class OrRule(Rule):
    parts: List[RefRule]

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


# Part 2 patch


@dataclass
class RuleZeroMatcher(Matcher):

    rule42: Matcher
    rule31: Matcher

    def match(self, s, pos):

        # Match at least one rule 42 for rule 8.
        ok, new_pos = self.rule42.match(s, pos)

        # Match N rule 42s. Some of these may be from rule 8 some from
        # rule 11. We just need to make sure that the subsequent rule
        # 31s are each paired with one of these 42s. (Any extra 42s
        # can be considered matched by rule 8.)
        opened = 0
        while ok:
            ok, new_pos = self.rule42.match(s, new_pos)
            if ok:
                opened += 1

        # Need to have matched at least one 42/31 pair for rule 11.
        if opened == 0:
            return False, pos

        # Match at most opened 31s, must be at least 1.

        ok = True
        closed = 0
        while ok and closed < opened:
            ok, new_pos = self.rule31.match(s, new_pos)
            if ok:
                closed += 1

        return (True, new_pos) if closed > 0 else (False, pos)


@dataclass
class PatchedRuleZero(Rule):
    def matcher(self, rules):
        return RuleZeroMatcher(rules["42"].matcher(rules), rules["31"].matcher(rules))


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


def root_matcher(rules):
    m = rules["0"].matcher(rules)

    def f(s):
        ok, pos = m.match(s, 0)
        return ok if pos == len(s) else False

    return f


if __name__ == "__main__":

    part = 2

    rules, entries = parse(fileinput.input())

    if part == 2:
        rules["0"] = PatchedRuleZero()

    m = root_matcher(rules)

    print(sum(m(e) for e in entries))
