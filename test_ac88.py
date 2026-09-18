"""AC88 tests: pin write_ctrl atomicity for the MODE field (all-or-nothing), the distinct-resource
model, and the machine being well-defined on any controller word. The atomicity tests FAIL on the
frozen ac87.write_ctrl (which writes a partial MODE when energy/material cannot fund the full
transition)."""
import unittest
import numpy as np
import ac12
import ac87
import ac88
import ac5_program as prog


def setUpModule():
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (1,); ac12.MOVE = 10**9; ac12.DEV = ac88.ac71.DEV
    ac12.REGISTER_THRESHOLD = 4


def _acquire(seed=0):
    """Organism with the recipe installed in slot 0 and abundant energy/material."""
    _, _, _, priority = ac88.ac4.acquire(seed)
    o, offs = ac12.acquire(seed)
    encoded = ac88.description_bits(priority)
    o.body.traces[1, :ac88.DESC_BITS] = encoded[:, None]
    o.body.energy = 5000
    o.body.material = 5000
    return o, encoded, priority


def _ctrl_equals(o, word):
    return bool(np.array_equal(o.body.traces[1, ac88.CTRL_OFFS],
                               np.repeat(word[:, None], 7, axis=1)))


def _mode_transition_size(o, target):
    """Number of replicas a write toward `target` must change in the MODE field (bits 0-3)."""
    return int((o.body.traces[1, ac88.CTRL_OFFS[:4]] != target[:4, None]).sum())


class TestWriteCtrlAtomicity(unittest.TestCase):
    def test_energy_too_small_refuses_atomic(self):
        o, encoded, priority = _acquire()
        b = o.body
        target = ac88.encode_ctrl(1, ac88.PHASE_COPY, 9999)
        n_mode = _mode_transition_size(o, target)
        self.assertGreater(n_mode, 0)
        b.energy = n_mode - 1           # cannot fund the whole MODE transition
        b.material = 10**6
        before = o.body.traces[1, ac88.CTRL_OFFS].copy()
        e0, m0 = int(b.energy), int(b.material)
        e = ac88.ac9.event()
        n = ac88.write_ctrl(o, e, target)
        self.assertEqual(n, 0, 'must refuse, not write a partial MODE')
        self.assertEqual(int(b.energy), e0, 'energy must be unchanged on refusal')
        self.assertEqual(int(b.material), m0, 'material must be unchanged on refusal')
        self.assertTrue(np.array_equal(o.body.traces[1, ac88.CTRL_OFFS], before),
                        'no replica may change on refusal')
        self.assertEqual(e.get('ctrl_writes', 0), 0)

    def test_material_too_small_refuses_atomic(self):
        o, encoded, priority = _acquire()
        b = o.body
        target = ac88.encode_ctrl(1, ac88.PHASE_COPY, 9999)
        n_mode = _mode_transition_size(o, target)
        self.assertGreater(n_mode, 0)
        b.energy = 10**6
        b.material = n_mode - 1         # cannot fund the whole MODE transition
        before = o.body.traces[1, ac88.CTRL_OFFS].copy()
        e0, m0 = int(b.energy), int(b.material)
        e = ac88.ac9.event()
        n = ac88.write_ctrl(o, e, target)
        self.assertEqual(n, 0)
        self.assertEqual(int(b.energy), e0)
        self.assertEqual(int(b.material), m0)
        self.assertTrue(np.array_equal(o.body.traces[1, ac88.CTRL_OFFS], before))
        self.assertEqual(e.get('ctrl_writes', 0), 0)

    def test_full_funding_writes_whole_word(self):
        o, encoded, priority = _acquire()
        target = ac88.encode_ctrl(1, ac88.PHASE_COPY, 9999)
        e = ac88.ac9.event()
        n = ac88.write_ctrl(o, e, target)
        self.assertGreater(n, 0)
        self.assertTrue(_ctrl_equals(o, target), 'a fully-funded write must complete the word')
        self.assertEqual(n, e['ctrl_writes'])

    def test_distinct_resource_not_w_gated(self):
        # The coordinator's own register write is a distinct resource from the W-catalyzed CONTENT
        # repair (ac4.react actions 2-5): with W = 0 but sufficient energy/material the MODE write
        # PROCEEDS. This pins the frozen AC87 declaration ("written atomically, bounded by
        # 18x7=126 replicas"), not a new claim.
        o, encoded, priority = _acquire()
        b = o.body
        b.life[:4] = 0                 # no W catalysts
        target = ac88.encode_ctrl(1, ac88.PHASE_COPY, 9999)
        e = ac88.ac9.event()
        n = ac88.write_ctrl(o, e, target)
        self.assertGreater(n, 0, 'the controller register write is not gated by 8*W')
        self.assertTrue(_ctrl_equals(o, target))

    def test_old_code_writes_partial_mode(self):
        # Pin that the frozen ac87.write_ctrl HAS the defect this card fixes: when energy cannot
        # fund even the MODE transition it writes a partial MODE, so the atomicity tests above are
        # discriminative (they would fail on the old code).
        o, encoded, priority = _acquire()
        b = o.body
        target = ac87.encode_ctrl(1, ac87.PHASE_COPY, 9999)
        n_mode = int((b.traces[1, ac87.CTRL_OFFS[:4]] != target[:4, None]).sum())
        b.energy = n_mode - 1
        b.material = 10**6
        e = ac87.ac9.event()
        n = ac87.write_ctrl(o, e, target)
        self.assertGreater(n, 0, 'old code writes a partial word')
        self.assertLess(n, n_mode, 'old code writes fewer replicas than the MODE transition needs')


