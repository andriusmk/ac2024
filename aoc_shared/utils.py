from typing import Iterable, Iterator, TypeVar, Callable
import functools

T = TypeVar("T")

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

def parse_file(file_name: str, parse_lines: Callable[[Iterable[str]], T]) -> T:
    with open(file_name, "r", encoding="utf-8") as file:
        input_data = parse_lines(file)

    return input_data

def make_file_parser(content_parser: Callable[[Iterable[str]], T]) -> Callable[[str], T]:
    return lambda file_name: parse_file(file_name, content_parser)

def pipe(first_value, *functions):
    for function in functions:
        first_value = function(first_value)
    return first_value

def pair_adjacent(values: Iterable[T]) -> Iterator[tuple[T, T]]:
    iterator = iter(values)
    last_value = next(iterator)
    while (value := next(iterator, None)) is not None:
        yield last_value, value
        last_value = value

def read_file(name: str) -> str:
    with open(name, "r", encoding="utf-8") as file:
        return file.read()
