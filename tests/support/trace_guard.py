"""Fail-closed validation of the independent C-reference trace.

This module deliberately imports NO SOSEMANUK production implementation.
A schema-conforming JSON alone is never proof of C provenance: the raw C
stdout must be present, hashed and reparsed to exactly the same vectors.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re

U32_MAX = (1 << 32) - 1
SHA256 = re.compile(r"[0-9a-f]{64}\Z")
HEX = re.compile(r"(?:[0-9a-f]{2})+\Z")
SOURCE_KIND = "author_c_stdout_SOSEMANUK_VECTOR"
MIN_VECTORS = 2


class TraceValidationError(ValueError):
    """Fixture is missing, inconsistent, or not sufficiently evidenced."""


def _check(condition: bool, message: str) -> None:
    if not condition:
        raise TraceValidationError(message)


def _word(x: object) -> bool:
    return type(x) is int and 0 <= x <= U32_MAX


def _words(value: object, size: int) -> bool:
    return isinstance(value, list) and len(value) == size and all(map(_word, value))


def _hex(value: object, bytes_min: int, bytes_max: int) -> bool:
    return isinstance(value, str) and bool(HEX.fullmatch(value)) and bytes_min <= len(value)//2 <= bytes_max


def validate_shape(obj: object) -> None:
    """Structural checks; NOT sufficient to claim independent provenance."""
    _check(isinstance(obj, dict), "Trace root must be an object")
    _check(obj.get("source_kind") == SOURCE_KIND, "Wrong source_kind")
    _check(isinstance(obj.get("source_url"), str) and obj["source_url"].startswith("https://"),
           "Missing HTTPS source_url")
    _check(isinstance(obj.get("raw_stdout_sha256"), str)
           and SHA256.fullmatch(obj["raw_stdout_sha256"]) is not None,
           "raw_stdout_sha256 must be 64 lowercase hex digits")
    _check(isinstance(obj.get("normalized_stdout_sha256"), str)
           and SHA256.fullmatch(obj["normalized_stdout_sha256"]) is not None,
           "normalized_stdout_sha256 must be 64 lowercase hex digits")
    _check(obj.get("raw_stdout_encoding") in ("utf-8", "utf-16"),
           "Unsupported raw_stdout_encoding")
    _check(isinstance(obj.get("source_git_commit"), str)
           and re.fullmatch(r"[0-9a-f]{40}", obj["source_git_commit"]) is not None,
           "source_git_commit must be a pinned 40-digit commit SHA")
    for source_hash in ("source_c_sha256", "source_h_sha256"):
        _check(isinstance(obj.get(source_hash), str) and SHA256.fullmatch(obj[source_hash]),
               f"{source_hash} must contain a 64-digit SHA256")
    _check(isinstance(obj.get("compiler"), str) and bool(obj["compiler"].strip()),
           "Missing C compiler provenance")
    _check(isinstance(obj.get("build_command"), str)
           and "SOSEMANUK_VECTOR" in obj["build_command"],
           "Missing C build command with SOSEMANUK_VECTOR")
    vectors = obj.get("vectors")
    _check(isinstance(vectors, list) and len(vectors) >= MIN_VECTORS,
           f"At least {MIN_VECTORS} nonempty C trace vectors are required")

    unique = set()
    for vi, v in enumerate(vectors):
        where = f"vectors[{vi}]"
        _check(isinstance(v, dict), f"{where}: must be an object")
        _check(_hex(v.get('key'), 1, 32), f"{where}: invalid key")
        _check(_hex(v.get('iv'), 16, 16), f"{where}: invalid 128-bit IV")
        pair = (v['key'], v['iv'])
        _check(pair not in unique, f"{where}: duplicated key/IV")
        unique.add(pair)
        keys = v.get('subkeys')
        _check(isinstance(keys, list) and len(keys) == 25
               and all(_words(k, 4) for k in keys), f"{where}: need 25 x 4 u32 subkeys")
        init = v.get('initial_state')
        _check(isinstance(init, dict) and _words(init.get('s'), 10)
               and _word(init.get('r1')) and _word(init.get('r2')),
               f"{where}: initial state must contain 10 LFSR and R1/R2 words")
        clocks = v.get('clocks')
        _check(isinstance(clocks, list) and len(clocks) >= 8 and len(clocks) % 4 == 0,
               f"{where}: clocks need >=8 entries and a multiple of 4")
        current = init['s']
        for ci, c in enumerate(clocks):
            prefix = f"{where}.clocks[{ci}]"
            _check(isinstance(c, dict), prefix + ': not an object')
            _check(all(_word(c.get(k)) for k in ('r1', 'r2', 'f', 'dropped')),
                   prefix + ': missing/wrong 32-bit clock word')
            nxt = c.get('after_s')
            _check(_words(nxt, 10), prefix + ': invalid after_s')
            _check(c['dropped'] == current[0], prefix + ': dropped word is inconsistent')
            _check(nxt[:9] == current[1:], prefix + ': LFSR shift is inconsistent')
            current = nxt
        blocks = v.get('serpent_blocks')
        streams = v.get('stream_blocks')
        _check(isinstance(blocks, list) and len(blocks) >= 2, where + ': need two Serpent1 blocks')
        _check(isinstance(streams, list) and len(streams) >= 10, where + ': author C must output ten stream blocks (160 bytes)')
        for bi in range(2):
            b = blocks[bi]
            _check(isinstance(b, dict) and _words(b.get('input'),4) and _words(b.get('output'),4),
                   f'{where}: malformed Serpent1 block {bi}')
            entries = clocks[bi*4:bi*4+4]
            _check(b['input'] == [c['f'] for c in entries],
                   f'{where}: Serpent1 input does not match FSM trace')
            s = streams[bi]
            _check(_hex(s,16,16), f'{where}: invalid keystream block {bi}')
            whitened = [x ^ c['dropped'] for x,c in zip(b['output'],entries)]
            expected = b''.join(x.to_bytes(4,'little') for x in whitened).hex()
            _check(s == expected, f'{where}: keystream block not consistent with whitening')


def verify_trace(json_path: Path, raw_path: Path) -> dict:
    """Require raw log, matching SHA256, and reparse to match every JSON vector.

    Note: hashes detect tampering/inconsistency, NOT a cryptographic proof that
    third-party source code was authentic; preserve pinned C commit and source hashes.
    """
    json_path = Path(json_path)
    raw_path = Path(raw_path)
    _check(json_path.is_file(), f"Missing independent C JSON fixture: {json_path}")
    _check(raw_path.is_file(), f"Missing ORIGINAL C stdout: {raw_path}")
    try:
        obj = json.loads(json_path.read_text(encoding='utf-8'))
        validate_shape(obj)
        data = raw_path.read_bytes()
        _check(bool(data), "C stdout is empty")
        sha = hashlib.sha256(data).hexdigest()
        _check(sha == obj['raw_stdout_sha256'], "C stdout SHA256 mismatch")
        from tools.ref_diff.extract_reference_trace import parse_one, decode_log
        decoded, encoding = decode_log(data)
        _check(encoding == obj['raw_stdout_encoding'], "C stdout encoding mismatch")
        normalized = '\n'.join(decoded.splitlines()) + '\n'
        normalized_sha = hashlib.sha256(normalized.encode('ascii')).hexdigest()
        _check(normalized_sha == obj['normalized_stdout_sha256'], "Normalized stdout SHA256 mismatch")
        reconstructed = parse_one(decoded, obj['source_url'], sha)
        validate_shape({**obj, 'vectors': reconstructed['vectors']})
        _check(reconstructed['vectors'] == obj['vectors'],
               "JSON vectors differ from the reparsed, hashed C stdout")
        # Cross-check the two trace cases against independent, checked-in KATs.
        kat_file = json_path.parent / 'estream_vectors.json'
        _check(kat_file.is_file(), "Missing independent eSTREAM KAT corpus")
        kats = json.loads(kat_file.read_text(encoding='utf-8'))
        known = {(k['key'], k['iv']):k['keystream'] for k in kats}
        matched = 0
        for v in obj['vectors']:
            expected = known.get((v['key'], v['iv']))
            if expected is not None:
                seen = ''.join(v['stream_blocks'][:10])
                _check(seen == expected[:320],
                       'Independent 160-byte KAT disagrees with C trace output')
                matched += 1
        _check(matched >= 2, 'Need at least two vectors matching independent checked-in KATs')
        return obj
    except (OSError, UnicodeError, ValueError, KeyError, TypeError, OverflowError) as exc:
        if isinstance(exc, TraceValidationError):
            raise
        raise TraceValidationError(f"Invalid C reference trace: {exc}") from exc
