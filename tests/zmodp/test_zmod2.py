import pytest

from zmodp import ZMod


@pytest.mark.parametrize('a,b,expected', [
    (0, 0, 0),
    (0, 1, 1),
    (1, 1, 0),
    (1, 0, 1),
])
def test_zmod2_addition(a, b, expected):
    A = ZMod(2)(a)
    B = ZMod(2)(b)
    assert A + B == expected


@pytest.mark.parametrize('a,b,expected', [
    (0, 0, 0),
    (0, 1, 1),
    (1, 1, 0),
    (1, 0, 1),
])
def test_zmod2_subtraction(a, b, expected):
    A = ZMod(2)(a)
    B = ZMod(2)(b)
    assert A - B == expected


@pytest.mark.parametrize('a,b,expected', [
    (0, 0, 0),
    (0, 1, 0),
    (1, 1, 1),
    (1, 0, 0),
])
def test_zmod2_multiplication(a, b, expected):
    A = ZMod(2)(a)
    B = ZMod(2)(b)
    assert A * B == expected


@pytest.mark.parametrize('a,b,expected', [
    (0, 1, 0),
    (1, 1, 1),
])
def test_zmod2_division(a, b, expected):
    A = ZMod(2)(a)
    B = ZMod(2)(b)
    assert A / B == expected


@pytest.mark.parametrize('a', [0, 1])
def test_zmod2_zero_division(a):
    A = ZMod(2)(a)
    B = ZMod(2)(0)
    with pytest.raises(ZeroDivisionError):
        A / B  # pylint: disable=W0104
