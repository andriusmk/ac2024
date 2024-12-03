from typing import Iterable, Iterator
import sys
from aoc_shared.utils import distance, make_file_parser, pipe, pair_adjacent
from day03.day03_shared import parse_int_tuples,  Item, InputData
import re
import operator
import itertools
from pprint import pprint

mul_statement = re.compile(r"mul\((\d{1,3}+),(\d{1,3}+)\)")

def main(argv: list[str]):
    pipe(argv[1], read_file, process, print)

def read_file(name: str) -> str:
    with open(name, "r", encoding="utf-8") as file:
        return file.read()

def process(input_data: str) -> int:
    dos = input_data.split("do()")
    only_dos = (s.split("don't()")[0] for s in dos)
    products = itertools.chain.from_iterable(map(extract_products, only_dos))
    return sum(products)

def extract_products(input_data: str) -> Iterator[int]:
    matches = re.findall(mul_statement, input_data)
    number_pairs = (map(int, pair) for pair in matches)
    products = (operator.mul(*pair) for pair in number_pairs)
    return products


if __name__ == "__main__":
    main(sys.argv)
