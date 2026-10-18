"""Standard Serpent prekeys; SOSEMANUK retains 25 round keys (100 words)."""
from ..core.word32 import MASK32, rotl32
from .sbox import apply_sbox
PHI = 0x9e3779b9

def serpent_key_schedule(key: bytes, rounds: int=24) -> tuple[tuple[int,int,int,int], ...]:
    """Produce rounds+1 Serpent subkeys; supports 1..32 byte keys.

Short byte-aligned keys are padded with 0x01 and then zero bytes.
    """
    if not (1 <= len(key) <= 32):
        raise ValueError('Serpent/SOSEMANUK key must be 1..32 bytes')
    if not (1 <= rounds <= 32):
        raise ValueError('number of rounds must be 1..32')
    padded = key + (bytes([1]) + bytes(31-len(key)) if len(key) < 32 else b'')
    w = [int.from_bytes(padded[4*i:4*i+4], 'little') for i in range(8)]
    for i in range(4*(rounds+1)):
        w.append(rotl32(w[i] ^ w[i+3] ^ w[i+5] ^ w[i+7] ^ PHI ^ i, 11))
    subkeys = []
    for round_index in range(rounds+1):
        block = tuple(w[8+4*round_index:12+4*round_index])
        subkeys.append(apply_sbox((3-round_index)%8, block))
    return tuple(subkeys)
