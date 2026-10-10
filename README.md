# SOSEMANUK — Dự án triển khai mã hóa dòng bằng Python

> **Bài tập nhóm 6 thành viên — Lý thuyết mật mã**  
> Repository: <https://github.com/trinhvandai05/SOSEMANUK>  
> Ngôn ngữ: **Python 3.10+** · Kiểm thử: **`unittest`** · Quy trình: **nhánh tính năng → Pull Request → review → merge `main`**

## Trạng thái repo: **SKELETON v1.4 — CHƯA CÓ MÃ TRIỂN KHAI**

- Gói này được sinh từ **đúng cây file của Full v1.4** (cùng 64 đường dẫn file), phục vụ nhóm **6 thành viên tự triển khai**.
- **Tất cả file `.py` đều rỗng (0 byte)**, bao gồm mã nguồn, unit tests, `run_tests.py`, các công cụ trace và ví dụ. File dữ liệu `tests/vectors/*.json` và tài liệu được giữ lại làm đầu vào/định hướng.
- **Chưa có phép thử thực thi** và **chưa gate nào được xác nhận PASS**. Tuyệt đối không hiểu `python run_tests.py` không báo lỗi là test đạt: khi file rỗng, nó không chạy test nào.
- Mục tiêu của bản Full v1.4 *sau khi nhóm triển khai* là bộ kiểm thử 55 test, trong đó có 8 bài cần oracle C độc lập. Những con số này là **thông tin về bản Full tham chiếu, không phải kết quả của Skeleton**.
- `tools/ref_diff/build_reference_trace.py` và `extract_reference_trace.py` hiện cũng rỗng; TV5 phải tự triển khai hoặc tạo một công cụ độc lập rồi ghi nguồn cho oracle C.
- `src/sosemanuk/__init__.py` và các `__init__.py` khác để trống có chủ đích; **TV6** chỉ thêm public API sau khi `api.py` đã sẵn sàng.
- **Không giải nén Skeleton đè lên repository đang có code!** Chỉ dùng Skeleton để tạo repo ban đầu, hoặc đồng bộ bằng cách thêm những file còn thiếu trên nhánh riêng, không thay thế file `.py` đã được các thành viên viết.


## 1. Mục tiêu dự án

Nhóm tự triển khai thuật toán mã hóa dòng **SOSEMANUK** dựa trên đặc tả, không chỉ xây dựng một chương trình có khả năng mã hóa/giải mã mà còn kiểm chứng tính đúng của từng thành phần.

**Sản phẩm cần bàn giao:**

1. Mã nguồn Python có thể đọc, chạy và kiểm thử độc lập từng module.
2. Bộ unit test cho phép toán 32-bit, trường hữu hạn, LFSR, FSM và SERPENT.
3. Bộ integration test cho khởi tạo khóa/IV, sinh keystream và API mã hóa/giải mã.
4. Kết quả so sánh với **test vector tham chiếu**, không chỉ kiểm tra `decrypt(encrypt(x)) == x`.
5. Tài liệu mô tả toán học, thiết kế, cách chạy chương trình và kết quả kiểm thử.
6. Bản demo và báo cáo/thuyết trình tổng kết sau khi các kiểm thử đúng thuật toán đã đạt.

**Phạm vi:** dự án phục vụ học tập. SOSEMANUK là stream cipher **không có cơ chế xác thực dữ liệu tích hợp**; không dùng trực tiếp để bảo vệ dữ liệu quan trọng trong ứng dụng mới.

> **Trạng thái:** Các file `.py` trong gói **Skeleton** ban đầu là file trống. Chức năng nào đã hoàn thành phải được xác nhận bằng Pull Request và test; không suy ra rằng toàn bộ thuật toán đã hoạt động chỉ từ việc có tên file.

## 2. Phân công công việc — 6 thành viên

