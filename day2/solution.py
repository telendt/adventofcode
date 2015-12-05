#!/usr/bin/env python
from typing import Iterable, Tuple

Dimensions = Tuple[int, int, int]


def dimensions(filename: str = 'input.txt') -> Iterable[Dimensions]:
    with open(filename) as input:
        for line in input:
            yield tuple(int(i) for i in line.split('x'))


def paper(dims: Dimensions) -> int:
    h, l, w = dims
    sides = [l*w, w*h, h*l]
    return 2 * sum(sides) + min(sides)


def ribbon(dims: Dimensions) -> int:
    h, l, w = dims
    return 2*sum(sorted([h, l, w])[:2]) + h*l*w


if __name__ == '__main__':
    dims = list(dimensions())
    # part 1
    print(sum(map(paper, dims)))
    # part 2
    print(sum(map(ribbon, dims)))
