from dataclasses import dataclass, InitVar
import dataclasses as dc

from .vector import FrozenVector

@dataclass(frozen=True)
class FrozenVector:
    v: FrozenVector = dc.field(init=False)
    x: InitVar[int]
    y: InitVar[int]
    def __post_init__(self, x: int, y: int):
        object.__setattr__(self, "v", FrozenVector(x, y))


def test_vector_init():
    v = FrozenVector(1, 2)
    assert v == FrozenVector(1, 2)

def test_vector_fields():
    v = FrozenVector(3, 4)
    assert v.x == 3
    assert v.y == 4

def test_vector_iadd():
    v = FrozenVector(5, 6)
    v += FrozenVector(2, 3)
    assert v == FrozenVector(7, 9)

def test_vector_add():
    v1 = FrozenVector(3, 5)
    v2 = FrozenVector(2, 3)
    v = v1 + v2
    assert v == FrozenVector(5, 8)
    assert v1 == FrozenVector(3, 5)
    assert v2 == FrozenVector(2, 3)

def test_vector_isub():
    v = FrozenVector(5, 6)
    v -= FrozenVector(2, 3)
    assert v == FrozenVector(3, 3)

def test_vector_sub():
    v1 = FrozenVector(3, 5)
    v2 = FrozenVector(2, 3)
    v = v1 - v2
    assert v == FrozenVector(1, 2)
    assert v1 == FrozenVector(3, 5)
    assert v2 == FrozenVector(2, 3)

def test_vector_mul():
    assert 3 * FrozenVector(3, 4) == FrozenVector(9, 12)

def test_vector_imul():
    v = FrozenVector(2, 3)
    v *= 5
    assert v == FrozenVector(10, 15)

def test_vector_precedence():
    assert FrozenVector(1, 2) + 7 * FrozenVector(1, 1) == FrozenVector(8, 9)

def test_frozen_add():
    v = FrozenVector(5, 7)
    v.v.add(FrozenVector(1, 1))
    assert v.v == FrozenVector(6, 8)

def test_frozen_sub():
    v = FrozenVector(11, 13)
    v.v.sub(FrozenVector(2, 3))
    assert v.v == FrozenVector(9, 10)

def test_frozen_scale():
    v = FrozenVector(7, 13)
    v.v.scale(2)
    assert v.v == FrozenVector(14, 26)