Điền họ tên/GitHub username vào cột **Người nhận** trước khi bắt đầu. Mỗi người phải bàn giao **code + unit test + ghi chú công thức/đầu vào/đầu ra + kết quả kiểm thử**.

| Mã | Người nhận | Nhánh đề xuất | Phần việc chính | File phụ trách | Điều kiện hoàn thành |
|---|---|---|---|---|---|
| **TV1** | _Chưa phân công_ | `feature/arithmetic` | Phép toán word 32-bit, `GF(2^8)`, phép nhân/chia với α | `core/word32.py`, `core/gf256.py`, `core/alpha.py` | Kiểm tra endian/overflow/rotate; bảng α khớp oracle |
| **TV2** | _Chưa phân công_ | `feature/lfsr-fsm` | LFSR 10 word, FSM 2 thanh ghi, quy tắc cập nhật 1 clock | `core/lfsr.py`, `core/fsm.py` | Cả hai nhánh `mux`; trace LFSR/FSM đúng; không dùng nhầm R1 mới |
| **TV3** | _Chưa phân công_ | `feature/serpent-primitives` | 8 S-box, bitslicing, Linear Transformation và output transform (Serpent1) | `serpent/sbox.py`, `serpent/linear_transform.py`, `output_transform.py` | S-box chuẩn; bitslice khớp bản đơn giản; output transform khớp trace |
| **TV4** | _Chưa phân công_ | `feature/serpent24` | Key schedule SERPENT, Serpent24, các checkpoint round 12/18/24 | `serpent/key_schedule.py`, `serpent/serpent24.py`, `tests/support/serpent32.py` | Subkey, Serpent32 KAT, checkpoint đúng oracle |
| **TV5** | _Chưa phân công_ | `feature/initialization` | Context khóa/luồng, key setup, IV setup, ánh xạ trạng thái ban đầu | `context.py`, `key_setup.py`, `iv_setup.py`, `validation.py` | Tách `KeyContext` / `StreamContext`; initial state đúng trace |
| **TV6** | _Chưa phân công_ | `feature/stream-api` | Ghép 4 clock, giữ buffer keystream, API mã hóa/giải mã, demo và kiểm thử end-to-end | `keystream.py`, `api.py`, `run_demo.py`, `examples/basic_encrypt.py` | Vector keystream đúng; chia chunk tùy ý vẫn cùng kết quả; demo chạy được |

Tất cả đường dẫn trong bảng trên được hiểu là tương đối với **`src/sosemanuk/`**, trừ `tests/`, `run_demo.py` và `examples/`.

### 2.1. Mỗi người chịu trách nhiệm test phần mình

| Thành viên | Test phải viết hoặc hoàn thiện |
|---|---|
| TV1 | `tests/unit/test_word32.py`, `test_gf256.py`, `test_alpha.py` |
| TV2 | `tests/unit/test_lfsr.py`, `test_fsm.py` và dữ liệu kiểm tra 1 clock |
| TV3 | `tests/unit/test_output_transform.py`; test S-box và Linear Transformation trong `tests/unit/test_sbox_lt.py` |
| TV4 | `tests/unit/test_key_schedule_serpent24.py`, `tests/integration/test_serpent32_oracle.py` |
| TV5 | `tests/integration/test_context.py` và test key/IV setup, trạng thái ban đầu |
| TV6 | `tests/integration/test_api.py`, `test_reference_vectors.py`, `tests/property/test_streaming.py` |

**Vai trò phối hợp:** **TV2** là người phụ trách tích hợp và tổng hợp báo cáo/slide; **TV5** quản lý nguồn gốc (provenance) của golden vectors; **TV6** quản lý duy nhất `src/sosemanuk/__init__.py` khi public API đã sẵn sàng. **Trong Skeleton, mọi `__init__.py` phải để trống** để unit test ở các module chưa phụ thuộc không bị lỗi import.

