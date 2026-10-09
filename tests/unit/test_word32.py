import unittest

from sosemanuk.core.word32 import (
    u32,
    add32,
    rotl32,
    rotr32,
    load32le,
    store32le,
)


class TestWord32(unittest.TestCase):

    def test_u32_overflow(self):
        self.assertEqual(u32(0x100000004), 4)
        self.assertEqual(u32(-1), 0xFFFFFFFF)

    def test_add32(self):
        self.assertEqual(add32(0xFFFFFFFF, 2), 1)
        self.assertEqual(add32(2, 3), 5)

    def test_rotl32(self):
        self.assertEqual(rotl32(0x80000001, 1), 3)
        self.assertEqual(rotl32(0x12345678, 8), 0x34567812)
        self.assertEqual(rotl32(0x12345678, 0), 0x12345678)
        self.assertEqual(rotl32(0x12345678, 32), 0x12345678)

    def test_rotr32(self):
        self.assertEqual(rotr32(3, 1), 0x80000001)
        self.assertEqual(rotr32(0x12345678, 8), 0x78123456)

    def test_little_endian(self):
        self.assertEqual(
            load32le(bytes.fromhex("78563412")),
            0x12345678,
        )
        self.assertEqual(
            store32le(0x12345678).hex(),
            "78563412",
        )

    def test_bad_input(self):
        with self.assertRaises(ValueError):
            load32le(b"abc")


if __name__ == "__main__":
    unittest.main()