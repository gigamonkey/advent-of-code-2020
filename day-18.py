#!/usr/bin/env python

import fileinput
from dataclasses import dataclass
from operator import add
from operator import mul
from typing import Callable
from typing import Optional

# 1 + 2 * 3 + 4 * 5 + 6
#   3   * 3 + 4 * 5 + 6
#       9   + 4 * 5 + 6
#          13   * 5 + 6
#              65   + 6
#                  71


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


def parse(input):
    return [(line[:-1], parse_expr(line[:-1])[0]) for line in input]


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


if __name__ == "__main__":

    print(sum(x[1].eval() for x in parse(fileinput.input())))
