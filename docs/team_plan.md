# Kế hoạch nhóm (4 thành viên, có thể điều chỉnh)

| Thành viên | Module phụ trách | Gate |
| --- | --- | --- |
| A | `word32`, `gf256`, `alpha`, `lfsr` | bảng alpha, phản hồi LFSR, tính tuyến tính |
| B | `fsm`, `output_transform`, `keystream`, `context` | hai nhánh mux, 4-clock block, chunk buffer |
| C | SERPENT `sbox`, `linear_transform`, `key_schedule` | 8 S-box và Serpent32 KAT |
| D | `serpent24`, `key_setup`, `iv_setup`, `api` | checkpoint, initial state, full KAT |

**Trước khi code:** cả nhóm thống nhất conventions.md, module_contracts.md. Mỗi người tạo một nhánh Git và commit test của chính phần mình. Không thay đổi chữ ký hàm nếu chưa thảo luận cả nhóm.

**Gate tổng hợp:** tất cả unit test pass, Serpent32 pass vector, SOSEMANUK pass 160-byte KAT và 131072-byte XOR digest. Sau đó mới làm demo, benchmark và kiểm tra thống kê (những công việc này không thể thay cho correctness test).
