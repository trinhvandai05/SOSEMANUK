"""Reference C-trace tests. SKIPPED until a verified C fixture is provided.

Isolation rule: every test imports ONLY the module it checks and takes all
other inputs from the C fixture (subkeys, initial state, LFSR windows).
So TV2/TV3 can run their trace tests before TV4/TV5 exist, and a bug in one
module fails only that module's test instead of cascading.

    test_c_subkeys_all_25            serpent_key_schedule   (TV4)
    test_c_serpent24_checkpoints...  serpent24, C subkeys    (TV4)
    test_c_initial_state             iv_setup,  C subkeys    (TV5)
    test_c_fsm_first_eight           fsm_step,  C windows    (TV2)
    test_c_lfsr_first_eight          lfsr_step, C windows    (TV2)
    test_c_output_transform...       S2 + output_transform   (TV3)
    test_c_first_two_blocks          generate_block, C state (TV6)
"""
import json
import unittest
from pathlib import Path
import os
from tests.support.trace_guard import verify_trace

ROOT = Path(__file__).resolve().parents[2]
TRACE = Path(os.environ.get('SOSEMANUK_REFERENCE_TRACE', str(ROOT / 'tests/vectors/reference_trace.json')))
RAW = Path(os.environ.get('SOSEMANUK_REFERENCE_STDOUT', str(ROOT / 'tools/ref_diff/c_reference_stdout.txt')))


def load_trace():
    return verify_trace(TRACE, RAW)['vectors']


def c_subkeys(v):
    return tuple(tuple(k) for k in v['subkeys'])


def window_before(v, n):
    """LFSR words (s_t .. s_t+9) right before clock n (0-based), from C only."""
    return list(v['initial_state']['s'] if n == 0 else v['clocks'][n - 1]['after_s'])


def registers_before(v, n):
    if n == 0:
        return v['initial_state']['r1'], v['initial_state']['r2']
    return v['clocks'][n - 1]['r1'], v['clocks'][n - 1]['r2']


@unittest.skipUnless(TRACE.exists(), 'G2/G4/G5 NOT VERIFIED: independent C reference_trace.json absent')
class TestReferenceTrace(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Only the fixture here: no project import, so a missing module never
        # turns every trace test into an ERROR.
        cls.vectors = load_trace()

    def each(self):
        for v in self.vectors:
            yield v, bytes.fromhex(v['key']), bytes.fromhex(v['iv'])

    def test_c_subkeys_all_25(self):
        from sosemanuk.serpent.key_schedule import serpent_key_schedule
        for v, key, _ in self.each():
            with self.subTest(key=v['key']):
                self.assertEqual([list(k) for k in serpent_key_schedule(key, 24)], v['subkeys'])

    def test_c_serpent24_checkpoints_via_initial_state(self):
        """Indirect checkpoint oracle: the 12 initial words ARE the 12 checkpoint words.

        Uses C subkeys, so a key-schedule bug cannot leak in. If this passes but
        test_c_initial_state fails, the bug is in the mapping (TV5), not Serpent24.
        """
        from sosemanuk.serpent.serpent24 import serpent24
        for v, _, iv in self.each():
            cp = serpent24(iv, c_subkeys(v))
            i = v['initial_state']; s = i['s']
            with self.subTest(key=v['key']):
                self.assertEqual(list(cp[12]), [s[9], s[8], s[7], s[6]])
                self.assertEqual(list(cp[18]), [i['r1'], s[4], i['r2'], s[5]])
                self.assertEqual(list(cp[24]), [s[3], s[2], s[1], s[0]])

    def test_c_initial_state(self):
        from sosemanuk.context import KeyContext
        from sosemanuk.iv_setup import iv_setup
        for v, _, iv in self.each():
            i = v['initial_state']
            st = iv_setup(KeyContext(c_subkeys(v)), iv)
            with self.subTest(key=v['key']):
                self.assertEqual(st.s, i['s'])
                self.assertEqual((st.r1, st.r2), (i['r1'], i['r2']))

    def test_c_fsm_first_eight(self):
        from sosemanuk.core.fsm import fsm_step
        for v, _, _ in self.each():
            for n, c in enumerate(v['clocks'][:8]):
                r1, r2 = registers_before(v, n)
                with self.subTest(key=v['key'], step=n + 1):
                    self.assertEqual(fsm_step(r1, r2, window_before(v, n)), (c['r1'], c['r2'], c['f']))

    def test_c_lfsr_first_eight(self):
        from sosemanuk.core.lfsr import lfsr_step
        for v, _, _ in self.each():
            for n, c in enumerate(v['clocks'][:8]):
                s = window_before(v, n)
                with self.subTest(key=v['key'], step=n + 1):
                    self.assertEqual((lfsr_step(s), s), (c['dropped'], c['after_s']))

    def test_c_output_transform_first_two_blocks(self):
        from sosemanuk.output_transform import output_transform
        from sosemanuk.serpent.sbox import apply_sbox
        for v, _, _ in self.each():
            cs = v['clocks']
            for b in range(2):
                blk = v['serpent_blocks'][b]
                dropped = [c['dropped'] for c in cs[4 * b:4 * b + 4]]
                with self.subTest(key=v['key'], block=b):
                    self.assertEqual(blk['input'], [x['f'] for x in cs[4 * b:4 * b + 4]])
                    # C prints Serpent1 output BEFORE whitening with dropped words.
                    self.assertEqual(list(apply_sbox(2, tuple(blk['input']))), blk['output'])
                    expected = [x ^ y for x, y in zip(blk['output'], dropped)]
                    self.assertEqual(list(output_transform(blk['input'], dropped)), expected)

    def test_c_first_two_blocks(self):
        from sosemanuk.context import StreamContext
        from sosemanuk.keystream import generate_block
        for v, _, _ in self.each():
            i = v['initial_state']
            st = StreamContext(s=list(i['s']), r1=i['r1'], r2=i['r2'])
            with self.subTest(key=v['key']):
                self.assertEqual([generate_block(st).hex() for _ in range(2)], v['stream_blocks'][:2])

    def test_c_trace_provenance_structure(self):
        for v in self.vectors:
            with self.subTest(key=v['key']):
                self.assertEqual(len(v['subkeys']), 25)
                self.assertEqual(len(v['initial_state']['s']), 10)
                self.assertGreaterEqual(len(v['clocks']), 8)
                self.assertTrue(all(len(x) == 32 for x in v['stream_blocks']))


if __name__ == '__main__':
    unittest.main()
