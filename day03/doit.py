from typing import Iterable
import sys
from aoc_shared.utils import distance, make_file_parser, pipe, pair_adjacent
from day03.day03_shared import parse_int_tuples,  Item, InputData
import re
import operator
from pprint import pprint


def main(argv: list[str]):
    pipe(argv[1], read_file, process, print)

def read_file(name: str) -> str:
    with open(name, "r", encoding="utf-8") as file:
        return file.read()


def process(input_data: str) -> int:
    mul_statement = re.compile(r"mul\((\d{1,3}+),(\d{1,3}+)\)")
    matches = re.findall(mul_statement, input_data)
    number_pairs = (map(int, pair) for pair in matches)
    products = (operator.mul(*pair) for pair in number_pairs)
    return sum(products)

if __name__ == "__main__":
    main(sys.argv)
