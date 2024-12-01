from __future__ import annotations
from typing import Any, Iterator, Iterable
from dataclasses import dataclass, InitVar
from functools import partial, reduce
from collections import defaultdict
from itertools import repeat
import dataclasses as dc
import operator
import re
import math

from aoc_shared.vector import FrozenVector
from aoc_shared.aoc import main
from aoc_shared.utils import pipe_f

@dataclass(frozen=True, slots=True)
class Robot:
    position: FrozenVector = dc.field(init=False)
    velocity: FrozenVector = dc.field(init=False)
    x: InitVar[int]
    y: InitVar[int]
    vx: InitVar[int]
    vy: InitVar[int]
    def __post_init__(self, x: int, y: int, vx: int, vy: int):
        object.__setattr__(self, "position", FrozenVector(x, y))
        object.__setattr__(self, "velocity", FrozenVector(vx, vy))


def parse(text: str) -> Iterator[Robot]:
    for line in text.split("\n"):
        if m := re.match(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)", line):
            parsed = map(pipe_f(m.group, int), (1, 2, 3, 4))
            yield Robot(*parsed)


def process(data: str) -> Any:
    initial_state = parse(data)
    part_1 = calculate(100, FrozenVector(101, 103), FrozenVector(2, 2), initial_state)
    return part_1, 0

def calculate(time: int, bbox: FrozenVector, divider: FrozenVector, initial: Iterable[Robot]):
    init_pos = tuple(initial)
    final_positions = tuple(map(pipe_f(
        partial(moved, time),
        partial(box, bbox)), init_pos))
    # display(bbox, map(lambda r: r.position, init_pos))

    quadrants: dict[tuple[int, int], int] = {}
    for pos in final_positions:
        if quad := quadrant(bbox, divider, pos):
            if not quadrants.get(quad):
                quadrants[quad] = 1
            else:
                quadrants[quad] += 1

    result = reduce(operator.mul, quadrants.values(), 1)

    return result

def display(size: FrozenVector, positions: Iterable[FrozenVector]) -> None:
    rows: list[list[str]] = []
    for __ in range(size.y):
        rows.append(list(repeat(".", size.x)))

    for position in positions:
        rows[position.y][position.x] = "*"

    for row in rows:
        print("".join(row))

def box(bbox: FrozenVector, vector: FrozenVector):
    x = vector.x % bbox.x
    y = vector.y % bbox.y
    return FrozenVector(x, y)

def moved(time: int, robot: Robot) -> FrozenVector:
    return robot.position + time * robot.velocity

def quadrant(bbox: FrozenVector, dividers: FrozenVector, position: FrozenVector) -> tuple[int, int] | None:
    qx = segment(bbox.x, dividers.x, position.x)
    qy = segment(bbox.y, dividers.y, position.y)
    if qx is None or qy is None:
        return None
    return qx, qy

def segment(length: int, divider: int, value: int) -> int | None:
    dead_interval = (length // divider) + 1
    q, m = divmod(value, dead_interval)
    if (m-dead_interval+1) == 0:
        return None
    return q


def format_output(result: tuple[int, int]) -> str:
    part_1, __ = result
    return f"Part 1: {part_1}\nPart 2: ?"


if __name__ == "__main__":
    main(pipe_f(process, format_output))
