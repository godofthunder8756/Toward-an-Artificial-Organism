"""AC79 tests: pin the description-maintenance mechanism, the gate shape, and the recorded outcomes."""
import json
import unittest
from pathlib import Path
import numpy as np
import ac12
import ac76
import ac79


def setUpModule():
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (); ac12.MOVE = 10**9; ac12.DEV = ac79.ac71.DEV
    ac12.REGISTER_THRESHOLD = 4


class TestDescriptionMaintenanceMechanism(unittest.TestCase):
    def test_priority_roundtrip(self):
        for p in [(0, 1, 2, 3), (3, 2, 1, 0), (1, 3, 0, 2), (2, 0, 3, 1)]:
            self.assertEqual(ac76.decode_priority(ac76.encode_priority(p)), p)

    def test_description_repair_is_paid(self):
        # reg_description must restore minority replicas to the majority AND pay per repaired replica
        import ac9, ac4
        _, _, _, priority = ac4.acquire(0)
        alloc = ac12.Alloc('allocate', 0, 0)
        o, offs = ac12.acquire(0)
        alloc.offs = offs
        o.body.traces[1, :8] = ac76.encode_priority(priority)[:, None]
        o.body.traces[1, 0, 0] ^= 1              # flip exactly one replica of bit 0 -> minority
        e = ac9.event()
        e0, m0 = int(o.body.energy), int(o.body.material)
        dec = ac79.reg_description(o, e)
        self.assertEqual(len(set(o.body.traces[1, 0].tolist())), 1,
                         'bit 0 replicas must agree after repair (minority restored)')
        self.assertEqual(o.body.energy, e0 - 1, 'one energy paid per repaired replica')
        self.assertEqual(o.body.material, m0 - 1, 'one material paid per repaired replica')
        self.assertEqual(e['spent_e'], 1)
        self.assertEqual(e['spent_m'], 1)
        self.assertEqual(e['reg_writes'], 1)
        self.assertEqual(dec, tuple(priority), 'repaired description decodes to the original priority')

    def test_reinstantiation_excludes_register(self):
        # reg_maintained must re-derive the program but leave the register bits untouched
        import ac9, ac4, ac5_program as prog
        _, _, _, priority = ac4.acquire(0)
        alloc = ac12.Alloc('allocate', 0, 0)
        o, offs = ac12.acquire(0)
        alloc.offs = offs
        o.body.traces[1, :8] = ac76.encode_priority(priority)[:, None]
        o.body.traces[0, offs[0]] = 1                     # register bit -> relinquished
        target = prog.program(priority)
        o.body.traces[0, 0, 0:4] = 1 - int(target[0])     # corrupt program bit 0
        o.body.traces[0, 1, 0:4] = 1 - int(target[1])     # and bit 1 (cross the corruption signal)
        e = ac9.event()
        ac79.reg_maintained(o, e)
        self.assertEqual(int(o.body.traces[0, offs[0]].sum() >= 4), 1,
                         'register bit must be excluded from re-instantiation')
        self.assertEqual(int(o.body.traces[0, 0].sum() >= 4), int(target[0]),
                         'program bit 0 must be re-instantiated to the correct value')

    def test_pristine_reproduces_ac76_regen(self):
        # the pristine arm must be byte-identical to AC76's frozen regen arm (state_hash included)
        a = ac79.run(0, 0, 'pristine', corrupt=True)
        b = ac76.run(0, 0, 'regen', corrupt=True)
        self.assertEqual(a['state_hash'], b['state_hash'],
                         'pristine arm must reproduce AC76 regen exactly')
        for k in ('completed', 'first_dead', 'program_correct', 'flipped_still_wrong',
                  'demand', 'register'):
            self.assertEqual(a[k], b[k], f'field {k} must match AC76 regen')

    def test_gate_keys(self):
        g = ac79.gates([])
        self.assertEqual(set(g.keys()), {
            'G1_maintained_recovers', 'G2_unmaintained_fails', 'G3_maintenance_load_bearing',
            'G4_no_repair_dies', 'G5_control_clean', 'G6_completeness_determinism'})


class TestRecordedOutcomes(unittest.TestCase):
    @unittest.skipUnless(Path('ac79_results_v1/results.json').exists(), 'finals not yet run')
    def test_recorded_freeze(self):
        with open('ac79_results_v1/results.json') as f:
            results = json.load(f)
        rows = results['rows']
        g = ac79.gates(rows)
        self.assertTrue(all(v for v in g.values() if v is not None), f'gates not all pass: {g}')
        maintained = [r for r in rows if r['arm'] == 'maintained' and r['corrupt']]
        unmaintained = [r for r in rows if r['arm'] == 'unmaintained' and r['corrupt']]
        surv_m = [r for r in maintained if r['completed']]
        alive_u = [r for r in unmaintained if r['alive_at_corruption']]
        self.assertTrue(all(r['flipped_still_wrong'] == 0 and r['description_same'] == 1
                            for r in surv_m),
                        'maintained survivors must recover the program and keep the description intact')
        self.assertTrue(all(r['flipped_still_wrong'] > 0 and r['description_valid'] == 0
                            for r in alive_u),
                        'unmaintained must fail to recover with an invalid description')


if __name__ == '__main__':
    unittest.main()
