from typing import Iterable, Iterator
from itertools import count, groupby, pairwise
from functools import partial
import time
import operator
import math

from aoc_shared.utils import pipe_f
from aoc_shared.aoc import main
from task import parse, display, moved, FrozenVector, box

def process(data: str) -> None:
    bbox = FrozenVector(101, 103)
    initial = tuple(parse(data))
    for i in count(start=0):
        positions = tuple(map(pipe_f(partial(moved, i), partial(box, bbox)), initial))
        if (analysis := analyze(positions)) >= 10:
            print("second:", i)
            print("score:", analysis)
            print()
            display(bbox, positions)
            for __ in range(3):
                print()
            time.sleep(1)

def analyze(positions: Iterable[FrozenVector]) -> float:
    row_scores = tuple(map(score, scan_rows(positions)))
    mean = sum(row_scores) / len(row_scores)
    std_devs = math.sqrt((1 / (len(row_scores) - 1)) * sum(map(lambda x: pow((x - mean), 2), row_scores)))
    return std_devs

def scan_rows(positions: Iterable[FrozenVector]) -> Iterator[tuple[int, ...]]:
    row_key = operator.attrgetter("y")
    for k, g in groupby(sorted(positions, key=row_key), key=row_key):
        yield tuple(map(operator.attrgetter("x"), g))

def score(row: Iterable[int]) -> int:
    current_chain = 0
    result = 0
    for x1, x2 in pairwise(sorted(row)):
        if x2 - x1 <= 1:
            current_chain += 1
        else:
            result += current_chain * current_chain
            current_chain = 0

    return result

if __name__ == "__main__":
    main(process)
