#!/usr/bin/env python
import sys
from typing import Sequence


def ncomb1(n: int, seq: Sequence[int], _i: int=0) -> int:
    r"""Return number of different combinations of seq that sums to n.

    >>> ncomb1(25, [20, 15, 10, 5, 5])
    4
    """
    if _i >= len(seq) or n <= 0:
        return 0
    return (1 if n == seq[_i] else ncomb1(n - seq[_i], seq, _i + 1)) + \
        ncomb1(n, seq, _i + 1)


def ncomb2(n: int, seq: Sequence[int]) -> int:
    r"""
    >>> ncomb2(25, [20, 15, 10, 5, 5])
    3
    """
    minnum = n
    cnt = 0

    def comb(value: int, i: int, num: int) -> None:
        nonlocal minnum, cnt
        if num > minnum or i >= len(seq) or value <= 0:
            return
        if value == seq[i]:
            if num == minnum:
                cnt += 1
            else:  # num < minnum
                cnt = 1
                minnum = num
        comb(value - seq[i], i + 1, num + 1)  # take
        comb(value, i + 1, num)               # don't take

    comb(n, 0, 1)
    return cnt


if __name__ == '__main__':
    containers = [int(line) for line in sys.stdin]
    print(ncomb1(150, containers))
    print(ncomb2(150, containers))
