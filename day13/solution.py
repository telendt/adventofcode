#!/usr/bin/env python
import re
import sys
import collections
import itertools
from typing import Mapping, Iterable

INST = re.compile(r'''
    ^
    (?P<person1>\w+)
    [ ]would[ ]
    (?P<op>gain|lose)
    [ ]
    (?P<units>\d+)
    [ ]happiness[ ]units[ ]by[ ]sitting[ ]next[ ]to[ ]
    (?P<person2>\w+)
    \.
    $
    ''', re.VERBOSE)


def _perm_total(d: Mapping[str, Mapping[str, int]]) -> Iterable[int]:
    assert len(d) >= 2
    keys = iter(d.keys())
    first = next(keys)
    # this has O(n!) time complexity
    # can we do better?
    for perm in itertools.permutations(keys):
        prev = first
        total = 0
        for p in perm:
            total += d[prev][p] + d[p][prev]
            prev = p
        yield total + d[p][first] + d[first][p]


def max_happiness(d: Mapping[str, Mapping[str, int]]) -> int:
    r"""
    >>> max_happiness({
    ...     'a': {'b': 54, 'c': -79, 'd': -2},
    ...     'b': {'a': 83, 'c': -7, 'd': -63},
    ...     'c': {'a': -62, 'b': 60, 'd': 55},
    ...     'd': {'a': 46, 'b': -7, 'c': 41}})
    330
    """
    return max(_perm_total(d))


if __name__ == '__main__':
    table = collections.defaultdict(dict)
    for line in sys.stdin:
        m = INST.match(line)
        v = int(m.group('units'))
        table[m.group('person1')][m.group('person2')] = \
            -v if m.group('op') == 'lose' else v

    print(max_happiness(table))

    for p in list(table.keys()):
        table[p]['Me'] = table['Me'][p] = 0

    print(max_happiness(table))
