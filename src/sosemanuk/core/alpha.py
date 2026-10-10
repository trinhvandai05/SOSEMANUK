"""
Nhân và chia với alpha trong GF((2^8)^4).

SOSEMANUK xây GF(2^32) từ:

P(X) = X^4
     + beta^23  * X^3
     + beta^245 * X^2
     + beta^48  * X
     + beta^239

Trong đó beta là nghiệm của Q(X) trong GF(2^8).

Hai bảng tra cứu 256 phần tử được sinh từ
định nghĩa toán học, không hard-code.
"""

from .gf256 import multiply, power, inverse
from .word32 import MASK32


# Các hệ số của đa thức P(X)

C3 = power(2, 23)
C2 = power(2, 245)
C1 = power(2, 48)
C0 = power(2, 239)

C0_INV = inverse(C0)


def _pack(
    b0: int,
    b1: int,
    b2: int,
    b3: int
) -> int:
    """
    Ghép 4 byte thành một word 32-bit.

    b0 là byte thấp nhất.
    b3 là byte cao nhất.
    """

    return (
        b0
        | (b1 << 8)
        | (b2 << 16)
        | (b3 << 24)
    )


def _mul_table_entry(b: int) -> int:
    """
    Sinh một phần tử trong bảng nhân alpha.
    """

    return _pack(
        multiply(C0, b),
        multiply(C1, b),
        multiply(C2, b),
        multiply(C3, b)
    )


def _div_table_entry(b: int) -> int:
    """
    Sinh một phần tử trong bảng chia alpha.
    """

    c = multiply(C0_INV, b)

    return _pack(
        multiply(C1, c),
        multiply(C2, c),
        multiply(C3, c),
        c
    )


# Sinh hai bảng tra cứu khi import module.

MUL_ALPHA_TABLE = tuple(
    _mul_table_entry(b)
    for b in range(256)
)

DIV_ALPHA_TABLE = tuple(
    _div_table_entry(b)
    for b in range(256)
)


def mul_alpha(x: int) -> int:
    """
    Nhân một word 32-bit với alpha.

    Dịch trái 8 bit và XOR với mask được
    xác định từ byte cao nhất của x.
    """

    x &= MASK32

    high_byte = x >> 24

    shifted = (x << 8) & MASK32

    return (
        shifted
        ^ MUL_ALPHA_TABLE[high_byte]
    )


def div_alpha(x: int) -> int:
    """
    Chia một word 32-bit cho alpha.

    Dịch phải 8 bit và XOR với mask được
    xác định từ byte thấp nhất của x.
    """

    x &= MASK32

    low_byte = x & 0xFF

    shifted = x >> 8

    return (
        shifted
        ^ DIV_ALPHA_TABLE[low_byte]
    )