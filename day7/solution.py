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
                           ('fun', Callable[[Mapping[str, int]], None])])


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

    def f(data: Mapping[str, int]) -> None:
        data[right] = cmd(*[int(p) if p.isdigit() else data[p]
                            for p in params])
    return Task(name=right,
                deps=set(p for p in params if not p.isdigit()),
                fun=f)


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
        task.fun(values)
        for dependent in dependents[task.name]:
            dependent.deps.remove(task.name)
            if not dependent.deps:
                no_deps.append(dependent)

    print(values['a'])
