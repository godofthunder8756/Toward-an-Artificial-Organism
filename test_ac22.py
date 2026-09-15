"""AC22 tests: the scaled world's declarative layer, and its reducibility to the frozen world.

Run with: .venv/bin/python -B -m unittest test_ac22
"""
import unittest
import numpy as np
import ac22_world as w
import ac21_format as fmt
from ac1 import decode


class TestReducibility(unittest.TestCase):
    """The scaled construction must be a generalization, not a different thing."""

    def test_frozen_scale_with_frozen_layout_reproduces_the_frozen_program(self):
        mismatches=w.reducibility_check()
        self.assertEqual(mismatches,[],f'{len(mismatches)} mismatches vs ac5_program')

    def test_both_conventions_are_carried_as_data(self):
        """The frozen world's layout differs from a contiguous one in BOTH the bit positions and
        the action numbers; assuming otherwise produced two rounds of false mismatches."""
        self.assertNotEqual(w.FROZEN_CONSTITUENT_BITS,tuple(range(5)))
        self.assertNotEqual(w.FROZEN_CONSTITUENT_ACTIONS,tuple(range(5)))
        self.assertEqual(w.FROZEN_CONSTITUENT_ACTIONS,(0,1,6,7,8))


class TestScaledWorld(unittest.TestCase):
    def test_declared_scale_meets_both_measured_axes(self):
        self.assertGreaterEqual(w.RULES,w.C+w.B,'slots must cover C+B')
        self.assertGreaterEqual(w.MASK_BITS,w.OBS_BITS,'mask must cover the observation word')

    def test_capacity_fits_the_bank(self):
        cap=w.capacity_check()
        self.assertTrue(cap['fits'])
        self.assertLess(cap['program_bits'],cap['bank_bits'])

    def test_target_reproduces_its_demonstration_completely(self):
        hit,total=w.coverage(tuple(range(w.B)))
        self.assertEqual(hit,total)
        self.assertEqual(total,4096)

    def test_acquired_structure_is_broader_than_the_present_design(self):
        self.assertAlmostEqual(w.acquired_bits(4),4.585,places=2)
        self.assertAlmostEqual(w.acquired_bits(6),9.492,places=2)
        self.assertGreater(w.acquired_bits(6),w.acquired_bits(4))

    def test_constituent_actions_are_respected_not_inferred(self):
        """Changing the declared action mapping must change the target, which is what 'carried as
        data' means."""
        a=w.target_rules(tuple(range(3)))
        b=w.target_rules(tuple(range(3)),constituent_actions=(5,5,5,5,5,5))
        self.assertNotEqual(a,b)

    def test_narrow_mask_cannot_address_the_high_banks(self):
        """The mask-axis finding reproduced inside the world module: with a 9-bit mask the banks
        whose disagreement bits sit above bit 8 are unaddressable, and coverage falls short even
        though there are slots for every bank."""
        hit_narrow,total=w.coverage(tuple(range(w.B)),mask_bits=9)
        hit_wide,_=w.coverage(tuple(range(w.B)),mask_bits=12)
        self.assertLess(hit_narrow,total)
        self.assertEqual(hit_wide,total)

    def test_fewer_slots_than_banks_falls_short(self):
        hit,total=w.coverage(tuple(range(w.B)),rules=w.C+w.B-2)
        self.assertLess(hit,total)
        self.assertGreater(hit,0)


if __name__=='__main__':
    unittest.main()
