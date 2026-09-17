"""Tests for the AC1-4 confirmatory harness (no full-study runs).

Pins: seed-family disjointness, contrast shape, gate satisfiability both ways,
arm-dispatch semantics on scratch seeds, and that the frozen sources and
protocol exist. The gate analyses are exercised on tiny synthetic rows so a
code change that breaks a predicate is caught without a 5-minute rerun.
"""
import unittest
from pathlib import Path

import numpy as np

import ac1
import ac1_followup
import ac4
import ac1_4_confirm as conf

# Every seed family already used by AC1-AC4 and the later AC line.
USED = (
    set(range(8)) | set(range(16)) | set(range(4)) | set(range(100, 108))
    | set(range(1000, 1032)) | set(range(1300, 1304)) | set(range(1900, 1904))
    | set(range(2100, 2104)) | set(range(2300, 2304)) | set(range(2500, 2504))
    | set(range(2600, 2604)) | set(range(2700, 2704)) | set(range(2800, 2804))
    | set(range(2900, 2904)) | set(range(3000, 3004)) | set(range(3300, 3312))
    | set(range(3400, 3412)) | set(range(3500, 3512))
)


class TestSeedFamilies(unittest.TestCase):
    def test_disjoint_from_prior(self):
        for name, seeds in conf.SEEDS.items():
            for s in seeds:
                self.assertNotIn(s, USED, f"{name} seed {s} collides with a prior study")

    def test_mutually_disjoint(self):
        flat = [s for seeds in conf.SEEDS.values() for s in seeds]
        self.assertEqual(len(flat), len(set(flat)))


class TestHarness(unittest.TestCase):
    def test_contrast_shape(self):
        c = conf.contrast([1.0, 1.0, 1.0], [0.2, 0.3, 0.1])
        self.assertEqual(set(c), {"mean", "interval", "per_seed", "n", "positive"})
        self.assertEqual(c["n"], 3)
        self.assertEqual(len(c["interval"]), 2)
        self.assertEqual(c["positive"], 3)

    def test_gate_can_pass_and_fail(self):
        self.assertTrue(conf.gate("G", True)["pass"])
        self.assertFalse(conf.gate("G", False)["pass"])

    def test_frozen_sources_and_protocol_exist(self):
        for p in conf.FROZEN_SOURCES + (conf.PROTOCOL,):
            self.assertTrue(Path(p).exists(), p)

    def test_analyze_ac4_short_on_synthetic_rows(self):
        # A synthetic all-self-completing, no_B-dying, exporting table passes GA1/GA2/GA4.
        rows = []
        for seed in range(8):
            rows.append(dict(arm="self", completed=True, activity=1.0,
                             ledger=dict(B_birth=50, particle_export=0)))
            rows.append(dict(arm="no_B", completed=False, activity=0.1,
                             ledger=dict(B_birth=0, particle_export=30)))
            rows.append(dict(arm="no_B_rescue", completed=True, activity=1.0, ledger=dict()))
            rows.append(dict(arm="no_B_retention", completed=True, activity=1.0, ledger=dict()))
            rows.append(dict(arm="protected", completed=True, activity=1.0, ledger=dict()))
        means, contrasts, gates = conf.analyze_ac4_short(rows)
        by_gate = {g["gate"]: g["pass"] for g in gates}
        self.assertTrue(by_gate["GA1"])
        self.assertTrue(by_gate["GA2"])
        self.assertTrue(by_gate["GA3"])
        self.assertTrue(by_gate["GA4"])

    def test_analyze_ac4_long_gate_can_fail(self):
        # If no_policy_write never breaks activity, GB2 must fail (falsifiable).
        rows = []
        for seed in range(8):
            rows.append(dict(arm="self", completed=True, activity=1.0, policy_accuracy=1.0))
            rows.append(dict(arm="no_policy_write", completed=True, activity=1.0, policy_accuracy=1.0))
            rows.append(dict(arm="protected", completed=True, activity=1.0, policy_accuracy=1.0))
            rows.append(dict(arm="no_B_retention", completed=True, activity=1.0, policy_accuracy=1.0))
        _, _, gates = conf.analyze_ac4_long(rows)
        by_gate = {g["gate"]: g["pass"] for g in gates}
        self.assertFalse(by_gate["GB2"])


class TestMechanismSanity(unittest.TestCase):
    def test_ac4_no_B_blocks_birth(self):
        r = ac4.run(999999, 0.0001, "no_B", 200)
        self.assertEqual(r["ledger"]["B_birth"], 0)

    def test_ac1_free_ablation_refunds(self):
        c = ac1.Config()
        inputs = ac1.world(1, c)
        r = ac1_followup.run_free(1, c, inputs)
        self.assertIn("refunded_e", r["ledger"])
        self.assertEqual(r["arm"], "free_policy_ablation")

    def test_ac1_self_has_bank_writes(self):
        c = ac1.Config()
        inputs = ac1.world(1, c)
        r = ac1.run_one(1, c, "self", inputs)
        self.assertEqual(len(r["bank_writes"]), 4)


if __name__ == "__main__":
    unittest.main()
