#!/usr/bin/env python
import hashlib
import sys
import itertools


def mine(secret: str, n: int) -> int:
    r"""
    >>> mine("abcdef", 5)
    609043
    >>> mine("pqrstuv", 5)
    1048970
    """
    p = secret.encode()
    for i in itertools.count(1):
        if hashlib.md5(b'%s%d' % (p, i)).hexdigest().startswith('0' * n):
            return i


if __name__ == '__main__':
    secret = sys.argv[1]
    print(mine(secret, 5))
    print(mine(secret, 6))
