# import cProfile
from typing import Any, TypeVar, Iterable, Iterator, Callable, Sequence
import sys

from itertools import count, repeat, takewhile, dropwhile, starmap, chain
from functools import partial, lru_cache
import operator
from aoc_shared.utils import sum_vec, make_file_parser, pipe, in_boundaries, Vector2D, T
from aoc_shared.progress_bar import print_progress_bar


def main(argv: list[str]):
    parse_input = make_file_parser(parser)
    pipe(argv[2], parse_input, partial(process, int(argv[1])), print)


def parser(file) -> tuple[int, ...]:
    return tuple(map(int, file.read().split()))


def show_progress(step: int, total: int):
    print_progress_bar(step, total, prefix="Progress:", suffix="done.", length=50)


def process(steps: int, values: Iterable[int]) -> Any:
    return sum(map(partial(length_after, steps), values))


@lru_cache(maxsize=None, typed=False)
def length_after(steps: int, value: int) -> int:
    def perform_step() -> int:
        next_steps = steps - 1

        if value == 0:
            return length_after(next_steps, 1)
        
        if ((decimals := decimal_digits(value)) & 1) == 0:
            left, right = split_int(decimals >> 1, value)
            return length_after(next_steps, left) + length_after(next_steps, right)
        
        return length_after(next_steps, value * 2024)

    result = perform_step() if steps > 0 else 1
    
    # some diagnostics may go here
    return result


def decimal_digits(value: int) -> int:
    return len(str(value))


def split_int(at: int, value: int) -> tuple[int, int]:
    return divmod(value, pow(10, at))


if __name__ == "__main__":
    main(sys.argv)
    # cProfile.run('main(sys.argv)')
