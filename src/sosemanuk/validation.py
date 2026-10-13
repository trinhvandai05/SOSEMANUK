"""Strict conversion of cryptographic byte inputs.

Never call bytes(number): bytes(16) silently creates a known all-zero key.
"""


def require_bytes(value: object, name: str) -> bytes:
    """Accept byte-oriented values only; fail closed for ints/str/lists."""
    if not isinstance(value, (bytes, bytearray, memoryview)):
        raise TypeError(f"{name} must be bytes-like, got {type(value).__name__}")
    return bytes(value)
