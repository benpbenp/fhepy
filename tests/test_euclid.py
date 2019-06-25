from fhepy.euclid import ex_euclid


def test_ex_euclid():
    assert ex_euclid(240, 46) == (2, -9, 47)
    assert ex_euclid(46, 240) == (2, 47, -9)
