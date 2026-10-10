"""
FSM phi tuyến của SOSEMANUK.

Quy ước:
    words[0] = s_t
    words[9] = s_(t+9)

FSM chỉ đọc LFSR, không cập nhật LFSR.
"""

from .word32 import MASK32, rotl32

TRANS_MULTIPLIER = 0x54655307


def mux(control: int, x: int, delta: int) -> int:
    """
    Nếu LSB(control) = 0: trả về x.
    Nếu LSB(control) = 1: trả về x XOR delta.

    Trong SOSEMANUK:
        x     = s_(t+1)
        delta = s_(t+8)
    """
    return x ^ (delta if (control & 1) else 0)


def trans(x: int) -> int:
    """
    Trans(x) = ROTL32(
        (0x54655307 * x) mod 2^32,
        7
    )
    """
    return rotl32(
        (TRANS_MULTIPLIER * x) & MASK32,
        7
    )


def fsm_step(
    r1: int,
    r2: int,
    words: list[int]
) -> tuple[int, int, int]:
    """
    Thực hiện một clock FSM.

    Input:
        r1: R1 cũ
        r2: R2 cũ
        words: 10 word của LFSR hiện tại

    Output:
        (new_r1, new_r2, f_t)

    Không thay đổi trực tiếp LFSR.
    """

    if len(words) != 10:
        raise ValueError(
            "FSM requires exactly 10 LFSR words"
        )

    # Bước 1: Cập nhật R1
    new_r1 = (
        r2 + mux(r1, words[1], words[8])
    ) & MASK32

    # Bước 2: Cập nhật R2 bằng R1 CŨ
    new_r2 = trans(r1)

    # Bước 3: Tính f_t
    f = (
        ((words[9] + new_r1) & MASK32)
        ^ new_r2
    ) & MASK32

    return new_r1, new_r2, f