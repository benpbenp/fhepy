from collections import deque
from itertools import zip_longest


class PolynomialBase:
    field = None

    def __init__(self, coefficients):
        """
        Coefficients of terms in increasing order of degree,
        chopping off any trailing zeros.
        """
        self.coefficients = []
        _buffer = []
        for c in coefficients:
            if not isinstance(c, self.field):
                c = self.field(c)
            if c == 0:
                _buffer.append(c)
            else:
                self.coefficients += _buffer + [c]
                _buffer = []
        if not self.coefficients:
            self.coefficients = [self.field(0)]

    @classmethod
    def build_term(cls, coef, degree):
        return cls([0]*degree + [coef])

    @classmethod
    def build_terms(cls, dct):
        """
        Given a dictionary of degree: coefficient pairs,
        build the polynomial
        """
        last_degree = -1
        coefficients = []
        for degree, coefficient in sorted(dct.items()):
            fill_size = degree - last_degree - 1
            coefficients += [0] * fill_size
            coefficients.append(coefficient)
            last_degree = degree
        return cls(coefficients)
    
    def terms(self):
        for i, coef in enumerate(self.coefficients):
            if coef != 0:
                yield self.__class__([0]*i + [coef])

    def lc(self):
        """
        Leading Coefficient
        """
        return self.coefficients[-1]

    def degree(self):
        if self == 0:
            return -1
        else:
            return len(self.coefficients) - 1

    def __str__(self):
        terms = deque([])
        constant = self.coefficients[0]
        if constant != 0 or len(self.coefficients) == 1:
            terms.appendleft(str(constant))
        if len(self.coefficients) > 1:
            linear_coefficient = self.coefficients[1]
            if linear_coefficient == 1:
                terms.appendleft("x")
            elif linear_coefficient != 0:
                terms.appendleft(f'{linear_coefficient}x')
        for degree, coef in enumerate(self.coefficients[2:]):
            if coef == 0:
                continue
            term = f'x**{degree + 2}'
            if coef != 1:
                term = f'{coef}*({term})'
            terms.appendleft(term)

        return " + ".join(terms)

    def __repr__(self):
        return f'<{self.__class__.__name__}>: {str(self)}'

    def __add__(self, other):
        return self.__class__([
            a + b
            for a, b 
            in zip_longest(
                self.coefficients, other.coefficients, fillvalue=self.field(0)
            )
        ])

    def __sub__(self, other):
        return self.__class__([
            a - b
            for a, b 
            in zip_longest(
                self.coefficients, other.coefficients, fillvalue=self.field(0)
            )
        ])

    def __mul__(self, other):
        product = self.__class__([])
        for term in self.terms():
            for other_term in other.terms():
                product_coef = term.lc() * other_term.lc()
                product_degree = term.degree() + other_term.degree()
                product_term = self.__class__([0]*product_degree + [product_coef])
                product = product + product_term
        return product

    def __eq__(self, other):
        if isinstance(other, int):
            return self == self.__class__([other])
        for a, b in zip_longest(self.coefficients, other.coefficients, fillvalue=self.field(0)):
            if a != b:
                return False
        return True

    def divmod(self, other):
        q = self.__class__([0]) 
        r = self
        d = other.degree()
        c = other.lc()
        while r.degree() >= d:
            s = self.__class__.build_term(r.lc() / c, r.degree() - d)
            q = q + s
            r = r - s*other
        return q, r


_memoized = {}


def Polynomials(field):
    if field not in _memoized:
        name = f'PolynomialOver{field.__name__}'
        bases = (PolynomialBase,)
        dct = {'field': field}
        _memoized[field] = type(name, bases, dct)
    return _memoized[field]

    

