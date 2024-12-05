from typing import Any, Iterable, Iterator, Type, TypeVar, Callable
import sys
from aoc_shared.utils import make_file_parser, pipe

Rule = tuple[int, ...]
Update = tuple[int, ...]
InputData = tuple[tuple[Rule, ...], tuple[Update, ...]]

T = TypeVar("T")

def main(argv: list[str]):
    parse_input = make_file_parser(parser)
    pipe(argv[1], parse_input, process, print)

def parser(lines: Iterator[str]) -> InputData:
    def parse_rules() -> Iterator[Rule]:
        while line := next(lines).strip():
            yield split_map(int, "|", line)

    rules = tuple(parse_rules())
    updates = tuple(split_map(int, ",", line.strip()) for line in lines)
    return rules, updates

def split_map(value_type: Callable[[str], T], sep: str, text: str) -> tuple[T, ...]:
    return tuple(map(value_type, text.split(sep)))

def process(input_data: InputData) -> Any:
    rules, updates = input_data
    good_sum = 0
    bad_sum = 0
    for update in updates:
        was_good, corrected = check_update(rules, update)
        mid = middle(corrected)
        if was_good:
            good_sum += mid
        else:
            bad_sum += mid

    return f"{good_sum=}\n{bad_sum=}"

def middle(xs):
    return xs[len(xs) // 2]

def check_update(rules: tuple[Rule, ...], update: tuple[int, ...]) -> tuple[bool, Update]:
    page_positions = {page: idx for idx, page in enumerate(update)}
    pages = list(update)
    is_good = True
    while True:
        corrected = False
        for rule in rules:
            p1, p2 = rule
            x, y = map(page_positions.get, rule)
            if x is None or y is None:
                continue
            if x > y:
                pages[y], pages[x] = p1, p2
                page_positions[p1], page_positions[p2] = y, x
                corrected = True
                is_good = False
        if not corrected:
            break

    return is_good, tuple(pages)
        

if __name__ == "__main__":
    main(sys.argv)
