# import cProfile
from typing import Any, TypeVar, Iterable, Iterator, Callable, Sequence
import sys
from pprint import pprint

from itertools import count, repeat, takewhile, starmap, groupby
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
    filesystem = decompress(input_data)
    compacted = compact2(filesystem)
    return checksum(compacted)


def checksum(fs: Iterable[int|None]) -> int:
    return sum(starmap(operator.mul, (block for block in enumerate(fs) if block[1] is not None)))


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

def compact2(fs: Iterable[int | None]) -> Iterator[int]:
    idx_blocks = enumerate(fs)
    gaps: list[tuple[int, int]] = []
    files: list[tuple[int, int, int]] = []
    for file_id, group in groupby(idx_blocks, operator.itemgetter(1)):
        file = tuple(group)
        start = file[0][0]
        length = len(file)
        if file_id is None:
            gaps.append((start, length))
        else:
            files.append((start, length, file_id))
    for idx, (start, length, file_id) in reversed(tuple(enumerate(files))):
        for gap_idx, (gap_start, gap_length) in enumerate(gaps):
            if gap_start >= start:
                break
            if gap_length >= length:
                files[idx] = (gap_start, length, file_id)
                gaps[gap_idx] = (gap_start + length, gap_length - length)
                break
    
    files.sort(key=operator.itemgetter(0))
    # pprint(files)
    fs_idx = 0
    for start, length, file_id in files:
        if start > fs_idx:
            yield from repeat(None, start - fs_idx)
        yield from repeat(file_id, length)
        fs_idx = start + length


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
