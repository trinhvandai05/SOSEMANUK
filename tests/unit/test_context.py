
import pytest
from dataclasses import FrozenInstanceError

from sosemanuk.context import KeyContext, StreamContext


def test_key_context_creation():
    """Test creating a KeyContext."""
    subkeys = ((1, 2, 3, 4),)
    ctx = KeyContext(subkeys=subkeys)

    assert ctx.subkeys == subkeys


def test_key_context_immutable():
    """Test KeyContext cannot be reassigned."""
    ctx = KeyContext(subkeys=((1, 2, 3, 4),))

    with pytest.raises(FrozenInstanceError):
        ctx.subkeys = ((5, 6, 7, 8),)


def test_stream_context_creation():
    """Test creating a StreamContext."""
    ctx = StreamContext(
        s=[0] * 10,
        r1=1,
        r2=2
    )

    assert len(ctx.s) == 10
    assert ctx.r1 == 1
    assert ctx.r2 == 2
    assert ctx.buffer == b''
    assert ctx.buffer_pos == 0


def test_stream_context_mutable():
    """Test StreamContext supports state updates."""
    ctx = StreamContext(
        s=[0] * 10,
        r1=1,
        r2=2
    )

    ctx.r1 = 100
    ctx.r2 = 200
    ctx.s[0] = 123

    assert ctx.r1 == 100
    assert ctx.r2 == 200
    assert ctx.s[0] == 123


def test_stream_context_invalid_state():
    """Test rejecting an invalid LFSR state length."""
    with pytest.raises(ValueError):
        StreamContext(
            s=[0] * 5,
            r1=1,
            r2=2
        )
