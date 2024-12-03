from typing import Iterable
import sys
from aoc_shared.utils import distance, make_file_parser, pair_adjacent, pipe
from day02_shared import parse_int_tuples,  Item, InputData
from pprint import pprint
import itertools

def main(argv: list[str]):
    parse_input = make_file_parser(parse_int_tuples)
    pipe(argv[1], parse_input, process, print)


def process(input_data: InputData) -> int:
    return sum(1 for report in input_data if is_any_safe(report))


def is_any_safe(report: Item) -> bool:
    combinations = itertools.chain((report,), reduced_sets(report))
    return any(is_safe(r) for r in combinations)

def reduced_sets(report: Item) -> Iterable[Item]:
    removed_value = report[0]
    values = list(report[1:])
    for index in range(len(values)):
        yield tuple(values)
        values[index], removed_value = removed_value, values[index]
    yield tuple(values)


def is_safe(report: Item) -> bool:
    pairs = tuple(pair_adjacent(report))
    increasing = (x < y for x, y in pairs)
    decreasing = (x > y for x, y in pairs)
    safe_distance = (1 <= distance(x, y) <= 3 for x, y in pairs)
    return (all(increasing) or all(decreasing)) and all(safe_distance)

if __name__ == "__main__":
    main(sys.argv)
