from .vector import Vector

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