**Quy tắc chống xung đột:** Nếu cần sửa file thuộc phần việc của thành viên khác, trao đổi trước trên Issue/PR. Không âm thầm thay đổi giao diện API đã thống nhất. **Lưu ý:** `docs/team_plan.md` đã được cập nhật đồng bộ cho nhóm 6 người.

### 2.2. Người review chéo — thống nhất với `docs/team_plan.md`

**Nguyên tắc:** ưu tiên để **người trực tiếp sử dụng module** làm người review module đó. Các PR ảnh hưởng tới contract/chữ ký hàm phải thông báo trước cho module phụ thuộc.

| PR của | Người review chính |
|---|---|
| TV1 — arithmetic | **TV2** (sử dụng GF/α trong LFSR) |
| TV2 — LFSR/FSM | **TV6** (sử dụng tại keystream) |
| TV3 — SERPENT primitive/output | **TV4** (sử dụng S-box/LT trong Serpent24) |
| TV4 — key schedule/Serpent24 | **TV5** (sử dụng trong IV setup) |
| TV5 — key/IV setup, provenance | **TV6 và TV2** |
| TV6 — stream/API | **TV1 và TV2** |

**TV2** phụ trách xác nhận merge tích hợp sau các gate, nhưng **không tự approve PR do chính mình viết**. Tất cả thành viên review cả phần test và oracle, không chỉ mã nguồn.

## 3. Kiến trúc và cấu trúc thư mục

```text
sosemanuk/
├── README.md
├── pyproject.toml
├── docs/
│   ├── conventions.md
│   ├── module_contracts.md
│   ├── spec_notes.md
│   ├── team_plan.md
│   ├── test_plan.md
│   └── verification.md
├── src/
│   └── sosemanuk/
│       ├── core/
│       │   ├── word32.py          # TV1
│       │   ├── gf256.py           # TV1
│       │   ├── alpha.py           # TV1
│       │   ├── lfsr.py            # TV2
│       │   └── fsm.py             # TV2
│       ├── serpent/
│       │   ├── sbox.py            # TV3
│       │   ├── linear_transform.py # TV3
│       │   ├── key_schedule.py    # TV4
│       │   └── serpent24.py       # TV4
│       ├── output_transform.py    # TV3
│       ├── validation.py          # TV5, input bytes-like
│       ├── context.py             # TV5
│       ├── key_setup.py           # TV5
│       ├── iv_setup.py            # TV5
│       ├── keystream.py           # TV6
│       └── api.py                 # TV6
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── property/
│   ├── support/
│   └── vectors/
│       └── SOURCES.md
├── examples/
│   └── basic_encrypt.py
├── tools/
│   └── show_trace.py
├── run_tests.py
└── run_demo.py
```

**Luồng chính:**

```text
Key → SERPENT key schedule → KeyContext
                              │
IV ───────────────────────────┴→ Serpent24 → StreamContext (LFSR, R1, R2)
                                                    │
                                        4 × (FSM + LFSR clock)
                                                    │
                                       f[0..3], dropped[0..3]
                                                    │
                                      Serpent1 (S2 bitslice) ⊕ dropped
                                                    │
                                        16 byte keystream / nhóm
                                                    │
                                            XOR với plaintext
```

**Chú ý kỹ thuật:**

- Một word có đúng **32 bit**. Cộng/nhân số nguyên có yêu cầu tràn phải giới hạn modulo `2^32`.
- Dữ liệu key, IV, keystream theo quy ước word **little-endian**.
- Trong một clock, FSM đọc LFSR **cũ**, dùng `R1` **cũ** để cập nhật `R2`, sinh `f_t`, sau đó mới cập nhật LFSR.
- `Serpent1` là **S-box S2 bitsliced**, **không** phải một round SERPENT đầy đủ; đầu ra còn phải XOR với các word LFSR bị đẩy ra.
- Chi tiết bắt buộc đọc trước khi code: [`docs/conventions.md`](docs/conventions.md) và [`docs/module_contracts.md`](docs/module_contracts.md).

