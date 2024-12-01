from typing import Iterable
import sys

from aoc_shared.utils import repetitions, process_file
from day01_shared import parse_int_pairs

Item = tuple[int, int]
InputData = Iterable[Item]


def main(argv: list[str]):
    print(process_file(parse_int_pairs, process, argv[1]))


def process(input_data: InputData) -> int:
    first, second = zip(*input_data)
    reps = repetitions(second)

    def score(value: int) -> int:
        return value * reps.get(value, 0)

    return sum(score(value) for value in first)


if __name__ == "__main__":
    main(sys.argv)
