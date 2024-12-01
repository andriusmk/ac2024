# import cProfile
from typing import Any, TypeVar, Iterable, Iterator, Callable, Sequence
import dataclasses as dc
import sys

from itertools import count, repeat, takewhile, starmap, chain, groupby, pairwise
from functools import partial
import operator
from aoc_shared.utils import sum_vec, make_file_parser, pipe, pipe_f, in_boundaries, Vector2D, T
from aoc_shared.progress_bar import print_progress_bar

Point = tuple[Vector2D, int]

@dc.dataclass(slots=True)
class WalkResult:
    kind: str
    area: int = 1
    hfences: tuple[Vector2D, ...] = ()
    vfences: tuple[Vector2D, ...] = ()

    def __add__(self, other):
        return WalkResult(self.kind,
            self.area + other.area,
            (*self.hfences, *other.hfences),
            (*self.vfences, *other.vfences))

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



    def walk_area(starting_plot: Vector2D) -> WalkResult:
        if starting_plot in visited_plots:
            return WalkResult("", area=0)
        
        visited_plots.add(starting_plot)

        kind = get_kind(starting_plot)
        # print(f"{kind}: {starting_plot}")

        my_result = WalkResult(kind)

        x, y = starting_plot

        neighbour = x+1, y
        if in_boundaries(field_size, neighbour) and get_kind(neighbour) == kind:
            #print(f"Go to: {neighbour}")
            result = walk_area(neighbour)
            my_result += result
        else:
            #print(f"VFence: {neighbour}")
            my_result.vfences = (*my_result.vfences, neighbour)

        neighbour = x-1, y
        if in_boundaries(field_size, neighbour) and get_kind(neighbour) == kind:
            #print(f"Go to: {neighbour}")
            result = walk_area(neighbour)
            my_result += result
        else:
            #print(f"VFence: {starting_plot}")
            my_result.vfences = (*my_result.vfences, starting_plot)

        neighbour = x, y+1
        if in_boundaries(field_size, neighbour) and get_kind(neighbour) == kind:
            #print(f"Go to: {neighbour}")
            result = walk_area(neighbour)
            my_result += result
        else:
            #print(f"HFence: {neighbour}")
            my_result.hfences = (*my_result.hfences, neighbour)

        neighbour = x, y-1
        if in_boundaries(field_size, neighbour) and get_kind(neighbour) == kind:
            #print(f"Go to: {neighbour}")
            result = walk_area(neighbour)
            my_result += result
        else:
            #print(f"HFence: {starting_plot}")
            my_result.hfences = (*my_result.hfences, starting_plot)

        return my_result

    def all_neighbours(point: Vector2D) -> Iterator[Vector2D]:
        return (sum_vec(point, n) for n in neighbour_vectors if neighbour_vectors)

    def get_kind(point: Vector2D) -> str:
        x, y = point

        return garden[y][x]

    cost = sum(map(pipe_f(walk_area, calculate_cost), scan(garden)))

    return cost


def calculate_cost(walk_result: WalkResult) -> int:
    if not walk_result.area:
        return 0

    total_sides = 0
    for y, g in groupby(sorted(walk_result.hfences, key=operator.itemgetter(1)), key=operator.itemgetter(1)):
        sides = 1
        #print(f"{y=}")
        for seg1, seg2 in pairwise(sorted(g, key=operator.itemgetter(0))):
         #   print(f"{seg1} -> {seg2}")
            if seg2[0] - seg1[0] > 1:
                sides += 1
            elif y > 0 and seg2 in walk_result.vfences:
                sides += 2
        #print(f"{sides=}")
        total_sides += sides

    for x, g in groupby(sorted(walk_result.vfences, key=operator.itemgetter(0)), key=operator.itemgetter(0)):
        sides = 1
        #print(f"{x=}")
        for seg1, seg2 in pairwise(sorted(g, key=operator.itemgetter(1))):
        #    print(f"{seg1} -> {seg2}")
            if seg2[1] - seg1[1] > 1:
                sides += 1
        #print(f"{sides=}")
        total_sides += sides

    cost = total_sides * walk_result.area
    print(f"{walk_result.kind}: {walk_result.area} * {total_sides} = {cost}")
    return cost

def scan(garden: tuple[str, ...]) -> Iterator[Vector2D]:
    width = len(garden[0])
    for y in range(len(garden)):
        for x in range(width):
            yield x, y


if __name__ == "__main__":
    main(sys.argv)
    # cProfile.run('main(sys.argv)')
