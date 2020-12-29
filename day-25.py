#!/usr/bin/env python

magic_number = 20201227

test = {5764801, 17807724}

puzzle = {4707356, 12092626}


def steps(subject_number, v=1, i=0):
    while True:
        i += 1
        v = (v * subject_number) % magic_number
        yield (i, v)


def crack(public):
    key_steps = {}
    for i, v in steps(7):
        if v in public:
            key_steps[i] = v
            print(f"Loop {i} -> {v}")
        if v == max(public):
            break
    a, b = sorted(list(key_steps))
    for i, v in steps(key_steps[a]):
        # print(f"Loop {i} -> {v}")
        if i == b:
            return v


if __name__ == "__main__":

    print(crack(test))
    print(crack(puzzle))
