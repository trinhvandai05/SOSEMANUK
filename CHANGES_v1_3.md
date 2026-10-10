# v1.3 — sửa 3 lỗi vận hành của luồng trace C (10/10/2026)

Không đổi thuật toán, không đổi `src/`. **Không đính kèm** `reference_trace.json`: theo quy định của nhóm, TV5 tự build C và sinh fixture.

| File | Thay đổi | Lỗi đã tái hiện ở v1.2 |
|---|---|---|
| `tools/ref_diff/README.md` | Lệnh build C cụ thể (PowerShell + bash): tắt `SOSEMANUK_ECRYPT`, `gcc -x c` | Làm theo README cũ → `fatal error: ecrypt-sync.h` (file không có trong mirror); `.C` bị gcc dịch như C++ |
| `tools/ref_diff/extract_reference_trace.py` | Đọc strict, nhận BOM UTF-16; thêm `raw_stdout_encoding`, `normalized_stdout_sha256` | Windows PowerShell 5.1 `>` ghi UTF-16LE → script báo sai "No ... test vectors found" |
| `tests/unit/test_reference_trace.py` | Mỗi test chỉ import module của mình, lấy input khác từ fixture C; chạy cả 2 vector | `setUpClass` gọi `key_setup` → khi TV4/TV5 chưa xong, cả 8 test trace ERROR (TV2/TV3 không dùng được oracle); bug key schedule làm fail 4 test thay vì 1 |
| `docs/verification.md`, `.gitignore` | Ghi đúng "38 đạt + 8 SKIP"; bỏ qua `tools/ref_diff/ref/` | — |

Kiểm chứng (Linux, gcc, Python 3.12): fixture sinh từ log UTF-16, log CRLF và log LF đều cho cùng `normalized_stdout_sha256`; `--require-reference-trace` → 46/46. PowerShell chưa được chạy thử trực tiếp.

Khoanh vùng sau khi sửa (mỗi lỗi cài vào → test trace fail):

| Lỗi | Test fail |
|---|---|
| Key schedule (pad 0x80) | `subkeys` |
| Serpent24 (checkpoint trước LT) | `serpent24_checkpoints`, `initial_state` |
| Ánh xạ (đổi s5/s6) | `initial_state` |
| FSM (R2 từ R1 mới) | `fsm`, `first_two_blocks` |
| LFSR (đổi α/α⁻¹) | `lfsr`, `first_two_blocks` |
| Serpent1 (đảo thứ tự f) | `output_transform`, `first_two_blocks` |
| Skeleton chỉ có core + S-box/LT | chỉ 4 test cần module chưa viết bị lỗi; FSM/LFSR/output transform vẫn chạy |
