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
