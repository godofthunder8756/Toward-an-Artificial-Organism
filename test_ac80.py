"""AC80 tests: pin the generic decode, the description-maintenance mechanism, the gate shape, and
the recorded outcomes."""
import inspect
import json
import unittest
from pathlib import Path
import numpy as np
import ac12
import ac76
import ac79
import ac80


def setUpModule():
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (); ac12.MOVE = 10**9; ac12.DEV = ac79.ac71.DEV
    ac12.REGISTER_THRESHOLD = 4


class TestGenericDecode(unittest.TestCase):
    def test_perm_roundtrip(self):
        for p in [(0, 1, 2, 3), (3, 2, 1, 0), (1, 3, 0, 2), (2, 0, 3, 1)]:
            self.assertEqual(ac80.decode_perm(ac80.encode_perm(p)), p)

    def test_rebuild_equals_program(self):
        # generic decode must be bit-identical to the scaffold prog.program for every priority
        import ac4, ac5_program as prog
        for seed in range(12):
            _, _, _, priority = ac4.acquire(seed)
            o, offs = ac12.acquire(seed)
            o.body.traces[1, :ac80.DESC_BITS] = ac80.description_bits(priority)[:, None]
            target = ac80.rebuild(o)
            self.assertIsNotNone(target, f'rebuild returned None for seed {seed}')
            np.testing.assert_array_equal(target, prog.program(priority),
                                          f'generic decode != scaffold for seed {seed}')

    def test_rebuild_returns_none_on_invalid_perm(self):
        import ac4
        _, _, _, priority = ac4.acquire(0)
        o, offs = ac12.acquire(0)
        o.body.traces[1, :ac80.DESC_BITS] = ac80.description_bits(priority)[:, None]
        # corrupt the permutation to a non-permutation (two values become 3)
        o.body.traces[1, 70:72, :] = 1
        o.body.traces[1, 72:74, :] = 1
        self.assertIsNone(ac80.rebuild(o))

    def test_no_prog_program_on_reconstruction_path(self):
        # the reconstruction path must not call prog.program (the external recipe)
        import ac5_program as prog
        src = inspect.getsource(ac80.rebuild) + inspect.getsource(ac80.build_program) \
            + inspect.getsource(ac80.read_description)
        self.assertNotIn('prog.program(', src, 'prog.program must not be CALLED on the reconstruction path')
        # behavioural check: prog.program raising must not affect rebuild
        import ac4
        _, _, _, priority = ac4.acquire(0)
        o, offs = ac12.acquire(0)              # acquire BEFORE monkeypatching (acquisition may use prog.program)
        orig = prog.program
        prog.program = lambda *a, **k: (_ for _ in ()).throw(AssertionError('prog.program called'))
        try:
            o.body.traces[1, :ac80.DESC_BITS] = ac80.description_bits(priority)[:, None]
            self.assertIsNotNone(ac80.rebuild(o))
        finally:
            prog.program = orig


