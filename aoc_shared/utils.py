from typing import Iterable, Iterator, TypeVar, Callable, Any
import functools

T = TypeVar("T")
Vector2D = tuple[int, int]

def distance(x: int, y: int) -> int:
    return abs(x - y)

def repetitions(input: Iterable[T]) -> dict[T, int]:
    result: dict[T, int] = {}
    for value in input:
        result[value] = result.get(value, 0) + 1
    return result

def process_file(parse_input: Callable[[Iterable[str]], T], calculate_result: Callable[[T], int], file_name: str) -> int:
    with open(file_name, "r", encoding="utf-8") as file:
        input_data = parse_input(file)

    return calculate_result(input_data)

def parse_file(file_name: str, parse_lines: Callable[[Iterator[str]], T]) -> T:
    with open(file_name, "r", encoding="utf-8") as file:
        input_data = parse_lines(file)

    return input_data

def make_file_parser(content_parser: Callable[[Iterator[str]], T]) -> Callable[[str], T]:
    return lambda file_name: parse_file(file_name, content_parser)

def pipe(first_value, *functions):
    for function in functions:
        first_value = function(first_value)
    return first_value

def pipe_f(*functions):
    return lambda x: pipe(x, *functions)

def pair_adjacent(values: Iterable[T]) -> Iterator[tuple[T, T]]:
    iterator = iter(values)
    last_value = next(iterator)
    while (value := next(iterator, None)) is not None:
        yield last_value, value
        last_value = value

def read_file(name: str) -> str:
    with open(name, "r", encoding="utf-8") as file:
        return file.read()

def sum_vec(v1: tuple[int, int], v2: tuple[int, int]) -> tuple:
    x1, y1 = v1
    x2, y2 = v2
    return x1+x2, y1+y2

def in_boundaries(size: Vector2D, position: Vector2D) -> bool:
    sx, sy = size
    x, y = position
    return 0 <= x < sx and 0 <= y < sy
