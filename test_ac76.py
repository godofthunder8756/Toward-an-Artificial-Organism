"""AC76 tests: pin the re-instantiation mechanism, the gate shape, and the recorded outcomes."""
import json
import unittest
from pathlib import Path
import numpy as np
import ac12
import ac76


def setUpModule():
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (); ac12.MOVE = 10**9; ac12.DEV = ac76.ac71.DEV
    ac12.REGISTER_THRESHOLD = 4


class TestRegenerationMechanism(unittest.TestCase):
    def test_priority_roundtrip(self):
        for p in [(0, 1, 2, 3), (3, 2, 1, 0), (1, 3, 0, 2), (2, 0, 3, 1)]:
            self.assertEqual(ac76.decode_priority(ac76.encode_priority(p)), p)

    def test_reinstantiation_excludes_register(self):
        # reg_from_priority must re-derive the program but leave the register bits untouched
        import ac9, ac4, ac5_program as prog
        _, _, _, priority = ac4.acquire(0)
        alloc = ac12.Alloc('allocate', 0, 0)
        o, offs = ac12.acquire(0)
        alloc.offs = offs
        o.body.traces[1, :8] = ac76.encode_priority(priority)[:, None]
        # set a register bit (dynamic decision state) and a program bit (bit 0) corrupt, then re-instantiate
        o.body.traces[0, offs[0]] = 1                              # register bit -> relinquished
        target = prog.program(priority)
        o.body.traces[0, 0, 0:4] = 1 - int(target[0])              # corrupt program bit 0
        o.body.traces[0, 1, 0:4] = 1 - int(target[1])              # and bit 1 (to cross the signal threshold)
        e = ac9.event()
        ac76.reg_from_priority(o, e)
        # the register bit must survive (still reads relinquished); bit 0 must be re-derived
        self.assertEqual(int(o.body.traces[0, offs[0]].sum() >= 4), 1,
                         'register bit must be excluded from re-instantiation')
        self.assertEqual(int(o.body.traces[0, 0].sum() >= 4), int(target[0]),
                         'program bit 0 must be re-instantiated to the correct value')

    def test_gate_keys(self):
        g = ac76.gates([])
        self.assertEqual(set(g.keys()), {
            'G1_regen_recovers', 'G2_baseline_cements', 'G3_regeneration_load_bearing',
            'G4_control_clean', 'G5_completeness_determinism'})


class TestRecordedOutcomes(unittest.TestCase):
    @unittest.skipUnless(Path('ac76_results_v1/results.json').exists(), 'finals not yet run')
    def test_recorded_freeze(self):
        with open('ac76_results_v1/results.json') as f:
            results = json.load(f)
        rows = results['rows']
        g = ac76.gates(rows)
        self.assertTrue(all(v for v in g.values() if v is not None), f'gates not all pass: {g}')
        regen = [r for r in rows if r['arm'] == 'regen' and r['corrupt']]
        baseline = [r for r in rows if r['arm'] == 'baseline' and r['corrupt']]
        self.assertTrue(all(r['flipped_still_wrong'] == 0 for r in regen),
                        'recorded freeze must show regen recovering the corrupted bits')
        self.assertTrue(all(r['flipped_still_wrong'] > 0 for r in baseline),
                        'recorded freeze must show baseline cementing the corrupted bits')


if __name__ == '__main__':
    unittest.main()
