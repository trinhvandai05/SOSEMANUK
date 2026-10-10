# Oracle sources

1. **Official reference-derived KAT:** Crypto++ `TestVectors/sosemanuk.txt` records author C reference run compiled with `SOSEMANUK_VECTOR`, including K=A7C083FEB7, IV=001122...EEFF, full 160-byte output.
   https://tahoe-lafs.org/trac/pycryptopp/browser/git/src-cryptopp/TestVectors/sosemanuk.txt
2. **Independent eSTREAM implementation vector:** nonzero 256-bit sequential key, all-zero IV, 128 keystream bytes:
   https://hawkynt.github.io/Cipher/docs/algorithms/stream-ciphers/sosemanuk-darkcrypt.html
3. **Source specification/reference algorithm:**
   https://cr.yp.to/streamciphers/sosemanuk/desc.pdf
   https://github.com/cchcc/SOSEMANUK/blob/master/C/SOSEMANUK.C

These are byte-level known-answer tests; they must not be replaced by roundtrip or self-generated output. Test cases store the exact expected bytes. If new internal-state fixtures are added, write the provenance + reference commit to this file.

4. **Long eSTREAM KAT:** Crypto++ `TestVectors/sosemanuk.txt` Set 6 vector 3, key 256-bit, nonzero IV, ciphertext of 131072 zero bytes, and published 64-byte XOR digest. A wrong recurrence or stream continuation will fail it.
   https://github.com/weidai11/cryptopp/blob/master/TestVectors/sosemanuk.txt
5. **Serpent32 KAT:** libgcrypt/nettle test vectors for 128-bit/256-bit keys; independently validates S-box, LT, key schedule (and key padding) before SOSEMANUK integration.
   https://hawkynt.github.io/Cipher/docs/algorithms/block-ciphers/serpent.html
   https://sources.debian.org/src/nettle/3.8.1-2/testsuite/serpent-test.c

6. **KAT khóa 128-bit (#2):** nguồn chính là mã C tham chiếu của tác giả biên dịch với `SOSEMANUK_VECTOR`, phần **Detailed test vector 2**. Nguồn mirror mã C: https://github.com/cchcc/SOSEMANUK/blob/master/C/SOSEMANUK.C . Kết quả 160 byte đã được đối chiếu theo phản biện của nhóm. Nguồn Rust https://rust.algorithmexamples.com/web/cryptography/sosemanuk.html chỉ là nguồn phụ, không thay mã tham chiếu.

7. **Intermediate trace — C reference stdout (CHƯA ĐÍNH KÈM):** Dự kiến `tests/vectors/reference_trace.json`, được parse từ stdout C (không phải Python), đi kèm `source_url`, `raw_stdout_sha256`, compiler/command và commit/version khi có. Xem `tools/ref_diff/README.md`. Nếu chưa có fixture chính thống, G2/G4/G5 chưa được xác minh độc lập.


## v1.4 — ghi provenance sau khi tạo trace C

- **Source Git commit:** (điền từ `build_reference_trace.py`)
- **SHA256 SOSEMANUK.C / SOSEMANUK.H:** (điền từ fixture JSON)
- **C compiler + build flags:** GCC, `-O2 -std=c99 -x c -DSOSEMANUK_VECTOR`
- **Raw stdout SHA256:** (điền từ fixture JSON)
- **Normalized stdout SHA256:** (điền từ fixture JSON)
- **TV5 chuẩn bị / TV2 kiểm tra:** (điền tên + ngày)

Lưu nguyên `tools/ref_diff/c_reference_stdout.txt` cùng `tests/vectors/reference_trace.json`. Các hash xác nhận tính toàn vẹn của log so với fixture, không thay nguồn C đã pin. Không thay log này bằng output từ `tools/show_trace.py`.
