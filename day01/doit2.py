from typing import Iterable, Iterator
import sys

def main(argv: list[str]):
    with open(argv[1], "r") as f:
        pairs = tuple(read_pairs(f))

    first, second = zip(*pairs)
    reps = repetitions(second)

    print(sum(score(reps, value) for value in first))

def score(reps: dict[int, int], value: int) -> int:
    return value * reps.get(value, 0)

def repetitions(input: Iterable[int]) -> dict[int, int]:
    result: dict[int, int] = {}
    for value in input:
        result[value] = result.get(value, 0) + 1
    return result

def read_pairs(lines: Iterable[str]) -> Iterator[tuple[int, int]]:
    for line in lines:
        first, second = (int(l.strip()) for l in line.split(" ") if l)
        yield first, second

def distance(x: int, y: int) -> int:
    return abs(x - y)

if __name__ == "__main__":
    main(sys.argv)
