from collections import deque


class PolynomialBase:
    field = None

    def __init__(self, coefficients):
        """
        Coefficients of terms in increasing order of degree,
        chopping off any trailing zeros.
        """
        while len(coefficients) > 1 and coefficients[-1] == 0:
            coefficients.pop()

        self.coefficients = [
            coef
            if isinstance(coef, self.field)
            else self.field(coef)
            for coef in coefficients
        ]
        

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


_memoized = {}


def Polynomials(field):
    if field not in _memoized:
        name = f'PolynomialOver{field.__name__}'
        bases = (PolynomialBase,)
        dct = {'field': field}
        _memoized[field] = type(name, bases, dct)
    return _memoized[field]

    

