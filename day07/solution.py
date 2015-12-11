#!/usr/bin/env python
"""
Solution to day 7 - no eval and with proper toposort.

Part 1:

    $ ./solution.py < input.txt

Part 2 calculated by modifying input:

    $ sed s"#^.* -> b\$#$(./solution.py < input.txt) -> b#" input.txt |\
          ./solution.py
"""
import collections
import operator
import sys
from typing import Mapping, List, Callable, NamedTuple

COMMANDS = {
    'NOT': operator.inv,
    'AND': operator.and_,
    'OR': operator.or_,
    'LSHIFT': operator.lshift,
    'RSHIFT': operator.rshift,
    'NOOP': lambda x: x,  # for value bindings
}
Task = NamedTuple('Task', [('name', str),
                           ('deps', List[str]),
                           ('call', Callable[[Mapping[str, int]], int])])


def parse_task(line: str) -> Task:
    left, right = line.strip().split(' -> ')
    args = left.split(' ')

    if len(args) == 3:
        cmd = COMMANDS[args[1]]
        params = [args[0], args[2]]
    elif len(args) == 2:
        cmd = COMMANDS[args[0]]
        params = [args[1]]
    elif len(args) == 1:
        cmd = COMMANDS['NOOP']
        params = [args[0]]
    else:
        raise ValueError('incorrect format "{}"'.format(line))

    def call(env: Mapping[str, int]) -> int:
        return cmd(*[int(p) if p.isdigit() else env[p]
                     for p in params])

    return Task(name=right,
                deps=set(p for p in params if not p.isdigit()),
                call=call)


if __name__ == '__main__':
    dependents = collections.defaultdict(collections.deque)
    no_deps = collections.deque()
    for line in sys.stdin:
        task = parse_task(line)
        if task.deps:
            for d in task.deps:
                dependents[d].append(task)
        else:
            no_deps.append(task)

    # https://en.wikipedia.org/wiki/Topological_sorting#Kahn.27s_algorithm
    values = {}
    while no_deps:
        task = no_deps.pop()
        values[task.name] = task.call(env=values)
        for dependent in dependents[task.name]:
            dependent.deps.remove(task.name)
            if not dependent.deps:
                no_deps.append(dependent)

    print(values['a'])
