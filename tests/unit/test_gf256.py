import unittest
from sosemanuk.core.gf256 import multiply,power,inverse
class TestGF(unittest.TestCase):
    def test_base(self):
        self.assertEqual(multiply(0x80,2),0xa9)
        self.assertEqual(power(2,0),1)
        self.assertEqual(power(2,8),0xa9)
    def test_inverse(self):
        for a in range(1,256):
            self.assertEqual(multiply(a,inverse(a)),1)
    def test_distributive(self):
        for a in range(0,256,13):
            for b in range(0,256,19):
                self.assertEqual(multiply(0x79,a^b), multiply(0x79,a)^multiply(0x79,b))
