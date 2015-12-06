#!/usr/bin/env python
"""
Overengineered, I know....
"""

import abc
import typing
import re
import array
import itertools

INSTRUCTION = re.compile(r'''
^                                     # start
(?P<cmd>toggle|turn[ ]on|turn[ ]off)  # command
[ ]                                   # space
(?P<x1>\d+),(?P<y1>\d+)               # first point coords
[ ]                                   # space
through                               # keyword
[ ]                                   # space
(?P<x2>\d+),(?P<y2>\d+)               # second point coords
\n                                    # optional new line
$                                     # stop
''', re.VERBOSE)
Coords = typing.NamedTuple('Coords', [('x', int), ('y', int)])


class Grid(metaclass=abc.ABCMeta):
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    @abc.abstractmethod
    def toggle(self, start: Coords, stop: Coords) -> None:
        NotImplemented

    @abc.abstractmethod
    def on(self, start: Coords, stop: Coords) -> None:
        NotImplemented

    @abc.abstractmethod
    def off(self, start: Coords, stop: Coords) -> None:
        NotImplemented


class BinaryGrid(Grid):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)
        self.__bitset = 0

    def __get_mask(self, start: Coords, stop: Coords) -> int:
        x1, x2 = sorted((start.x, stop.x))
        y1, y2 = sorted((start.y, stop.y))
        rownum = (1 << x2 - x1 + 1) - 1 << x1
        mask = 0
        for i in range(y1, y2 + 1):
            mask |= rownum << i * self.width
        return mask

    def toggle(self, start: Coords, stop: Coords) -> None:
        self.__bitset ^= self.__get_mask(start, stop)

    def on(self, start: Coords, stop: Coords) -> None:
        self.__bitset |= self.__get_mask(start, stop)

    def off(self, start: Coords, stop: Coords) -> None:
        self.__bitset &= ~self.__get_mask(start, stop)

    def count_lit(self) -> int:
        return bin(self.__bitset).count('1')


# part 2 is pure trolling, @ericwastl
class LevelsGrid(Grid):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)
        # one byte per light should be enough
        self.__rows = [array.array('B', bytearray(width))
                       for _ in range(height)]

    def __mut(self, start: Coords, stop: Coords, delta: int) -> None:
        x1, x2 = sorted((start.x, stop.x))
        y1, y2 = sorted((start.y, stop.y))
        for x, y in itertools.product(range(x1, x2+1), range(y1, y2+1)):
            v = self.__rows[y][x] + delta
            self.__rows[y][x] = 0 if v < 0 else v

    def toggle(self, start: Coords, stop: Coords) -> None:
        self.__mut(start, stop, 2)

    def on(self, start: Coords, stop: Coords) -> None:
        self.__mut(start, stop, 1)

    def off(self, start: Coords, stop: Coords) -> None:
        self.__mut(start, stop, -1)

    def count_lit(self) -> int:
        return sum(itertools.chain(*self.__rows))


class MultiGrid(Grid):
    def __init__(self, *grids: Grid) -> None:
        # assert len(grids) > 0
        # assert (grids[0].width, grids[0].height) == \
        #     (grids[1].width, grids[1].height) == ...
        super().__init__(grids[0].width, grids[0].height)
        self.__grids = grids

    def toggle(self, start: Coords, stop: Coords) -> None:
        for g in self.__grids:
            g.toggle(start, stop)

    def on(self, start: Coords, stop: Coords) -> None:
        for g in self.__grids:
            g.on(start, stop)

    def off(self, start: Coords, stop: Coords) -> None:
        for g in self.__grids:
            g.off(start, stop)


if __name__ == '__main__':
    g1 = BinaryGrid(1000, 1000)
    g2 = LevelsGrid(1000, 1000)
    mg = MultiGrid(g1, g2)
    actions = {
        "toggle": mg.toggle,
        "turn on": mg.on,
        "turn off": mg.off,
    }
    with open('input.txt') as input:
        for line in input:
            m = INSTRUCTION.match(line)
            actions[m.group('cmd')](
                start=Coords(int(m.group('x1')), int(m.group('y1'))),
                stop=Coords(int(m.group('x2')), int(m.group('y2'))))
    print(g1.count_lit())
    print(g2.count_lit())
