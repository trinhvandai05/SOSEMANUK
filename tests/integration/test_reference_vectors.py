import unittest,json,pathlib
from sosemanuk import Sosemanuk
HERE=pathlib.Path(__file__).resolve().parents[1]
class TestKnownAnswer(unittest.TestCase):
    def test_known_answer(self):
        vectors=json.loads((HERE/'vectors'/'estream_vectors.json').read_text())
        for v in vectors:
            with self.subTest(vector=v['id']):
                key=bytes.fromhex(v['key'])
                iv=bytes.fromhex(v['iv'])
                expected=bytes.fromhex(v['keystream'])
                self.assertEqual(Sosemanuk(key,iv).keystream(len(expected)),expected)

    def test_estream_131072_byte_xor_digest(self):
        # eSTREAM Set 6, vector 3: XOR 2,048 consecutive 64-byte chunks.
        v=json.loads((HERE/'vectors'/'estream_digest.json').read_text())
        ciphertext=Sosemanuk(bytes.fromhex(v['key']),bytes.fromhex(v['iv'])).keystream(v['length'])
        digest=bytearray(64)
        for i, value in enumerate(ciphertext):
            digest[i%64] ^= value
        self.assertEqual(digest.hex(),v['xor_digest_64'].lower())
