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

from aoc_shared.vector import  Vector, FrozenVector
from aoc_shared.aoc import main
from aoc_shared.utils import pipe_f

@dataclass(slots=True)
class State:
    map_size: FrozenVector
    robot: FrozenVector
    walls: set[FrozenVector]
    boxes: set[FrozenVector]
    commands: str

def process(data: str) -> int:
    commands: dict[str, FrozenVector] = {
        ">": FrozenVector(1, 0),
        "<": FrozenVector(-1, 0),
        "^": FrozenVector(0, -1),
        "v": FrozenVector(0, 1),
    }
    state = parse(data)
    for cmd in state.commands:
        move(state, commands[cmd])
    return sum(map(gps, state.boxes))

def gps(position: FrozenVector) -> int:
    return 100 * position.y + position.x

def move(state: State, direction: FrozenVector) -> None:
    test_pos = direction + state.robot
    if test_pos in state.walls:
        return
    
    if test_pos in state.boxes:
        if not push(state, test_pos, test_pos, direction):
            return

    state.robot = test_pos

def push(state: State, origin: FrozenVector, position: FrozenVector, direction: FrozenVector) -> bool:
    test_pos = direction + position

    if test_pos in state.walls:
        return False
    
    if test_pos in state.boxes:
        return push(state, origin, test_pos, direction)
    
    state.boxes.discard(origin)
    state.boxes.add(test_pos)

    return True

def parse(data: str) -> State:
    field_map, commands = data.strip().split("\n\n")
    walls: set[FrozenVector] = set()
    boxes: set[FrozenVector] = set()
    robot: FrozenVector | None = None

    for y, line in enumerate(field_map.split("\n")):
        for x, obj in enumerate(line):
            match obj:
                case "#":
                    walls.add(FrozenVector(x, y))
                case "O":
                    boxes.add(FrozenVector(x, y))
                case "@":
                    robot = FrozenVector(x, y)
                case _:
                    pass

    assert robot is not None

    map_size = FrozenVector(len(line), y + 1)
    return State(
        map_size=map_size,
        robot=robot,
        walls=walls,
        boxes=boxes,
        commands=commands.replace("\n", "")
    )


if __name__ == "__main__":
    main(process)