class TestMachineWellDefinedOnAnyWord(unittest.TestCase):
    def test_advance_does_not_crash_on_spurious_states(self):
        for active in (0, 1):
            for phase in range(8):
                o, encoded, priority = _acquire()
                succ = ac88.Succession('real', encoded)
                e = ac88.ac9.event()
                o.body.traces[1, ac88.CTRL_OFFS] = ac88.encode_ctrl(active, phase, 0)[:, None]
                ac88.advance(o, e, succ, 5000, True)   # must not raise
                self.assertTrue(np.array_equal(ac88.read_slot(o, 0), encoded))

    def test_spurious_activation_treated_as_start(self):
        o, encoded, priority = _acquire()
        succ = ac88.Succession('real', encoded)
        e = ac88.ac9.event()
        o.body.traces[1, ac88.CTRL_OFFS] = ac88.encode_ctrl(1, ac88.PHASE_IDLE, 0)[:, None]
        ac88.advance(o, e, succ, 5000, True)
        self.assertIsNotNone(succ._entry, 'spurious activation must be treated as a start')


class TestGateShape(unittest.TestCase):
    def test_gate_keys_match_ac87(self):
        self.assertEqual(set(ac88.gates([]).keys()), set(ac87.gates([]).keys()))


class TestRecordedFreeze(unittest.TestCase):
    @unittest.skipUnless(__import__('pathlib').Path('ac88_results_v1/results.json').exists(),
                         'finals not yet run')
    def test_recorded_freeze(self):
        import json
        with open('ac88_results_v1/results.json') as f:
            results = json.load(f)
        rows = results['rows']
        g = ac88.gates(rows)
        self.assertTrue(all(v for v in g.values() if v is not None), f'gates not all pass: {g}')
        if __import__('pathlib').Path('ac87_results_v1/results.json').exists():
            with open('ac87_results_v1/results.json') as f:
                frozen = json.load(f)['rows']
            fmap = {(r['seed'], r['history'], r['arm'], r['damage'], r['corrupt'],
                     r['transition']): r for r in frozen}
            diffs = []
            for r in rows:
                k = (r['seed'], r['history'], r['arm'], r['damage'], r['corrupt'],
                     r['transition'])
                if k in fmap and r['state_hash'] != fmap[k]['state_hash']:
                    diffs.append(k)
            self.assertEqual(diffs, [], 'corrected runner must reproduce frozen AC87 state hashes')


if __name__ == '__main__':
    unittest.main()