## 4. Thứ tự triển khai và điều kiện nghiệm thu (gates)

Có thể làm song song, nhưng **không được merge module phụ thuộc vào một thành phần chưa được kiểm thử**.

| Gate | Nội dung | Phụ trách chính | Chỉ coi là đạt khi |
|---|---|---|---|
| **G0** | Thống nhất conventions, chữ ký hàm, vector, cách chạy test | Cả nhóm | 6 thành viên chấp thuận giao diện; expected output bắt buộc lấy từ `tests/vectors/`, không tự sinh từ code vừa viết |
| **G1** | `word32`, `gf256`, `alpha` | TV1 | Test số học và bảng α tham chiếu đạt |
| **G2** | LFSR, FSM | TV2 | 8 clock đầu khớp fixture **C tham chiếu độc lập**; nếu chưa có fixture: **CHƯA ĐẠT G2**, dù KAT cuối đạt |
| **G3** | S-box, LT, output transform | TV3 | Bảng S-box đúng; bitslice và Serpent1 đúng |
| **G4** | Key schedule, Serpent24 | TV4 | Serpent32 KAT + subkeys/checkpoints đối chiếu **trace C**, không chỉ kiểm shape |
| **G5** | Key/IV setup, initial state | TV5 | 10 word LFSR + R1/R2 khớp **trace C**, không suy ngược từ output của cùng hàm đang test |
| **G6** | Keystream + API | TV6 | Official KAT, multi-block, chunk buffering đạt |
| **G7** | Tích hợp, demo, tài liệu, kiểm tra hồi quy | Cả nhóm | Tất cả test bắt buộc chạy và PASS |

Lộ trình phụ thuộc:

- TV1 và TV3 có thể bắt đầu ngay sau G0.
- TV2 sử dụng primitive của TV1; TV4 dùng các primitive của TV3.
- TV5 phụ thuộc key schedule/Serpent24 của TV4.
- TV6 cần FSM/LFSR của TV2, output transform của TV3 và setup của TV5.
- Trong lúc chờ phụ thuộc, các thành viên có thể viết hợp đồng hàm và unit test dựa trên **oracle độc lập**, không phải tự giả định đầu ra đúng.

**G2/G4/G5 chỉ được xác nhận khi có ĐỒNG THỜI `tests/vectors/reference_trace.json` và `tools/ref_diff/c_reference_stdout.txt`, cùng vượt qua strict gate (0 SKIP).**

- Tự động clone/build C và sinh fixture bằng `python tools/ref_diff/build_reference_trace.py`, theo `tools/ref_diff/README.md`. Có thể dùng `extract_reference_trace.py` nếu đã có stdout C. Không lấy `tools/show_trace.py` làm nguồn expected.
- Chạy `python run_tests.py --require-reference-trace` để CI/trưởng nhóm kiểm tra nghiêm ngặt. Nếu chưa có fixture, lệnh này sẽ **FAIL** — đúng theo quy định gate.
- Các KAT đầu cuối vẫn có giá trị độc lập, nhưng **không thay thế** oracle checkpoint/clock.

**Không xem `Ran 0 tests — OK` là PASS.** Một test có ý nghĩa phải thật sự thực thi các assertion cần thiết.

## 5. Cài đặt và chạy test trên Windows

Ví dụ đường dẫn làm việc: **`D:\sosemanuk`**. Mở **PowerShell** trong VS Code hoặc Windows Terminal.

```powershell
cd D:\sosemanuk
py -3 --version
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
```

Không cần kích hoạt virtual environment để chạy các lệnh bên dưới.

**Chạy một file test cụ thể:**

```powershell
.\.venv\Scripts\python.exe -m unittest tests.unit.test_word32 -v
```

