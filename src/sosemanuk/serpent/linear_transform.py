"""Linear transformation from the Serpent block cipher."""
from ..core.word32 import rotl32, rotr32, MASK32

def linear_transform(words: tuple[int,int,int,int]) -> tuple[int,int,int,int]:
    x0,x1,x2,x3 = words
    x0=rotl32(x0,13)
    x2=rotl32(x2,3)
    x1 ^= x0 ^ x2
    x3 ^= x2 ^ ((x0 << 3) & MASK32)
    x1=rotl32(x1,1)
    x3=rotl32(x3,7)
    x0 ^= x1 ^ x3
    x2 ^= x3 ^ ((x1 << 7) & MASK32)
    x0=rotl32(x0,5)
    x2=rotl32(x2,22)
    return x0,x1,x2,x3

def inverse_linear_transform(words: tuple[int,int,int,int]) -> tuple[int,int,int,int]:
    x0,x1,x2,x3 = words
    x2=rotr32(x2,22)
    x0=rotr32(x0,5)
    x2 ^= x3 ^ ((x1 << 7) & MASK32)
    x0 ^= x1 ^ x3
    x3=rotr32(x3,7)
    x1=rotr32(x1,1)
    x3 ^= x2 ^ ((x0 << 3) & MASK32)
    x1 ^= x0 ^ x2
    x2=rotr32(x2,3)
    x0=rotr32(x0,13)
    return x0,x1,x2,x3