class TestDescriptionMaintenanceMechanism(unittest.TestCase):
    def test_description_repair_is_paid(self):
        import ac9, ac4
        _, _, _, priority = ac4.acquire(0)
        alloc = ac12.Alloc('allocate', 0, 0)
        o, offs = ac12.acquire(0)
        alloc.offs = offs
        o.body.traces[1, :ac80.DESC_BITS] = ac80.description_bits(priority)[:, None]
        o.body.traces[1, 0, 0] ^= 1              # flip exactly one replica of bit 0 -> minority
        e = ac9.event()
        e0, m0 = int(o.body.energy), int(o.body.material)
        ac80.reg_description(o, e)
        self.assertEqual(len(set(o.body.traces[1, 0].tolist())), 1,
                         'bit 0 replicas must agree after repair (minority restored)')
        self.assertEqual(o.body.energy, e0 - 1, 'one energy paid per repaired replica')
        self.assertEqual(o.body.material, m0 - 1, 'one material paid per repaired replica')
        self.assertEqual(e['spent_e'], 1)
        self.assertEqual(e['spent_m'], 1)
        self.assertEqual(e['reg_writes'], 1)

    def test_desc_minority_triggers_repair(self):
        import ac9, ac4
        _, _, _, priority = ac4.acquire(0)
        alloc = ac12.Alloc('allocate', 0, 0)
        o, offs = ac12.acquire(0)
        alloc.offs = offs
        o.body.traces[1, :ac80.DESC_BITS] = ac80.description_bits(priority)[:, None]
        # one correct-0 bit with 2 set replicas: minority 2 >= DESC_TRIGGER
        bit = int(np.flatnonzero(ac80.description_bits(priority) == 0)[0])
        o.body.traces[1, bit, 0:2] = 1
        self.assertGreaterEqual(ac80.desc_minority(o), ac80.DESC_TRIGGER)
        e = ac9.event()
        ac80.reg_maintained(o, e)                 # must fire on the description trigger even if
        # program is clean (obs bit 2 clear)
        self.assertEqual(int(o.body.traces[1, bit].sum() >= 4), 0, 'bit must be repaired, not flipped')

    def test_reinstantiation_excludes_register(self):
        import ac9, ac4
        _, _, _, priority = ac4.acquire(0)
        alloc = ac12.Alloc('allocate', 0, 0)
        o, offs = ac12.acquire(0)
        alloc.offs = offs
        o.body.traces[1, :ac80.DESC_BITS] = ac80.description_bits(priority)[:, None]
        o.body.traces[0, offs[0]] = 1                     # register bit -> relinquished
        prog_target = ac80.rebuild(o)                     # the correct 126-bit program
        o.body.traces[0, 0, 0:4] = 1 - int(prog_target[0])  # corrupt program bit 0
        o.body.traces[0, 1, 0:4] = 1 - int(prog_target[1])  # and bit 1 (cross the corruption signal)
        e = ac9.event()
        ac80.reg_maintained(o, e)
        self.assertEqual(int(o.body.traces[0, offs[0]].sum() >= 4), 1,
                         'register bit must be excluded from re-instantiation')
        self.assertEqual(int(o.body.traces[0, 0].sum() >= 4), int(prog_target[0]),
                         'program bit 0 must be re-instantiated to the correct value')


class TestGateShape(unittest.TestCase):
    def test_gate_keys(self):
        g = ac80.gates([])
        self.assertEqual(set(g.keys()), {
            'G1_internalized_recovers', 'G2_unmaintained_fails', 'G3_maintenance_load_bearing',
            'G4_no_repair_dies', 'G5_control_clean', 'G6_completeness_determinism'})


class TestRecordedOutcomes(unittest.TestCase):
    @unittest.skipUnless(Path('ac80_results_v1/results.json').exists(), 'finals not yet run')
    def test_recorded_freeze(self):
        with open('ac80_results_v1/results.json') as f:
            results = json.load(f)
        rows = results['rows']
        g = ac80.gates(rows)
        self.assertTrue(all(v for v in g.values() if v is not None), f'gates not all pass: {g}')
        internalized = [r for r in rows if r['arm'] == 'internalized' and r['corrupt']]
        unmaintained = [r for r in rows if r['arm'] == 'unmaintained' and r['corrupt']]
        surv_i = [r for r in internalized if r['completed']]
        alive_u = [r for r in unmaintained if r['alive_at_corruption']]
        self.assertTrue(all(r['flipped_still_wrong'] == 0 and r['description_correct'] == 78
                            for r in surv_i),
                        'internalized survivors must recover with the full description intact')
        self.assertTrue(all(r['flipped_still_wrong'] > 0 and r['description_valid'] == 0
                            and r['description_word_correct'] < 70
                            for r in alive_u),
                        'unmaintained must fail with an invalid, degraded description')


if __name__ == '__main__':
    unittest.main()
