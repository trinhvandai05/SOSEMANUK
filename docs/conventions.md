# Quy ước bất biến trước khi code

- `s[0]...s[9]` = `s_t...s_(t+9)`; ban đầu `s[0]` tương ứng `s_1` trong đặc tả, và `s[9]` tương ứng `s_10`.
- Tất cả các word có 32 bit. Phép `+`/`*` số nguyên đều modulo `2^32` nếu kết quả là word. `GF(2^32)` dùng XOR và phép alpha riêng.
- Key/IV được đọc thành 4-byte words **little-endian**; output word cũng little-endian.
- 1 clock: tính FSM từ `s` cũ và R1/R2 cũ; tính `f_t` từ `s[9]` cũ và FSM mới; update LFSR. `clock` trả dropped word và `f_t`.
- `Serpent1` không phải SERPENT round đầy đủ: chỉ S2 ở dạng bitslice; sau đó XOR với dropped LFSR words.
- `apply_sbox(box, (x0,x1,x2,x3))`: bit thứ j tạo 4-bit input x0[j] + 2*x1[j] + 4*x2[j] + 8*x3[j].
- `Serpent24`: checkpoint 12/18 sau LT; checkpoint 24 sau LT và XOR K24.
- `KeyContext` không đổi; `StreamContext` thay đổi; dùng KeyContext với nhiều IV khác nhau được, tuyệt đối tránh lặp `(key,IV)`.
- SOSEMANUK là cipher mã hóa dòng **không kèm xác thực** (không nên dùng làm hệ thống bảo mật triển khai mới).
