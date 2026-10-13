"""Key setup runs once per secret key; its context is reusable."""
from .context import KeyContext
from .serpent.key_schedule import serpent_key_schedule
from .validation import require_bytes


def key_setup(key: bytes | bytearray | memoryview) -> KeyContext:
    return KeyContext(serpent_key_schedule(require_bytes(key, 'key'), 24))
