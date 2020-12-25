#!/usr/bin/env python

import fileinput
from dataclasses import dataclass
from operator import add
from operator import mul
from typing import Callable
from typing import Optional

# 1 + 2 * 3 + 4 * 5 + 6 => (((((1 + 2) * 3) + 4) * 5) + 6)

ops = {"+": add, "*": mul}


@dataclass
class Expression:
    pass


@dataclass
class Value(Expression):
    value: int

    def eval(self):
        return self.value


@dataclass
class Binary(Expression):
    op: Callable[[int, int], int]
    left: Expression
    right: Optional[Expression] = None

    def eval(self):
        return self.op(self.left.eval(), self.right.eval())


def parse_expr(s, pos=0):

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


def parse(input, fn=parse_expr):
    return [(line[:-1], fn(line[:-1], 0)[0]) for line in input]


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
    return ops[s[pos]], eat_whitespace(s, pos + 1)


def eat_whitespace(s, pos):
    while pos < len(s) and s[pos] == " ":
        pos += 1
    return pos


#
# Part 2
#


def addition(s, pos):

    # Number of parenthesized expression
    left, pos = term(s, pos)

    while pos < len(s) and s[pos] == "+":
        fn, pos = op(s, pos)

        # Next number or parenthesized expression
        right, pos = term(s, pos)

        left = Binary(fn, left, right)
        if pos < len(s) and s[pos] == ")":
            return left, eat_whitespace(s, pos + 1)

    return left, eat_whitespace(s, pos)


def product(s, pos):

    # Number, parenthesized expression, or an addition
    left, pos = addition(s, pos)

    while pos < len(s) and s[pos] == "*":
        fn, pos = op(s, pos)

        # Next number, parenthesized expression, or addition
        right, pos = addition(s, pos)

        left = Binary(fn, left, right)
        if pos < len(s) and s[pos] == ")":
            return left, eat_whitespace(s, pos + 1)

    return left, eat_whitespace(s, pos)


def term(s, pos):
    if s[pos] == "(":
        return product(s, pos + 1)
    else:
        buf = ""
        while pos < len(s) and s[pos].isdigit():
            buf += s[pos]
            pos += 1
        return Value(int(buf)), eat_whitespace(s, pos)


def factor(s, pos):
    "A thing on either side of a *. Either a value, a parenthesized expression, or a sum."
    if s[pos] == "(":
        return parse_expr(s, pos + 1)
    else:
        buf = ""
        while pos < len(s) and s[pos].isdigit():
            buf += s[pos]
            pos += 1
        return Value(int(buf)), eat_whitespace(s, pos)


if __name__ == "__main__":

    part = 2

    fn = parse_expr if part == 1 else product

    print(sum(x[1].eval() for x in parse(fileinput.input(), fn)))
