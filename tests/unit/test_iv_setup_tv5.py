
"""Unit tests for TV5 IV setup and initial state mapping."""

import importlib
import sys
import types

import pytest

from sosemanuk.context import KeyContext, StreamContext


@pytest.fixture
def checkpoints():
    """Deterministic Serpent24 checkpoints."""
    return {
        12: (120, 121, 122, 123),
        18: (180, 181, 182, 183),
        24: (240, 241, 242, 243),
    }


@pytest.fixture
def iv_module(monkeypatch, checkpoints):
    """Mock Serpent24 before importing IV setup."""

    module_name = "sosemanuk.serpent.serpent24"
    fake_module = types.ModuleType(module_name)

    calls = []

    def fake_serpent24(iv, subkeys):
        calls.append((iv, subkeys))
        return checkpoints

    fake_module.serpent24 = fake_serpent24

    with monkeypatch.context() as patch:
        patch.setitem(
            sys.modules,
            module_name,
            fake_module,
        )

        # Import IV setup with the mocked dependency.
        sys.modules.pop("sosemanuk.iv_setup", None)

        module = importlib.import_module(
            "sosemanuk.iv_setup"
        )

        yield module, calls

    sys.modules.pop("sosemanuk.iv_setup", None)


def make_key_context():
    """Create a deterministic key context."""
    subkeys = ((1, 2, 3, 4),) * 24
    return KeyContext(subkeys=subkeys)


# ==========================================
# TEST GROUP 1: INITIAL STATE MAPPING
# ==========================================

def test_map_returns_stream_context(iv_module, checkpoints):
    module, _ = iv_module

    result = module.map_initial_state(checkpoints)

    assert isinstance(result, StreamContext)


def test_map_contains_10_words(iv_module, checkpoints):
    module, _ = iv_module

    result = module.map_initial_state(checkpoints)

    assert len(result.s) == 10


def test_map_word_order(iv_module, checkpoints):
    module, _ = iv_module

    result = module.map_initial_state(checkpoints)

    expected = [
        243, 242, 241, 240,
        181, 183,
        123, 122, 121, 120,
    ]

    assert result.s == expected


def test_map_fsm_registers(iv_module, checkpoints):
    module, _ = iv_module

    result = module.map_initial_state(checkpoints)

    assert result.r1 == 180
    assert result.r2 == 182


def test_map_initial_buffer_empty(iv_module, checkpoints):
    module, _ = iv_module

    result = module.map_initial_state(checkpoints)

    assert result.buffer == b""
    assert result.buffer_pos == 0


# ==========================================
# TEST GROUP 2: IV INPUT VALIDATION
# ==========================================

def test_iv_accepts_bytes(iv_module):
    module, _ = iv_module

    result = module.iv_setup(
        make_key_context(),
        b"test_iv",
    )

    assert isinstance(result, StreamContext)


def test_iv_accepts_bytearray(iv_module):
    module, calls = iv_module

    result = module.iv_setup(
        make_key_context(),
        bytearray(b"test_iv"),
    )

    assert isinstance(result, StreamContext)
    assert calls[0][0] == b"test_iv"


def test_iv_accepts_memoryview(iv_module):
    module, calls = iv_module

    result = module.iv_setup(
        make_key_context(),
        memoryview(b"test_iv"),
    )

    assert isinstance(result, StreamContext)
    assert calls[0][0] == b"test_iv"


def test_iv_rejects_invalid_types(iv_module):
    module, _ = iv_module

    invalid_values = [
        123,
        "invalid_iv",
        [1, 2, 3],
        None,
    ]

    for value in invalid_values:
        with pytest.raises(TypeError):
            module.iv_setup(
                make_key_context(),
                value,
            )


# ==========================================
# TEST GROUP 3: SERPENT24 INTEGRATION MOCK
# ==========================================

def test_iv_passes_correct_arguments(iv_module):
    module, calls = iv_module

    context = make_key_context()
    iv = b"test_iv"

    result = module.iv_setup(context, iv)

    assert calls == [
        (iv, context.subkeys)
    ]

    assert isinstance(result, StreamContext)
