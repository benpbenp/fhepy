import pytest

from polynomials import Polynomials
from zmodp import ZMod

ZMod2 = ZMod(2)
ZMod7 = ZMod(7)
ZMod11 = ZMod(11)


@pytest.mark.parametrize('field,coefficients,expected', [
    (ZMod2, [0], "0"),
    (ZMod2, [1], "1"),
    (ZMod2, [3], "1"),
    (ZMod7, [6], "6"),
    (ZMod7, [7], "0")])
def test_constant(field, coefficients, expected):
    poly = Polynomials(field)
    assert str(poly(coefficients)) == expected


@pytest.mark.parametrize('field,coefficients,expected', [
    (ZMod2, [0, 1], "x"),
    (ZMod2, [1, 1], "x + 1"),
    (ZMod2, [3, 3], "x + 1"),
    (ZMod7, [6, 1], "x + 6"),
    (ZMod7, [7, 6], "6x")])
def test_degree_1(field, coefficients, expected):
    poly = Polynomials(field)
    assert str(poly(coefficients)) == expected


@pytest.mark.parametrize('field,coefficients,expected', [
    (ZMod2, [0, 1, 1], "x**2 + x"),
    (ZMod2, [1, 1, 1], "x**2 + x + 1"),
    (ZMod2, [1, 0, 1], "x**2 + 1"),
    (ZMod2, [0, 0, 1], "x**2"),
    (ZMod2, [3, 3, 3], "x**2 + x + 1"),
    (ZMod7, [6, 0, 1], "x**2 + 6"),
    (ZMod7, [7, 0, 6], "6*(x**2)"),
    (ZMod7, [6, 1, 1], "x**2 + x + 6"),
    (ZMod7, [7, 1, 6], "6*(x**2) + x"),
    (ZMod7, [6, 2, 1], "x**2 + 2x + 6"),
    (ZMod7, [7, 5, 6], "6*(x**2) + 5x")
])
def test_degree_2(field, coefficients, expected):
    poly = Polynomials(field)
    assert str(poly(coefficients)) == expected
