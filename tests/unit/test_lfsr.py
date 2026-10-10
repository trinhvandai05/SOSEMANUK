"""
Unit tests cho module LFSR của SOSEMANUK.

Chạy bằng:
python -m unittest discover -s tests/unit -p "test_lfsr.py" -v
"""

import random
import unittest

from sosemanuk.core.lfsr import lfsr_step


class TestLFSR(unittest.TestCase):

    def test_manual_example(self):
        """
        Kiểm tra bằng ví dụ tính tay.

        s_t     = 0x01000000
        s_(t+3) = 0x00000100
        s_(t+9) = 0x00000005

        mul_alpha(s_t)     = 0xE19FCF13
        div_alpha(s_(t+3)) = 0x00000001

        Feedback:
        0x05 XOR 0x01 XOR 0xE19FCF13
        = 0xE19FCF17
        """

        words = [
            0x01000000,
            0x00000003,
            0x00000000,
            0x00000100,
            0x00000000,
            0x00000000,
            0x00000000,
            0x00000000,
            0x00000004,
            0x00000005,
        ]

        dropped = lfsr_step(words)

        self.assertEqual(
            dropped,
            0x01000000
        )

        self.assertEqual(
            words,
            [
                0x00000003,
                0x00000000,
                0x00000100,
                0x00000000,
                0x00000000,
                0x00000000,
                0x00000000,
                0x00000004,
                0x00000005,
                0xE19FCF17,
            ]
        )

    def test_simple_example(self):
        """Kiểm tra một trạng thái đơn giản."""

        words = list(range(10))

        dropped = lfsr_step(words)

        self.assertEqual(dropped, 0)

        self.assertEqual(
            words,
            list(range(1, 10)) + [0x2811C0F7]
        )

    def test_zero_state(self):
        """Trạng thái toàn zero vẫn giữ nguyên zero."""

        words = [0] * 10

        dropped = lfsr_step(words)

        self.assertEqual(dropped, 0)
        self.assertEqual(words, [0] * 10)

    def test_invalid_state_length(self):
        """LFSR phải có đúng 10 thanh ghi."""

        for n in (0, 9, 11):

            words = [0] * n

            with self.subTest(length=n):

                with self.assertRaises(ValueError):
                    lfsr_step(words)

            self.assertEqual(words, [0] * n)

    def test_first_ten_dropped(self):
        """
        10 clock đầu sẽ đẩy lần lượt
        10 word ban đầu ra ngoài.
        """

        words = list(range(10))

        dropped_words = [
            lfsr_step(words)
            for _ in range(10)
        ]

        self.assertEqual(
            dropped_words,
            list(range(10))
        )

    def test_linearity(self):
        """
        LFSR có tính tuyến tính trên GF(2):

        F(A XOR B) = F(A) XOR F(B)
        """

        rng = random.Random(89)

        for _ in range(100):

            a = [
                rng.getrandbits(32)
                for _ in range(10)
            ]

            b = [
                rng.getrandbits(32)
                for _ in range(10)
            ]

            ab = [
                x ^ y
                for x, y in zip(a, b)
            ]

            dropped_a = lfsr_step(a)
            dropped_b = lfsr_step(b)
            dropped_ab = lfsr_step(ab)

            self.assertEqual(
                dropped_ab,
                dropped_a ^ dropped_b
            )

            self.assertEqual(
                ab,
                [x ^ y for x, y in zip(a, b)]
            )

    def test_uint32(self):
        """Kiểm tra giới hạn word 32-bit."""

        words = [0xFFFFFFFF] * 10

        dropped = lfsr_step(words)

        self.assertEqual(
            dropped,
            0xFFFFFFFF
        )

        self.assertTrue(
            all(
                0 <= x <= 0xFFFFFFFF
                for x in words
            )
        )


if __name__ == "__main__":
    unittest.main()