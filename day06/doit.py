# import cProfile
from typing import Any, Iterable, Iterator, Type, TypeVar, Callable
import sys
from dataclasses import dataclass, field
import re
import itertools
from aoc_shared.utils import make_file_parser, pipe, sum_vec
from aoc_shared.progress_bar import print_progress_bar
from multiprocessing import Pool

Vector2D = tuple[int, int]

T = TypeVar("T")

@dataclass(frozen=True, slots=True)
class InputData:
    field_size: Vector2D
    obstacles: set[Vector2D]
    position: Vector2D | None
    vector: Vector2D | None

def main(argv: list[str]):
    parse_input = make_file_parser(parser)
    pipe(argv[1], parse_input, process, print)

def parser(lines: Iterator[str]) -> InputData:
    vectors = {
        "^": (0, -1),
        "V": (0, 1),
        "<": (-1, 0),
        ">": (1, 0)
    }
    vector = None
    position = None
    obstacles = set()
    def get_position(m, row):
        return m.start(), row
    
    for row, line in enumerate(lines):
        line = line.strip()
        matches = re.finditer(r"(\^|>|V|<|#)", line)
        for m in matches:
            symbol = m.group(1)
            if guard := vectors.get(symbol):
                vector = guard
                position = get_position(m, row)
            if symbol == "#":
                obstacles.add(get_position(m, row))
    size = (len(line), row+1)
    return InputData(size, obstacles, position, vector)

def walk(data: InputData) -> Iterator[tuple[Vector2D, Vector2D]]:
    if not data.position or not data.vector:
        return
    position = data.position
    vector = data.vector
    yield position, vector

    while True:
        test_position = sum_vec(position, vector)
        if not in_boundaries(data.field_size, test_position):
            break
        while test_position in data.obstacles:
            vector = rotate(vector)
            test_position = sum_vec(position, vector)
        # we are free to go
        position = test_position
        yield position, vector

def in_boundaries(size: Vector2D, position: Vector2D) -> bool:
    sx, sy = size
    x, y = position
    return 0 <= x < sx and 0 <= y < sy
    # return all(x >= 0 for x in position) and all(p < s for p, s in zip(position, size))

def is_loop(input_data: InputData) -> bool:
    visited = set()
    result = False
    for state in walk(input_data):
        if state in visited:
            result = True
            break
        visited.add(state)
    return result

def process(input_data: InputData) -> Any:
    if input_data.position is None or input_data.vector is None:
        return None
    walk_states = tuple(walk(input_data))
    free_walk = len(set(x for x, _ in walk_states))
    visited_positions = set()
    loop_count = 0
    total = len(walk_states)

    print_progress_bar(0, total, prefix="Progress:", suffix="done", length=50)
    for step, (position, vector) in enumerate(walk_states, start=1):
        visited_positions.add(position)
        new_position = sum_vec(position, vector)
        if new_position in input_data.obstacles:
            new_position = sum_vec(position, rotate(vector))
            if new_position in input_data.obstacles:
                continue
        if new_position not in visited_positions:
            new_obstacles = input_data.obstacles.union(((new_position),))
            new_data = InputData(input_data.field_size, new_obstacles, position, vector)
            if is_loop(new_data):
                loop_count += 1
        print_progress_bar(step, total, prefix="Progress:", suffix="done", length=50)
    print()

    return f"{free_walk=}\n{loop_count=}"

def rotate(value: Vector2D) -> Vector2D:
    x, y = value
    return -y, x        

if __name__ == "__main__":
    main(sys.argv)
    # cProfile.run('main(sys.argv)')
