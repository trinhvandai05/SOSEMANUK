import unittest
from tests.support.serpent32 import serpent32_encrypt
class TestSerpent32Oracle(unittest.TestCase):
    def test_libgcrypt_and_nettle_vectors(self):
        # Byte ordering as used by libgcrypt/nettle, not byte-reversed NESSIE printout.
        vectors=[
            ('00'*16,'d29d576fcea3a3a7ed9099f29273d78e','b2288b968ae8b08648d1ce9606fd992d'),
            ('00'*32,'d095576fcea3e3a7ed98d9f29073d78e','b90ee5862de69168f2bdd5125b45472b'),
            ('000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f',
             '00112233445566778899aabbccddeeff','2868b7a2d28ecd5e4fdefac3c4330074'),
        ]
        for key,pt,expected in vectors:
            with self.subTest(key=key):
                self.assertEqual(serpent32_encrypt(bytes.fromhex(key),bytes.fromhex(pt)).hex(),expected)
                
                