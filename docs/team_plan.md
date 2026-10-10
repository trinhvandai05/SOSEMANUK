# Kế hoạch nhóm 6 thành viên (hiện hành)

Bảng gốc 4 người đã được thay thế. Xem `README.md` để có bảng chi tiết, nhánh Git và review.

| Người | Mô-đun | Kiểm tra đầu ra | Reviewer chính |
|---|---|---|---|
| TV1 | `word32`, `gf256`, `alpha` | Bảng alpha, overflow/endian | TV2 |
| TV2 | `lfsr`, `fsm`; trưởng nhóm tích hợp và tổng hợp tài liệu | Mỗi bước khớp trace độc lập | TV6 |
| TV3 | `sbox`, LT, `output_transform` | S-box, LT, Serpent1 | TV4 |
| TV4 | `key_schedule`, `serpent24`, Serpent32 test fixture | Serpent32 KAT, checkpoints | TV5 |
| TV5 | `validation`, `context`, `key_setup`, `iv_setup`; quản lý provenance vector | Initial state khớp tham chiếu | TV6 + TV2 |
| TV6 | `keystream`, `api`, `__init__`, demo và API tests | KAT và chia chunk | TV1 + TV2 |

**G0:** Ký hợp đồng API/conventions trước code. Expected output phải lấy từ oracle độc lập, không sinh từ chính implementation đang test.

**Quan trọng:** `src/sosemanuk/__init__.py` ở bản Skeleton để trống cho đến khi `api` hoàn thiện; tránh import lỗi dây chuyền khi TV1 chạy unit tests.

**Oracle C trung gian:** `tests/vectors/reference_trace.json` cùng `tools/ref_diff/c_reference_stdout.txt` chưa có trong gói v1.4 vì chưa có log C gốc được xác thực. Dùng `tools/ref_diff/extract_reference_trace.py` để tạo từ stdout `SOSEMANUK_VECTOR`; giữ `SOURCES.md` có SHA256 của raw log và URL/commit nguồn. Test trace không được tự động đánh dấu PASS khi fixture vắng mặt.

**Phân vai bổ sung:** TV2 trưởng nhóm tích hợp + báo cáo/slide; TV5 quản lý provenance; TV6 sở hữu `__init__.py` và module API. **README là nguồn phân công chuẩn**; bảng trên đồng bộ với README.

**Các Gate:** G1 arithmetic, G2 LFSR/FSM, G3 Serpent primitives/output, G4 key schedule/Serpent24, G5 setup, G6 stream/API, G7 tích hợp.