**Chạy toàn bộ test:**

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py" -v
```

**Chạy demo** (chỉ sau khi TV6 đã triển khai):

```powershell
.\.venv\Scripts\python.exe run_demo.py
```

Bản Skeleton ban đầu có các file test/demo trống, nên lệnh test hoặc demo chưa chứng minh thuật toán đã hoàn thành. Xem thêm [`docs/test_plan.md`](docs/test_plan.md).

## 6. Quy trình GitHub bắt buộc cho thành viên

### 6.1. Tạo nhánh cho công việc mới

Chỉ làm bước clone nếu máy **chưa có** repository ở `D:\sosemanuk`:

```powershell
git clone https://github.com/trinhvandai05/SOSEMANUK.git D:\sosemanuk
```

Sau đó:

```powershell
cd D:\sosemanuk
git switch main
git pull --ff-only origin main
git switch -c feature/ten-module
```

Ví dụ TV1 dùng `feature/arithmetic`, TV2 dùng `feature/lfsr-fsm`. Nếu nhánh đã tồn tại, dùng `git switch feature/ten-module`, không chạy lại `-c`.

### 6.2. Sau khi code và test

```powershell
cd D:\sosemanuk
git branch --show-current
git status
git diff --check
```

Chỉ stage các file liên quan đến phần việc:

```powershell
git add src/sosemanuk/core/word32.py tests/unit/test_word32.py
git commit -m "feat(word32): implement operations and tests"
git push -u origin feature/arithmetic
```

Các lần push tiếp theo trên nhánh đã thiết lập upstream có thể dùng `git push`.

### 6.3. Tạo Pull Request

Trên GitHub chọn **Pull requests → New pull request**:

```text
base: main
compare: feature/ten-module
```

Mô tả PR tối thiểu:

```markdown
## Mục tiêu
- Module/chức năng đã triển khai:

## File thay đổi
- ...

## Kiểm thử
- Lệnh đã chạy:
- Số lượng test PASS / FAIL:
- Oracle / test vector đã so sánh:

