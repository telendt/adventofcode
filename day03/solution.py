#!/usr/bin/env python
import itertools
import functools
import typing

Location = typing.NamedTuple('Location', [('x', int),
                                          ('y', int)])


EAST = ord('>')
WEST = ord('<')
NORTH = ord('^')
SOUTH = ord('v')


def instructions(filename: str='input.txt') -> typing.Iterable[int]:
    with open(filename, 'rb') as input:
        readpage = functools.partial(input.read, input.raw._blksize)
        for c in itertools.chain.from_iterable(iter(readpage, b'')):
            yield c


def locations(instructions: typing.Iterable[int]) -> typing.Iterable[Location]:
    x, y = 0, 0
    for c in instructions:
        yield Location(x, y)
        if c == NORTH:
            y += 1
        elif c == SOUTH:
            y -= 1
        elif c == EAST:
            x += 1
        elif c == WEST:
            x -= 1
        else:
            raise ValueError(bytes([c]))
    yield Location(x, y)


if __name__ == '__main__':
    inst = list(instructions())
    # part 1
    print(len(set(locations(inst))))
    # part 2
    print(len(set(locations(inst[::2])) | set(locations(inst[1::2]))))
