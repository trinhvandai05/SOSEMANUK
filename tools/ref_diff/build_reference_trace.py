"""Obtain pinned C-author source, compile and create a verifiable trace fixture.

Requires git and gcc on the USER machine and access to the public repository.
Does not import any SOSEMANUK production code to compute expected values.
Usage: python tools/ref_diff/build_reference_trace.py
       python tools/ref_diff/build_reference_trace.py --source-dir PATH
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools.ref_diff.extract_reference_trace import parse_one, decode_log
from tests.support.trace_guard import TraceValidationError, verify_trace, validate_shape

SOURCE_URL = 'https://github.com/cchcc/SOSEMANUK'
C_URL = SOURCE_URL + '/blob/master/C/SOSEMANUK.C'


def execute(argv: list[str], *, cwd: Path | None = None) -> str:
    r = subprocess.run(argv, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    return r.stdout.decode('utf-8', errors='replace').strip()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source-dir', type=Path, help='Previously checked-out source repository with C/SOSEMANUK.C')
    ap.add_argument('--gcc', default='gcc', help='C compiler executable')
    args = ap.parse_args()
    base = ROOT/'tools/ref_diff'
    source = args.source_dir
    if source is None:
        source = base/'ref'/'author_source'
        if not (source/'C/SOSEMANUK.C').is_file():
            source.parent.mkdir(parents=True, exist_ok=True)
            print('Cloning public C reference to', source, flush=True)
            execute(['git','clone','--depth','1',SOURCE_URL+'.git',str(source)])
    source = source.resolve()
    c_file = source/'C'/'SOSEMANUK.C'
    h_file = source/'C'/'SOSEMANUK.H'
    if not (c_file.is_file() and h_file.is_file()):
        raise SystemExit(f'Missing source files at {source}/C')
    code = c_file.read_bytes()
    header = h_file.read_bytes()
    if b'SOSEMANUK_VECTOR' not in code or b'SOSEMANUK_ECRYPT' not in header:
        raise SystemExit('Unexpected C reference file contents')
    try:
        revision = execute(['git','rev-parse','HEAD'],cwd=source)
    except (OSError,subprocess.CalledProcessError):
        raise SystemExit('C source must be a Git checkout: missing verified commit information')
    if not re.fullmatch(r'[0-9a-f]{40}', revision):
        raise SystemExit('Invalid C reference Git commit identifier')
    gcc = shutil.which(args.gcc)
    if gcc is None:
        raise SystemExit('Missing gcc. Install MSYS2 MinGW-w64/GCC or run in WSL.')
    with tempfile.TemporaryDirectory(prefix='sosemanuk_c_') as work:
        temp = Path(work)
        (temp/'SOSEMANUK.C').write_bytes(code)
        modified_header = re.sub(rb'^\s*#\s*define\s+SOSEMANUK_ECRYPT\s*$',
                                 b'/* ECRYPT disabled for stand-alone C test vectors */',
                                 header, flags=re.MULTILINE)
        if modified_header == header:
            raise SystemExit('Cannot disable SOSEMANUK_ECRYPT as expected')
        (temp/'sosemanuk.h').write_bytes(modified_header)
        binary = temp/('vector.exe' if platform.system()=='Windows' else 'vector')
        compile_args = [gcc,'-O2','-std=c99','-x','c','-DSOSEMANUK_VECTOR',
                        '-o',str(binary),str(temp/'SOSEMANUK.C')]
        execute(compile_args)
        result = subprocess.run([str(binary)],capture_output=True,check=True)
        raw = result.stdout
    text, encoding = decode_log(raw)
    raw_sha = hashlib.sha256(raw).hexdigest()
    normalized_sha = hashlib.sha256(('\n'.join(text.splitlines())+'\n').encode('ascii')).hexdigest()
    pinned_url = f'{SOURCE_URL}/blob/{revision}/C/SOSEMANUK.C'
    obj = parse_one(text, pinned_url, raw_sha)
    obj.update({
        'raw_stdout_encoding':encoding,
        'normalized_stdout_sha256':normalized_sha,
        'source_git_commit':revision,
        'source_c_sha256':hashlib.sha256(code).hexdigest(),
        'source_h_sha256':hashlib.sha256(header).hexdigest(),
        'build_command':'gcc -O2 -std=c99 -x c -DSOSEMANUK_VECTOR',
        'compiler':execute([gcc,'--version']).splitlines()[0],
        'generated_on':platform.platform(),
        'generated_at_utc':datetime.now(timezone.utc).isoformat(),
    })
    validate_shape(obj)
    stdout_target = base/'c_reference_stdout.txt'
    fixture_target = ROOT/'tests/vectors/reference_trace.json'
    # Test temporary staged files BEFORE overwriting a previous verified pair.
    staged_raw = base/'c_reference_stdout.staging.txt'
    staged_json = fixture_target.parent/'reference_trace.staging.json'
    try:
        staged_raw.write_bytes(raw)
        staged_json.write_text(json.dumps(obj,indent=2)+'\n',encoding='utf-8')
        checked = verify_trace(staged_json,staged_raw)
        staged_raw.replace(stdout_target)
        staged_json.replace(fixture_target)
    finally:
        staged_raw.unlink(missing_ok=True)
        staged_json.unlink(missing_ok=True)
    print(f'PASS: {len(checked["vectors"])} C vectors verified against independent KATs')
    print('C source Git commit:', revision)
    print('Raw C stdout SHA256:', raw_sha)
    print('Run: python run_tests.py --require-reference-trace')


if __name__ == '__main__':
    main()
