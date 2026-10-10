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