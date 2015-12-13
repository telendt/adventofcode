#!/usr/bin/env python
import numbers
import collections.abc
import sys
import json
from typing import Any, Optional


def sum_nums(obj: Any, *, skip_val: Optional[str]=None) -> int:
    r"""

    >>> sum_nums([1, 2, 3])
    6
    >>> sum_nums({"a":2,"b":4})
    6
    >>> sum_nums([[[3]]])
    3
    >>> sum_nums({"a":{"b":4},"c":-1})
    3
    >>> sum_nums([])
    0
    >>> sum_nums({})
    0
    >>> sum_nums([1,2,3], skip_val='red')
    6
    >>> sum_nums([1,{"c":"red","b":2},3], skip_val='red')
    4
    >>> sum_nums({"d":"red","e":[1,2,3,4],"f":5}, skip_val='red')
    0
    >>> sum_nums([1,"red",5], skip_val='red')
    6
    """
    if isinstance(obj, numbers.Number):
        return obj
    if isinstance(obj, (str, bytes, bytearray)):
        return 0
    if isinstance(obj, collections.abc.Mapping):
        obj = obj.values()
        if skip_val is not None and skip_val in obj:
            return 0
    if isinstance(obj, collections.abc.Iterable):
        return sum(sum_nums(e, skip_val=skip_val)
                   for e in obj)
    return 0


if __name__ == '__main__':
    obj = json.load(sys.stdin)

    print(sum_nums(obj))
    print(sum_nums(obj, skip_val='red'))
