import pytest
from zmodp import ZMod


@pytest.mark.parametrize('a,b,expected', [
    (0, 0, 0),
    (0, 1, 1),
    (0, 2, 2),
    (1, 1, 2),
    (1, 0, 1),
    (1, 2, 0),
    (2, 0, 2),
    (2, 1, 0),
    (2, 2, 1),
])
def test_zmod3_addition(a, b, expected):
    A = ZMod(3)(a)
    B = ZMod(3)(b)
    assert A + B == expected


@pytest.mark.parametrize('a,b,expected', [
    (0, 0, 0),
    (0, 1, 2),
    (0, 2, 1),
    (1, 1, 0),
    (1, 0, 1),
    (1, 2, 2),
    (2, 0, 2),
    (2, 1, 1),
    (2, 2, 0),
])
def test_zmod3_subtraction(a, b, expected):
    A = ZMod(3)(a)
    B = ZMod(3)(b)
    assert A - B == expected


@pytest.mark.parametrize('a,b,expected', [
    (0, 0, 0),
    (0, 1, 0),
    (0, 2, 0),
    (1, 1, 1),
    (1, 0, 0),
    (1, 2, 2),
    (2, 0, 0),
    (2, 1, 2),
    (2, 2, 1),
])
def test_zmod3_multiplication(a, b, expected):
    A = ZMod(3)(a)
    B = ZMod(3)(b)
    assert A * B == expected


@pytest.mark.parametrize('a,b,expected', [
    (0, 1, 0),
    (1, 1, 1),
    (2, 1, 2),
    (0, 2, 0),
    (1, 2, 2),
    (2, 2, 1),
])
def test_zmod3_division(a, b, expected):
    A = ZMod(3)(a)
    B = ZMod(3)(b)
    assert A / B == expected


@pytest.mark.parametrize('a', [0, 1, 2])
def test_zmod3_zero_division(a):
    A = ZMod(3)(a)
    B = ZMod(3)(0)
    with pytest.raises(ZeroDivisionError):
        A / B  # pylint: disable=W0104
