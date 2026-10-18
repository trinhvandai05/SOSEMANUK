"""TEST ONLY: full 32-round SERPENT to validate reused Serpent components.
Not imported by production sources.
"""
from sosemanuk.serpent.key_schedule import serpent_key_schedule
from sosemanuk.serpent.sbox import apply_sbox
from sosemanuk.serpent.linear_transform import linear_transform
from sosemanuk.core.word32 import load32le,store32le

def serpent32_encrypt(key: bytes, plaintext: bytes) -> bytes:
    if len(plaintext) != 16:
        raise ValueError('exactly one 128-bit block expected')
    keys=serpent_key_schedule(key,32)
    words=tuple(load32le(plaintext[i:i+4]) for i in range(0,16,4))
    for r in range(32):
        words=tuple(x ^ y for x,y in zip(words,keys[r]))
        words=apply_sbox(r%8,words)
        if r!=31:
            words=linear_transform(words)
    words=tuple(x ^ y for x,y in zip(words,keys[32]))
    return b''.join(store32le(w) for w in words)
