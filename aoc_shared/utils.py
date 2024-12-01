from typing import Iterable, TypeVar

T = TypeVar("T")

def distance(x: int, y: int) -> int:
    return abs(x - y)

def repetitions(input: Iterable[T]) -> dict[T, int]:
    result: dict[T, int] = {}
    for value in input:
        result[value] = result.get(value, 0) + 1
    return result

