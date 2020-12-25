#!/usr/bin/env python

from dataclasses import dataclass
from operator import add
from operator import mul
from typing import Callable

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
    right: Expression

    def eval(self):
        return self.op(self.left.eval(), self.right.eval())


if __name__ == "__main__":

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
