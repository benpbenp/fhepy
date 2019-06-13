import pytest
from zmodp import ZMod
from polynomials import Polynomials

ZMod7 = ZMod(7)
P7 = Polynomials(ZMod7)


def test_build_terms_zero():
    assert P7.build_terms({0: 0}) == 0 == P7([0])

def test_build_terms_one():
    assert P7.build_terms({0: 1}) == 1 == P7([1])

def test_build_terms_higher_degree():
    assert P7.build_terms({4: 1}) == P7([0, 0, 0, 0, 1])

def test_build_terms_two_terms():
    assert P7.build_terms({4: 1, 1: 1}) == P7([0, 1, 0, 0, 1])

def test_build_terms_three_terms():
    assert P7.build_terms({4: 1, 3: 6, 1: 1}) == P7([0, 1, 0, 6, 1])
