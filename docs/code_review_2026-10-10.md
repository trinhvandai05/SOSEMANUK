# Rà soát và sửa lỗi mã SOSEMANUK — 10/10/2026

## Sửa đã hoàn thành

1. **Strict byte inputs:** thêm `validation.require_bytes`, dùng ở `key_setup`, `iv_setup` và `Sosemanuk.process`. Không còn trường hợp `bytes(16)` âm thầm trở thành khóa toàn zero.
2. **Rõ ngữ nghĩa stream:** `Sosemanuk` chỉ có `.process()` và `.keystream()`. Hàm cấp module `encrypt()` và `decrypt()` tạo stream mới để xử lý từng thông điệp hoàn chỉnh.
3. **Key 128-bit official-reference test:** bổ sung vector thứ 2 gồm 160 byte vào `tests/vectors/estream_vectors.json` từ nguồn được chỉ rõ trong `SOURCES.md`.
4. **Tách test SERPENT:** `test_sbox_lt.py` dành cho TV3, `test_key_schedule_serpent24.py` dành cho TV4.
5. **Nhóm 6 người:** đồng bộ README và `docs/team_plan.md` cùng các module, reviewer, gate; bản Skeleton giữ các file Python trống.
6. **Chú thích trung thực:** test bitslice chỉ chứng thực cách đóng bit, test checkpoint chỉ chứng thực hình dạng; không gọi đó là oracle độc lập.

## Giới hạn chưa hoàn thành

- Chưa có *oracle trung gian độc lập* lấy trực tiếp từ mã C tham chiếu (`reference_trace.json`), nên chưa có test kiểm đúng từng checkpoint riêng.
- Chưa có kiểm tra đầy đủ 512 giá trị alpha table trực tiếp với dữ liệu C tham chiếu.
- KAT chỉ đảm bảo tính đúng trên vector đã thử, không chứng minh an toàn mã hóa hoặc chống side-channel.

## Kiểm tra bản Full

Chạy: `python run_tests.py`, `python run_demo.py`; kiểm tra KAT 128-bit, 5-byte, 256-bit và eSTREAM XOR-digest dài.

Bản này là code phục vụ học tập, không dùng bảo vệ dữ liệu quan trọng trong triển khai thực tế.
