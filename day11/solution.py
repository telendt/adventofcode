#!/usr/bin/env python
"""
Brute force, no regular expressions
"""
import collections
import itertools

FORBIDDEN_CHARS = frozenset(['i', 'o', 'l'])


def has_three_inc(s: str) -> bool:
    r"""Check if s has one increasing straight of at least 3 chars.

    >>> has_three_inc('hijklmmn')
    True
    >>> has_three_inc('abbceffg')
    False
    """
    prev = -2
    cnt = 2
    for o in map(ord, s):
        cnt = (cnt - 1) if (o - prev) == 1 else 2
        if cnt == 0:
            return True
        prev = o
    return False


def contains_forbidden_chars(s: str) -> bool:
    r"""
    >>> contains_forbidden_chars("bazinga")
    True
    >>> contains_forbidden_chars("abc")
    False
    """
    return any(c in FORBIDDEN_CHARS for c in s)


def has_two_pairs(s: str) -> bool:
    r"""Check if s has two

    Chesks if password contains at least two different,
    non-overlapping pairs of letters, like aa, bb, or zz.

    >>> has_two_pairs('abbceffg')
    True
    >>> has_two_pairs('abbbcegjk')
    False
    >>> has_two_pairs('abbabb')
    False
    """
    prev = None
    for i, j in zip(s, itertools.islice(s, 1, None)):
        if i == j != prev:
            if prev is not None:
                return True
            prev = i
    return False


def is_valid_password(s: str) -> bool:
    r"""
    >>> is_valid_password('abcdffaa')
    True
    >>> is_valid_password('abcdefgh')
    False
    >>> is_valid_password('hxbxxyzz')
    True
    """
    return has_three_inc(s) and not contains_forbidden_chars(s) and \
        has_two_pairs(s)


def next_password(s: str) -> str:
    r"""
    >>> next_password('xx')
    'xy'
    >>> next_password('azz')
    'baa'
    """
    # could speed this up by preventing forbiden chars
    q = collections.deque()
    for c in reversed(s):
        if c == 'z':
            q.appendleft('a')
        else:
            q.appendleft(chr(ord(c) + 1))
            break
    return s[:-len(q)] + ''.join(q)


def next_valid_password(s: str) -> str:
    r"""
    >>> next_valid_password('abcdefgh')
    'abcdffaa'
    >>> next_valid_password('ghijklmn')
    'ghjaabcc'
    """
    # recursion hits recursion depth limit :(
    while True:
        s = next_password(s)
        if is_valid_password(s):
            return s


if __name__ == '__main__':
    new = next_valid_password('hxbxwxba')
    print(new, flush=True)
    print(next_valid_password(new), flush=True)
