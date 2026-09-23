"""Tests for AC108 (K7) — cognitive-organizational coupling, both directions, selective interventions.

These pin the mechanism and the coupling arms so a future code change that alters the record is caught.
The two directions are asserted on single deterministic individuals (seed 0): direction 1 (maintenance
-> accuracy/use) via the `no_write` arm, direction 2 (content -> adaptation) via the `force_machinery`
arm, plus the clean control (interventions inert absent a cause) and the frozen-copy reproduction license.

Run: .venv/bin/python -B -m unittest test_ac108
"""
import unittest
import ac108
import ac107
import ac106
import ac12


def setUpModule():
    # pin the ambient module state the study depends on (the AC16/AC17 lesson)
    ac12.PORTS = 4
    ac12.YIELD_M = 64
    ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None
    ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (1,)
    ac12.MOVE = 10**9
    ac12.DEV = ac108.DEV
    ac12.REGISTER_THRESHOLD = 4


class TestDirection1Maintenance(unittest.TestCase):
    def test_candidate_writes_and_reads_machinery_in_cut(self):
        # the paid write flips 1->0 in the cut: candidate reads E_machinery (0) and writes 7 replicas.
        cut = ac108.run(0, 0, 'candidate', 'cut')
        self.assertEqual(cut['bel_at_cut_end'], 0)
        self.assertEqual(cut['bel_writes'], 7)
        self.assertEqual(cut['bel_attempts'], 1)

    def test_no_write_never_writes_and_reads_world_in_cut(self):
        # cutting the maintenance leaves the estimate at its acquired value (E_world=1): inaccurate in
        # the cut, and no maintenance spend.
        cut = ac108.run(0, 0, 'no_write', 'cut')
        self.assertEqual(cut['bel_at_cut_end'], 1)
        self.assertEqual(cut['bel_writes'], 0)
        self.assertEqual(cut['bel_attempts'], 0)

    def test_no_write_is_read_honest_not_forced(self):
        # no_write reads the ACTUAL bit (stays 1), whereas scramble FORCES the read to 1 while still
        # writing 0 in the cut -- the two are mechanically distinct.
        nw = ac108.run(0, 0, 'no_write', 'cut')
        scr = ac108.run(0, 0, 'scramble', 'cut')
        self.assertEqual(nw['bel_at_cut_end'], 1)
        self.assertEqual(nw['bel_writes'], 0)
        self.assertEqual(scr['bel_writes'], 7)   # scramble still writes (maintenance intact)


class TestDirection2Content(unittest.TestCase):
    def test_candidate_adapts_in_move(self):
        move = ac108.run(0, 0, 'candidate', 'move')
        self.assertEqual(move['bel_at_first_drop'], 1)
        self.assertGreaterEqual(move['relinquishments'], 1)
        self.assertIsNone(move['first_dead'])

    def test_force_machinery_holds_and_dies_in_move(self):
        # forcing the E_machinery content reverses the adaptation: the organism holds the stale route
        # and dies (seed 0), where the candidate relinquishes and survives.
        cand = ac108.run(0, 0, 'candidate', 'move')
        fm = ac108.run(0, 0, 'force_machinery', 'move')
        self.assertEqual(fm['relinquishments'], 0)
        self.assertIsNotNone(fm['first_dead'])
        self.assertIsNone(cand['first_dead'])


class TestCleanControl(unittest.TestCase):
    def test_no_write_and_scramble_inert_absent_cause(self):
        # no_write and scramble read the acquired value (E_world), so they are byte-identical to the
        # candidate when no cause is present.
        cand = ac108.run(0, 0, 'candidate', 'no_cause')
        nw = ac108.run(0, 0, 'no_write', 'no_cause')
        scr = ac108.run(0, 0, 'scramble', 'no_cause')
        self.assertEqual(nw['state_hash'], cand['state_hash'])
        self.assertEqual(scr['state_hash'], cand['state_hash'])

    def test_force_machinery_absent_cause_only_adds_proactive_spend(self):
        # forcing E_machinery activates the proactive-renewal consumption even absent a cause -- a
        # disclosed consequence of the forced content, identical in survival/routes/relinquishments.
        cand = ac108.run(0, 0, 'candidate', 'no_cause')
        fm = ac108.run(0, 0, 'force_machinery', 'no_cause')
        self.assertEqual(fm['completed'], cand['completed'])
        self.assertEqual(fm['routes'], cand['routes'])
        self.assertEqual(fm['relinquishments'], cand['relinquishments'])
        self.assertEqual(fm['demand'], cand['demand'])
        self.assertGreater(fm['proactive_writes'], cand['proactive_writes'])


class TestFrozenCopyReproduction(unittest.TestCase):
    def test_frozen_arms_reproduce_ac107(self):
        # the extension is inert for the frozen arms: ac108's candidate/r2 reproduce ac107 byte-for-byte.
        repro = ac108.reproduction_check(seeds=[0], conditions=('move',), arms=('candidate', 'r2'))
        self.assertTrue(all(repro.values()), repro)


if __name__ == '__main__':
    unittest.main()
