# Test plan / các gate bắt buộc

1. word32: overflow, rotate, endian.
2. GF(2^8)/alpha: bảng được sinh từ định nghĩa, check tham chiếu `mul_alpha_table[1] == E19FCF13`; alpha inverse và tuyến tính.
3. FSM/LFSR: độc lập, các branch mux, old-vs-new register, clock trace.
4. Serpent: toàn bộ 8 bảng S-box, implementation theo bit / theo minterm khớp nhau; LT và LT^-1.
5. Serpent key schedule / Serpent24 / state mapping: checkpoint tests, 25 keys.
6. Known-answer tests: first bytes of original reference, 128-byte independent vector, multi-block.
7. Streaming: split at 0,1,3,15,16,17,31,32,... arbitrary chunk sizes, no repeated IV.

*WARNING:* `decrypt(encrypt(m))=m` không xác minh thuật toán; một dòng khóa sai cũng pass. Oracle đầu cuối từ mã tham chiếu là điều kiện chính.

8. Long eSTREAM known-answer: 131072 byte keystream XOR-folded into 64 byte digest.
9. Serpent32 128/256-bit vectors against independent libgcrypt and nettle results.
