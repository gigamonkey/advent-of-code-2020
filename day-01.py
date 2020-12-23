#!/usr/bin/env python

import fileinput

numbers = [int(line) for line in fileinput.input()]

d = {}

for n in numbers:
    if n in d:
        print(f"{n} * {d[n]} = {n * d[n]}")
    else:
        d[2020-n] = n
