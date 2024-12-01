from __future__ import annotations
from typing import Protocol
from dataclasses import dataclass

class VectorProtocol(Protocol):
    @property
    def x(self) -> int:
        ...
    
    @property
    def y(self) -> int:
        ...


@dataclass(frozen=True, slots=True)
class FrozenVector:
    x: int
    y: int

    def __add__(self, other: VectorProtocol) -> FrozenVector:
        return FrozenVector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: VectorProtocol) -> FrozenVector:
        return FrozenVector(self.x - other.x, self.y - other.y)

    def __rmul__(self, value: int) -> FrozenVector:
        return FrozenVector(value * self.x, value * self.y)
    

@dataclass(slots=True)
class Vector:
    x: int
    y: int

    def __iadd__(self, other: VectorProtocol) -> Vector:
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self, other: VectorProtocol) -> Vector:
        self.x -= other.x
        self.y -= other.y
        return self

    def __add__(self, other: VectorProtocol) -> Vector:
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: VectorProtocol) -> Vector:
        return Vector(self.x - other.x, self.y - other.y)

    def __rmul__(self, value: int) -> Vector:
        return Vector(value * self.x, value * self.y)
    
    def __imul__(self, value: int) -> Vector:
        self.x *= value
        self.y *= value
        return self
    
    def add(self, other: VectorProtocol) -> None:
        self += other
    
    def sub(self, other: VectorProtocol) -> None:
        self -= other

    def scale(self, value: int) -> None:
        self *= value

    def set_to(self, other: VectorProtocol) -> None:
        self.x = other.x
        self.y = other.y
