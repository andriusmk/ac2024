import task

def test_process():
    data = """
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
""".strip()
    assert task.process(data) == 480

def test_vector_init():
    v = task.Vector(1, 2)
    assert v == task.Vector(1, 2)

def test_vector_fields():
    v = task.Vector(3, 4)
    assert v.x == 3
    assert v.y == 4

def test_vector_iadd():
    v = task.Vector(5, 6)
    v += task.Vector(2, 3)
    assert v == task.Vector(7, 9)

def test_vector_add():
    v1 = task.Vector(3, 5)
    v2 = task.Vector(2, 3)
    v = v1 + v2
    assert v == task.Vector(5, 8)
    assert v1 == task.Vector(3, 5)
    assert v2 == task.Vector(2, 3)

def test_vector_isub():
    v = task.Vector(5, 6)
    v -= task.Vector(2, 3)
    assert v == task.Vector(3, 3)

def test_vector_sub():
    v1 = task.Vector(3, 5)
    v2 = task.Vector(2, 3)
    v = v1 - v2
    assert v == task.Vector(1, 2)
    assert v1 == task.Vector(3, 5)
    assert v2 == task.Vector(2, 3)

def test_parse():
    data = """
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176
""".strip()
    result = tuple(task.parse(data))
    assert len(result) == 2
    assert result[0] == task.Config(
        task.Vector(94, 34),
        task.Vector(22, 67),
        task.Vector(8400, 5400)
    )
    assert result[1] == task.Config(
        task.Vector(26, 66),
        task.Vector(67, 21),
        task.Vector(12748, 12176)
    )

def test_cost():
    assert task.cost(task.Run(80, 40)) == 280

def test_play_1():
    config = task.Config(
        task.Vector(94, 34),
        task.Vector(22, 67),
        task.Vector(8400, 5400)
    )
    assert task.play(config) == task.Run(94, 34)

def test_play_2():
    config = task.Config(
        task.Vector(26, 66),
        task.Vector(67, 21),
        task.Vector(12748, 12176)
    )
    assert task.play(config) is None
