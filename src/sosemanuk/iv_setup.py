"""IV injection and state loading (1-based spec indices -> Python 0-based)."""
from .context import KeyContext, StreamContext
from .serpent.serpent24 import serpent24
from .validation import require_bytes


def map_initial_state(checkpoints: dict[int, tuple[int, int, int, int]]) -> StreamContext:
    y12 = checkpoints[12]
    y18 = checkpoints[18]
    y24 = checkpoints[24]
    s = [y24[3], y24[2], y24[1], y24[0], y18[1], y18[3],
         y12[3], y12[2], y12[1], y12[0]]
    return StreamContext(s=s, r1=y18[0], r2=y18[2])


def iv_setup(key_context: KeyContext, iv: bytes | bytearray | memoryview) -> StreamContext:
    return map_initial_state(serpent24(require_bytes(iv, 'iv'), key_context.subkeys))
