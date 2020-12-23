#!/usr/bin/env python

import fileinput

fields = {
    "byr": True,
    "iyr": True,
    "eyr": True,
    "hgt": True,
    "hcl": True,
    "ecl": True,
    "pid": True,
    "cid": False,
}

required = {k for k, v in fields.items() if v}


def parse(input):
    return list(stanzas(input))


def stanzas(input):
    buf = []
    for line in input:
        if line[:-1]:
            buf += line[:-1].split(" ")
        else:
            yield to_dict(buf)
            buf = []
    if buf:
        yield to_dict(buf)


def to_dict(x):
    return dict(p.split(":") for p in x)


def ok(passport):
    return not (required - set(passport))


if __name__ == "__main__":

    print(sum(ok(p) for p in parse(fileinput.input())))
