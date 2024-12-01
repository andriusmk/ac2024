# import cProfile
from typing import Any, TypeVar, Iterable, Iterator, Callable, Sequence
import sys

from itertools import count, repeat, takewhile, starmap
from functools import partial
import operator
from aoc_shared.utils import sum_vec, make_file_parser, pipe, in_boundaries, Vector2D, T
from aoc_shared.progress_bar import print_progress_bar

def main(argv: list[str]):
    parse_input = make_file_parser(parser)
    pipe(argv[1], parse_input, process, print)

def parser(file) -> str:
    return "".join(line.strip() for line in file)

def show_progress(step: int, total: int):
    print_progress_bar(step, total, prefix="Progress:", suffix="done.", length=50)


def process(input_data: str) -> Any:
    filesystem = tuple(decompress(input_data))
    compacted = compact(filesystem)
    return checksum(compacted)


def checksum(fs: Iterable[int]) -> int:
    return sum(starmap(operator.mul, enumerate(fs)))


def compact(fs: Sequence[int | None]) -> Iterator[int]:
    length = len(fs)
    read = ((idx, value) for idx, value in zip(count(length - 1, -1), reversed(fs)) if value is not None)
    end_idx = length
    for idx, value_in in enumerate(fs):
        if idx >= end_idx:
            break
        if value_in is None:
            end_idx, end_value = next(read)
            yield end_value
        else:
            yield value_in


def decompress(data: str) -> Iterator[int | None]:
    id_gen = count()
    blocks = iter(data)
    while (file_blocks := next(blocks, None)) is not None:
        free_blocks = next(blocks, None)
        file_id = next(id_gen)
        yield from repeat(file_id, int(file_blocks))
        if free_blocks is None:
            break
        yield from repeat(None, int(free_blocks))

if __name__ == "__main__":
    main(sys.argv)
    # cProfile.run('main(sys.argv)')
