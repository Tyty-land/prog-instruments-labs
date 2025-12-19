import sys

def test_smoke():
    assert True


def test_python():
    assert sys.version_info.major == 3


def test_addition():
    result = 1 + 1
    expected = 2
    assert result == expected, f"{result} != {expected}"