# Công Hùng
import unittest

from sosemanuk.core.lfsr import lfsr_step
from sosemanuk.core.fsm import fsm_step


def clock_step(words, r1, r2):
    """
    Ghép một clock LFSR + FSM.

    FSM phải đọc LFSR cũ trước khi LFSR dịch.
    """

    new_r1, new_r2, f = fsm_step(
        r1, r2, words
    )

    dropped = lfsr_step(words)

    return new_r1, new_r2, f, dropped


class TestClock(unittest.TestCase):

    def test_one_clock(self):

        words = [
            0x01000000,
            0x00000003,
            0,
            0x00000100,
            0, 0, 0, 0,
            0x00000004,
            0x00000005
        ]

        r1, r2 = 1, 2

        r1, r2, f, dropped = clock_step(
            words, r1, r2
        )

        # Kiểm tra FSM
        self.assertEqual(r1, 0x00000009)
        self.assertEqual(r2, 0x32A983AA)
        self.assertEqual(f, 0x32A983A4)

        # Kiểm tra LFSR
        self.assertEqual(
            dropped, 0x01000000
        )

        self.assertEqual(
            words[-1], 0xE19FCF17
        )

        self.assertEqual(len(words), 10)

    def test_four_clocks(self):

        words = list(range(10))
        original = words.copy()

        r1 = 1
        r2 = 2

        dropped_words = []
        f_values = []

        for _ in range(4):

            r1, r2, f, dropped = clock_step(
                words, r1, r2
            )

            dropped_words.append(dropped)
            f_values.append(f)

        # Bốn word LFSR đầu tiên bị đẩy ra
        self.assertEqual(
            dropped_words,
            original[:4]
        )

        # Bốn giá trị FSM được tạo
        self.assertEqual(len(f_values), 4)

        # LFSR vẫn có đúng 10 word
        self.assertEqual(len(words), 10)

        # Mọi word nằm trong 32-bit
        self.assertTrue(
            all(0 <= x <= 0xFFFFFFFF for x in words)
        )


if _name_ == "_main_":
    unittest.main()