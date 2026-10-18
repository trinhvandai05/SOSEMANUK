"""No-extra-dependencies test runner; strict mode requires independent C evidence.

    python run_tests.py
    python run_tests.py --require-reference-trace
"""
from pathlib import Path
import os
import sys
import unittest

ROOT = Path(__file__).resolve().parent
STRICT = '--require-reference-trace' in sys.argv
if STRICT:
    sys.argv.remove('--require-reference-trace')

# A test can override the fixture location for a reproducible negative regression.
TRACE = Path(os.getenv('SOSEMANUK_REFERENCE_TRACE', str(ROOT/'tests/vectors/reference_trace.json')))
RAW = Path(os.getenv('SOSEMANUK_REFERENCE_STDOUT', str(ROOT/'tools/ref_diff/c_reference_stdout.txt')))

if STRICT:
    try:
        from tests.support.trace_guard import TraceValidationError, verify_trace
        checked = verify_trace(TRACE, RAW)
        print(f"Verified {len(checked['vectors'])} C trace vectors against raw stdout and independent KATs", file=sys.stderr)
    except Exception as exc:
        print(f"FAIL: invalid independent C trace: {exc} — G2/G4/G5 NOT VERIFIED", file=sys.stderr)
        raise SystemExit(2)

sys.path.insert(0, str(ROOT / 'src'))
suite = unittest.defaultTestLoader.discover(str(ROOT / 'tests'), pattern='test_*.py', top_level_dir=str(ROOT))
result = unittest.TextTestRunner(verbosity=2).run(suite)
if STRICT and (result.skipped or result.testsRun < 46):
    print(f"FAIL: strict mode requires >=46 executed, ZERO skipped tests (got tests={result.testsRun}, skipped={len(result.skipped)})", file=sys.stderr)
    raise SystemExit(2)
raise SystemExit(0 if result.wasSuccessful() else 1)
