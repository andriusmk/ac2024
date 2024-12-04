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

# def vertical(lines: Matrix) -> Iterable[str]:
#     return ("".join(line) for line in zip(*lines))

# def diagonal(lines: Matrix) -> Iterator[str]:
#     word_len = len(word)
#     width = len(lines[0])
#     height = len(lines)
#     print(f"{width=}")
#     print(f"{height=}")

#     def right(x0: int) -> Iterator[str]:
#         print(f"{x0=}")
#         y = x0
#         for x in range(x0+1):
#             print(x, y)
#             if (0 <= x < width) and (height > y >= 0):
#                 yield lines[x][y]
#             y -= 1

#     def left(x0: int) -> Iterator[str]:
#         print(f"{x0=}")
#         y = 0
#         for x in range(x0+1):
#             print(x, y)
#             if (0 <= x < width) and (height > y >= 0):
#                 yield lines[x][y]
#             y += 1

#     for x in range(width+height-1):
#         yield "".join(right(x))       
    

def process(input_data: Matrix) -> Any:
    count = 0
    for x in range(width(input_data)):
        for y in range(height(input_data)):
            for direction in neighbors:
                for i, (s, w) in enumerate(zip(scan(input_data, (x, y), direction), word)):
                    if s != w:
                        break
                else:
                    if i == len(word)-1:
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
