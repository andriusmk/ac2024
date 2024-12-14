from __future__ import annotations
from typing import Any, Iterable
from dataclasses import dataclass
import re
import math

from aoc_shared.aoc import main

@dataclass(slots=True)
class Vector:
    x: int
    y: int

    def __iadd__(self, other: Vector) -> Vector:
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self, other: Vector) -> Vector:
        self.x -= other.x
        self.y -= other.y
        return self

    def __add__(self, other: Vector) -> Vector:
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector) -> Vector:
        return Vector(self.x - other.x, self.y - other.y)

@dataclass(frozen=True, slots=True)
class Config:
    a: Vector
    b: Vector
    prize: Vector

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
        
def make_vector(m: re.Match, group_x: int, group_y: int) -> Vector:
    return Vector(int(m.group(group_x)), int(m.group(group_y)))


def process(data: str) -> Any:
    return sum(cost(result) for conf in parse(data)
                if (result := play(conf)) is not None)


def play(conf: Config) -> Run | None:
    """Solve a game of with given configuration
    
    given:
        x_a*a + x_b*b = X
        y_a*a + y_b*b = Y

    solution:
        k_x, k_y: k_x*x_a = k_y*y_a

        k_x = lcm(x_a, y_a) / x_a
        k_y = lcm(x_a, y_a) / y_a
        b = (X*k_x - Y*k_y) / (x_b*k_x - y_b*k_y)
        a = (X - x_b*b) / x_a
        
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
    main(process)
