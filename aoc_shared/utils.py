from typing import Iterable, TypeVar, Callable

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
