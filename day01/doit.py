from typing import Iterable
import sys
from aoc_shared.utils import distance, make_file_parser, pipe
from day01_shared import parse_int_pairs

Item = tuple[int, int]
InputData = Iterable[Item]


def main(argv: list[str]):
    parse_input = make_file_parser(parse_int_pairs)
    pipe(argv[1], parse_input, process, print)


def process(input_data: InputData) -> int:
    first, second = zip(*input_data)
    sorted_pairs = tuple(zip(sorted(first), sorted(second)))
    return sum(distance(*pair) for pair in sorted_pairs)


if __name__ == "__main__":
    main(sys.argv)
