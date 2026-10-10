"""
Các phép toán trên trường hữu hạn GF(2^8).

Đa thức bất khả quy:
Q(X) = X^8 + X^7 + X^5 + X^3 + 1

Biểu diễn hexadecimal: 0x1A9
"""

POLYNOMIAL = 0x1A9


def multiply(a: int, b: int) -> int:
    """
    Nhân hai phần tử trong GF(2^8).

    Phép cộng trong trường là XOR.
    Phép nhân được rút gọn theo Q(X).
    """

    if not (0 <= a < 256 and 0 <= b < 256):
        raise ValueError(
            "GF(2^8) elements must be in [0, 255]"
        )

    result = 0

    for _ in range(8):

        if b & 1:
            result ^= a

        b >>= 1
        a <<= 1

        # Reduction theo Q(X)
        if a & 0x100:
            a ^= POLYNOMIAL

    return result & 0xFF


def power(a: int, exponent: int) -> int:
    """
    Tính a^exponent trong GF(2^8).

    Sử dụng binary exponentiation.
    Hỗ trợ cả số mũ âm khi a != 0.
    """

    if exponent < 0:

        if a == 0:
            raise ZeroDivisionError(
                "Zero has no multiplicative inverse"
            )

        a = inverse(a)
        exponent = -exponent

    result = 1

    while exponent > 0:

        if exponent & 1:
            result = multiply(result, a)

        a = multiply(a, a)
        exponent >>= 1

    return result


def inverse(a: int) -> int:
    """
    Tính nghịch đảo nhân của a trong GF(2^8).

    Với a != 0:
        a^255 = 1
        a^(-1) = a^254
    """

    if a == 0:
        raise ZeroDivisionError(
            "Zero has no multiplicative inverse"
        )

    return power(a, 254)