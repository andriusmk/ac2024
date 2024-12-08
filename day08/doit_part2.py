# import cProfile
from typing import Any, TypeVar, Iterable, Iterator, Callable
import sys
import re
import itertools as it
from functools import partial
from aoc_shared.utils import sum_vec, make_file_parser, pipe, in_boundaries, Vector2D, T
from aoc_shared.progress_bar import print_progress_bar

Frequency = tuple[Vector2D, ...]
InputData = tuple[Vector2D, tuple[Frequency, ...]]

def main(argv: list[str]):
    parse_input = make_file_parser(parser)
    pipe(argv[1], parse_input, process, print)

def parser(lines: Iterator[str]) -> InputData:
    frequencies: dict[str, list[Vector2D]] = {}
    for row, line in enumerate(lines):
        line = line.strip()
        for m in re.finditer("[0-9A-Za-z]", line):
            freq_id = m.group(0)
            col = m.start()
            if not (freq := frequencies.get(freq_id)):
                freq = []
                frequencies[freq_id] = freq
            freq.append((col, row))
    return (len(line), row + 1), tuple(map(tuple, frequencies.values()))

def show_progress(step: int, total: int):
    print_progress_bar(step, total, prefix="Progress:", suffix="done.", length=50)


def process(input_data: InputData) -> Any:
    antinodes: set[Vector2D] = set()
    field_size, frequencies = input_data
    for freq in frequencies:
        for e1, e2 in pairs(freq):
            nodes = it.takewhile(partial(in_boundaries, field_size), gen_antinodes(e1, e2))
            antinodes.update(nodes)
    return len(antinodes)

def gen_antinodes(e1: Vector2D, e2: Vector2D) -> Iterator[Vector2D]:
    vector = diff(e1, e2)
    yield e1
    while True:
        e1 = sum_vec(e1, vector)
        yield e1

def pairs(collection: Iterable[T]) -> Iterator[tuple[T, T]]:
    return ((x, y) for x in collection for y in collection if x != y)

def diff(vector1: Vector2D, vector2: Vector2D) -> Vector2D:
    x1, y1 = vector1
    x2, y2 = vector2
    return x1 - x2, y1 - y2

if __name__ == "__main__":
    main(sys.argv)
    # cProfile.run('main(sys.argv)')
