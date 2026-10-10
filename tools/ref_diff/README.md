> **Skeleton v1.4:** các script Python trong `tools/ref_diff/` đang rỗng. Tài liệu bên dưới mô tả cơ chế của bản Full và là yêu cầu triển khai cho TV5; không thể chạy trực tiếp các lệnh tạo oracle trên Skeleton chưa viết code.

# Tạo oracle C tham chiếu độc lập — SOSEMANUK v1.4

Mục tiêu: tạo **hai tệp từ mã C tham chiếu**, không dùng kết quả Python đang được kiểm thử:

1. `tools/ref_diff/c_reference_stdout.txt`: stdout gốc của chương trình C.
2. `tests/vectors/reference_trace.json`: dữ liệu trích ra từ stdout gốc.

## Cách nhanh nhất (Windows PowerShell, Ubuntu hoặc macOS)

Máy cần Git, Python >= 3.10, **GCC** (Windows có thể dùng MSYS2/MinGW-w64), kết nối GitHub.

Từ thư mục `D:\sosemanuk`:

```powershell
python tools/ref_diff/build_reference_trace.py
python run_tests.py --require-reference-trace
```

Chương trình thực hiện:

1. Clone `https://github.com/cchcc/SOSEMANUK` vào `tools/ref_diff/ref/author_source` (bỏ qua thư mục này trong Git).
2. Ghi commit Git của C reference (nếu clone thành công).
3. Kiểm tra `SOSEMANUK_VECTOR`, tắt macro ECRYPT API trong **bản header tạm** (không sửa nguồn gốc).
4. Biên dịch `SOSEMANUK.C` bằng `gcc -x c -DSOSEMANUK_VECTOR`.
5. Thực thi chương trình C, giữ nguyên stdout, parse thành JSON và lưu compiler/source hash/commit.
6. Kiểm tra stdout thật với JSON và hai KAT 160 byte đã lưu sẵn. Chỉ ghi đè fixture khi kiểm tra thành công.

Nếu trên Windows `gcc` chưa có, cài GCC qua MSYS2 và đảm bảo `gcc --version` chạy trong PowerShell, hoặc thực hiện trong WSL.

Nếu đã có source reference riêng, chạy:

```powershell
python tools/ref_diff/build_reference_trace.py --source-dir D:\duong-dan\toi\SOSEMANUK
```

## Khi không tải được mã C hoặc thiếu GCC

Không dùng `tools/show_trace.py` để thay thế oracle. Lệnh test thường vẫn chạy (có 8 SKIP), nhưng strict mode phải FAIL. Giữ trạng thái **G2/G4/G5 CHƯA ĐẠT**.

## Nguồn gốc và kiểm chứng

- Bản C tác giả được mirror tại <https://github.com/cchcc/SOSEMANUK/blob/master/C/SOSEMANUK.C>.
- Xem `tests/vectors/SOURCES.md` để điền commit Git, SHA256 và lệnh build.
- `raw_stdout_sha256` và `normalized_stdout_sha256` là hash của log C; hash không xác thực danh tính tác giả/nguồn một cách độc lập. TV5 phải giữ provenance, TV2 phải review lại.
- Khi chạy strict, hệ thống không tin metadata có sẵn: đọc raw stdout và **parse lại**, so toàn bộ output với JSON và hai vector KAT.
- Không commit executable biên dịch hoặc thư mục clone nguồn tham chiếu.

## Cú pháp nâng cao

```powershell
python tools/ref_diff/extract_reference_trace.py --input tools/ref_diff/c_reference_stdout.txt --out tests/vectors/reference_trace.json
```

Lệnh `extract_reference_trace.py` chỉ chuyển log C có sẵn thành JSON. Lệnh này **không thay việc build C và xác minh độc lập stdout**. Cần giữ hai tệp cùng nhau.
