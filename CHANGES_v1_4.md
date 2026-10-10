> **Lưu ý gói Skeleton:** phần CHANGELOG này nói về mã Full v1.4. Skeleton chỉ giữ cây thư mục, tài liệu và test vectors; tất cả `.py` đều rỗng.

# v1.4 — fail-closed reference-gate + reproducible C oracle workflow

Ngày: 2026-10-10. Kế thừa trực tiếp từ v1.3; toàn bộ thư mục `src/sosemanuk/` **không đổi**.

- Sửa lỗi nghiêm trọng: fixture `vectors=[]` hay metadata giả không thể làm strict gate PASS.
- `tests/support/trace_guard.py`: validate schema, ít nhất 2 vector, 25 subkeys, 12 state words, >=8 clocks, >=2 Serpent1 blocks, 10 stream blocks, range 32 bit, kiểm logic drop/shift/whitening.
- Phải có raw C stdout thực và SHA256; parser chạy lại raw stdout, so với toàn bộ JSON; so **hai KAT 160 byte độc lập**.
- `run_tests.py --require-reference-trace`: thiếu/invalid raw stdout hoặc JSON → exit 2. Strict mode không chấp nhận SKIP.
- `tests/unit/test_trace_guard.py`: 9 regression tests, gồm chạy subprocess strict với fixture rỗng.
- `tools/ref_diff/build_reference_trace.py`: tự clone C reference, build GCC, ghi commit/hash, chạy và xác minh fixture, không dùng Python SOSEMANUK để tạo expected.
- Cập nhật `README.md`, `docs/verification.md`, `docs/test_plan.md`, `tests/vectors/SOURCES.md`, `tools/ref_diff/README.md`.

**Môi trường tạo gói v1.4 không có quyền mạng cho container tải C reference** nên chưa tạo C oracle độc lập; kết quả hiện tại **55 discovered, 47 PASS, 8 SKIP**. Strict mode FAIL đúng thiết kế; chưa được gọi G2/G4/G5 PASS.
