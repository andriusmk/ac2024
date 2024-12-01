# import cProfile
from typing import Any, Iterable, Iterator, Callable
import sys
import operator as op
from aoc_shared.utils import make_file_parser, pipe, pipe_f
from aoc_shared.progress_bar import print_progress_bar

Equation = tuple[int, tuple[int, ...]]
InputData = tuple[Equation, ...]
Operator = Callable[[int, int], int]

def main(argv: list[str]):
    parse_input = make_file_parser(parser)
    pipe(argv[1], parse_input, process, print)

def parser(lines: Iterator[str]) -> InputData:
    def parse_line(line: str) -> Equation:
        result_s, operands_ss = line.split(":")
        result = int(result_s.strip())
        operands = tuple(map(int, operands_ss.strip().split()))
        return result, operands
    return tuple(map(parse_line, lines))

def make_calculator(ops: tuple[Operator, ...]) -> Callable[[tuple[int, ...]], Iterator[int]]:
    def calculate(values: tuple[int, ...]) -> Iterator[int]:
        if len(values) == 1:
            yield values[0]
        else:
            v = values[-1]
            rest = values[:-1]
            for x in calculate(rest):
                for operator in ops:
                    yield operator(x, v)
    return calculate


def show_progress(step: int, total: int):
    print_progress_bar(step, total, prefix="Progress:", suffix="done.", length=50)


def process(input_data: InputData) -> Any:
    result1 = 0
    result2 = 0
    calculate1 = make_calculator((op.add, op.mul))
    calculate2 = make_calculator((op.add, op.mul, lambda x, y: int(str(x) + str(y))))
    data_len = len(input_data)
    show_progress(0, data_len)

    for step, (x, values) in enumerate(input_data, start=1):
        result1 += x if (x in calculate1(values)) else 0
        result2 += x if (x in calculate2(values)) else 0
        show_progress(step, data_len)

    return result1, result2


if __name__ == "__main__":
    main(sys.argv)
    # cProfile.run('main(sys.argv)')
