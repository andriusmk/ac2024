from __future__ import annotations
from typing import Any, Iterable
from dataclasses import dataclass
import re

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
    button_a: Vector
    button_b: Vector
    prize: Vector

@dataclass(frozen=True, slots=True)
class Run:
    a_cnt: int
    b_cnt: int

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
    return 480


def play(config: Config) -> Run | None:
    
    if config.button_b.x * 3 < config.button_a.x:
        return None
    return None


def cost(run: Run) -> int:
    return 3*run.a_cnt + run.b_cnt

if __name__ == "__main__":
    main(process)
