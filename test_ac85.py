"""AC85 tests: pin the description layout, the read-the-convention decode, the description-maintenance
mechanism, the gate shape, and the recorded outcomes."""
import inspect
import json
import unittest
from pathlib import Path
import numpy as np
import ac12
import ac76
import ac79
import ac85
import ac5_program as prog


def setUpModule():
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (); ac12.MOVE = 10**9; ac12.DEV = ac79.ac71.DEV
    ac12.REGISTER_THRESHOLD = 4


def _acquire(seed):
    """Return (organism, reg_offs, encoded, priority) with the 130-bit description installed."""
    _, _, _, priority = ac85.ac4.acquire(seed)
    o, offs = ac12.acquire(seed)
    encoded = ac85.description_bits(priority)
    o.body.traces[1, :ac85.DESC_BITS] = encoded[:, None]
    return o, offs, encoded, priority


class TestDescriptionLayout(unittest.TestCase):
    def test_offsets(self):
        self.assertEqual(ac85.PERM_OFFSET, 70)
        self.assertEqual(ac85.MASK_OFFSET, 78)
        self.assertEqual(ac85.ACTION_OFFSET, 114)
        self.assertEqual(ac85.DESC_BITS, 130)

    def test_mask_action_roundtrip(self):
        for m in (4, 8, 16, 32):
            self.assertEqual(ac85.decode_mask(ac85.encode_mask(m)), m)
        for a in (2, 3, 4, 5):
            self.assertEqual(ac85.decode_action(ac85.encode_action(a)), a)

    def test_description_encodes_convention(self):
        # the stored masks/actions materialize the convention for the priority
        import ac4
        _, _, _, priority = ac4.acquire(0)
        d = ac85.description_bits(priority)
        self.assertEqual(ac85.decode_perm(d[ac85.PERM_OFFSET:ac85.PERM_OFFSET + 8]),
                         tuple(priority))
        self.assertEqual(ac85.read_masks(d), [4 << b for b in priority])
        self.assertEqual(ac85.read_actions(d), [2 + b for b in priority])


class TestGenericDecode(unittest.TestCase):
    def test_rebuild_equals_acquired(self):
        # generic decode must be bit-identical to the ACQUIRED (ac9_priority_v2 reordered) program
        for seed in range(12):
            o, offs, encoded, priority = _acquire(seed)
            acquired = (o.body.traces[0, :prog.PROGRAM_BITS].sum(axis=-1) > 3).astype(np.uint8)
            target = ac85.rebuild(o)
            self.assertIsNotNone(target, f'rebuild returned None for seed {seed}')
            np.testing.assert_array_equal(target, acquired,
                                          f'rebuild != acquired for seed {seed}')

    def test_rebuild_returns_none_on_invalid_perm(self):
        o, offs, encoded, priority = _acquire(0)
        o.body.traces[1, 70:72, :] = 1
        o.body.traces[1, 72:74, :] = 1
        self.assertIsNone(ac85.rebuild(o))

    def test_rebuild_returns_none_on_inconsistent_mask(self):
        # a stored mask inconsistent with the stored permutation -> None (never a silent wrong program)
        o, offs, encoded, priority = _acquire(0)
        # flip mask-0's bit 1 (value 2) in the majority (4 replicas): perm[0] expects mask 4<<perm[0]
        o.body.traces[1, ac85.MASK_OFFSET + 1, 0:4] = 1 - o.body.traces[1, ac85.MASK_OFFSET + 1, 0:4]
        self.assertIsNone(ac85.rebuild(o))

    def test_no_prog_program_on_reconstruction_path(self):
        src = inspect.getsource(ac85.rebuild) + inspect.getsource(ac85.build_program) \
            + inspect.getsource(ac85.read_description)
        self.assertNotIn('prog.program(', src, 'prog.program must not be CALLED on the reconstruction path')
        # the reconstruction path must not CONSTRUCT masks/actions from a bank index; the 4<<b /
        # 2+b expressions may appear only as the consistency CROSS-CHECK that rejects a degraded
        # description (they are the RHS of a comparison, not a construction of the bank rule).
        bank_src = inspect.getsource(ac85.build_program)
        self.assertIn('prog.encode_rule(1, m, a)', bank_src,
                      'the bank rules must be built from the READ mask/action values')
        self.assertNotIn('prog.encode_rule(1, 4 <<', bank_src,
                         'the bank rule must not be built from a derived 4<<b mask')
        self.assertNotIn('prog.encode_rule(1,', bank_src.replace('prog.encode_rule(1, m, a)', ''),
                         'no other bank-rule construction is allowed')
        # behavioural check: prog.program raising must not affect rebuild
        import ac4
        _, _, _, priority = ac4.acquire(0)
        o, offs = ac12.acquire(0)              # acquire BEFORE monkeypatching (acquisition may use prog.program)
        orig = prog.program
        prog.program = lambda *a, **k: (_ for _ in ()).throw(AssertionError('prog.program called'))
        try:
            o.body.traces[1, :ac85.DESC_BITS] = ac85.description_bits(priority)[:, None]
            self.assertIsNotNone(ac85.rebuild(o))
        finally:
            prog.program = orig


