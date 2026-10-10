# Trạng thái kiểm chứng — SOSEMANUK Skeleton v1.4 (nhóm 6 người)

**TRẠNG THÁI: CHƯA TRIỂN KHAI.** Toàn bộ `.py` trong ZIP Skeleton là file rỗng; chưa thể chạy unit test, integration test, demo hoặc công cụ sinh oracle C.

## Dữ liệu đã chuẩn bị

- `tests/vectors/estream_vectors.json` và `estream_digest.json` có dữ liệu known-answer từ bản Full v1.4 để nhóm đối chiếu khi tự viết thuật toán.
- `tests/vectors/SOURCES.md` ghi nguồn và các giới hạn của oracle.
- `docs/test_plan.md`, `docs/conventions.md` và `docs/module_contracts.md` mô tả công việc cần hoàn thành.

## Nghiệm thu trong tương lai — không phải kết quả hiện có

1. **G1:** arithmetic và bảng alpha đúng đối chiếu oracle.
2. **G2:** LFSR/FSM khớp trace C độc lập.
3. **G3:** S-box/LT/output transform có kết quả chuẩn.
4. **G4:** key schedule/Serpent24 có checkpoint đúng.
5. **G5:** IV setup khớp initial state tham chiếu.
6. **G6:** keystream API khớp KAT, xử lý đúng buffer, input validation.
7. **G7:** toàn bộ unittest/integration, demo và tài liệu nhóm được kiểm tra.

Để nghiệm thu G2/G4/G5 cần bổ sung cả `tools/ref_diff/c_reference_stdout.txt` và `tests/vectors/reference_trace.json` từ C tham chiếu có provenance rõ ràng. **Không được tự sinh expected output từ code Python của chính nhóm rồi coi là oracle.**

Khi `run_tests.py` chưa có mã, dù lệnh `python run_tests.py` trả code 0 cũng **không có ý nghĩa là PASS**. Khi viết xong test runner phải kiểm tra số bài chạy thực tế, số PASS/SKIP/FAIL, và strict gate phải fail-closed nếu thiếu/giả oracle.

Thống kê **55 total / 47 PASS / 8 SKIP** là của **bản Full v1.4**, *không áp dụng cho Skeleton*.
