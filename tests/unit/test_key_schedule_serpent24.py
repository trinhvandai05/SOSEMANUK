import unittest
from sosemanuk.serpent.key_schedule import serpent_key_schedule
from sosemanuk.serpent.serpent24 import serpent24


class TestScheduleAndSerpent24(unittest.TestCase):
    def test_schedule_length(self):
        self.assertEqual(len(serpent_key_schedule(bytes(range(16)))), 25)
        self.assertEqual(len(serpent_key_schedule(bytes(range(32)), 32)), 33)

    def test_checkpoint_shape(self):
        """Shape only, NOT a reference trace oracle: see docs/test_plan.md."""
        cp = serpent24(bytes(16), serpent_key_schedule(bytes(32)))
        self.assertEqual(set(cp), {12, 18, 24})
        self.assertTrue(all(len(x) == 4 for x in cp.values()))
        
        