#!/usr/bin/env python

import fileinput
from dataclasses import dataclass
from operator import add
from operator import mul
from typing import Optional

# 1 + 2 * 3 + 4 * 5 + 6 => (((((1 + 2) * 3) + 4) * 5) + 6)


@dataclass
class Expression:
    pass


@dataclass
class Value(Expression):
    value: int

    def eval(self):
        return self.value

    def parenthesized(self):
        return str(self.value)

    def text(self, _):
        return str(self.value)

    def sexp(self):
        return str(self.value)

    @property
    def precedence(self):
        return 3


@dataclass
class Binary(Expression):
    op: str
    left: Expression
    right: Optional[Expression] = None

    def eval(self):
        fn = add if self.op == "+" else mul
        return fn(self.left.eval(), self.right.eval())

    def parenthesized(self):
        return f"({self.left.parenthesized()} {self.op} {self.right.parenthesized()})"

    @property
    def precedence(self):
        return 2 if self.op == "+" else 1

    def text(self, parent_precedence):
        p = self.precedence

        if p < parent_precedence:
            return f"({self.text(p)})"
        else:
            return f"{self.left.text(p)} {self.op} {self.right.text(p)}"

    def sexp(self):
        return f"({self.op} {self.left.sexp()} {self.right.sexp()})"


def parse(input, fn):
    return [(line[:-1], fn(line[:-1])) for line in input]


def parse_expr1(s):
    e, pos = parse_expr(s, 0)
    assert pos == len(s)
    return e


def parse_expr(s, pos):

    # Read first expression (value or parenthesized)
    left, pos = expr(s, pos)

    while pos < len(s):
        # Read the op
        fn, pos = op(s, pos)

        # Read next expression (value or parenthesized)
        right, pos = expr(s, pos)

        left = Binary(fn, left, right)
        if pos < len(s) and s[pos] == ")":
            return left, eat_whitespace(s, pos + 1)

    return left, len(s)


def expr(s, pos):
    if s[pos] == "(":
        return parse_expr(s, pos + 1)
    else:
        buf = ""
        while pos < len(s) and s[pos].isdigit():
            buf += s[pos]
            pos += 1
        return Value(int(buf)), eat_whitespace(s, pos)


def op(s, pos):
    return s[pos], eat_whitespace(s, pos + 1)


def eat_whitespace(s, pos):
    while pos < len(s) and s[pos] == " ":
        pos += 1
    return pos


#
# Part 2
#


def parse_expr2(s):
    p, pos = product(s, 0)
    assert pos == len(s), f"{s} rest: {s[pos:]}"
    return p


def addition(s, pos):
    left, pos = term(s, pos)

    while pos < len(s) and s[pos] == "+":
        fn, pos = op(s, pos)
        right, pos = term(s, pos)
        left = Binary(fn, left, right)

    return left, eat_whitespace(s, pos)


def product(s, pos):
    left, pos = addition(s, pos)

    while pos < len(s) and s[pos] == "*":
        fn, pos = op(s, pos)
        right, pos = addition(s, pos)
        left = Binary(fn, left, right)

    return left, eat_whitespace(s, pos)


def term(s, pos):
    if s[pos] == "(":
        e, pos = product(s, pos + 1)
        assert s[pos] == ")"
        return e, eat_whitespace(s, pos + 1)
    else:
        buf = ""
        while pos < len(s) and s[pos].isdigit():
            buf += s[pos]
            pos += 1
        return Value(int(buf)), eat_whitespace(s, pos)


def show_lines(input, show_tree=False):
    for line in input:
        text = line[:-1]
        p, _ = product(text, 0)
        print(f"{text} -> {p.eval()}")
        if show_tree:
            print(f"  {p.text(0)}")


def check_lines(input):
    for line in input:
        text = line[:-1]
        p = parse_expr2(text)
        new_text = p.text(0)

        if new_text != text:
            new_p, _ = product(new_text, 0)
            new_new_text = new_p.text(0)
            if new_new_text != new_text:
                print(f"Uh oh")
                print(f"  orig:   {text}")
                print(f"  first:  {new_text}")
                print(f"  second: {new_new_text}")
                print(f"  first:  {p.parenthesized()}")
                print(f"  second: {new_p.parenthesized()}")
                print(f"  first:  {p.sexp()}")
                print(f"  second: {new_p.sexp()}")
                print()
            else:
                print(f"Redundant parens in {text}; could be {new_text}")


if __name__ == "__main__":

    part = 2

    fn = parse_expr1 if part == 1 else parse_expr2

    # check_lines(fileinput.input())

    print(sum(x.eval() for _, x in parse(fileinput.input(), fn)))
