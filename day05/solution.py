#!/usr/bin/env python
import re

vowels = re.compile(r'[aeiou]')
pairs = re.compile(r'([a-z])\1')
forbidden = re.compile(r'(?:ab|cd|pq|xy)')

double_pairs = re.compile(r'([a-z]{2}).*\1')
mirror = re.compile(r'([a-z]).\1')


def is_nice1(s: str) -> bool:
    r"""Check if string is nice (part 1).

    >>> is_nice1("ugknbfddgicrmopn")
    True
    >>> is_nice1("aaa")
    True
    >>> is_nice1("jchzalrnumimnmhp")
    False
    >>> is_nice1("haegwjzuvuyypxyu")
    False
    >>> is_nice1("dvszwmarrgswjxmb")
    False
    """
    return forbidden.search(s) is None and \
        pairs.search(s) is not None and \
        len(vowels.findall(s)) >= 3


def is_nice2(s: str) -> bool:
    r"""Check if string is nice (part 2).

    >>> is_nice2("qjhvhtzxzqqjkmpb")
    True
    >>> is_nice2("xxyxx")
    True
    >>> is_nice2("uurcxstgmygtbstg")
    False
    >>> is_nice2("ieodomkazucvgmuy")
    False
    """
    return double_pairs.search(s) is not None and \
        mirror.search(s) is not None


if __name__ == '__main__':
    with open('input.txt') as input:
        total1 = 0
        total2 = 0
        for line in input:
            if is_nice1(line):
                total1 += 1
            if is_nice2(line):
                total2 += 1
        print(total1)
        print(total2)
