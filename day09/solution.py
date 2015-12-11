#!/usr/bin/env python
"""
Finds distance of shortest and longest Hamiltonian paths.
No fancy TSP algorithms, just brute-force.

   $ ./solution.py < input.txt
"""
import re
import sys
import collections
import itertools
from typing import Mapping, Iterable

INST = re.compile(
    r'^(?P<city1>\w+) to (?P<city2>\w+) = (?P<dist>\d+)(?:\r?\n)?',
    re.IGNORECASE)


def possible_paths_distances(
        graph: Mapping[str, Mapping[str, int]]) -> Iterable[int]:
    r"""Return iterator with lengths all possible permutations.

    >>> sorted(possible_paths_distances({'a': {'b': 1, 'c': 2},
    ...     'b': {'a': 1, 'c': 3}, 'c': {'a': 2, 'b': 3}}))
    [3, 3, 4, 4, 5, 5]
    """
    for p in itertools.permutations(graph.keys()):
        yield sum(graph[c1][c2] for c1, c2 in zip(p[:-1], p[1:]))


if __name__ == '__main__':
    graph = collections.defaultdict(dict)
    for line in sys.stdin:
        m = INST.match(line)
        city1, city2, dist = \
            m.group('city1'), m.group('city2'), m.group('dist')
        graph[city1][city2] = graph[city2][city1] = int(dist)

    print(min(possible_paths_distances(graph)))
    print(max(possible_paths_distances(graph)))
