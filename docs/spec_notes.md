# Ghi chú công thức / lưu đồ

## Trường và alpha

GF(2^8) được tạo bởi Q(X)=X^8+X^7+X^5+X^3+1=0x1A9; beta là X mod Q.
Đặt P(X)=X^4+beta^23 X^3+beta^245 X^2+beta^48 X+beta^239; alpha là nghiệm P.

`mul_alpha(x) = ((x << 8) & 0xffffffff) ^ mul_table[x >> 24]`.
`div_alpha(x) = (x >> 8) ^ div_table[x & 0xff]`.

## LFSR/FSM

`new_s = s[9] ^ div_alpha(s[3]) ^ mul_alpha(s[0])`.
`R1_t = (R2_old + (s[1] ^ (s[8] if (R1_old & 1) else 0))) mod 2^32`.
`R2_t = ROTL32((0x54655307 * R1_old) mod 2^32, 7)`.
`f_t = ((s[9] + R1_t) mod 2^32) ^ R2_t`.

## IV setup

Checkpoints y12, y18, y24, each with four words (y0,y1,y2,y3):

- `(s7,s8,s9,s10)=(y12[3],y12[2],y12[1],y12[0])`
- `(s5,s6,R1,R2)=(y18[1],y18[3],y18[0],y18[2])`
- `(s1,s2,s3,s4)=(y24[3],y24[2],y24[1],y24[0])`.

## Luồng

4 clocks -> 4 f words + 4 dropped words -> S2 bitslice -> XOR dropped -> 16 bytes keystream -> plaintext XOR.

Nguồn tham khảo: [SOSEMANUK paper](https://cr.yp.to/streamciphers/sosemanuk/desc.pdf) và [X-CRYPT reference implementation](https://github.com/cchcc/SOSEMANUK/blob/master/C/SOSEMANUK.C).
