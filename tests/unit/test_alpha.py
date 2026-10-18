import unittest,random
from sosemanuk.core.alpha import *
class TestAlpha(unittest.TestCase):
    def test_reference_entry(self):
        self.assertEqual(MUL_ALPHA_TABLE[0],0)
        self.assertEqual(MUL_ALPHA_TABLE[1],0xe19fcf13)
        self.assertEqual(mul_alpha(0x01000000),0xe19fcf13)
        self.assertEqual(div_alpha(0x00000100),1)
    def test_inverse(self):
        for x in (0,1,0xffffffff,0x80000000,0x01000000):
            self.assertEqual(div_alpha(mul_alpha(x)),x)
        rand=random.Random(12345)
        for _ in range(500):
            x=rand.getrandbits(32)
            self.assertEqual(div_alpha(mul_alpha(x)),x)
    def test_linearity(self):
        for x,y in [(0x77ff0099,0x12345678),(0x1,0xfedcba98)]:
            self.assertEqual(mul_alpha(x^y),mul_alpha(x)^mul_alpha(y))
