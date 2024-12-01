from typing import Iterable
import sys

from aoc_shared.utils import repetitions, make_file_parser, pipe
from day01_shared import parse_int_pairs

Item = tuple[int, int]
InputData = Iterable[Item]


def main(argv: list[str]):
    input_parser = make_file_parser(parse_int_pairs)
    pipe(argv[1], input_parser, process, print)


def process(input_data: InputData) -> int:
    first, second = zip(*input_data)
    reps = repetitions(second)

    def score(value: int) -> int:
        return value * reps.get(value, 0)

    return sum(score(value) for value in first)


if __name__ == "__main__":
    main(sys.argv)
