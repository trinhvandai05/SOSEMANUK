import unittest
from sosemanuk.validation import require_bytes


class TestValidation(unittest.TestCase):
    def test_byteslike_inputs(self):
        for value in (b'abc', bytearray(b'abc'), memoryview(b'abc')):
            with self.subTest(value=type(value).__name__):
                self.assertEqual(require_bytes(value, 'key'), b'abc')
                self.assertIs(type(require_bytes(value, 'key')), bytes)

    def test_rejects_unintended_inputs(self):
        for value in (0, 16, 'abc', [0, 1, 2], None):
            with self.subTest(value=repr(value)):
                with self.assertRaises(TypeError):
                    require_bytes(value, 'key')
