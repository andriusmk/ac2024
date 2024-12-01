import doit, doit2

TEST_INPUT = """3   4
    4   3
    2   5
    1   3
    3   9
    3   3"""

def test_doit():
    assert doit.process(doit.parse_input(TEST_INPUT.split("\n"))) == 11

def test_doit2():
    assert doit2.process(doit2.parse_input(TEST_INPUT.split("\n"))) == 31