class TestDescriptionMaintenanceMechanism(unittest.TestCase):
    def test_description_repair_is_paid(self):
        import ac9, ac4
        o, offs, encoded, priority = _acquire(0)
        o.body.traces[1, 0, 0] ^= 1              # flip exactly one replica of bit 0 -> minority
        e = ac9.event()
        e0, m0 = int(o.body.energy), int(o.body.material)
        ac85.reg_description(o, e)
        self.assertEqual(len(set(o.body.traces[1, 0].tolist())), 1,
                         'bit 0 replicas must agree after repair (minority restored)')
        self.assertEqual(o.body.energy, e0 - 1, 'one energy paid per repaired replica')
        self.assertEqual(o.body.material, m0 - 1, 'one material paid per repaired replica')
        self.assertEqual(e['spent_e'], 1)
        self.assertEqual(e['spent_m'], 1)
        self.assertEqual(e['reg_writes'], 1)

    def test_desc_minority_triggers_repair(self):
        import ac9, ac4
        o, offs, encoded, priority = _acquire(0)
        bit = int(np.flatnonzero(ac85.description_bits(priority) == 0)[0])
        o.body.traces[1, bit, 0:2] = 1
        self.assertGreaterEqual(ac85.desc_minority(o), ac85.DESC_TRIGGER)
        e = ac9.event()
        ac85.reg_maintained(o, e, set(offs))
        self.assertEqual(int(o.body.traces[1, bit].sum() >= 4), 0,
                         'bit must be repaired, not flipped')

    def test_reinstantiation_excludes_register(self):
        import ac9, ac4
        o, offs, encoded, priority = _acquire(0)
        o.body.traces[0, offs[0]] = 1                     # register bit -> relinquished
        prog_target = ac85.rebuild(o)                     # the correct 126-bit program
        o.body.traces[0, 0, 0:4] = 1 - int(prog_target[0])  # corrupt program bit 0
        o.body.traces[0, 1, 0:4] = 1 - int(prog_target[1])  # and bit 1 (cross the corruption signal)
        e = ac9.event()
        ac85.reg_maintained(o, e, set(offs))
        self.assertEqual(int(o.body.traces[0, offs[0]].sum() >= 4), 1,
                         'register bit must be excluded from re-instantiation')
        self.assertEqual(int(o.body.traces[0, 0].sum() >= 4), int(prog_target[0]),
                         'program bit 0 must be re-instantiated to the correct value')


class TestGateShape(unittest.TestCase):
    def test_gate_keys(self):
        g = ac85.gates([])
        self.assertEqual(set(g.keys()), {
            'G1_internalized_recovers', 'G2_unmaintained_fails', 'G3_maintenance_load_bearing',
            'G4_no_repair_dies', 'G5_control_clean', 'G6_completeness_determinism'})


class TestRecordedOutcomes(unittest.TestCase):
    @unittest.skipUnless(Path('ac85_results_v1/results.json').exists(), 'finals not yet run')
    def test_recorded_freeze(self):
        with open('ac85_results_v1/results.json') as f:
            results = json.load(f)
        rows = results['rows']
        g = ac85.gates(rows)
        self.assertTrue(all(v for v in g.values() if v is not None), f'gates not all pass: {g}')
        internalized = [r for r in rows if r['arm'] == 'internalized' and r['corrupt']]
        unmaintained = [r for r in rows if r['arm'] == 'unmaintained' and r['corrupt']]
        surv_i = [r for r in internalized if r['completed']]
        alive_u = [r for r in unmaintained if r['alive_at_corruption']]
        self.assertTrue(all(r['flipped_still_wrong'] == 0 and r['description_correct'] == 130
                            for r in surv_i),
                        'internalized survivors must recover with the full description intact')
        self.assertTrue(all(r['flipped_still_wrong'] > 0 and r['description_valid'] == 0
                            and r['description_word_correct'] < 70
                            for r in alive_u),
                        'unmaintained must fail with an invalid, degraded description')


if __name__ == '__main__':
    unittest.main()
