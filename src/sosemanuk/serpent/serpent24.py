"""Reduced Serpent for IV injection, with three checkpoints.

All 24 rounds include the LT; after round 24, XOR K24 before
returning checkpoint 24. Checkpoints 12 and 18 are after LT only.
"""
from ..core.word32 import load32le
from .sbox import apply_sbox
from .linear_transform import linear_transform

def serpent24(iv: bytes, subkeys: tuple) -> dict[int,tuple[int,int,int,int]]:
    if len(iv) != 16:
        raise ValueError('IV must contain exactly 16 bytes')
    if len(subkeys) != 25:
        raise ValueError('Serpent24 requires 25 subkeys')
    state = tuple(load32le(iv[4*i:4*i+4]) for i in range(4))
    checkpoints = {}
    for r in range(24):
        state = tuple(x ^ k for x,k in zip(state,subkeys[r]))
        state = apply_sbox(r % 8, state)
        state = linear_transform(state)
        if r+1 in (12,18):
            checkpoints[r+1] = state
    state = tuple(x ^ k for x,k in zip(state,subkeys[24]))
    checkpoints[24] = state
    return checkpoints
