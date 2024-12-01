from typing import Iterable, Iterator
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
    reps = repetitions(second)

    return sum(score(reps, value) for value in first)


def parse_line(line: str) -> Item:
    first, second = map(int, line.strip().split())
    return first, second


def score(reps: dict[int, int], value: int) -> int:
    return value * reps.get(value, 0)


def repetitions(input: Iterable[int]) -> dict[int, int]:
    result: dict[int, int] = {}
    for value in input:
        result[value] = result.get(value, 0) + 1
    return result


if __name__ == "__main__":
    main(sys.argv)
