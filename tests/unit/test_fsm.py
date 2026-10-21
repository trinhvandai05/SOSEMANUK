<<<<<<< HEAD
"""Unit tests cho FSM SOSEMANUK."""

import unittest

from sosemanuk.core.fsm import (
    mux,
    trans,
    fsm_step,
)


class TestFSM(unittest.TestCase):

    def setUp(self):
        # s[t+1] = 3
        # s[t+8] = 4
        # s[t+9] = 5
        self.words = [
            0, 3, 0, 0, 0,
            0, 0, 0, 4, 5
        ]

    def test_mux_even(self):
        self.assertEqual(mux(0, 3, 4), 3)
        self.assertEqual(mux(2, 3, 4), 3)

    def test_mux_odd(self):
        self.assertEqual(mux(1, 3, 4), 7)
        self.assertEqual(mux(3, 3, 4), 7)

    def test_trans_known_values(self):
        self.assertEqual(trans(0), 0)
        self.assertEqual(trans(1), 0x32A983AA)
        self.assertEqual(trans(2), 0x65530754)
        self.assertEqual(
            trans(0xFFFFFFFF),
            0xCD567CD5
        )

    def test_odd_branch_known_answer(self):
        # R1 cũ = 1, R2 cũ = 2
        self.assertEqual(
            fsm_step(1, 2, self.words),
            (
                0x00000009,
                0x32A983AA,
                0x32A983A4
            )
        )

    def test_even_branch_known_answer(self):
        self.assertEqual(
            fsm_step(0, 2, self.words),
            (
                0x00000005,
                0x00000000,
                0x0000000A
            )
        )

    def test_wraparound_32bit(self):
        words = [0] * 10
        words[1] = 2
        words[9] = 0xFFFFFFFF

        self.assertEqual(
            fsm_step(0, 0xFFFFFFFF, words),
            (1, 0, 0)
        )

    def test_uses_old_r1_for_trans(self):
        new_r1, new_r2, _ = fsm_step(
            1, 2, self.words
        )

        self.assertEqual(
            new_r2,
            0x32A983AA
        )

        self.assertNotEqual(
            new_r2,
            trans(new_r1)
        )

    def test_does_not_modify_lfsr(self):
        old = self.words.copy()

        fsm_step(1, 2, self.words)

        self.assertEqual(self.words, old)

    def test_invalid_lfsr_length(self):
        for n in (0, 9, 11):

            with self.subTest(n=n):

                with self.assertRaises(ValueError):
                    fsm_step(1, 2, [0] * n)


if __name__ == "__main__":
    unittest.main()
=======

import unittest  # Import thư viện unittest để viết và chạy các bài kiểm thử tự động

from sosemanuk.core.fsm import trans, mux, fsm_step  # Import 3 hàm: trans (biến đổi trạng thái), mux (hàm chọn/ghép dữ liệu) và fsm_step (thực hiện một bước FSM)

class TestFSM(unittest.TestCase):  # Khai báo lớp TestFSM để chứa các bài kiểm thử FSM

    def test_mux(self):  # Kiểm thử hoạt động của hàm mux
        self.assertEqual(mux(0, 3, 4), 3)  # Kiểm tra mux với tham số đầu là 0 thì kết quả phải bằng 3
        self.assertEqual(mux(1, 3, 4), 7)  # Kiểm tra mux với tham số đầu là 1 thì kết quả phải bằng 7

    def test_old_register_and_f(self):  # Kiểm thử các thanh ghi cũ và giá trị đầu ra f của FSM
        s = [0, 3, 0, 0, 0, 0, 0, 0, 4, 5]  # Khởi tạo danh sách trạng thái s gồm 10 phần tử
        r1, r2, f = fsm_step(1, 2, s)  # Gọi fsm_step với đầu vào 1, 2 và trạng thái s; nhận 3 giá trị trả về r1, r2, f
        self.assertEqual(r1, 9)  # Kiểm tra giá trị thanh ghi r1 trả về phải bằng 9
        self.assertEqual(r2, trans(1))  # Kiểm tra r2 phải bằng kết quả của hàm trans(1)
        self.assertEqual(f, (14 ^ trans(1)))  # Kiểm tra f phải bằng phép XOR giữa 14 và trans(1)
        self.assertNotEqual(r2, trans(r1))  # Kiểm tra r2 khác trans(r1), tức r2 không bằng kết quả trans áp dụng lên r1

    def test_even_branch(self):  # Kiểm thử nhánh xử lý chẵn của FSM
        s = [0, 3, 0, 0, 0, 0, 0, 0, 4, 5]  # Khởi tạo trạng thái s với 10 phần tử
        self.assertEqual(fsm_step(0, 2, s)[0], 5)  # Gọi fsm_step với đầu vào 0, 2 và kiểm tra phần tử trả về đầu tiên bằng 5
>>>>>>> 3157cced6792c93eebea13203ac43b83e7a0b090
