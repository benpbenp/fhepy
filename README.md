# fhepy
## Fully Homomorphic Encryption in Python

### Overview
Fully Homomorphic Encryption (FHE) refers to any scheme under which meaningful computations
can be performed on an encrypted ciphertext, without revealing any information about the
underlying plain text.

It is one of several means of Privacy-Preserving Computation (PPC) currently under active research.
Applications of PPC abound in areas such as health care, genomics, defense, and finance.

The aim of this Python package is to implement as many FHE schemes as possible,
in a fully Pythonic manner, in order to promote these concepts as widely as possible.

This package is in the very early stages of development.

### Functionality

#### Modular integer arithmetic

A class representing the finite field of the integers modulo p for some prime p,
can be created using the fhepy.zmodp.ZMod function:

```python
from fhepy.zmodp import ZMod
Z7 = ZMod(7)
Z7(2) + Z7(6)
# Z7(1)

Z7(1) - Z7(6)
# Z7(2)

Z7(2) * Z7(6)
# Z7(5)

Z7(5) / Z7(2)
# Z7(6)
```
Division is implemented using the extended Euclidean algorithm. (cf. https://en.wikipedia.org/wiki/Finite_field_arithmetic#Multiplicative_inverse)

#### Polynomial Arithmetic

The Ring of Polynomials with coefficients drawn from finite field ZMod(p) for some prime p,
can be represented with a class created with the Polynomials function in fhepy.polynomials.

```python
from fhepy.polynomials import Polynomials
from fhepy.zmodp import ZMod

ZMod7 = ZMod(7)
P7 = Polynomials(ZMod7)
```
A new polynomial in this ring can be instantiated from P7 with a list of coefficients as an argument:

```python
print(P7([1,5, 3]))                                                                                                           
# 3*(x**2) + 5x + 1
```

Polynomials can be added, multiplied, and subtracted using the usual operators.

Remainder division can also be performed using the .divmod operator.
For example, to divide the polynomial 3*(x**2) + 5*x + 1 by the polynomial x:
```python
print(P7([1,5, 3]).divmod(P7([0, 1])))
# (<PolynomialOverZMod7>: 3x + 5, <PolynomialOverZMod7>: 1)
```
The two elements of the returned tuple are the quotient, 3x + 5, and the remainder, 1.


#### The Fan-Vercauteren Encryption Scheme

This scheme is under development, and is implemented in the module fhepy.fv.

To use the scheme, the fv.FVScheme class must first be instantiated with parameters to set which
polynomial ring we will be operating under.
```python
from fhepy.fv import FVScheme
fv = FVScheme(
        plaintext_coefficient_modulus=7,
        ciphertext_coefficient_modulus=7,
        polynomial_modulus_degree=16,
     )
```
Once instantiated, a public, private key pair can be created.
```python
(private, public) = fv.keygen()
```
The public key can be used to encrypt plaintexts, and the private key can be used to decrypt them.
Note that currently, a "plaintext" is just another polynomial.

```python
private_key, public_key = fv.keygen()
message = fv.plaintext_polynomials(range(15))
ciphertext = fv.encrypt(message, public_key)
assert ciphertext != message
decrypted = fv.decrypt(ciphertext, private_key)
assert message == decrypted
```
