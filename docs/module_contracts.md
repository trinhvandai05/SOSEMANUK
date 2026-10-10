# Hợp đồng module cho nhóm

| Module | Input | Output | Có tác dụng phụ? |
| --- | --- | --- | --- |
| `require_bytes` | bytes/bytearray/memoryview, field name | immutable bytes; reject int/str/list | không |
| `gf256` | hai byte / số mũ | một byte | không |
| `alpha` | uint32 | uint32 | không |
| `lfsr_step` | `list[int]` đúng 10 từ | dropped `s_t` | sửa list tại chỗ |
| `fsm_step` | r1, r2, 10 LFSR words cũ | new_r1, new_r2, f | không |
| `serpent_key_schedule` | key bytes, rounds | tuple subkeys | không |
| `serpent24` | IV đúng 16 byte, 25 subkeys | checkpoint dict {12,18,24} | không |
| `map_initial_state` | 3 checkpoint | StreamContext | không |
| `output_transform` | 4 f, 4 dropped | 4 uint32 keystream | không |
| `clock` | StreamContext | dropped, f | sửa StreamContext |
| `generate` | StreamContext, size | bytes với đúng size | sửa context; giữ buffer dư |
| `Sosemanuk.process` | data bytes | data XOR keystream | sửa context |

Quy tắc hợp nhất: Không sửa chữ ký hoặc thứ tự word nếu chưa cập nhật `conventions.md` và test. Mỗi thành viên tự chạy `python -m unittest discover -s tests -v` trước khi merge.

**API convention:** use instance `.process` only for successive chunks of one stream. For a complete message use module-level `encrypt(key, iv, data)` / `decrypt(...)`, each initializing a new stream. Never reuse a (key, IV) pair for different messages.
