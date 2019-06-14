from euclid import ex_euclid


class ZModBase:
    base = None
    val = None

    def __str__(self):
        return str(self.val)

    def __init__(self, val):
        self.val = val % self.base

    def __add__(self, other):
        return self.__class__(self.val + other.val)

    def __sub__(self, other):
        return self.__class__(self.val - other.val)

    def __mul__(self, other):
        return self.__class__(self.val * other.val)

    def __truediv__(self, other):
        """
        self/other == self * other**-1
        """
        if other == 0:
            raise ZeroDivisionError
        return self * other.inverse()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.val == other.val
        if isinstance(other, int):
            return self == self.__class__(other)
        return super().__eq__(other)

    def inverse(self):
        """
        Return the multiplicative inverse, using the extended
        Euclidean Algorithm which finds s and t such that
        s*n + t*a = 1
        where n is the modular base and a is the value.
        Reducing this identity modulo n gives
        t*a = 1 mod n, aka what we are looking for.

        There are potentially other ways of getting the multiplicative
        inverse, see https://en.wikipedia.org/wiki/Finite_field_arithmetic#Multiplicative_inverse
        """
        if self == 0:
            raise ZeroDivisionError

        _, s, _ = ex_euclid(self.val, self.base)
        return self.__class__(s)


_memoized = {}


def ZMod(base):
    """
    Class constructor, returning the following class for
    e.g. base = 3:
    class ZMod3(ZModBase):
        base = 3
    """
    if base not in _memoized:
        name = 'ZMod{}'.format(base)
        bases = (ZModBase,)
        dct = {'base': base}
        _memoized[base] = type(name, bases, dct)

    return _memoized[base]
