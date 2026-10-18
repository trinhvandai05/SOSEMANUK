import unittest
from sosemanuk import key_setup,iv_setup
from sosemanuk.keystream import clock,generate
from sosemanuk.context import StreamContext
from sosemanuk.serpent.serpent24 import serpent24
from sosemanuk.iv_setup import map_initial_state
class TestContext(unittest.TestCase):
    def test_initial_mapping(self):
        cp={12:(1,2,3,4),18:(5,6,7,8),24:(9,10,11,12)}
        ctx=map_initial_state(cp)
        self.assertEqual(ctx.s,[12,11,10,9,6,8,4,3,2,1])
        self.assertEqual((ctx.r1,ctx.r2),(5,7))
    def test_isolation_and_buffer(self):
        key=key_setup(bytes(range(32)))
        ctx1=iv_setup(key,bytes(16))
        ctx2=iv_setup(key,bytes(16))
        self.assertEqual(generate(ctx1,3)+generate(ctx1,39),generate(ctx2,42))
        self.assertEqual(ctx1.s,ctx2.s)
        ctx3=iv_setup(key,bytes([1])+bytes(15))
        self.assertNotEqual(ctx2.s,ctx3.s)
    def test_clock_word_width(self):
        ctx=iv_setup(key_setup(bytes(range(16))),bytes(16))
        for _ in range(100):
            d,f=clock(ctx)
            self.assertTrue(0 <= d < 2**32 and 0 <= f < 2**32)
            self.assertTrue(all(0<=w<2**32 for w in ctx.s))
