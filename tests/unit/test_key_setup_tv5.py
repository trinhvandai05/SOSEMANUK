
"""Unit tests for TV5 key initialization.

The Serpent key schedule is mocked because its implementation
belongs to another module and is not yet available.
"""

import importlib
import sys
import types

import pytest

from sosemanuk.context import KeyContext


@pytest.fixture
def key_setup_module(monkeypatch):
    """Load key_setup with a mocked Serpent key schedule."""

    module_name = "sosemanuk.serpent.key_schedule"
    fake_module = types.ModuleType(module_name)

    # Mock the unfinished key schedule
    def fake_schedule(key, count):
        assert isinstance(key, bytes)
        assert count == 24
        return ((1, 2, 3, 4),) * count

    # Attach the mock function to the fake module
    fake_module.serpent_key_schedule = fake_schedule

    with monkeypatch.context() as patch:
        patch.setitem(sys.modules, module_name, fake_module)

        # Ensure key_setup imports the mocked dependency
        patch.delitem(
            sys.modules,
            "sosemanuk.key_setup",
            raising=False,
        )

        module = importlib.import_module(
            "sosemanuk.key_setup"
        )

        yield module

    # Remove the mocked version from the module cache
    sys.modules.pop("sosemanuk.key_setup", None)


def test_key_setup_returns_context(key_setup_module):
    """Test that key_setup returns a KeyContext."""
    result = key_setup_module.key_setup(
        b"1234567890123456"
    )

    assert isinstance(result, KeyContext)


def test_key_setup_has_24_subkeys(key_setup_module):
    """Test that the generated context has 24 subkeys."""
    result = key_setup_module.key_setup(
        b"1234567890123456"
    )

    assert len(result.subkeys) == 24


def test_key_setup_accepts_bytearray(key_setup_module):
    """Test that bytearray keys are accepted."""
    result = key_setup_module.key_setup(
        bytearray(b"1234567890123456")
    )

    assert isinstance(result, KeyContext)


def test_key_setup_accepts_memoryview(key_setup_module):
    """Test that memoryview keys are accepted."""
    result = key_setup_module.key_setup(
        memoryview(b"1234567890123456")
    )

    assert isinstance(result, KeyContext)


def test_key_setup_rejects_string(key_setup_module):
    """Test that string keys are rejected."""
    with pytest.raises(TypeError):
        key_setup_module.key_setup("invalid_key")


def test_key_setup_rejects_integer(key_setup_module):
    """Test that integer keys are rejected."""
    with pytest.raises(TypeError):
        key_setup_module.key_setup(12345)


def test_key_setup_passes_key_to_schedule(
    key_setup_module, monkeypatch
):
    """Test that the correct key and count are passed."""

    received = []

    def recording_schedule(key, count):
        received.append((key, count))
        return ((1, 2, 3, 4),) * count

    monkeypatch.setattr(
        key_setup_module,
        "serpent_key_schedule",
        recording_schedule,
    )

    key_setup_module.key_setup(b"test_key")

    assert received == [(b"test_key", 24)]
