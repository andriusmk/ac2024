import doit, doit2
from day01_shared import parse_int_pairs

TEST_INPUT = """
    3   4
    4   3
    2   5
    1   3
    3   9
    3   3
    """

def test_doit():
    assert doit.process(parse_int_pairs(TEST_INPUT.strip().split("\n"))) == 11

def test_doit2():
    assert doit2.process(parse_int_pairs(TEST_INPUT.strip().split("\n"))) == 31