## Vấn đề còn lại
- ...
```

Người review kiểm tra cả **code, test, nguồn oracle, quy ước word và endianness**. Chỉ merge khi đạt gate liên quan. Ưu tiên **Squash and merge** để lịch sử `main` gọn hơn.

### 6.4. Cập nhật code của người khác mà không mất code mình

Nếu đang làm trên nhánh riêng và đã commit các thay đổi dở dang:

```powershell
cd D:\sosemanuk
git switch feature/ten-module
git fetch origin
git merge origin/main
```

Nếu xuất hiện merge conflict, giải quyết theo nội dung hợp đồng module, chạy lại test rồi commit. **Không dùng `git push --force` để giải quyết conflict.**

Sau khi PR đã merge, bắt đầu công việc mới từ `main` mới nhất:

```powershell
git switch main
git pull --ff-only origin main
git switch -c feature/cong-viec-moi
```

**Quy tắc nhóm:** không push trực tiếp lên `main` sau lần khởi tạo repo; không sửa/xóa công việc của người khác khi chưa trao đổi; không commit `.venv/`, khóa bí mật hay dữ liệu nhạy cảm.

## 7. Chính sách kiểm thử — điều quan trọng nhất

### 7.1. Kiểm thử tính đúng

- **Unit test:** mỗi phép toán/hàm phải có test hợp lệ, biên, trường hợp dễ lỗi.
- **Known-answer test (KAT):** so sánh keystream, subkey, checkpoint hoặc trạng thái với dữ liệu tham chiếu có nguồn xác định.
- **Integration test:** kiểm tra key setup → IV setup → các clock → keystream → XOR.
- **Streaming test:** gọi `generate(3)` rồi `generate(13)` phải tương đương `generate(16)` từ cùng trạng thái ban đầu; xử lý đúng buffer keystream dư.
- **Property test:** kiểm tra phép nghịch đảo, tính tuyến tính của LFSR, roundtrip và tính nhất quán theo chunk — chỉ là **bổ trợ**, không thay cho KAT.

**Cảnh báo:** `decrypt(encrypt(m)) == m` vẫn đúng ngay cả khi cả hai lần đều dùng một keystream **sai**. Vì thế test roundtrip không đủ để chứng minh đã triển khai đúng SOSEMANUK.

### 7.2. Oracle và truy xuất nguồn gốc

Tài nguyên nằm ở [`tests/vectors/`](tests/vectors/) và nguồn được ghi trong [`tests/vectors/SOURCES.md`](tests/vectors/SOURCES.md). Không được sửa expected output để ép test PASS. Nếu bổ sung vector, ghi rõ tài liệu, phiên bản/tham chiếu, key, IV, thứ tự byte và cách tạo vector.

### 7.3. Sau khi đúng thuật toán mới làm thí nghiệm mở rộng

Có thể bổ sung đo throughput, thời gian khởi tạo, lượng bộ nhớ và thống kê giả ngẫu nhiên. **Kiểm định thống kê không thay thế KAT hoặc đánh giá an toàn mật mã.**

## 8. Checklist bàn giao của từng thành viên

- [ ] Đã đọc `docs/conventions.md` và `docs/module_contracts.md`.
- [ ] Code đúng phạm vi module; không tự thay đổi giao diện chung.
- [ ] Có docstring/type hint hợp lý cho các hàm chính.
- [ ] Có unit test cho giá trị thường, biên và trường hợp lỗi.
- [ ] Đã đối chiếu ít nhất một kết quả quan trọng với oracle nếu module có vector tương ứng.
- [ ] Đã chạy test liên quan và ghi kết quả trong PR.
- [ ] Đã push đúng nhánh `feature/...`.
- [ ] Đã có thành viên khác review trước khi merge.
- [ ] Sau merge, các test tích hợp liên quan vẫn đạt.

## 9. Tài liệu tham khảo

- [SOSEMANUK — đặc tả gốc](https://cr.yp.to/streamciphers/sosemanuk/desc.pdf)
- [Bộ test vector SOSEMANUK của Crypto++](https://github.com/weidai11/cryptopp/blob/master/TestVectors/sosemanuk.txt)
- [Tài liệu chuẩn và nguồn dữ liệu kiểm thử nội bộ](tests/vectors/SOURCES.md)
- [Hướng dẫn conventions](docs/conventions.md)
- [Hợp đồng module](docs/module_contracts.md)
- [Kế hoạch kiểm thử](docs/test_plan.md)

---

**Nguyên tắc kết thúc dự án:** *Một module được coi là xong khi code đúng, có test chạy thực sự, đối chiếu với oracle phù hợp và đã được review — không phải khi chỉ có hàm hoặc chạy không báo lỗi.*


## Ghi chú về API byte-stream (sau rà soát)

- API từ chối `int`, `str`, `list` khi dùng làm key, IV hoặc message; chỉ nhận `bytes`, `bytearray`, `memoryview`. Tránh lỗi `bytes(16)` biến số nguyên thành khóa 0.
- Đối tượng `Sosemanuk` **chỉ có** `keystream(n)` và `process(data)`. Mỗi lệnh gọi `process` tiêu thụ keystream và **tiến state**. Không có `encrypt/decrypt` alias trên instance.
- Muốn mã hóa/giải mã một thông điệp hoàn chỉnh, dùng `from sosemanuk import encrypt, decrypt` rồi gọi `encrypt(key, iv, plaintext)` hoặc `decrypt(key, iv, ciphertext)`; mỗi hàm tạo stream mới.
- Không tái sử dụng cùng cặp `(key, IV)` để mã hóa hai thông điệp **độc lập**. Khối học tập này chưa có authentication và không harden chống side-channel.
- KAT khóa 128-bit được bổ sung vào `tests/vectors/estream_vectors.json`. Kiểm tra `Serpent24` theo từng checkpoint bằng fixture chuẩn độc lập vẫn là việc cần thực hiện nếu muốn đầy đủ oracle trung gian.
