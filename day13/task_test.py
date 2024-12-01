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
    assert task.process(data)[0] == 480

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
        task.FrozenVector(94, 34),
        task.FrozenVector(22, 67),
        task.FrozenVector(8400, 5400)
    )
    assert result[1] == task.Config(
        task.FrozenVector(26, 66),
        task.FrozenVector(67, 21),
        task.FrozenVector(12748, 12176)
    )

def test_cost():
    assert task.cost(task.Run(80, 40)) == 280

def test_play_1():
    config = task.Config(
        task.FrozenVector(94, 34),
        task.FrozenVector(22, 67),
        task.FrozenVector(8400, 5400)
    )
    assert task.play(config) == task.Run(80, 40)

def test_play_2():
    config = task.Config(
        task.FrozenVector(26, 66),
        task.FrozenVector(67, 21),
        task.FrozenVector(12748, 12176)
    )
    assert task.play(config) is None

def test_play_3():
    config = task.Config(
        task.FrozenVector(17, 86),
        task.FrozenVector(84, 37),
        task.FrozenVector(7870, 6450)
    )
    assert task.play(config) == task.Run(38, 86)

def test_play_4():
    config = task.Config(
        task.FrozenVector(69, 23),
        task.FrozenVector(27, 71),
        task.FrozenVector(18641, 10279)
    )
    assert task.play(config) is None
