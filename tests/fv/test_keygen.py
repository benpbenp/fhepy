import pytest

from fhepy.fv import FVScheme
from fhepy.polynomials import Polynomials
from fhepy.zmodp import ZMod


@pytest.fixture
def small_fv_scheme():
    return FVScheme(
        plaintext_coefficient_modulus=7,
        ciphertext_coefficient_modulus=874,
        polynomial_modulus_degree=16,
    )


def test_keygen(small_fv_scheme):
    private_key, public_key = small_fv_scheme.keygen()
    assert private_key.__class__.__name__ == 'PolynomialOverZMod874'
    assert public_key[0].__class__.__name__ == 'PolynomialOverZMod874'
    assert public_key[1].__class__.__name__ == 'PolynomialOverZMod874'


def test_encrypt_decrypt(small_fv_scheme):
    private_key, public_key = small_fv_scheme.keygen()
    message = small_fv_scheme.plaintext_polynomials(range(15))
    ciphertext = small_fv_scheme.encrypt(message, public_key)
    assert ciphertext != message
    decrypted = small_fv_scheme.decrypt(ciphertext, private_key)
    assert message == decrypted
