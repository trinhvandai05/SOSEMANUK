"""Serpent1: S2 bitslice of four FSM words, then XOR dropped LFSR words.

Words are passed and returned in chronological order (earliest first).
"""
from .serpent.sbox import apply_sbox

def output_transform(f_values: list[int], dropped: list[int]) -> tuple[int,int,int,int]:
    if len(f_values)!=4 or len(dropped)!=4:
        raise ValueError('expected four FSM and four LFSR words')
    s2_words = apply_sbox(2, tuple(f_values))
    return tuple(a ^ b for a,b in zip(s2_words,dropped))
