from __future__ import annotations
from typing import Any, Iterable
from dataclasses import dataclass
import re
import math

from aoc_shared.vector import FrozenVector
from aoc_shared.aoc import main
from aoc_shared.utils import pipe_f

@dataclass(frozen=True, slots=True)
class Config:
    a: FrozenVector
    b: FrozenVector
    prize: FrozenVector

@dataclass(frozen=True, slots=True)
class Run:
    a: int
    b: int

def parse(text: str) -> Iterable[Config]:
    configs = text.split("\n\n")
    pattern = r"^Button A: X\+(\d+), Y\+(\d+)\n" + r"^Button B: X\+(\d+), Y\+(\d+)\n" + r"^Prize: X=(\d+), Y=(\d+)$"
    for c in configs:
        if m := re.match(pattern, c.strip(), re.MULTILINE):
            button_a = make_vector(m, 1, 2)
            button_b = make_vector(m, 3, 4)
            prize = make_vector(m, 5, 6)
            yield Config(button_a, button_b, prize)
        
def make_vector(m: re.Match, group_x: int, group_y: int) -> FrozenVector:
    return FrozenVector(int(m.group(group_x)), int(m.group(group_y)))

def sum_all_cost(parsed_input) -> int:
    return sum(cost(result) for conf in parsed_input
                if (result := play(conf)) is not None)

def process(data: str) -> Any:
    parsed_input = tuple(parse(data))
    part_1 = sum_all_cost(parsed_input)

    for conf in parsed_input:
        conf.prize.x += 10000000000000
        conf.prize.y += 10000000000000

    part_2 = sum_all_cost(parsed_input)
    return part_1, part_2


def format_output(result: tuple[int, int]) -> str:
    part_1, part_2 = result
    return f"Part 1: {part_1}\nPart 2: {part_2}"


def play(conf: Config) -> Run | None:
    """Solve a game of with given configuration
    
    given:
        ```
        x_a*a + x_b*b = X
        y_a*a + y_b*b = Y
        ```

    solution:
        ```
        k_x, k_y: k_x*x_a = k_y*y_a
        k_x = lcm(x_a, y_a) / x_a  
        k_y = lcm(x_a, y_a) / y_a  
        b = (X*k_x - Y*k_y) / (x_b*k_x - y_b*k_y)  
        a = (X - x_b*b) / x_a
        ```
    
    Args:
        config (Config): game configuration
    
    Returns:
        Run | None: input to win
    """
    x_a = conf.a.x
    x_b = conf.b.x
    y_a = conf.a.y
    y_b = conf.b.y
    x = conf.prize.x
    y = conf.prize.y

    lcm = math.lcm(x_a, y_a)
    k_x = lcm // conf.a.x
    k_y = lcm // conf.a.y
    b, mb = divmod(x*k_x - y*k_y, x_b*k_x - y_b*k_y)
    if mb:
        return None
    
    a, ma = divmod(x - x_b*b, x_a)
    if ma:
        return None
    
    return Run(a, b)


def cost(run: Run) -> int:
    return 3*run.a + run.b

if __name__ == "__main__":
    main(pipe_f(process, format_output))
