from typing import Iterable

Item = tuple[int, int]
InputData = tuple[Item, ...]


def parse_int_pairs(stream: Iterable[str]) -> InputData:
    def parse_line(line: str) -> Item:
        first, second = map(int, line.strip().split())
        return first, second
    return tuple(parse_line(line) for line in stream)
