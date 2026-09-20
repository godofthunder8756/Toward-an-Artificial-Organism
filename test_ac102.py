"""AC102 tests: the budgeted-maintain source surgery, the 2x2 interaction, the staged
schedule, and the recorded final outcomes (recorded-outcome regressions pinned after the
freeze). Structural tests first, then the finals regressions.

setUpModule pins the ambient globals the run depends on (AC16's order-dependence lesson):
the runner sets ac12.* / ac95.* at acquisition, but the tests exercise module-level flags.
"""
import unittest
import numpy as np
import ac102
import ac100
import ac101
import ac95
import ac96
import ac99
import ac12
import ac4
import ac9
import ac71
import ac5_program as prog


def setUpModule():
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (1,); ac12.MOVE = 10**9; ac12.DEV = ac71.DEV
    ac12.REGISTER_THRESHOLD = 4


class TestArmConfig(unittest.TestCase):
    def test_arm_config(self):
        self.assertEqual(ac102._arm_config('neither'), (False, ac102.NO_MOVES, None))
        self.assertEqual(ac102._arm_config('move_only'), (False, ac102.SCHEDULE, None))
        self.assertEqual(ac102._arm_config('corrupt_only'), (True, ac102.NO_MOVES, None))
        self.assertEqual(ac102._arm_config('both'), (True, ac102.SCHEDULE, None))
        self.assertEqual(ac102._arm_config('staged'), (True, ac102.SCHEDULE, ac102.REPAIR_BUDGET))
        self.assertEqual(ac102._arm_config('never'), (True, ac102.SCHEDULE, 0))

    def test_budget_constant(self):
        # REPAIR_BUDGET must be < the W=3 _cap (24) so the schedule actually binds, and > 0
        # so `staged` is not the same as `never`.
        self.assertLess(ac102.REPAIR_BUDGET, 24)
        self.assertGreater(ac102.REPAIR_BUDGET, 0)


class TestBudgetedMaintain(unittest.TestCase):
    """The budgeted maintain is ac95.maintain with a reg_from_active budget; at budget=None it
    must reproduce ac95.maintain byte-for-byte (the surgery is the ONLY change)."""

    def _organism(self):
        _, _, _, priority = ac4.acquire(3)
        ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
        ac12.MOVE_KEYS = (1,); ac12.MOVE = 10**9
        import ac71
        ac12.DEV = ac71.DEV
        ac12.REGISTER_THRESHOLD = 4
        o, offs = ac12.acquire(3)
        return o, offs, priority

    def test_surgery_source_assertions(self):
        # the surgery markers are present in ac95 (a frozen-file drift guard)
        import inspect
        src = inspect.getsource(ac95.reg_from_active)
        self.assertIn("n = min(_cap(b), len(sites))", src)
        src_m = inspect.getsource(ac95.maintain)
        self.assertIn("reg_from_active(o, e, reg_offs)", src_m)

    def test_budget_none_is_frozen(self):
        # single-step: budgeted reg_from_active with budget=None writes the same as frozen
        o, offs, priority = self._organism()
        # corrupt the first 8 bits (4 of 7 replicas wrong) directly
        encoded = ac95.description_bits(priority)
        o.body.traces[1, :ac95.DESC_BITS] = encoded[:, None]
        acquired = (o.body.traces[0, :prog.PROGRAM_BITS].sum(axis=-1) > 3).astype(np.uint8)
        for bit in range(ac95.CORRUPT_BITS):
            w = 1 - int(acquired[bit])
            o.body.traces[0, bit, 0:4] = w
            o.body.traces[0, bit, 4:7] = int(acquired[bit])
        e1 = ac9.event(); e2 = ac9.event()
        reg_offs = ac95.resolve_offsets(o)
        # frozen reg_from_active
        b1 = o.body.traces[0].copy()
        ac95.reg_from_active(o, e1, reg_offs)
        got1 = o.body.traces[0].copy()
        o.body.traces[0] = b1
        # budgeted reg_from_active with budget=None (the exec'd copy in ac102's namespace)
        # reach it via a fresh build to avoid module-state coupling
        ns = dict(vars(ac95))
        import inspect
        reg_src = inspect.getsource(ac95.reg_from_active)
        reg_src = reg_src.replace("def reg_from_active(o, e, reg_offs):",
                                  "def reg_from_active(o, e, reg_offs, budget=None):")
        reg_src = reg_src.replace("    n = min(_cap(b), len(sites))",
                                  "    n = min(_cap(b), len(sites))\n    if budget is not None:\n        n = min(n, budget)")
        exec(compile(reg_src, 't_reg', 'exec'), ns)
        ns['reg_from_active'](o, e2, reg_offs, None)
        self.assertTrue(np.array_equal(got1, o.body.traces[0]))
        self.assertEqual(e1['reg_writes'], e2['reg_writes'])

    def test_budget_bounds_writes(self):
        o, offs, priority = self._organism()
        encoded = ac95.description_bits(priority)
        o.body.traces[1, :ac95.DESC_BITS] = encoded[:, None]
        acquired = (o.body.traces[0, :prog.PROGRAM_BITS].sum(axis=-1) > 3).astype(np.uint8)
        for bit in range(ac95.CORRUPT_BITS):
            w = 1 - int(acquired[bit])
            o.body.traces[0, bit, 0:4] = w
            o.body.traces[0, bit, 4:7] = int(acquired[bit])
        e = ac9.event()
        reg_offs = ac95.resolve_offsets(o)
        # use MAINTAIN_BUDGETED's underlying reg_from_active by reconstructing it
        ns = dict(vars(ac95))
        import inspect
        reg_src = inspect.getsource(ac95.reg_from_active)
        reg_src = reg_src.replace("def reg_from_active(o, e, reg_offs):",
                                  "def reg_from_active(o, e, reg_offs, budget=None):")
        reg_src = reg_src.replace("    n = min(_cap(b), len(sites))",
                                  "    n = min(_cap(b), len(sites))\n    if budget is not None:\n        n = min(n, budget)")
        exec(compile(reg_src, 't_reg2', 'exec'), ns)
        ns['reg_from_active'](o, e, reg_offs, ac102.REPAIR_BUDGET)
        self.assertLessEqual(e['reg_writes'], ac102.REPAIR_BUDGET)
        self.assertGreater(e['reg_writes'], 0)


