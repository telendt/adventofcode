#!/usr/bin/env python
import functools
import itertools
from typing import Iterable

FLOOR_UP = ord('(')


def delta_gen(filename: str = 'input.txt') -> Iterable[int]:
    with open(filename, 'rb') as input:
        readpage = functools.partial(input.read, input.raw._blksize)
        for c in itertools.chain.from_iterable(iter(readpage, b'')):
            yield 1 if c == FLOOR_UP else -1


def basement_pos(gen: Iterable[int]) -> int:
    current_floor = 0
    for pos, delta in enumerate(gen, 1):
        current_floor += delta
        if current_floor < 0:
            return pos
    return -1


if __name__ == '__main__':
    deltas = list(delta_gen())  # "cache" Santa's steps
    # part 1
    print(sum(deltas))
    # part 2
    print(basement_pos(deltas))
