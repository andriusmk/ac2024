from typing import Iterable, Iterator
import sys

def main(argv: list[str]):
    with open(argv[1], "r", encoding="utf-8") as f:
        pairs = tuple(read_pairs(f))

    first, second = zip(*pairs)
    sorted_pairs = tuple(zip(sorted(first), sorted(second)))
    print(sum(distance(*pair) for pair in sorted_pairs))

def read_pairs(lines: Iterable[str]) -> Iterator[tuple[int, int]]:
    for line in lines:
        first, second = (int(l.strip()) for l in line.split(" ") if l)
        yield first, second

def distance(x: int, y: int) -> int:
    return abs(x - y)

if __name__ == "__main__":
    main(sys.argv)
