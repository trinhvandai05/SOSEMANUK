# Công Hùng
""FSM step uses OLD LFSR words and OLD R1 for the mux and Trans."""
from .word32 import MASK32, rotl32
TRANS_MULTIPLIER = 0x54655307

def trans(x: int) -> int:
    return rotl32((x * TRANS_MULTIPLIER) & MASK32, 7)

def mux(control: int, x: int, y: int) -> int:
    """Select x or x XOR y based on the least significant control bit."""
    return x ^ (y if (control & 1) else 0)

def fsm_step(r1: int, r2: int, words: list[int]) -> tuple[int, int, int]:
    """Return new_r1, new_r2, f_t, without modifying the LFSR."""
    if len(words) != 10:
        raise ValueError('FSM needs 10 LFSR words')
    new_r1 = (r2 + mux(r1, words[1], words[8])) & MASK32
    new_r2 = trans(r1)
    f = ((words[9] + new_r1) & MASK32) ^ new_r2
    return new_r1, new_r2, f