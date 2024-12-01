import sys
from aoc_shared.utils import pipe, read_file
from day03_shared import extract_products

def main(argv: list[str]):
    pipe(argv[1], read_file, process, print)


def process(input_data: str) -> int:
    return pipe(input_data, extract_products, sum)


if __name__ == "__main__":
    main(sys.argv)
