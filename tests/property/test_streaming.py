import unittest,random
from sosemanuk import Sosemanuk
class TestStreaming(unittest.TestCase):
    def test_chunk_splits(self):
        random_gen=random.Random(42)
        k=bytes(range(32));iv=bytes(range(16))
        data=bytes(random_gen.getrandbits(8) for _ in range(553))
        expected=Sosemanuk(k,iv).process(data)
        for seed in range(20):
            r=random.Random(seed)
            c=Sosemanuk(k,iv)
            parts=[];i=0
            while i<len(data):
                count=r.randint(1,39)
                parts.append(c.process(data[i:i+count]))
                i+=count
            self.assertEqual(b''.join(parts),expected)
    def test_non_multiple_of_block(self):
        k=bytes(range(16));iv=bytes(range(16))
        a=Sosemanuk(k,iv);b=Sosemanuk(k,iv)
        self.assertEqual(a.keystream(1)+a.keystream(15)+a.keystream(1),b.keystream(17))
