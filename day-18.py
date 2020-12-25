#!/usr/bin/env python

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
    return [parse_expr(line[:-1]) for line in input]


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
            return left, eat_whitespace(pos + 1)

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

    # 1 + 2 * 3 + 4 * 5 + 6

    print(
        Binary(
            add,
            Binary(
                mul,
                Binary(
                    add,
                    Binary(mul, Binary(add, Value(1), Value(2)), Value(3)),
                    Value(4),
                ),
                Value(5),
            ),
            Value(6),
        ).eval()
    )

    v1 = Value(1)
    b1 = Binary(add, v1)
    v2 = Value(2)
    b1.right = v2
    b2 = Binary(mul, b1)
    v3 = Value(3)
    b2.right = v3
    b3 = Binary(add, b2)
    v4 = Value(4)
    b3.right = v4
    b4 = Binary(mul, b3)
    v5 = Value(5)
    b4.right = v5
    b5 = Binary(add, b4)
    v6 = Value(6)
    b5.right = v6

    print(b5.eval())

    left = Value(1)
    b = Binary(add, left)
    right = Value(2)
    b1.right = right
    b2 = Binary(mul, b1)
    v3 = Value(3)
    b2.right = v3
    b3 = Binary(add, b2)
    v4 = Value(4)
    b3.right = v4
    b4 = Binary(mul, b3)
    v5 = Value(5)
    b4.right = v5
    b5 = Binary(add, b4)
    v6 = Value(6)
    b5.right = v6

    print(b5.eval())

    tree, pos = parse_expr("1 + 2 * 3 + 4 * 5 + 6")
    print(tree.eval())
