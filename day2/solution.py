#!/usr/bin/env python
from typing import Iterable, NamedTuple

Dimensions = NamedTuple('Dimensions', [('h', int), ('l', int), ('w', int)])


def dimensions(filename: str = 'input.txt') -> Iterable[Dimensions]:
    with open(filename) as input:
        for line in input:
            yield Dimensions(*[int(i) for i in line.split('x')])


def paper(dims: Dimensions) -> int:
    r"""Return surface area of the box with given dimensions.

    >>> paper(Dimensions(2, 3, 4))
    58
    >>> paper(Dimensions(1, 1, 10))
    43
    """
    h, l, w = dims
    sides = [l*w, w*h, h*l]
    return 2 * sum(sides) + min(sides)


def ribbon(dims: Dimensions) -> int:
    r"""Return length of ribbon required to wrap the box with given dimensions.

    >>> ribbon(Dimensions(2, 3, 4))
    34
    >>> ribbon(Dimensions(1, 1, 10))
    14
    """
    h, l, w = dims
    return 2*sum(sorted([h, l, w])[:2]) + h*l*w


if __name__ == '__main__':
    dims = list(dimensions())
    # part 1
    print(sum(map(paper, dims)))
    # part 2
    print(sum(map(ribbon, dims)))
