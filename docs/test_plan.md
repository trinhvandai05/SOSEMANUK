# Test plan / các gate bắt buộc

1. word32: overflow, rotate, endian.
2. GF(2^8)/alpha: bảng được sinh từ định nghĩa, check tham chiếu `mul_alpha_table[1] == E19FCF13`; alpha inverse và tuyến tính.
3. FSM/LFSR: độc lập, các branch mux, old-vs-new register, clock trace.
4. Serpent: toàn bộ 8 bảng S-box, implementation theo bit / theo minterm khớp nhau; LT và LT^-1.
5. Serpent key schedule / Serpent24 / state mapping: checkpoint tests, 25 keys.
6. Known-answer tests: 5-byte/128-bit/256-bit key KAT (160/160/128 byte), multi-block.
7. Streaming: split at 0,1,3,15,16,17,31,32,... arbitrary chunk sizes, no repeated IV.

*WARNING:* `decrypt(encrypt(m))=m` không xác minh thuật toán; một dòng khóa sai cũng pass. Oracle đầu cuối từ mã tham chiếu là điều kiện chính.

8. Long eSTREAM known-answer: 131072 byte keystream XOR-folded into 64 byte digest.
9. Serpent32 128/256-bit vectors against independent libgcrypt and nettle results.

## Điều kiện kiểm chứng oracle C (không tuyên bố quá mức)

- v1.4 cung cấp `tools/ref_diff/extract_reference_trace.py` (đọc log của mã C) và `tests/unit/test_reference_trace.py` (so subkey, checkpoints, initial state, clock, output transform).
- **Trong gói v1.4 hiện chưa đính kèm** hai tệp oracle stdout C và JSON đã xác minh. Vì vậy G2/G4/G5 **chưa được xác minh theo trace C**; các test tương ứng sẽ SKIP và gate nghiêm ngặt sẽ FAIL cho đến khi fixture có mặt.
- Tạo và xác minh oracle tự động: `python tools/ref_diff/build_reference_trace.py`; lưu cả stdout thật và JSON. Hướng dẫn tại `tools/ref_diff/README.md` và `SOURCES.md`.
- `tools/show_trace.py` sinh từ **Python đang kiểm thử**, chỉ để debug, tuyệt đối không dùng làm oracle độc lập.
- Cơ chế `--require-reference-trace` **bắt buộc** có ít nhất hai trace, raw stdout khớp SHA256, parse lại đúng JSON, hai KAT 160 byte và **0 SKIP**. Không coi test bị SKIP là PASS.
- Full alpha table 512 phần tử đối chiếu mã C vẫn cần bổ sung khi có dữ liệu C; các tính chất inverse/linearity không đủ để chứng minh lựa chọn đúng đa thức trường.
- Dữ liệu cho key/IV/message phải thuộc các kiểu byte-oriented (`bytes`, `bytearray`, `memoryview`).
