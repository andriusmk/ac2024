import task
from task import FrozenVector

def test_process():
    data = """
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""
    initial = task.parse(data)
    assert task.calculate(100, FrozenVector(11, 7), FrozenVector(2, 2), initial) == 12

def test_parse():
    data = """
p=0,4 v=3,-3
p=6,3 v=-1,-3
"""
    result = tuple(task.parse(data))
    assert result == (task.Robot(0, 4, 3, -3), task.Robot(6, 3, -1, -3))

def test_segment2():
    assert task.segment(7, 2, 0) == 0
    assert task.segment(7, 2, 1) == 0
    assert task.segment(7, 2, 2) == 0
    assert task.segment(7, 2, 3) is None
    assert task.segment(7, 2, 4) == 1
    assert task.segment(7, 2, 5) == 1
    assert task.segment(7, 2, 6) == 1

def test_segment3():
    assert task.segment(11, 3, 0) == 0
    assert task.segment(11, 3, 1) == 0
    assert task.segment(11, 3, 2) == 0
    assert task.segment(11, 3, 3) is None
    assert task.segment(11, 3, 4) == 1
    assert task.segment(11, 3, 5) == 1
    assert task.segment(11, 3, 6) == 1
    assert task.segment(11, 3, 7) is None
    assert task.segment(11, 3, 8) == 2
    assert task.segment(11, 3, 9) == 2
    assert task.segment(11, 3, 10) == 2
   
