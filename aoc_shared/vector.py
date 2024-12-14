from __future__ import annotations
from dataclasses import dataclass

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
