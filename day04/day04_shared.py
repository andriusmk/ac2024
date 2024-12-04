from typing import Iterable, Iterator

Item = tuple[int, ...]
InputData = tuple[Item, ...]


def parse_int_tuples(stream: Iterable[str]) -> InputData:
    def parse_line(line: str) -> Item:
        return tuple(map(int, line.strip().split()))
    return tuple(parse_line(line) for line in stream)
