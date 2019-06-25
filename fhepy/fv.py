"""
Module containing an implementation of the Fan-Vercauteren Scheme
cf. https://eprint.iacr.org/2012/144
"""
import math
import random

import numpy as np

from fhepy.polynomials import Polynomials
from fhepy.zmodp import ZMod


class FVScheme:
    """
    Implementation of  the Fan-Vercauteren Scheme
    cf. https://eprint.iacr.org/2012/144

    Args:
        plaintext_coefficient_modulus -- "t" in the literature
        ciphertext_coefficient_modulus -- "q" in the literature
        polynomial_modulus_degree -- "d" in the literature
    """

    def __init__(self, plaintext_coefficient_modulus,

                 ciphertext_coefficient_modulus, polynomial_modulus_degree):
        if (
            math.log(polynomial_modulus_degree, 2) !=
            int(math.log(polynomial_modulus_degree, 2))
        ):
            raise ValueError(
                "The polynomial_modulus_degree must be equal to 2**n for some integer n."
            )
        self.plaintext_coefficient_modulus = plaintext_coefficient_modulus
        self.ciphertext_coefficient_modulus = ciphertext_coefficient_modulus
        self.polynomial_modulus_degree = polynomial_modulus_degree

        self.plaintext_field = ZMod(self.plaintext_coefficient_modulus)
        self.plaintext_polynomials = Polynomials(self.plaintext_field)
        self.ciphertext_field = ZMod(self.ciphertext_coefficient_modulus)
        self.ciphertext_polynomials = Polynomials(self.ciphertext_field)
        self.plaintext_polynomial_modulus = self.plaintext_polynomials.build_terms(
            {polynomial_modulus_degree: 1, 0: 1})
        self.ciphertext_polynomial_modulus = self.ciphertext_polynomials.build_terms(
            {polynomial_modulus_degree: 1, 0: 1})

    def keygen(self):
        """
        Generate a private, public key pair

        Returns:
            (private_key, public_key) tuple
            private_key: a polynomial in the ciphertext polynomial ring
            public_key: a tuple of polynomials in the ciphertext polynomial ring
        """
        private_key = self.generate_private_key()
        public_key = self.generate_public_key(private_key)
        return private_key, public_key

    def generate_private_key(self):
        """
        A private key is just a polynomial with coefficients randomly chosen
        from (1, 0, -1)
        """
        coefficients = []
        for i in range(self.polynomial_modulus_degree):
            coefficients.append(random.choice([1, 0, -1]))
        return self.ciphertext_polynomials(coefficients)

    def generate_public_key(self, private_key):
        """
        A public key is a pair of polynomials, with the private key 'hidden' in
        the first of the pair.
        """
        coefficients = []
        for i in range(self.polynomial_modulus_degree):
            coefficients.append(random.randint(
                0, self.ciphertext_coefficient_modulus))
        a = self.ciphertext_polynomials(coefficients)
        e = self.generate_error_polynomial()
        _, pk0 = (e - a * private_key).divmod(self.ciphertext_polynomial_modulus)
        return (pk0, a)

    def generate_error_polynomial(self):
        """
        Generate an "error polynomial", which is a polynomial with
        coefficients drawn from the discrete Gaussian distribution around 0
        """
        randomNums = np.random.normal(
            scale=3, size=self.polynomial_modulus_degree)
        randomInts = np.round(randomNums)
        return self.ciphertext_polynomials(randomInts)

    def encrypt(self, plaintext, public_key):
        """
        Encrypt the plaintext with the given public key
        """
        e1 = self.generate_error_polynomial()
        e2 = self.generate_error_polynomial()
        u = self.generate_private_key()

        ct0 = (
            public_key[0] * u +
            e1 +
            (
                self.ciphertext_coefficient_modulus *
                plaintext/self.plaintext_coefficient_modulus
            )
        ).divmod(self.ciphertext_polynomial_modulus)

        ct1 = (public_key[1] * u +
               e2).divmod(self.ciphertext_polynomial_modulus)
        return (ct0, ct1)

    def decrypt(self, ciphertext, private_key):
        """
        Decrypt the ciphertext with the given private_key
        """
        scaled_plaintext = (
            ciphertext[1] * private_key + ciphertext[0]).divmod(self.ciphertext_polynomial_modulus)
        unscaled_coefficients = [
            round(coef*self.plaintext_coefficient_modulus /
                  self.ciphertext_coefficient_modulus)
            for coef in scaled_plaintext.coefficients
        ]
        return self.plaintext_polynomials(unscaled_coefficients)
