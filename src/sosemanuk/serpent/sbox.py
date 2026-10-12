"""Original Serpent S0..S7, bitsliced on four 32-bit lanes.

Input words are x0..x3: their bit j values encode a nibble with x0
as the LOW bit. The reference version deliberately prioritizes clarity.
"""
SBOXES = (
    (3,8,15,1,10,6,5,11,14,13,4,2,7,0,9,12),
    (15,12,2,7,9,0,5,10,1,11,14,8,6,13,3,4),
    (8,6,7,9,3,12,10,15,13,1,14,4,0,11,5,2),
    (0,15,11,8,12,9,6,3,13,1,2,4,10,7,5,14),
    (1,15,8,3,12,0,11,6,2,5,4,10,9,14,7,13),
    (15,5,2,11,4,10,9,12,0,3,14,8,13,6,7,1),
    (7,2,12,5,8,4,6,11,14,9,1,15,13,3,10,0),
    (1,13,15,0,14,8,2,11,7,4,12,10,9,3,5,6),
)

def apply_sbox(box: int, words: tuple[int,int,int,int] | list[int]) -> tuple[int,int,int,int]:
    if not (0 <= box < 8) or len(words) != 4:
        raise ValueError('invalid S-box or word count')
    result = [0,0,0,0]
    table = SBOXES[box]
    for bit in range(32):
        nibble = sum(((words[lane] >> bit) & 1) << lane for lane in range(4))
        mapped = table[nibble]
        for lane in range(4):
            result[lane] |= ((mapped >> lane) & 1) << bit
    return tuple(result)

def apply_sbox_minterms(box: int, words: tuple[int,int,int,int]) -> tuple[int,int,int,int]:
    """Independent truth-table formulation (Boolean masks), for comparison."""
    from ..core.word32 import MASK32
    inv = [MASK32 ^ w for w in words]
    result = [0,0,0,0]
    for val, mapped in enumerate(SBOXES[box]):
        mask = MASK32
        for lane in range(4):
            mask &= words[lane] if ((val >> lane) & 1) else inv[lane]
        for lane in range(4):
            if (mapped >> lane) & 1:
                result[lane] |= mask
    return tuple(w & MASK32 for w in result)
