
import pytest

from sosemanuk.validation import require_bytes


def test_accept_bytes():
    result = require_bytes(b"hello", "key")
    assert result == b"hello"


def test_accept_bytearray():
    result = require_bytes(bytearray(b"hello"), "key")
    assert result == b"hello"
    assert isinstance(result, bytes)


def test_accept_memoryview():
    result = require_bytes(memoryview(b"hello"), "key")
    assert result == b"hello"
    assert isinstance(result, bytes)


def test_reject_integer():
    with pytest.raises(TypeError):
        require_bytes(16, "key")


def test_reject_string():
    with pytest.raises(TypeError):
        require_bytes("hello", "key")


def test_reject_list():
    with pytest.raises(TypeError):
        require_bytes([1, 2, 3], "key")


def test_reject_none():
    with pytest.raises(TypeError):
        require_bytes(None, "key")


def test_error_message_contains_name():
    with pytest.raises(TypeError, match="secret_key"):
        require_bytes(123, "secret_key")
