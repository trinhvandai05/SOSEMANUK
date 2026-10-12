"""SOSEMANUK byte-stream API (confidentiality only, no authentication).

Never reuse a (key, IV) pair for independent messages. An instance owns a
mutable stream position. Call process() repeatedly only for consecutive
chunks of the SAME message. Use the module-level encrypt()/decrypt() helpers
for separate messages to start with a fresh keystream.

EDUCATIONAL implementation: not hardened against timing/side-channel attacks.
"""
from .context import KeyContext
from .key_setup import key_setup
from .iv_setup import iv_setup
from .keystream import generate
from .validation import require_bytes


class Sosemanuk:
    def __init__(self, key: bytes | bytearray | memoryview | KeyContext, iv: bytes | bytearray | memoryview):
        key_context = key if isinstance(key, KeyContext) else key_setup(key)
        self.context = iv_setup(key_context, iv)

    def keystream(self, length: int) -> bytes:
        return generate(self.context, length)

    def process(self, data: bytes | bytearray | memoryview) -> bytes:
        """XOR the next bytes in the stream; advances the state."""
        plaintext_or_ciphertext = require_bytes(data, 'data')
        pad = generate(self.context, len(plaintext_or_ciphertext))
        return bytes(p ^ z for p, z in zip(plaintext_or_ciphertext, pad))


def encrypt(key: bytes | bytearray | memoryview | KeyContext,
            iv: bytes | bytearray | memoryview, data: bytes | bytearray | memoryview) -> bytes:
    """Start a new stream and encrypt one complete message."""
    return Sosemanuk(key, iv).process(data)


def decrypt(key: bytes | bytearray | memoryview | KeyContext,
            iv: bytes | bytearray | memoryview, data: bytes | bytearray | memoryview) -> bytes:
    """Start a new stream and decrypt one complete message."""
    return Sosemanuk(key, iv).process(data)
