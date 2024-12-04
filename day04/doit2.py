from typing import Any, Iterable, Iterator
import sys
from aoc_shared.utils import distance, make_file_parser, pipe, pair_adjacent

Matrix = tuple[str, ...]
Vector = tuple[int, int]

word = "XMAS"
drow = "".join(reversed(word))
neighbors = ((0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1))

def main(argv: list[str]):
    parse_input = make_file_parser(parser)
    pipe(argv[1], parse_input, process, print)

def parser(lines: Iterable[str]) -> Matrix:
    return tuple(map(str.strip, lines))


def process(input_data: Matrix) -> Any:
    count = 0
    valid = {"SM", "MS"}
    for x in range(1, width(input_data)-1):
        for y in range(1, height(input_data)-1):
            if input_data[y][x] == "A":
                x1 = input_data[y-1][x-1] + input_data[y+1][x+1]
                x2 = input_data[y-1][x+1] + input_data[y+1][x-1]
                if x1 in valid and x2 in valid:
                    count += 1
    return count


def width(matrix: Matrix) -> int:
    return len(matrix[0])

def height(matrix: Matrix) -> int:
    return len(matrix)

def size(matrix: Matrix) -> Vector:
    return (width(matrix), height(matrix))

def sum_vec(*vectors) -> tuple:
    return tuple(map(sum, zip(*vectors)))

def in_boundaries(size: Vector, position: Vector) -> bool:
    return all(x >= 0 for x in position) and all(p < s for p, s in zip(position, size))

def scan(data: Matrix, position: Vector, direction: Vector) -> Iterator[str]:
    sz = size(data)
    while in_boundaries(sz, position):
        yield data[position[1]][position[0]]
        position = sum_vec(position, direction)


if __name__ == "__main__":
    main(sys.argv)
