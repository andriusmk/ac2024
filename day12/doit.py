# import cProfile
from typing import Any, TypeVar, Iterable, Iterator, Callable, Sequence
import dataclasses as dc
import sys

from itertools import count, repeat, takewhile, starmap, chain
from functools import partial
import operator
from aoc_shared.utils import sum_vec, make_file_parser, pipe, in_boundaries, Vector2D, T
from aoc_shared.progress_bar import print_progress_bar

Point = tuple[Vector2D, int]

# @dc.dataclass(frozen=True, slots=True)
# class Plot:
#     top_left: Point
#     bottom_left: Point = dc.field(init=False)
#     bottom_right: Point = dc.field(init=False)
#     top_right: Point = dc.field(init=False)

#     def __post_init__(self):
#         x, y = self.top_left
#         object.__setattr__(self, "bottom_left", (x, y+1))
#         object.__setattr__(self, "bottom_right", (x+1, y+1))
#         object.__setattr__(self, "top_right", (x+1, y))

def main(argv: list[str]):
    parse_input = make_file_parser(parser)
    pipe(argv[1], parse_input, process, print)

def parser(file) -> tuple[str, ...]:
    return tuple(map(str.strip, file))

def show_progress(step: int, total: int):
    print_progress_bar(step, total, prefix="Progress:", suffix="done.", length=50)


def process(garden: tuple[str, ...]) -> Any:
    field_size = (len(garden[0]), len(garden))
    visited_plots: set[Vector2D] = set()
    neighbour_vectors = [
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0)
    ]
    def walk_area(starting_plot: Vector2D) -> tuple[int, int]:
        if starting_plot in visited_plots:
            return 0, 0
        
        visited_plots.add(starting_plot)

        my_neighbours = all_neighbours(starting_plot)
        kind = get_kind(starting_plot)
        my_result = 1, 0

        for neighbour in my_neighbours:
            if in_boundaries(field_size, neighbour) and get_kind(neighbour) == kind:
                result = walk_area(neighbour)
                my_result = sum_vec(my_result, result)
            else:
                my_result = sum_vec(my_result, (0, 1))

        return my_result

    def all_neighbours(point: Vector2D) -> Iterator[Vector2D]:
        return (sum_vec(point, n) for n in neighbour_vectors if neighbour_vectors)

    def get_kind(point: Vector2D) -> str:
        x, y = point
        return garden[y][x]


    cost = 0

    for plot in scan(garden):
        # print(plot)
        area, perimeter = walk_area(plot)
        cost += area * perimeter

    return cost



def scan(garden: tuple[str, ...]) -> Iterator[Vector2D]:
    width = len(garden[0])
    for y in range(len(garden)):
        for x in range(width):
            yield x, y


if __name__ == "__main__":
    main(sys.argv)
    # cProfile.run('main(sys.argv)')
