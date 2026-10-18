import unittest,random
from sosemanuk import Sosemanuk,encrypt,decrypt
class TestAPI(unittest.TestCase):
    key=bytes(range(32)); iv=bytes(range(16))
    def test_roundtrip(self):
        for length in (0,1,2,3,15,16,17,31,32,33,79,80,81,1000):
            msg=bytes((i*37)%256 for i in range(length))
            self.assertEqual(decrypt(self.key,self.iv,encrypt(self.key,self.iv,msg)),msg)
    def test_invalid_inputs(self):
        with self.assertRaises(ValueError): Sosemanuk(b'',self.iv)
        with self.assertRaises(ValueError): Sosemanuk(self.key,b'\x00'*15)
        with self.assertRaises(ValueError): Sosemanuk(self.key,self.iv).keystream(-1)
    def test_reject_integer_key_iv_and_plaintext(self):
        for bad in (16, 'sixteen', [0]*16):
            with self.subTest(arg='key', type=type(bad).__name__):
                with self.assertRaises(TypeError):
                    Sosemanuk(bad, self.iv)
            with self.subTest(arg='iv', type=type(bad).__name__):
                with self.assertRaises(TypeError):
                    Sosemanuk(self.key, bad)
            with self.subTest(arg='data', type=type(bad).__name__):
                with self.assertRaises(TypeError):
                    Sosemanuk(self.key, self.iv).process(bad)

    def test_bytes_like_inputs_are_accepted(self):
        a = Sosemanuk(bytearray(self.key), memoryview(self.iv))
        b = Sosemanuk(self.key, self.iv)
        self.assertEqual(a.process(memoryview(b'hello')), b.process(b'hello'))

    def test_stream_instance_exposes_process_not_message_aliases(self):
        stream = Sosemanuk(self.key, self.iv)
        self.assertFalse(hasattr(stream, 'encrypt'))
        self.assertFalse(hasattr(stream, 'decrypt'))

    def test_module_level_helpers_start_fresh_stream(self):
        plaintext = b'Independent test message'
        ciphertext = encrypt(self.key, self.iv, plaintext)
        self.assertEqual(decrypt(self.key, self.iv, ciphertext), plaintext)

    def test_separate_instances(self):
        a=Sosemanuk(self.key,self.iv)
        b=Sosemanuk(self.key,self.iv)
        self.assertEqual(a.keystream(123),b.keystream(123))
