#!/usr/bin/env python
import re
import sys
from typing import NamedTuple, Sequence

RACE_TIME = 2503
INST = re.compile(r'''
    ^[A-Z][a-z]+
    [ ]can[ ]fly[ ]
    (?P<speed>\d+)
    [ ]km/s[ ]for[ ]
    (?P<fly_time>\d+)
    [ ]seconds,[ ]but[ ]then[ ]must[ ]rest[ ]for[ ]
    (?P<rest_time>\d+)
    [ ]seconds\.
    $''', re.VERBOSE)


class Reindeer(NamedTuple('Reindeer', [('speed', int),
                                       ('fly_time', int),
                                       ('rest_time', int)])):
    def distance_after(self, n: int) -> int:
        r"""Return distance traveled after n seconds.

        >>> Reindeer(14, 10, 127).distance_after(1000)
        1120
        >>> Reindeer(16, 11, 162).distance_after(1000)
        1056
        """
        a, b = divmod(n, self.fly_time + self.rest_time)
        return self.speed * (a * self.fly_time + min(b, self.fly_time))


def points_after(reindeers: Sequence[Reindeer], n: int) -> int:
    points = [0] * len(reindeers)
    for secs in range(1, n+1):
        dists = [r.distance_after(secs) for r in reindeers]
        max_dist = max(dists)
        for i, dist in enumerate(dists):
            if dist == max_dist:
                points[i] += 1
    return max(points)


if __name__ == '__main__':
    reindeers = [Reindeer(speed=int(m.group('speed')),
                          fly_time=int(m.group('fly_time')),
                          rest_time=int(m.group('rest_time')))
                 for m in map(INST.match, sys.stdin)]

    print(max(r.distance_after(RACE_TIME) for r in reindeers))
    print(points_after(reindeers, RACE_TIME))
