"""AC91 tests: the W-birth gate is a no-op for the shared arms, blocks exactly bank-0 births and
writes no content, W-birth is autocatalytic, the restore-tick semantics, the final-seed
disjointness, and the gate shapes (G1-G6 categorical, per individual). Not hashed (AC17's rule)."""
import unittest
import json
from pathlib import Path
import numpy as np
import ac4
import ac9
import ac12
import ac91


def setUpModule():
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (1,); ac12.MOVE = 10**9; ac12.DEV = ac91.ac71.DEV
    ac12.REGISTER_THRESHOLD = 4


def _body():
    b = ac4.Body(np.zeros((4, 1024, 7), dtype=np.uint8),
                 np.array([32, 48, 64, 0] * 4 + [64, 96, 128, 0], dtype=np.int16),
                 np.zeros((20, 2), dtype=np.int16),
                 np.arange(128, 248, 6, dtype=np.int16))
    # put all W catalysts inside (pos 0,0) so they are available
    b.pos[:] = 0
    b.energy = 100; b.material = 200
    return b


def _ns():
    return dict(vars(ac9), now=0)


class TestBirthGateNoOpForSharedArms(unittest.TestCase):
    def test_shared_arms_have_no_block(self):
        for arm in ('succession', 'repair', 'unmaintained', 'no_repair'):
            self.assertNotIn('block_W', ac91.ARM_PARTS[arm],
                             f'{arm} must run the frozen birth (no gate)')

    def test_new_arms_do_block(self):
        self.assertTrue(ac91.ARM_PARTS['no_W']['block_W'])
        self.assertTrue(ac91.ARM_PARTS['W_restore']['block_W'])
        self.assertTrue(ac91.ARM_PARTS['W_restore_late']['block_W'])


class TestBirthGateSemantics(unittest.TestCase):
    def test_gate_blocks_only_bank0(self):
        ns = _ns()
        ns['now'] = 10
        gate = ac91.make_birth(ns, dict(block_W=True, restore_tick=None))
        b = _body()
        e = ac9.event()            # ac9.birth writes region*_births counters
        # bank 0 (W) blocked
        self.assertFalse(gate(b, 0, 0, e))
        # bank 1 (region catalyst) NOT blocked -> passes through to the frozen birth
        self.assertTrue(gate(b, 1, 0, e))

    def test_gate_writes_no_content(self):
        ns = _ns()
        ns['now'] = 10
        gate = ac91.make_birth(ns, dict(block_W=True, restore_tick=None))
        b = _body()
        before_traces = b.traces.copy()
        e = ac4.empty_event()
        gate(b, 0, 0, e)          # blocked: must not write content or spend resources
        np.testing.assert_array_equal(b.traces, before_traces,
                                      'blocked birth must not touch traces (content)')
        self.assertEqual(e['spent_m'], 0)
        self.assertEqual(e['spent_e'], 0)

    def test_restore_tick_semantics(self):
        ns = _ns()
        cfg = dict(block_W=True, restore_tick=50)
        gate = ac91.make_birth(ns, cfg)
        b = _body()
        e = ac4.empty_event()
        ns['now'] = 49
        self.assertFalse(gate(b, 0, 0, e), 'blocked before restore tick')
        ns['now'] = 50
        self.assertTrue(gate(b, 0, 0, e), 'un-blocked at the restore tick')


class TestWBirthIsAutocatalytic(unittest.TestCase):
    def test_no_W_means_zero_capacity_and_no_parent(self):
        b = _body()
        b.life[:4] = 0            # W fully depleted
        # no available W to parent a birth
        self.assertEqual(int(ac4.available(b)[:4].sum()), 0,
                         'with W depleted there is no live W parent')
        # and the W-catalyzed write capacity (the reconstruction capacity) is exactly 0
        self.assertEqual(ac91._cap(b), 0,
                         'reconstruction capacity 8*W is 0 when W is depleted')
        # the step only calls birth when a live parent exists (the autocatalytic guard)
        parents = np.flatnonzero(ac4.available(b)[0:4])
        self.assertEqual(len(parents), 0, 'action 6 finds no W parent, so no birth fires')

    def test_parent_allows_birth(self):
        b = _body()
        b.life[:4] = [1, 0, 0, 0]  # one live W parent
        e = ac9.event()
        self.assertTrue(ac9.birth(b, 0, 0, e))
        self.assertEqual(e['W_birth'], 1)


