import unittest
from sosemanuk.output_transform import output_transform
from sosemanuk.serpent.sbox import apply_sbox
class TestOutput(unittest.TestCase):
    def test_serpent1_and_whitening(self):
        f=[0,0xffffffff,0xaaaaaaaa,0x12345678]
        dropped=[0,1,2,3]
        expected=[a^b for a,b in zip(apply_sbox(2,tuple(f)),dropped)]
        self.assertEqual(list(output_transform(f,dropped)),expected)
    def test_no_lt_or_key_add(self):
        self.assertEqual(output_transform([0]*4,[0]*4),(0,0,0,0xffffffff))
