"""KeyContext is immutable; StreamContext is mutable and not thread-safe."""
from dataclasses import dataclass, field

@dataclass(frozen=True)
class KeyContext:
    subkeys: tuple[tuple[int,int,int,int], ...]

@dataclass
class StreamContext:
    s: list[int]
    r1: int
    r2: int
    buffer: bytes = b''
    buffer_pos: int = 0
    def __post_init__(self):
        if len(self.s) != 10:
            raise ValueError('internal LFSR state must contain 10 words')
