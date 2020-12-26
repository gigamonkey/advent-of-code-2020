#!/usr/bin/env python

import fileinput
import re
from dataclasses import dataclass
from typing import List

rule_pat = re.compile(r"(\d+): (.*)")

verbose = False


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


# Part 2 patch


@dataclass
class RuleZeroMatcher(Matcher):

    rule42: Matcher
    rule31: Matcher

    def match(self, s, pos):

        # Match at least one rule 42 for rule 8.
        ok, new_pos = self.rule42.match(s, pos)

        if verbose:
            print(f"Got first 42, ending at {new_pos}")

        # Match N rule 42s. Some of these may be from rule 8 some from
        # rule 11. We just need to make sure that the subsequent rule
        # 31s are each paired with one of these 42s. (Any extra 42s
        # can be considered matched by rule 8.)
        opened = 0
        while ok:
            ok, new_pos = self.rule42.match(s, new_pos)
            if ok:
                opened += 1
                if verbose:
                    print(f"Got another 42, ending at {new_pos} {opened}")

        # Need to have matched at least one 42/31 pair for rule 11.
        if opened == 0:
            if verbose:
                print(f"No more 42s.")
            return False, pos

        # Match at most opened 31s, must be at least 1.

        ok = True
        closed = 0
        while ok and closed < opened:
            ok, new_pos = self.rule31.match(s, new_pos)
            if ok:
                closed += 1
                if verbose:
                    print(f"Got another 31, ending at {new_pos} {closed}")

        if closed > 0:
            if verbose:
                print(f"Good. closed: {closed}; opened: {opened}")
            return True, new_pos
        else:
            if verbose:
                print(f"closed: {closed}; opened: {opened}")
            return False, pos


@dataclass
class RuleEightMatcher(Matcher):

    # 8: 42 | 42 8

    rule42: Matcher

    def match(self, s, pos):
        print(f"Matching rule 42 in rule 8 loop at {pos}")
        ok, new_pos = self.rule42.match(s, pos)
        print(f"In rule 8 first match: {ok} {new_pos}")
        if ok:
            while ok:
                # new pos won't change if we don't match.
                print(f"Matching rule 42 in rule 8 loop at {new_pos}")
                ok, new_pos = self.rule42.match(s, new_pos)
                print(f"In rule 8 loop: {ok} {new_pos}")
            return True, new_pos
        else:
            return False, pos


@dataclass
class RuleElevenMatcher(Matcher):

    # 11: 42 31 | 42 11 31

    rule42: Matcher
    rule31: Matcher

    def match(self, s, pos):
        print(f"Matching rule 11 at {pos}: {s[pos:]}")
        ok, new_pos = self.rule42.match(s, pos)
        print(f"After firstd {ok} {new_pos}")
        if ok:
            # Match N rule 42s
            count = 0
            print(f"Matched first 42 in rule 11, {new_pos} {count}")
            while ok:
                ok, new_pos = self.rule42.match(s, new_pos)
                if ok:
                    print(f"Matched 42 in rule 11, {new_pos} {count}")
                count += 1

            # Match N rule 31s
            while count > 0:
                ok, new_pos = self.rule31.match(s, new_pos)
                if ok:
                    print(f"Matched 31 in rule 11, {new_pos} {count}")
                if not ok:
                    return False, pos
                count -= 1

            # Match closing rule 31
            ok, new_pos = self.rule31.match(s, new_pos)
            if ok:
                print(f"Matched final 31 in rule 11, {new_pos} {count}")
                return True, new_pos

        return False, pos


@dataclass
class PatchedRuleZero:
    def matcher(self, rules):
        return RuleZeroMatcher(rules["42"].matcher(rules), rules["31"].matcher(rules))


@dataclass
class PatchedRuleEight:
    def matcher(self, rules):
        return RuleEightMatcher(rules["42"].matcher(rules))


@dataclass
class PatchedRuleEleven:
    def matcher(self, rules):
        return RuleElevenMatcher(rules["42"].matcher(rules), rules["31"].matcher(rules))


# Part 2 patch
# 8: 42 | 42 8
# 11: 42 31 | 42 11 31

# Rule 8 is a 42+


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
        if ok and pos < len(s):
            if verbose:
                print(f"Matched but didn't go to end of string. {pos} < {len(s)}")
        elif not ok:
            if verbose:
                print(f"Didn't match. pos: {pos}: len(s): {len(s)}")

        return ok if pos == len(s) else False

    return f


if __name__ == "__main__":

    rules, entries = parse(fileinput.input())

    # r = compile(rules)

    # rules["8"] = PatchedRuleEight()
    # rules["11"] = PatchedRuleEleven()
    del rules["8"]
    del rules["11"]
    rules["0"] = PatchedRuleZero()
    m = root_matcher(rules)

    # print(sum(r(e) for e in entries))
    # print(sum(m(e) for e in entries))

    if False:
        good = 0
        for e in entries:
            if not m(e):
                print(f"BAD: {e}")
            else:
                print(f"GOOD: {e}")
                good += 1

        print(good)

    print(sum(m(e) for e in entries))
