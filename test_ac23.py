"""AC23 tests: the scaled body layer, and its reducibility to the frozen observation.

Run with: .venv/bin/python -B -m unittest test_ac23
"""
import unittest
import numpy as np
import ac23_body as body
import ac9


class TestObservationReducibility(unittest.TestCase):
    """At the frozen width and layout the word must BE ac9.observe."""

    def test_matches_ac9_observe_on_randomized_states(self):
        rng=np.random.default_rng(7); checked=mismatches=0
        for seed in (0,1,2):
            o=ac9.acquire(seed)
            for _ in range(200):
                body._randomize(o,rng)
                checked+=1
                if body.observe(o)!=ac9.observe(o): mismatches+=1
        self.assertEqual(checked,600)
        self.assertEqual(mismatches,0)

    def test_urgent_memory_sets_the_urgency_bits(self):
        """Bit 3 (and 4) must come from memory urgency, not from a bank's disagreement. Urgency is
        a slot near expiry: `life > 0 and life <= 16`."""
        o=ac9.acquire(0)
        o.body.traces[:]=0; o.body.life[:]=0; o.body.boundary[:]=200
        o.memory.life[0,:]=8
        self.assertEqual((body.observe(o)>>3)&1,1,'a slot near expiry is urgent')
        o.memory.life[0,:]=100
        self.assertEqual((body.observe(o)>>3)&1,0,'a healthy slot is not urgent')
        o.memory.life[0,:]=0
        self.assertEqual((body.observe(o)>>3)&1,0,'an empty slot is not urgent either')

    def test_bit_five_is_never_set(self):
        """The frozen observation cannot set bit 5, which is why AC12's mask-32 rule is dead."""
        rng=np.random.default_rng(3)
        o=ac9.acquire(0); seen=set()
        for _ in range(300):
            body._randomize(o,rng); seen.add((body.observe(o)>>5)&1)
        self.assertEqual(seen,{0})

    def test_program_disagreement_bit(self):
        """Bit 2 is the disagreement of the whole 126-bit program bank, and one bit with minority
        replicas contributes only min(ones,7-ones) <= 3, so two disagreeing bits are needed to
        reach the threshold of 4 -- the same arithmetic that made AC19's corruption model
        delicate."""
        o=ac9.acquire(0)
        o.body.traces[:]=0; o.body.life[:]=0; o.body.boundary[:]=200
        self.assertEqual((body.observe(o)>>2)&1,0)
        o.body.traces[0,0,:4]=1                      # bit 0: four of seven replicas set
        self.assertEqual((body.observe(o)>>2)&1,0,'one disagreeing bit contributes at most 3')
        o.body.traces[0,1,:4]=1                      # bit 1: likewise -> 3+3 = 6 >= 4
        self.assertEqual((body.observe(o)>>2)&1,1,'two disagreeing bits reach the threshold')


class TestScaledWord(unittest.TestCase):
    def test_scaled_word_width_and_positions(self):
        o=ac9.acquire(0)
        word=body.observe(o,frozen_only=False)
        self.assertEqual(body.FROZEN_BITS,(0,1,2,3,4,6,7,8))
        self.assertEqual(body.SCALED_EXTRA_BITS,(9,10,11))
        self.assertLess(word,1<<body.OBS_BITS)

    def test_frozen_positions_are_untouched_by_the_extension(self):
        """Whatever the added bits do, the frozen eight must be unchanged -- that is what makes
        this a generalization."""
        rng=np.random.default_rng(11)
        o=ac9.acquire(0)
        mask=sum(1<<b for b in body.FROZEN_BITS)
        for _ in range(100):
            body._randomize(o,rng)
            self.assertEqual(body.observe(o,frozen_only=False)&mask,ac9.observe(o)&mask)

    def test_added_banks_are_only_read_when_present(self):
        """q_bank is defined for the added banks; with a four-bank body the added bits stay 0."""
        o=ac9.acquire(0)
        self.assertEqual(body.banks_of(o.body),4)
        self.assertEqual((body.observe(o,frozen_only=False)>>10)&1,0)
        self.assertEqual((body.observe(o,frozen_only=False)>>11)&1,0)


class TestBodyLayout(unittest.TestCase):
    def test_particles_start_after_the_bank_sites(self):
        o=ac9.acquire(0)
        self.assertEqual(body.particles_offset(o.body),4*body.banks_of(o.body))
        self.assertEqual(body.particles_offset(o.body),16,'the frozen particle offset')

    def test_available_matches_the_frozen_formula(self):
        rng=np.random.default_rng(5)
        o=ac9.acquire(0)
        for _ in range(50):
            body._randomize(o,rng)
            np.testing.assert_array_equal(body.available(o.body),ac9.ac4.available(o.body))

    def test_inventory_shape(self):
        o=ac9.acquire(0)
        self.assertEqual(len(body.inventory(o.body)),5)

    def test_scaled_acquisition_is_explicitly_unbuilt(self):
        """This module supplies the layout and the word; the scaled acquisition is the next
        increment. It must SAY so and raise, not quietly return a four-bank body."""
        self.assertEqual((body.BANKS,body.PARTICLES),(4,4))
        self.assertIsNotNone(body.acquire(0))
        with self.assertRaises(NotImplementedError):
            body.acquire(0,banks=6)


if __name__=='__main__':
    unittest.main()
