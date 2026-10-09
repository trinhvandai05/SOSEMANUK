"""Các phép toán cơ bản trên số nguyên 32-bit."""

MASK32 = 0xFFFFFFFF


def u32(x: int) -> int:
    """Giữ lại 32 bit thấp nhất."""
    return x & MASK32


def add32(a: int, b: int) -> int:
    """Cộng hai số theo modulo 2^32."""
    return (a + b) & MASK32


def rotl32(x: int, n: int) -> int:
    """Rotate-left trên 32 bit."""
    x = u32(x)
    n %= 32

    return u32(
        (x << n) | (x >> ((32 - n) % 32))
    )


def rotr32(x: int, n: int) -> int:
    """Rotate-right trên 32 bit."""
    return rotl32(x, -n)


def load32le(data: bytes) -> int:
    """Đọc đúng 4 byte ở thứ tự little-endian."""
    if len(data) != 4:
        raise ValueError("load32le yêu cầu đúng 4 byte")

    return int.from_bytes(data, byteorder="little")


def store32le(x: int) -> bytes:
    """Chuyển số 32-bit thành 4 byte little-endian."""
    return u32(x).to_bytes(4, byteorder="little")