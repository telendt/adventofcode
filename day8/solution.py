#!/usr/bin/env python
r"""
Usage:

    $ ./solution.py  < input.txt
"""
import sys
import ast

CHARS_TO_ESCAPE = frozenset(['"', '\\'])


if __name__ == '__main__':
    total1 = 0  # total number of chars "in code"
    total2 = 0  # total number of chars "in memory string"
    total3 = 0  # total number of chars to escape
    for line in sys.stdin:
        s = line.strip()
        total1 += len(s)
        total2 += len(ast.literal_eval(s))  # is it cheating?
        total3 += sum(1 for c in s if c in CHARS_TO_ESCAPE) + 2
    # part1
    print(total1 - total2)
    # part2
    print(total3)
