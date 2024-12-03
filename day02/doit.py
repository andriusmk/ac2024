from typing import Iterable
import sys
from aoc_shared.utils import distance, make_file_parser, pipe, pair_adjacent
from day02_shared import parse_int_tuples,  Item, InputData

def main(argv: list[str]):
    parse_input = make_file_parser(parse_int_tuples)
    pipe(argv[1], parse_input, process, print)


def process(input_data: InputData) -> int:
    return sum(1 for report in input_data if is_safe(report))

def is_safe(report: Item) -> bool:
    pairs = tuple(pair_adjacent(report))
    increasing = (x < y for x, y in pairs)
    decreasing = (x > y for x, y in pairs)
    safe_distance = (1 <= distance(x, y) <= 3 for x, y in pairs)
    return (all(increasing) or all(decreasing)) and all(safe_distance)

if __name__ == "__main__":
    main(sys.argv)
