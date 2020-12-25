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


def parse_expr(s):
    pass


if __name__ == "__main__":

    # 1 + 2 * 3 + 4 * 5 + 6

    expr = Binary(
        add,
        Binary(
            mul,
            Binary(
                add, Binary(mul, Binary(add, Value(1), Value(2)), Value(3)), Value(4)
            ),
            Value(5),
        ),
        Value(6),
    )

    print(expr.eval())

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
