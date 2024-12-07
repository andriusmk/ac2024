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

def calculate(ops: tuple[Operator, ...], values: tuple[int, ...]) -> Iterator[int]:
    if len(values) == 1:
        yield values[0]
    else:
        v = values[-1]
        rest = values[:-1]
        for x in calculate(ops, rest):
            for operator in ops:
                yield operator(x, v)
        # for operator in ops:
        #     yield from (operator(x, v) for x in calculate(ops, rest))

def process(input_data: InputData) -> Any:
    result1 = 0
    result2 = 0
    ops1 = (op.add, op.mul)
    ops2 = (op.add, op.mul, lambda x, y: int(str(x) + str(y)))
    print_progress_bar(0, len(input_data), prefix="Progress:", suffix="done.", length=50)

    for step, (x, values) in enumerate(input_data, start=1):
        result1 += x if (x in calculate(ops1, values)) else 0
        result2 += x if (x in calculate(ops2, values)) else 0
        print_progress_bar(step, len(input_data), prefix="Progress:", suffix="done.", length=50)

    print()
    return result1, result2


if __name__ == "__main__":
    main(sys.argv)
    # cProfile.run('main(sys.argv)')
