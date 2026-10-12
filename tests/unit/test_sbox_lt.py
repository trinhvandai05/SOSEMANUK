import unittest
import random
from sosemanuk.serpent.sbox import SBOXES, apply_sbox, apply_sbox_minterms
from sosemanuk.serpent.linear_transform import linear_transform, inverse_linear_transform


class TestSboxAndLT(unittest.TestCase):
    def test_sboxes_exhaustive(self):
        for k, table in enumerate(SBOXES):
            self.assertEqual(sorted(table), list(range(16)))
            for nibble in range(16):
                words = tuple((nibble >> lane) & 1 for lane in range(4))
                result = apply_sbox(k, words)
                result_nibble = sum((result[lane] & 1) << lane for lane in range(4))
                self.assertEqual(result_nibble, table[nibble])

    def test_bitslice_word_packing_equivalence(self):
        """Checks equivalent bit packing; both paths share the same S-box tables."""
        rnd = random.Random(987)
        for _ in range(30):
            x = tuple(rnd.getrandbits(32) for i in range(4))
            for k in range(8):
                self.assertEqual(apply_sbox(k, x), apply_sbox_minterms(k, x))

    def test_lt_inverse(self):
        rnd = random.Random(123)
        for _ in range(50):
            x = tuple(rnd.getrandbits(32) for i in range(4))
            self.assertEqual(inverse_linear_transform(linear_transform(x)), x)