class TestArmIdentity(unittest.TestCase):
    def test_move_only_is_ac100(self):
        for seed in (0, 4450, 4934):
            self.assertTrue(ac102.run(seed, 0, 'move_only')['state_hash'] ==
                            ac100.run(seed, 0, 'gray_ctl', schedule=ac102.SCHEDULE)['state_hash'])

    def test_both_is_ac101(self):
        for seed in (0, 4450, 4934):
            self.assertTrue(ac102.run(seed, 0, 'both')['state_hash'] ==
                            ac101.run(seed, 0, corrupt=True, schedule=ac102.SCHEDULE)['state_hash'])

    def test_staged_nobudget_is_both(self):
        for seed in (0, 4450):
            self.assertTrue(ac102.staged_nobudget_identity(seed, 0))


class TestInteractionEngineering(unittest.TestCase):
    """The engineering seed 1 dies under `both` (8408) but survives the single challenges —
    the death requires BOTH challenges."""

    def test_seed1_death_requires_both(self):
        self.assertTrue(ac102.run(1, 0, 'neither')['completed'])
        self.assertTrue(ac102.run(1, 0, 'move_only')['completed'])
        self.assertTrue(ac102.run(1, 0, 'corrupt_only')['completed'])
        r = ac102.run(1, 0, 'both')
        self.assertFalse(r['completed'])
        self.assertEqual(r['first_dead'], 8408)
        self.assertEqual(r['fw_at_corrupt'], 8)
        self.assertEqual(r['flipped_still_wrong'], 0)
        self.assertEqual(r['streak_final'][1], 4)  # streak stalls at 4, never drops

    def test_seed1_staged_does_not_rescue(self):
        r = ac102.run(1, 0, 'staged')
        self.assertFalse(r['completed'])
        self.assertEqual(r['first_dead'], 8408)   # identical death tick: timing does not rescue


