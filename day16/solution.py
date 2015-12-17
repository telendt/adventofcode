#!/usr/bin/env python
import sys
import re

RE = re.compile(r'([a-z]+): (\d+)')

X = {
    'children': 3,
    'cats': 7,
    'samoyeds': 2,
    'pomeranians': 3,
    'akitas': 0,
    'vizslas': 0,
    'goldfish': 5,
    'trees': 3,
    'cars': 2,
    'perfumes': 1,
}


if __name__ == '__main__':
    for line in sys.stdin:
        sue_id, rest = line.split(': ', maxsplit=1)
        ## PART1:
        # if all(X[feature] == int(value)
        #        for feature, value in RE.findall(rest)):
        ## PART2:
        if all(X[feature] < int(value) if feature in {'cats', 'trees'}
               else X[feature] > int(value) if feature in {'pomeranians',
                                                           'goldfish'}
               else X[feature] == int(value)
               for feature, value in RE.findall(rest)):
            print(sue_id.split(' ')[1])