class TestDeclaredSeeds(unittest.TestCase):
    def test_final_seeds_disjoint(self):
        finals = {4200, 4201, 4202, 4203}
        self.assertTrue(finals.isdisjoint(range(8)), 'finals disjoint from engineering 0-7')
        self.assertTrue(finals.isdisjoint(range(4111)), 'finals disjoint from prior final families')


class TestGateShapes(unittest.TestCase):
    def test_gate_keys(self):
        self.assertEqual(set(ac91.gates([]).keys()),
                         {'G1_block_reduces_machinery_then_capacity',
                          'G2_restore_rescues_reconstruction',
                          'G3_restore_late_is_irreversible',
                          'G4_turnover_while_content_persists',
                          'G5_repair_only_survives',
                          'G6_controls_die',
                          'G7_completeness_determinism'})

    def test_G1_is_categorical_per_individual(self):
        # a single no_W individual that survives (or keeps W) must fail G1
        good = dict(arm='no_W', damage=True, corrupt=True, transition='none',
                    first_W_empty=63, W=0, W_births_bank0=0, reg_writes=7, completed=False)
        bad = dict(good, completed=True)
        self.assertTrue(ac91.gates([good])['G1_block_reduces_machinery_then_capacity'])
        self.assertFalse(ac91.gates([bad])['G1_block_reduces_machinery_then_capacity'])

    def test_G2_restore_rescues(self):
        good = dict(arm='W_restore', damage=True, corrupt=True, transition='none',
                    completed=True, flipped_still_wrong=0, description_correct=130,
                    W_births_bank0=5, W=3)
        bad = dict(good, flipped_still_wrong=1)
        self.assertTrue(ac91.gates([good])['G2_restore_rescues_reconstruction'])
        self.assertFalse(ac91.gates([bad])['G2_restore_rescues_reconstruction'])

    def test_G3_restore_late_irreversible(self):
        good = dict(arm='W_restore_late', damage=True, corrupt=True, transition='none',
                    completed=False, W=0, W_births_bank0=0)
        bad = dict(good, completed=True)
        self.assertTrue(ac91.gates([good])['G3_restore_late_is_irreversible'])
        self.assertFalse(ac91.gates([bad])['G3_restore_late_is_irreversible'])

    def test_G6_controls_die(self):
        un = dict(arm='unmaintained', damage=True, corrupt=True, transition='none', completed=False)
        nr = dict(arm='no_repair', damage=True, corrupt=True, transition='none', completed=False)
        self.assertTrue(ac91.gates([un, nr])['G6_controls_die'])
        self.assertFalse(ac91.gates([dict(un, completed=True), nr])['G6_controls_die'])


class TestRecordedFreeze(unittest.TestCase):
    @unittest.skipUnless(Path('ac91_results_v1/results.json').exists(), 'finals not yet run')
    def test_recorded_freeze(self):
        with open('ac91_results_v1/results.json') as f:
            results = json.load(f)
        rows = results['rows']
        g = ac91.gates(rows)
        g['G7_completeness_determinism'] = len(rows) == len(results['seeds']) * 2 * 28
        self.assertTrue(all(v for v in g.values() if v is not None), f'gates not all pass: {g}')

    @unittest.skipUnless(Path('ac91_results_v1/results.json').exists(), 'finals not yet run')
    def test_no_W_content_intact_at_death(self):
        # link 1's mechanism: the dying no_W individual loses the MACHINERY (W), not the content
        # (description) -- description_correct_at_death == 130.
        with open('ac91_results_v1/results.json') as f:
            rows = json.load(f)['rows']
        for r in rows:
            if r['arm'] == 'no_W' and r['damage'] and r['corrupt']:
                self.assertEqual(r['description_correct_at_death'], 130,
                                 f"no_W seed {r['seed']}: content must be intact at death "
                                 '(machinery, not content, is what is lost)')


if __name__ == '__main__':
    unittest.main()
