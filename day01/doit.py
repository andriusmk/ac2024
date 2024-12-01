from typing import Iterable
import sys

Item = tuple[int, int]
InputData = Iterable[Item]


def main(argv: list[str]):
    with open(argv[1], "r", encoding="utf-8") as f:
        input_data = parse_input(f)
    print(process(input_data))


def parse_input(stream: Iterable[str]) -> InputData:
    return tuple(parse_line(line) for line in stream)


def process(input_data: InputData) -> int:
    first, second = zip(*input_data)
    sorted_pairs = tuple(zip(sorted(first), sorted(second)))
    return sum(distance(*pair) for pair in sorted_pairs)


def parse_line(line: str) -> Item:
    first, second = line.strip().split()
    return int(first), int(second)


def distance(x: int, y: int) -> int:
    return abs(x - y)


if __name__ == "__main__":
    main(sys.argv)
