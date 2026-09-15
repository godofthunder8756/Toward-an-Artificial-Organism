"""AC24 tests: the frozen developmental function measured in effective bits.

Run with: .venv/bin/python -B -m unittest test_ac24
"""
import itertools
import unittest
import ac24_functional as f


class TestBankTerminology(unittest.TestCase):
    """The three senses of "bank" must stay disentangled, because AC20-AC23 grew sense (c) while
    AC23 modelled sense (b)."""

    def test_frozen_rules_use_one_mask_bit_per_position(self):
        rules=f.frozen_rules((0,1,2,3))
        bank_rules=rules[5:]
        self.assertEqual([r[1] for r in bank_rules],[4,8,16,32],'masks 4<<bank, bits 2-5')
        self.assertEqual([r[2] for r in bank_rules],[2,3,4,5],'actions 2+bank')


class TestEffectiveStructure(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.obs={h:f.reachable_observations(history=h) for h in (0,1)}

    def test_each_history_has_19_reachable_observations(self):
        for h in (0,1): self.assertEqual(len(self.obs[h]),19)

    def test_exactly_two_of_four_positions_are_live_per_individual(self):
        """The inactive region's urgency mask can never match, because `activation` ties a region
        to the individual's history, and bit 5 is never set at all."""
        self.assertEqual(f.live_positions(self.obs[0]),[True,True,False,False])
        self.assertEqual(f.live_positions(self.obs[1]),[True,False,True,False])

    def test_which_positions_are_live_depends_on_history(self):
        self.assertNotEqual(f.live_positions(self.obs[0]),f.live_positions(self.obs[1]))

    def test_bit_five_never_set_in_either_history(self):
        for h in (0,1):
            self.assertEqual(sum(1 for o in self.obs[h] if (o>>5)&1),0)

    def test_live_masks_do_co_occur_so_order_matters(self):
        for h in (0,1):
            _,pairs=f.co_occurrence(self.obs[h],f.live_positions(self.obs[h]))
            self.assertGreater(pairs,0,'if the live masks never co-occurmed, order could not matter')

    def test_twenty_four_permutations_collapse_to_two_behaviours(self):
        """The headline: 4.58 nominal bits, 1.00 effective."""
        for h in (0,1):
            classes={}
            for priority in itertools.permutations(range(4)):
                classes.setdefault(f.behaviour(priority,self.obs[h]),[]).append(priority)
            self.assertEqual(len(classes),2,f'history {h}')
            self.assertEqual(sorted(len(v) for v in classes.values()),[12,12])

    def test_effective_is_one_bit_against_a_nominal_4_58(self):
        for h in (0,1):
            classes={f.behaviour(p,self.obs[h]) for p in itertools.permutations(range(4))}
            self.assertAlmostEqual(len(classes),2)
        self.assertGreater(4.58,1.0,'the nominal figure AC20-AC23 were sized against is 4.58')


class TestScaledTargets(unittest.TestCase):
    def test_scaled_effective_targets_are_stated(self):
        """The numbers the scaled design must hit, recorded so a future run can be checked against
        them rather than argued about."""
        import math
        self.assertAlmostEqual(math.log2(math.factorial(6)),9.49,places=2)
        self.assertAlmostEqual(math.log2(math.factorial(6)/6),6.91,places=2)
        self.assertAlmostEqual(math.log2(2),1.0,places=2)


if __name__=='__main__':
    unittest.main()
