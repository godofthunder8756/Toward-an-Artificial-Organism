"""AC75 tests: pin the erase mechanism, the gate shape, and the recorded outcomes.

Per the project's ambient-state rule, setUpModule pins the ac12 globals the study depends on, so an
earlier test file's residue cannot change the world these arms run in. The verification tools themselves
are NOT hashed into the study's snapshot (AC17's rule).
"""
import json
import unittest
from pathlib import Path
import numpy as np
import ac12
import ac75


def setUpModule():
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (1,); ac12.MOVE = 10**9; ac12.DEV = ac75.DEV
    ac12.REGISTER_THRESHOLD = 4


class TestEraseMechanism(unittest.TestCase):
    def test_erase_class_drop_clears_entry(self):
        # the single declared change: _drop also clears the entry's life and bits
        ac12.PORTS = 4
        alloc = ac75.AllocErase('allocate', 0, 0)
        import ac9, ac4
        o, offs = ac12.acquire(0)
        alloc.offs = offs; alloc.shadow = o.body.traces[0].copy()
        # deposit a route for key 1, then relinquish it, and confirm the entry is gone
        e = ac9.event()
        o.memory.life[0, 0] = 64
        o.memory.bits[0, 0] = np.array([1, 1, 0], dtype=np.uint8)[:, None]
        alloc.streak[1] = ac12.STREAK_N
        # set the register offset to a value that lets the drop proceed
        place = ac12.m12.slot_of_key(o.memory, 1)
        off = alloc.offs[2 * place[0] + place[1]]
        alloc._drop(o, e, 1)
        self.assertEqual(int((o.memory.life[place[0], place[1]] > 0).sum()), 0,
                         'erase-on-relinquish must clear the entry')
        self.assertIsNone(o.memory.read(1), 'read(1) must be None after erase')

    def test_restore_does_not_erase(self):
        # the rival leaves the entry (it only stops renewal) -- this is what the erase fixes
        alloc = ac75.AllocRestore('allocate', 0, 0)
        import ac9, ac4
        o, offs = ac12.acquire(0)
        alloc.offs = offs; alloc.shadow = o.body.traces[0].copy()
        e = ac9.event()
        o.memory.life[0, 0] = 64
        o.memory.bits[0, 0] = np.array([1, 1, 0], dtype=np.uint8)[:, None]
        alloc.streak[1] = ac12.STREAK_N
        alloc._drop(o, e, 1)
        self.assertIsNotNone(o.memory.read(1),
                             'restore (no erase) leaves the stale entry in place for its life')


class TestGateShape(unittest.TestCase):
    def test_gate_keys(self):
        g = ac75.gates([])
        self.assertEqual(set(g.keys()), {
            'G1_erase_survives_perm', 'G2_erase_survives_temp', 'G3_erase_reacquires_and_holds',
            'G4_erase_register_intact', 'G5_restore_fails_under_change', 'G6_repair_load_bearing',
            'G7_inert_without_change', 'G8_completeness_determinism'})

    def test_g7_requires_state_hash_equality(self):
        # erase/none must reproduce restore/none exactly, not merely behave similarly
        r = dict(seed=0, history=0, arm='erase', transition='none', relinquishments=0,
                 demand=[42, 0], state_hash='x')
        rr = dict(r); rr['arm'] = 'restore'
        self.assertTrue(ac75.gates([r, rr])['G7_inert_without_change'])


class TestRecordedOutcomes(unittest.TestCase):
    @unittest.skipUnless(Path('ac75_results_v1/results.json').exists(), 'finals not yet run')
    def test_recorded_freeze(self):
        with open('ac75_results_v1/results.json') as f:
            results = json.load(f)
        rows = results['rows']
        g = ac75.gates(rows)
        # the freeze must be green; a failing gate here means the code changed the record
        self.assertTrue(all(v for v in g.values() if v is not None), f'gates not all pass: {g}')
        # the erase's contribution is a real separation, pinned
        erase_temp = [r for r in rows if r['arm'] == 'erase' and r['transition'] == 'temp']
        restore_temp = [r for r in rows if r['arm'] == 'restore' and r['transition'] == 'temp']
        self.assertTrue(all(r['first_dead'] is None for r in erase_temp))
        self.assertTrue(any(r['first_dead'] is not None for r in restore_temp),
                        'the recorded freeze must show the no-erase rival failing under change')


if __name__ == '__main__':
    unittest.main()
