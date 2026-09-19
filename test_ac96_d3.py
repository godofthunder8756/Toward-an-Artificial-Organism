"""AC96-D3 tests: relinquishment fires, observer-discard on the streak, interruption during a streak.

Engineering (no freeze). Pins the three D3 items per individual on the two seeds where the
maintained-streak relinquishment actually fires in the perm world (seeds 0 and 3 -- the D2
handoff's recorded set):

1. Relinquishment fires: the maintained streak reaches STREAK_N, _drop fires (register bit set,
   entry erased), and the organism re-acquires (AC75).
2. Observer-discard on the streak: at a mid-streak tick (streak == 2, non-zero), replacing the
   succession observer AND clearing the host streak dict with fresh objects leaves the trajectory
   byte-identical (state_hash) -- the streak is recovered from maintained state alone.
3. Interruption during a streak: cutting W at the same mid-streak tick stops every paid streak
   write (no advance, no host-assisted drop), degrades the streak only sub-threshold (no majority
   flip, no spurious drop) over the W=0 window before the death cascade, and a machinery-only
   rescue restores the correct count (streak_at_rescue == streak_at_cut) with paid writes resuming.

Not hashed (AC17's rule) -- verification tool only.
"""
import unittest
import ac12
import ac95
import ac96


def setUpModule():
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (1,); ac12.MOVE = 10**9; ac12.DEV = ac95.ac71.DEV
    ac12.REGISTER_THRESHOLD = 4


class TestRelinquishmentFires(unittest.TestCase):
    """Item 1: the maintained streak reaches STREAK_N with a bound entry, _drop fires, the
    organism re-acquires."""

    def test_drop_fires_and_reacquires_on_seeds_0_3(self):
        for seed in (0, 3):
            r = ac96.run(seed, 0, 'gated', True, False, 'perm', streak_maintained=True)
            self.assertEqual(r['relinquishments'], 1, f'seed {seed}: drop did not fire')
            self.assertTrue(r['drop_ticks'], f'seed {seed}: no drop tick recorded')
            dtick, place, reg_bit = r['drop_ticks'][0]
            self.assertTrue(reg_bit, f'seed {seed}: register bit not set at drop')
            reacq = r['reacquire_ticks'].get(1, [])
            self.assertTrue(reacq, f'seed {seed}: key 1 never re-acquired')
            self.assertGreater(reacq[0], dtick, f'seed {seed}: re-acquisition before drop')
            # streak reached the threshold before the drop: the drop event reads before==5
            events = [e for e in r['streak_events'] if e[1] == 1 and e[0] >= ac96.MOVE_TICK]
            drop_events = [e for e in events if e[4] == 1]
            self.assertEqual(len(drop_events), 1, f'seed {seed}: expected exactly one drop event')
            self.assertEqual(drop_events[0][0], dtick, f'seed {seed}: drop event tick mismatch')
            self.assertEqual(drop_events[0][2], 5, f'seed {seed}: drop fired at streak 5')


class TestObserverDiscard(unittest.TestCase):
    """Item 2: observer-discard on the streak leaves the trajectory byte-identical."""

    def test_mid_streak_swap_byte_identical(self):
        for seed in (0, 3):
            d = ac96.observer_discard_equivalence(seed, 0)
            self.assertNotEqual(d.get('status'), 'no_mid_streak', f'seed {seed}: no mid-streak tick')
            self.assertTrue(d['swap_applied'], f'seed {seed}: swap hook never fired')
            self.assertEqual(d['streak_at_swap'], 2, f'seed {seed}: swap not at a non-zero streak')
            self.assertTrue(d['identical'], f'seed {seed}: observer-discard changed the trajectory')


class TestInterruption(unittest.TestCase):
    """Item 3: cut W mid-streak stops paid streak writes (no advance), degrades sub-threshold only,
    and a machinery-only rescue restores the correct count."""

    def test_w_gating_and_rescue(self):
        for seed in (0, 3):
            d = ac96.interruption_equivalence(seed, 0)
            self.assertNotEqual(d.get('status'), 'no_mid_streak', f'seed {seed}: no mid-streak tick')
            cut = d['cut']; rescue = d['rescue']
            # streak frozen at 2 at the cut (mid-streak, non-zero, below threshold)
            self.assertEqual(cut['streak_final'][1], 2, f'seed {seed}: streak not frozen at cut')
            # W=0 -> no paid streak write (no advance, no host-assisted drop)
            self.assertEqual(cut['streak_writes_after_cut'], 0,
                             f'seed {seed}: a paid streak write fired at W=0')
            self.assertEqual(cut['relinquishments'], 0,
                             f'seed {seed}: a drop fired at W=0 (host-assisted?)')
            # sub-threshold degradation only: no should-be-0 bit majority-flipped
            self.assertEqual(cut['streak_degraded_bits_end'], 0,
                             f'seed {seed}: a streak bit majority-flipped under damage')
            # no-rescue dies with W=0
            self.assertFalse(cut['completed'], f'seed {seed}: no-rescue cut arm survived')
            # machinery-only rescue restores W, the correct count, and paid writes resume
            self.assertTrue(rescue['completed'], f'seed {seed}: rescue arm did not survive')
            self.assertEqual(rescue['streak_at_rescue'], {0: 0, 1: 2},
                             f'seed {seed}: rescue did not recover the cut-time streak')
            self.assertGreater(rescue['streak_writes_after_cut'], 0,
                               f'seed {seed}: paid writes did not resume after rescue')


class TestInstrumentationInert(unittest.TestCase):
    """The D3 instrumentation is observational: the host-streak control (no `streak_events`
    attribute) still runs and returns the new fields with benign defaults."""

    def test_host_control_has_no_streak_events_and_survives(self):
        r = ac96.run(0, 0, 'gated', True, False, 'perm', streak_maintained=False)
        self.assertEqual(r['streak_events'], [])
        self.assertEqual(list(r['reacquire_ticks']), [0, 1])
        self.assertIsNone(r['first_W_empty'])
        self.assertIsNone(r['streak_bits_at_cut'])

    def test_maintained_streak_events_are_unproductive_only(self):
        r = ac96.run(0, 0, 'gated', True, False, 'perm', streak_maintained=True)
        for (t, key, before, after, dropped) in r['streak_events']:
            self.assertIn(key, (0, 1))
            self.assertIn(dropped, (0, 1))


if __name__ == '__main__':
    unittest.main()
