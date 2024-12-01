from __future__ import annotations
from typing import Any, Iterator, Iterable
from dataclasses import dataclass, InitVar
from functools import partial, reduce
from collections import defaultdict
from itertools import repeat, chain
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

def process(data: str) -> int:
    state, commands = parse(data)
    transform_map(state)
    left = FrozenVector(-1, 0)
    
    def move(direction: FrozenVector) -> None:
        test_pos = direction + state.robot
        test_pos2 = test_pos + left

        if state.walls.intersection((test_pos, test_pos2)):
            return

        if intersection := state.boxes.intersection((test_pos, test_pos2)):
            if not push(intersection.pop(), direction):
                return

        state.robot = test_pos

    def push(position: FrozenVector, direction: FrozenVector) -> bool:
        if boxes := can_push(position, direction):
            to_push = set(boxes)
            pushed = {box + direction for box in to_push}
            state.boxes -= to_push
            state.boxes |= pushed
            return True
        return False

    def can_push(position: FrozenVector, direction: FrozenVector) -> Iterator[FrozenVector] | None:
        test_poss = set(position + vector for vector in obstacle_vectors(direction))
        if test_poss & state.walls:
            return None
        
        boxes = test_poss & state.boxes
        pushables: tuple[Iterator[FrozenVector] | None, ...] = tuple(map(partial(can_push, direction=direction), boxes))
        if all(pushables):
            return chain(*pushables, (position,)) # type: ignore
        return None
           

    for move_dir in read_commands(commands):
        move(move_dir)
    return sum(map(gps, state.boxes))

def obstacle_vectors(vector: FrozenVector) -> Iterable[FrozenVector]:
    if not vector.x:
        return (
            FrozenVector(-1, vector.y),
            FrozenVector(0, vector.y),
            FrozenVector(1, vector.y)
        )
    return (2 * vector,)

def read_commands(commands: str) -> Iterator[FrozenVector]:
    cmd_vectors: dict[str, FrozenVector] = {
        ">": FrozenVector(1, 0),
        "<": FrozenVector(-1, 0),
        "^": FrozenVector(0, -1),
        "v": FrozenVector(0, 1),
    }
    return map(cmd_vectors.__getitem__, commands)

def gps(position: FrozenVector) -> int:
    return 100 * position.y + position.x


def push(state: State, origin: FrozenVector, position: FrozenVector, direction: FrozenVector) -> bool:
    test_pos = direction + position

    if test_pos in state.walls:
        return False
    
    if test_pos in state.boxes:
        return push(state, origin, test_pos, direction)
    
    state.boxes.discard(origin)
    state.boxes.add(test_pos)

    return True

def parse(data: str) -> tuple[State, str]:
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
    ), commands.replace("\n", "")

def transform_map(state: State):
    robot = FrozenVector(state.robot.x * 2, state.robot.y)
    boxes = set(FrozenVector(src.x * 2, src.y) for src in state.boxes)
    walls = set(FrozenVector(src.x * 2, src.y) for src in state.walls)
    # walls = set(chain.from_iterable((FrozenVector(src.x * 2, src.y),
    #                                  FrozenVector(src.x * 2 + 1, src.y))
    #                                  for src in state.walls))
    state.robot = robot
    state.boxes = boxes
    state.walls = walls

if __name__ == "__main__":
    main(process)
