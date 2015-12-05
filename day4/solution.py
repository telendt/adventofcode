#!/usr/bin/env python
import hashlib
import sys
import itertools


def find_matching(prefix: str, n: int) -> int:
    p = prefix.encode()
    for i in itertools.count(1):
        if hashlib.md5(b'%s%d' % (p, i)).hexdigest().startswith('0' * n):
            return i


if __name__ == '__main__':
    prefix = sys.argv[1]
    print(find_matching(prefix, 5))
    print(find_matching(prefix, 6))
