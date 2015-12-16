#!/usr/bin/env python
import re
import sys
import itertools
import collections
from typing import NamedTuple, Sequence, Iterable

INST = re.compile(r'''
    ^
    (?P<name>[A-Z][a-z]+)
    :[ ]capacity[ ]
    (?P<capacity>-?\d+)
    ,[ ]durability[ ]
    (?P<durability>-?\d+)
    ,[ ]flavor[ ]
    (?P<flavor>-?\d+)
    ,[ ]texture[ ]
    (?P<texture>-?\d+)
    ,[ ]calories[ ]
    (?P<calories>-?\d+)
    $
    ''', re.VERBOSE)

Ingredient = NamedTuple('Ingredient', [('name', str),
                                       ('capacity', int),
                                       ('durability', int),
                                       ('flavor', int),
                                       ('texture', int),
                                       ('calories', int)])


def seq(n: int, k: int, j: int=0) -> Iterable[Sequence[int]]:
    r"""Return k-element product from [0, n] range that sums up to n.

    >>> sorted(map(tuple, seq(3, 2)))
    [(0, 3), (1, 2), (2, 1), (3, 0)]
    """
    if k <= 1:
        yield collections.deque([n-j])
        raise StopIteration
    for i in range(n+1-j):
        for a, lst in itertools.product((i, ), seq(n, k-1, j+i)):
            lst.append(a)
            yield lst


def max_score(spoons: int, ingredients: Sequence[Ingredient],
              calories: int=None) -> int:
    r"""Return total score of the highest-scoring cookie.

    >>> ingredients = [Ingredient('Butterscotch', -1, -2, 6, 3, 8),
    ...                Ingredient('Cinnamon', 2, 3, -2, -1, 3)]
    >>> max_score(100, ingredients)
    62842880
    >>> max_score(100, ingredients, calories=500)
    57600000
    """
    score = 0
    for sp in seq(spoons, len(ingredients)):
        cap, dur, fla, tex, cal = 0, 0, 0, 0, 0
        for i, v in enumerate(sp):
            ingredient = ingredients[i]
            cap += v * ingredient.capacity
            dur += v * ingredient.durability
            fla += v * ingredient.flavor
            tex += v * ingredient.texture
            cal += v * ingredient.calories
        if calories is None or cal == calories:
            s = max(cap, 0) * max(dur, 0) * max(fla, 0) * max(tex, 0)
            score = max(score, s)
    return score


if __name__ == '__main__':
    ingredients = [Ingredient(**{k: v if k == 'name' else int(v)
                                 for k, v in m.groupdict().items()})
                   for m in map(INST.match, sys.stdin)]

    print(max_score(100, ingredients))
    print(max_score(100, ingredients, calories=500))
