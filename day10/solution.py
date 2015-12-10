#!/usr/bin/env python
import itertools
from typing import Iterable


def look_and_say(nums: Iterable[int]) -> Iterable[int]:
    r"""Look and say

    >>> list(look_and_say([2, 1, 1]))
    [1, 2, 2, 1]
    """
    for k, group in itertools.groupby(nums):
        yield sum(1 for _ in group)
        yield k


def las_n(nums: Iterable[int], n: int) -> Iterable[int]:
    return las_n(look_and_say(nums), n-1) if n > 0 else nums


if __name__ == '__main__':
    nums = [int(c) for c in '3113322113']
    print(sum(1 for _ in las_n(nums, 40)))
    print(sum(1 for _ in las_n(nums, 50)))
