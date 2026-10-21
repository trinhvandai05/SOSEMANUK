<<<<<<< HEAD
"""
LFSR 320-bit của SOSEMANUK.

s[t+10] = s[t+9] XOR div_alpha(s[t+3])
                    XOR mul_alpha(s[t])
"""

from .alpha import mul_alpha, div_alpha

LFSR_SIZE = 10


def lfsr_step(words: list[int]) -> int:
    """
    Cập nhật LFSR một clock.

    Input:
        words: list gồm 10 word 32-bit

    Output:
        Word cũ words[0] bị đẩy ra

    Side effect:
        Cập nhật trực tiếp words.
    """

    if len(words) != LFSR_SIZE:
        raise ValueError("LFSR requires exactly 10 words")

    dropped = words[0]

    new_word = (
        words[9]
        ^ div_alpha(words[3])
        ^ mul_alpha(words[0])
    )

    words[:] = words[1:] + [new_word]

    return dropped
=======
# Công Hùng
"""10-word LFSR; list[0] is the oldest word (s_t)."""
from .alpha import mul_alpha, div_alpha

def lfsr_step(words: list[int]) -> int:
    """Mutate ten words in place and return discarded s_t."""
    if len(words) != 10:
        raise ValueError('LFSR needs exactly 10 words')
    dropped = words[0]
    newest = words[9] ^ div_alpha(words[3]) ^ mul_alpha(words[0])
    words[:] = words[1:] + [newest]
    return dropped
>>>>>>> 3157cced6792c93eebea13203ac43b83e7a0b090
