"""AC28 tests: six-region maintenance chemistry.

Run with: .venv/bin/python -B -m unittest test_ac28
"""
import unittest
import numpy as np
import ac4
import ac25_confront as cf
import ac27_schedule as sched
import ac28_regions as rg


class TestSignalsFromBodyState(unittest.TestCase):
    def test_signal_is_derived_from_the_life_array(self):
        b=rg.acquire(0)
        self.assertEqual(rg.signal(b),0,'a healthy body demands nothing')
        b.life[2*rg.SITES]=8
        self.assertEqual(rg.signal(b),1<<2)

    def test_an_empty_region_is_not_urgent(self):
        """A dead region is not a need -- matching the frozen urgency rule, which requires life>0."""
        b=rg.acquire(0)
        b.life[3*rg.SITES:4*rg.SITES]=0
        self.assertEqual(rg.signal(b),0)

    def test_six_independent_regions(self):
        b=rg.acquire(0)
        for k in range(rg.REGIONS):
            b.life[:]=np.tile(np.array([32,48,64,0],dtype=np.int16),rg.REGIONS)
            b.life[k*rg.SITES]=8
            self.assertEqual(rg.signal(b),1<<k)


class TestBirthChemistry(unittest.TestCase):
    def test_birth_costs_the_frozen_price(self):
        b=rg.acquire(1); e=rg.fresh_event()
        before=rg.region_sites(b,0).copy()
        self.assertTrue(rg.birth_region(b,0,e))
        self.assertEqual(e['spent_m'],rg.BIRTH_MATERIAL)
        self.assertEqual(e['spent_e'],rg.BIRTH_ENERGY)
        self.assertEqual(b.life[0*4],before[0],'the parent is unchanged')
        self.assertEqual(b.life[0*4+3],rg.CHILD_LIFE,'the empty slot becomes a child')

    def test_birth_needs_a_parent(self):
        b=rg.acquire(1); e=rg.fresh_event()
        b.life[0:4]=0
        self.assertFalse(rg.birth_region(b,0,e))

    def test_birth_needs_an_empty_slot(self):
        b=rg.acquire(1); e=rg.fresh_event()
        b.life[0:4]=64
        self.assertFalse(rg.birth_region(b,0,e))

    def test_birth_needs_material(self):
        b=rg.acquire(1); e=rg.fresh_event()
        b.material=1
        self.assertFalse(rg.birth_region(b,0,e))
        self.assertEqual(b.material,1,'a failed payment spends nothing')

    def test_region_actions_do_not_collide_with_the_frozen_actions(self):
        frozen=set(range(10))
        self.assertFalse(frozen & set(rg.REGION_ACTIONS))
        self.assertEqual(len(set(rg.REGION_ACTIONS)),rg.REGIONS)

    def test_dispatch_sends_frozen_actions_to_the_frozen_chemistry(self):
        """Actions 0..9 must be handled by ac4.react, not by this module."""
        b=rg.acquire(3); e=rg.fresh_event()
        b.fuel=0
        rg.react(b,0,e)
        self.assertEqual(b.fuel,32,'ac4.react action 0 tops up fuel')


class TestConservation(unittest.TestCase):
    def test_identities_hold_over_a_driven_loop(self):
        """step() asserts the life-count, energy, material and spent-material identities every tick.
        Drive it hard -- draining and refilling regions -- and it must never break."""
        b=rg.acquire(4); rng=np.random.default_rng(0)
        for _ in range(300):
            for k in range(rg.REGIONS):
                if rng.random()<0.4: b.life[k*rg.SITES]=int(rng.integers(1,18))
            order=tuple(rng.permutation(rg.REGIONS))
            rg.step(b,order)
        self.assertGreater(int((b.life>0).sum()),0)

    def test_death_stops_the_chemistry(self):
        b=rg.acquire(5); b.energy=0
        e,action=rg.step(b,tuple(range(rg.REGIONS)))
        self.assertTrue(b.dead)
        self.assertIsNone(action)


class TestOrderStructure(unittest.TestCase):
    def test_criterion_met_over_six_region_rules(self):
        codes=cf.unique_codes(rg.REGIONS)
        self.assertEqual(cf.classes(codes,sched.all_pairs()),720)

    def test_control_one_region_at_a_time_gives_nothing(self):
        codes=cf.unique_codes(rg.REGIONS)
        self.assertEqual(cf.classes(codes,[1<<k for k in range(rg.REGIONS)]),1)

    def test_control_frozen_shape_gives_one_bit(self):
        codes=cf.unique_codes(rg.REGIONS)+[1<<6]
        self.assertEqual(cf.classes(codes,[1<<0,1<<0|1<<6]),2)

    def test_choice_follows_the_order(self):
        """The acquired object is the order: for an urgent pair, whichever position comes first in
        the permutation wins."""
        self.assertEqual(rg.choose((3,1),0b1010),3)
        self.assertEqual(rg.choose((1,3),0b1010),1)
        self.assertIsNone(rg.choose((0,),0b10))


if __name__=='__main__':
    unittest.main()
