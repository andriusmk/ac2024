from typing import Any, Iterable, Iterator, Type, TypeVar, Callable
import sys
from dataclasses import dataclass, field
import re
from aoc_shared.utils import make_file_parser, pipe, sum_vec

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

def walk(data: InputData) -> Iterator[Vector2D]:
    if not all((data.vector, data.position)):
        return
    visited = set()
    position = data.position
    vector = data.vector
    visited.add(position)
    while True:
        test_position = sum_vec(position, vector)
        if not in_boundaries(data.field_size, position):
            break
        while test_position in data.obstacles:
            vector = rotate(vector)
            test_position = sum_vec(position, vector)
        # we are free to go
        position = test_position
        visited.add(position)
        yield position

def in_boundaries(size: Vector2D, position: Vector2D) -> bool:
    return all(x >= 0 for x in position) and all(p < s for p, s in zip(position, size))

def process(input_data: InputData) -> Any:
    print(input_data)
    return len(set(walk(input_data)))

def rotate(value: Vector2D) -> Vector2D:
    x, y = value
    return -y, x        

if __name__ == "__main__":
    main(sys.argv)
