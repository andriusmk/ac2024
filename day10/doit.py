# import cProfile
from typing import Any, TypeVar, Iterable, Iterator, Callable, Sequence
import sys

from itertools import count, repeat, takewhile, starmap, chain
from functools import partial
import operator
from aoc_shared.utils import sum_vec, make_file_parser, pipe, in_boundaries, Vector2D, T
from aoc_shared.progress_bar import print_progress_bar

Point = tuple[Vector2D, int]

def main(argv: list[str]):
    parse_input = make_file_parser(parser)
    pipe(argv[1], parse_input, process, print)

def parser(file) -> tuple[str, ...]:
    return tuple(map(str.strip, file))

def show_progress(step: int, total: int):
    print_progress_bar(step, total, prefix="Progress:", suffix="done.", length=50)


def process(terrain: tuple[str, ...]) -> Any:
    field_size = (len(terrain[0]), len(terrain))
    points = scan(terrain)
    neighbour_vectors = [
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0)
    ]
    reachability: dict[Vector2D, set[Vector2D]] = {}
    total_score = 0

    def all_neighbours(point: Vector2D):
        return (good_nb for n in neighbour_vectors if in_boundaries(field_size, good_nb := sum_vec(point, n)))

    def get_height(point: Vector2D) -> int:
        x, y = point
        return int(terrain[y][x])

    def destinations_reachable(point: Vector2D, height: int) -> set[Vector2D]:
        if height == 9:
            return {point}

        if (destinations := reachability.get(point)) is not None:
            return destinations

        candidate_neighbours = ((nb, nb_height) for nb in all_neighbours(point) if (nb_height := get_height(nb)) == height + 1)
        reachable = set(chain.from_iterable(destinations_reachable(*item) for item in candidate_neighbours))
        reachability[point] = reachable
        return reachable

    for point, height in points:
        if height == 0:
            total_score += len(destinations_reachable(point, height))

    return total_score



def scan(terrain: tuple[str, ...]) -> Iterator[tuple[Vector2D, int]]:
    for y, line in enumerate(terrain):
        for x, h in enumerate(map(int, line)):
            yield (x, y), h


if __name__ == "__main__":
    main(sys.argv)
    # cProfile.run('main(sys.argv)')
