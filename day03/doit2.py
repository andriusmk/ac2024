import sys
from aoc_shared.utils import pipe, read_file
from day03_shared import extract_products
import itertools

def main(argv: list[str]):
    pipe(argv[1], read_file, process, print)


def process(input_data: str) -> int:
    dos = input_data.split("do()")
    only_dos = (s.split("don't()")[0] for s in dos)
    products = itertools.chain.from_iterable(map(extract_products, only_dos))
    return sum(products)


if __name__ == "__main__":
    main(sys.argv)
