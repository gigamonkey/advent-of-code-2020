#!/usr/bin/env python

import fileinput
import re

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

# byr (Birth Year) - four digits; at least 1920 and at most 2002.
# iyr (Issue Year) - four digits; at least 2010 and at most 2020.
# eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
# hgt (Height) - a number followed by either cm or in:
# If cm, the number must be at least 150 and at most 193.
# If in, the number must be at least 59 and at most 76.
# hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
# ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
# pid (Passport ID) - a nine-digit number, including leading zeroes.
# cid (Country ID) - ignored, missing or not.


four_digits_pat = re.compile(r"\d{4}$")
height = re.compile("(\d+)(cm|in)$")
hair_color = re.compile("#[0-9a-f]{6}$")
passport_id = re.compile("[0-9]{9}$")


def four_digits(min, max):
    def f(s):
        if m := four_digits_pat.match(s):
            return min <= int(m.group(0)) <= max
        else:
            return False

    return f


def hgt(s):
    if m := height.match(s):
        if m.group(2) == "cm":
            return 150 <= int(m.group(1)) <= 193
        elif m.group(2) == "in":
            return 59 <= int(m.group(1)) <= 76
        else:
            raise Exception(f"Bad unit {m.group(2)}")
    else:
        return False


validations = {
    "byr": four_digits(1920, 2002),
    "iyr": four_digits(2010, 2020),
    "eyr": four_digits(2020, 2030),
    "hgt": hgt,
    "hcl": lambda s: hair_color.match(s),
    "ecl": lambda s: s in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"},
    "pid": lambda s: passport_id.match(s),
    "cid": lambda s: True,
}


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


def valid(passport):
    return ok(passport) and all(validations[k](v) for k, v in passport.items())


if __name__ == "__main__":

    passports = parse(fileinput.input())

    # print(sum(ok(p) for p in passports))
    print(sum(valid(p) for p in passports))
