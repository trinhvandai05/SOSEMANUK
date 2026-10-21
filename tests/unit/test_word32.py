import unittest
from sosemanuk.core.word32 import rotl32, rotr32, load32le, store32le, u32
class TestWord32(unittest.TestCase):
    def test_rotation(self):
        self.assertEqual(rotl32(0x80000001,1),3)
        self.assertEqual(rotr32(3,1),0x80000001)
        self.assertEqual(rotl32(0x12345678,0),0x12345678)
    def test_endian(self):
        self.assertEqual(load32le(bytes.fromhex('78563412')),0x12345678)
        self.assertEqual(store32le(0x12345678).hex(),'78563412')
    def test_mask(self):
        self.assertEqual(u32(0x100000004),4)
