from dataclasses import dataclass, InitVar
import dataclasses as dc

from .vector import Vector

@dataclass(frozen=True)
class FrozenVector:
    v: Vector = dc.field(init=False)
    x: InitVar[int]
    y: InitVar[int]
    def __post_init__(self, x: int, y: int):
        object.__setattr__(self, "v", Vector(x, y))


def test_vector_init():
    v = Vector(1, 2)
    assert v == Vector(1, 2)

def test_vector_fields():
    v = Vector(3, 4)
    assert v.x == 3
    assert v.y == 4

def test_vector_iadd():
    v = Vector(5, 6)
    v += Vector(2, 3)
    assert v == Vector(7, 9)

def test_vector_add():
    v1 = Vector(3, 5)
    v2 = Vector(2, 3)
    v = v1 + v2
    assert v == Vector(5, 8)
    assert v1 == Vector(3, 5)
    assert v2 == Vector(2, 3)

def test_vector_isub():
    v = Vector(5, 6)
    v -= Vector(2, 3)
    assert v == Vector(3, 3)

def test_vector_sub():
    v1 = Vector(3, 5)
    v2 = Vector(2, 3)
    v = v1 - v2
    assert v == Vector(1, 2)
    assert v1 == Vector(3, 5)
    assert v2 == Vector(2, 3)

def test_vector_mul():
    assert 3 * Vector(3, 4) == Vector(9, 12)

def test_vector_imul():
    v = Vector(2, 3)
    v *= 5
    assert v == Vector(10, 15)

def test_vector_precedence():
    assert Vector(1, 2) + 7 * Vector(1, 1) == Vector(8, 9)

def test_frozen_add():
    v = FrozenVector(5, 7)
    v.v.add(Vector(1, 1))
    assert v.v == Vector(6, 8)

def test_frozen_sub():
    v = FrozenVector(11, 13)
    v.v.sub(Vector(2, 3))
    assert v.v == Vector(9, 10)

def test_frozen_scale():
    v = FrozenVector(7, 13)
    v.v.scale(2)
    assert v.v == Vector(14, 26)
