"""
Các phép toán cơ bản trên số nguyên 32-bit.

Sử dụng trong LFSR, FSM và SERPENT.
"""

MASK32 = 0xFFFFFFFF


def u32(x: int) -> int:
    """Giữ lại 32 bit thấp nhất của x."""
    return x & MASK32


def add32(a: int, b: int) -> int:
    """Cộng hai số modulo 2^32."""
    return (a + b) & MASK32


def rotl32(x: int, n: int) -> int:
    """Xoay vòng 32 bit sang trái n vị trí."""
    x = u32(x)
    n %= 32

    return u32(
        (x << n) | (x >> ((32 - n) % 32))
    )


def rotr32(x: int, n: int) -> int:
    """Xoay vòng 32 bit sang phải n vị trí."""
    return rotl32(x, -n)


def load32le(data: bytes) -> int:
    """Đọc 4 byte theo thứ tự little-endian."""
    if len(data) != 4:
        raise ValueError(
            "load32le requires exactly 4 bytes"
        )

    return int.from_bytes(data, "little")


def store32le(x: int) -> bytes:
    """Chuyển số 32-bit thành 4 byte little-endian."""
    return u32(x).to_bytes(4, "little")