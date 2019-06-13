from itertools import zip_longest
from hypothesis import given, assume
import hypothesis.strategies as st
import pytest
from zmodp import ZMod

from polynomials import Polynomials

ZMod2 = ZMod(2)
ZMod7 = ZMod(7)
P = Polynomials(ZMod2)
P7 = Polynomials(ZMod7)


@pytest.mark.parametrize('coef_a,coef_b,coef_sum', [
    ([0], [0], [0]),
    ([0], [1], [1]),
    ([1], [0], [1]),
    ([1], [1], [0]),
    ([2], [1], [1])
])
def test_addition_constants(coef_a, coef_b, coef_sum):
    assert P(coef_a) + P(coef_b) == P(coef_sum)


@given(coef_a=st.lists(st.integers()), coef_b=st.lists(st.integers()))
def test_addition(coef_a, coef_b):
    assert P(coef_a) + P(coef_b) == P([
        (a + b) % 2
        for a, b
        in zip_longest(coef_a, coef_b, fillvalue=0)
    ])


@pytest.mark.parametrize('degree', range(0, 5))
@pytest.mark.parametrize('coef_a,coef_b,coef_prod', [
    ([0], [0], [0]),
    ([0], [1], [0]),
    ([1], [0], [0]),
    ([1], [1], [1])
])
def test_multiplication_single_term(coef_a, coef_b, coef_prod, degree):
    coef_a = [0] * degree + coef_a
    coef_b = [0] * degree + coef_b
    coef_prod = [0] * degree * 2 + coef_prod
    assert P(coef_a) * P(coef_b) == P(coef_prod) 


def test_multiplication_example_1():
    """
    (1 + x)*(1+x) = 1 + x**2
    """
    assert P([1, 1]) * P([1,1]) == P([1, 0, 1])


def test_multiplication_example_2():
    """
    (1 + x)*x = x + x**2
    """
    assert P([1, 1]) * P([0,1]) == P([0, 1, 1])


@given(coef_a=st.lists(st.integers(), min_size=1), coef_b=st.lists(st.integers(), min_size=1))
def test_multiplication_inverse_of_division(coef_a, coef_b):
    a = P(coef_a)
    b = P(coef_b)
    assume(b != 0)
    product = a * b
    assert product.divmod(b) == (a, 0)
    if a != 0:
        assert product.divmod(a) == (b, 0)


@given(coef_a=st.lists(st.integers(), min_size=1), coef_b=st.lists(st.integers(), min_size=1))
def test_multiplication_inverse_of_division_zmod7(coef_a, coef_b):
    a = P7(coef_a)
    b = P7(coef_b)
    assume(b != 0)
    product = a * b
    assert product.divmod(b) == (a, 0)
    if a != 0:
        assert product.divmod(a) == (b, 0)


@given(coef_a=st.lists(st.integers(), min_size=17))
def test_polynomial_modulus(coef_a):
    a = P7(coef_a)
    poly_mod = P7.build_terms({16: 1, 0: 1})
    q, r = a.divmod(poly_mod)
    assert r.degree() < 16, r