class TestConservation(unittest.TestCase):
    def test_final_inventory_consistent(self):
        # the run's in-step ac4.balance asserts hold (no crash); check a final row is sane
        r = ac102.run(4934, 0, 'both')
        self.assertIn('material', r)
        self.assertIn('state_hash', r)


class TestFrozenRecord(unittest.TestCase):
    """Recorded-outcome regressions: pin the frozen AC102 result from rows.jsonl WITHOUT
    simulating. These catch any future code change that silently alters the freeze (AC17)."""

    @classmethod
    def setUpClass(cls):
        import json
        from pathlib import Path
        cls.rows = [json.loads(l) for l in
                    Path('ac102_results_v1/rows.jsonl').read_text().splitlines()]
        cls.by = {}
        for r in cls.rows:
            cls.by.setdefault((r['seed'], r['history']), {})[r['arm']] = r

    def _both(self, seed):
        return self.by[(seed, 0)]['both']

    def _staged(self, seed):
        return self.by[(seed, 0)]['staged']

    def test_interaction_single_challenges_survive(self):
        for seed in ac102.FINAL_SEEDS:
            for arm in ('neither', 'move_only', 'corrupt_only'):
                self.assertTrue(self.by[(seed, 0)][arm]['completed'],
                                f'seed {seed} {arm} died')

    def test_death_requires_both(self):
        # the two disclosed death-prone seeds die under `both` but survive every single challenge
        for seed in (4934, 5002):
            self.assertFalse(self._both(seed)['completed'])
            self.assertEqual(self._both(seed)['first_dead'], 8408)
            self.assertEqual(self._both(seed)['streak_final']['1'], 5)

    def test_reconstruction_recovers_under_both(self):
        for seed in ac102.FINAL_SEEDS:
            r = self._both(seed)
            self.assertEqual(r['fw_at_corrupt'], 8, seed)
            self.assertEqual(r['flipped_still_wrong'], 0, seed)

    def test_timing_hypothesis_falsified(self):
        # the death seeds die at 8408 under BOTH immediate and staged — staging does NOT rescue
        for seed in (4934, 5002):
            self.assertEqual(self._both(seed)['first_dead'], 8408, seed)
            self.assertEqual(self._staged(seed)['first_dead'], 8408, seed)
            self.assertEqual(self._staged(seed)['streak_final']['1'], 5, seed)

    def test_staged_breaks_recovery_on_some_seeds(self):
        # G4 FAIL: the staged schedule leaves fw nonzero on 4883 and 4928 (cementing stalls it)
        for seed in (4883, 4928):
            r = self._staged(seed)
            self.assertEqual(r['flipped_still_wrong'], 2, seed)
            self.assertFalse(r['completed'], seed)

    def test_never_repair_fails(self):
        for seed in ac102.FINAL_SEEDS:
            r = self.by[(seed, 0)]['never']
            self.assertEqual(r['flipped_still_wrong'], 8, seed)
            self.assertFalse(r['completed'], seed)

    def test_recorded_gates(self):
        import json
        from pathlib import Path
        gates = json.loads(Path('ac102_results_v1/results.json').read_text())['gates']
        self.assertTrue(gates['G1_interaction_death_requires_both'])
        self.assertTrue(gates['G2_reconstruction_recovers_under_both'])
        self.assertTrue(gates['G3_timing_hypothesis_falsified_staged_does_not_rescue'])
        self.assertFalse(gates['G4_staged_recovers_controller_eventually'])  # the recorded failure
        self.assertTrue(gates['G5_never_repair_must_fail'])
        self.assertTrue(gates['G6_state_sufficiency_observer_discard'])
        self.assertTrue(gates['G7_adversarial_stratum'])
        self.assertTrue(gates['G8_completeness_determinism_arm_identity'])

    def test_seed_disjointness(self):
        used_prior = set(range(8)) | set(range(4412, 4440)) | set(range(4440, 4452)) \
            | {4466, 4481, 4504, 4510} | set(range(4600, 4872)) | set(range(5100, 5508))
        self.assertTrue(set(ac102.FINAL_SEEDS).isdisjoint(used_prior))
        self.assertTrue(set(ac102.UNSEEN).isdisjoint(ac102.ADVERSARIAL))


if __name__ == '__main__':
    unittest.main()
