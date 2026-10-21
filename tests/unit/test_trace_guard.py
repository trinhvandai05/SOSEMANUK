"""Regression tests that block the empty/forged-fixture strict-mode loophole.

Synthetic objects used here only test validation, NEVER serve as oracle values.
"""
import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests.support.trace_guard import TraceValidationError, validate_shape, verify_trace

ROOT = Path(__file__).resolve().parents[2]


def synthetic_shape_only():
    # Intentionally NOT a valid SOSEMANUK trace: schema-focused test input.
    clock = {'r1': 0, 'r2': 0, 'f': 0, 'dropped': 0, 'after_s': [0] * 10}
    block = {'input': [0] * 4, 'output': [0] * 4}
    v = {'key': '01', 'iv': '00' * 16, 'subkeys': [[0]*4 for _ in range(25)],
         'initial_state': {'s': [0]*10, 'r1': 0, 'r2': 0},
         'clocks': [copy.deepcopy(clock) for _ in range(8)],
         'serpent_blocks': [copy.deepcopy(block) for _ in range(2)],
         'stream_blocks': ['00'*16]*10}
    v2 = copy.deepcopy(v)
    v2['key'] = '02'
    return {'source_kind': 'author_c_stdout_SOSEMANUK_VECTOR',
            'source_url':'https://github.com/cchcc/SOSEMANUK/blob/master/C/SOSEMANUK.C',
            'raw_stdout_sha256': '0'*64, 'normalized_stdout_sha256': '0'*64,
            'raw_stdout_encoding':'utf-8',
            'source_git_commit':'0'*40, 'source_c_sha256':'0'*64,
            'source_h_sha256':'0'*64, 'compiler':'gcc test',
            'build_command':'gcc -DSOSEMANUK_VECTOR', 'vectors': [v,v2]}


class TestTraceGuard(unittest.TestCase):
    def test_schema_example_does_not_mean_oracle(self):
        fake = synthetic_shape_only()
        validate_shape(fake)
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            (p/'reference_trace.json').write_text(json.dumps(fake),encoding='utf-8')
            with self.assertRaisesRegex(TraceValidationError, 'ORIGINAL C stdout'):
                verify_trace(p/'reference_trace.json', p/'missing.log')

    def test_empty_vectors_rejected(self):
        fake = synthetic_shape_only()
        fake['vectors'] = []
        with self.assertRaisesRegex(TraceValidationError, 'At least 2'):
            validate_shape(fake)

    def test_duplicate_vectors_rejected(self):
        fake = synthetic_shape_only()
        fake['vectors'][1]['key'] = fake['vectors'][0]['key']
        with self.assertRaisesRegex(TraceValidationError, 'duplicated'):
            validate_shape(fake)

    def test_insufficient_clocks_rejected(self):
        fake = synthetic_shape_only()
        fake['vectors'][0]['clocks'] = fake['vectors'][0]['clocks'][:4]
        with self.assertRaisesRegex(TraceValidationError, 'clocks need'):
            validate_shape(fake)

    def test_incorrect_stream_rejected(self):
        fake = synthetic_shape_only()
        fake['vectors'][0]['stream_blocks'][0] = '01' + '00'*15
        with self.assertRaisesRegex(TraceValidationError, 'whitening'):
            validate_shape(fake)

    def test_out_of_range_word_rejected(self):
        fake = synthetic_shape_only()
        fake['vectors'][0]['subkeys'][0][0] = 2**32
        with self.assertRaisesRegex(TraceValidationError, 'subkeys'):
            validate_shape(fake)

    def test_invalid_sha_rejected(self):
        fake = synthetic_shape_only()
        fake['raw_stdout_sha256'] = 'fake'
        with self.assertRaisesRegex(TraceValidationError, 'sha256'):
            validate_shape(fake)

    def test_fixture_hash_must_match_real_raw(self):
        fake = synthetic_shape_only()
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)
            (p/'reference_trace.json').write_text(json.dumps(fake),encoding='utf-8')
            (p/'stdout.txt').write_bytes(b'not the author C trace\n')
            with self.assertRaisesRegex(TraceValidationError, 'SHA256 mismatch'):
                verify_trace(p/'reference_trace.json',p/'stdout.txt')

    def test_strict_mode_rejects_old_empty_fixture_exploit(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            fixture = {'source_kind': 'author_c_stdout_SOSEMANUK_VECTOR',
                       'raw_stdout_sha256':'fake', 'vectors':[]}
            (path/'reference_trace.json').write_text(json.dumps(fixture),encoding='utf-8')
            env = dict(os.environ,
                       SOSEMANUK_REFERENCE_TRACE=str(path/'reference_trace.json'),
                       SOSEMANUK_REFERENCE_STDOUT=str(path/'c_reference_stdout.txt'))
            r = subprocess.run([sys.executable, str(ROOT/'run_tests.py'), '--require-reference-trace'],
                               capture_output=True, text=True, env=env, cwd=ROOT)
            self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
            self.assertIn('G2/G4/G5 NOT VERIFIED', r.stderr)


if __name__ == '__main__':
    unittest.main()
