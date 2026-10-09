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
