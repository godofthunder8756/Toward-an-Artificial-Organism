"""Tests for P1g (trackc_swap/gradmon.py, run_p1g_graded.py)."""
import subprocess
import sys
import unittest

import numpy as np

import run_p1g_graded as G
from run_trackc_paid import WEAR
from trackc_swap.env import WorldConfig
from trackc_swap.gradmon import KS_G, GradRunner, graded_summary, matched_nn
from trackc_swap.selfmon import SPLIT_K
from trackc_swap.train import TrainConfig


def synthetic(n=4000, effect=0.0, seed=0):
    """Abstention depends on a first-order confidence x (lower for conflict) and, with `effect`, on the
    conflict itself."""
    g = np.random.default_rng(seed)
    conf = g.random(n) < 0.5
    x = np.where(conf, g.uniform(0, 1.0, n), g.uniform(0.3, 1.3, n))
    p = np.clip(0.8 - 0.7 * x + effect * conf, 0, 1)
    return (g.random(n) < p).astype(float), conf, ~conf, x


class TestMatchedNN(unittest.TestCase):
    def test_first_order_only_gives_zero(self):
        ab, c, s, x = synthetic()
        d = matched_nn(ab, c, s, x)
        self.assertLess(abs(d["M2"]), 0.04)
        self.assertLess(abs(d["balance"]), 0.01)
        self.assertGreater(d["coverage"], 0.5)
        self.assertLess(d["coverage"], 0.85)        # conflict trials below x = 0.3 have no same trial near

    def test_second_order_effect_is_recovered(self):
        ab, c, s, x = synthetic(effect=0.2)
        self.assertAlmostEqual(matched_nn(ab, c, s, x)["M2"], 0.2, delta=0.05)

    def test_caliper_excludes_far_pairs(self):
        n = 200
        x = np.r_[np.zeros(n), np.ones(n)]
        c = np.r_[np.ones(n, bool), np.zeros(n, bool)]
        d = matched_nn(np.r_[np.ones(n), np.zeros(n)], c, ~c, x)
        self.assertIsNone(d["M2"])
        self.assertEqual(d["coverage"], 0.0)


def runner(arm="PYOKED", base=0.05):
    return GradRunner(arm, 9000, WorldConfig(horizon=100, wear=WEAR), TrainConfig(iters=2, n_envs=64, eval_episodes=1),
                      base=base)


def spy(r):
    ks = []
    orig = r.world.mark_k
    r.world.mark_k = lambda ev, k: (ks.extend(k[ev].tolist()), orig(ev, k))
    return ks


class TestDamage(unittest.TestCase):
    def test_natural_events_are_graded(self):
        r = runner()
        ks = spy(r)
        zeros = np.zeros((r.tc.rollout, r.tc.n_envs), dtype=np.float32)
        for _ in range(4):
            r.rollout(zeros, learn=False)
            r.end_episode_if_due()
        self.assertGreater(len(ks), 100)                 # the base damages without any body gain
        self.assertEqual(set(ks), set(KS_G))

    def test_probes_and_base_switch(self):
        r = runner()
        ks = spy(r)
        r.evaluate_g("zero", split_p=0.0, base_on=False)
        self.assertEqual(len(ks), 0)                     # base off: no event
        r.evaluate_g("zero", split_p=2 / 3, split_at=8, base_on=False)
        self.assertEqual(set(ks), {SPLIT_K})             # split probe A: P1e's half overwrite only
        ks.clear()
        _, _, lg, col = r.evaluate_g("zero", split_p=2 / 3, split_at=1, collect=True, probe_ks=KS_G, base_on=False)
        self.assertEqual(set(ks), set(KS_G))
        self.assertEqual(set(np.unique(col["k"])) - {0}, set(KS_G))
        self.assertTrue(np.array_equal(np.sort(lg[:, 12]), np.sort(col["k"].astype(float))))
        self.assertTrue(r.base_on and r.world.probe_ks == (SPLIT_K,))     # restored
        s = graded_summary(r.agent, col)
        self.assertEqual(set(s["per_k"]), {str(k) for k in KS_G})
        self.assertIn("nn", s["own"])

    def test_nofate_has_no_base(self):
        self.assertEqual(runner("PNOFATE", 0.3).base, 0.0)


def sc(valid=True, l1="DERIVED_AHEAD", l2="PRESENT", l3="NO_DIFFERENCE_DETECTED"):
    return {"valid": valid, "primary_at": 3600,
            "points": {"3600": {"P1G_1": {"label": l1}, "P1G_2": {"label": l2}, "P1G_3": {"label": l3}}}}


class TestScoring(unittest.TestCase):
    def test_overall_and_arrow(self):
        self.assertEqual(G.overall(sc()), "MONITOR_SECOND_ORDER")
        self.assertEqual(G.overall(sc(l2="NOT_DETECTED")), "MONITOR_FIRST_ORDER")
        self.assertEqual(G.overall(sc(l2="REVERSED")), "MONITOR_FIRST_ORDER")
        self.assertEqual(G.overall(sc(l2="UNDETERMINED")), "MONITOR_ORDER_UNDETERMINED")
        self.assertEqual(G.overall(sc(l1="NO_DIFFERENCE_DETECTED")), "NOT_CONFIRMED")
        self.assertEqual(G.overall(sc(l1="UNDETERMINED")), "UNDETERMINED")
        self.assertEqual(G.overall(sc(valid=False)), "INVALID")
        self.assertEqual(G.arrow(sc(l3="YOKED_AHEAD")), "FATE_SUBSTITUTES_FOR_MONITOR")
        self.assertEqual(G.arrow(sc(l3="DERIVED_AHEAD")), "FATE_STRENGTHENS_MONITOR")
        self.assertEqual(G.arrow(sc()), "EXPOSURE_SUFFICES")

    def test_g_measures_average_available_runs(self):
        run = lambda m, cov: {"own": {"nn": {"M2": m, "coverage": cov, "balance": 0.0}, "bins": {"M2": m},
                                      "median_conflict": 1.0, "median_same": 2.0},
                              "lda": None, "per_k": {str(k): {"abstain_conflict": 0.5, "abstain_same": 0.25}
                                                     for k in KS_G}}
        pt = {"graded_early": {"PFATE": run(0.2, 0.4)}, "graded_late": {"PFATE": run(None, 0.2)}}
        m = G.g_measures(pt, "PFATE")
        self.assertAlmostEqual(m["M2_nn_own"], 0.2)
        self.assertAlmostEqual(m["coverage_nn_own"], 0.3)
        self.assertIsNone(m["M2_nn_lda"])
        self.assertAlmostEqual(m["M_k9"], 0.25)

    def test_final_mode_needs_the_frozen_base(self):
        out = subprocess.run([sys.executable, "run_p1g_graded.py", "--mode", "final", "--out", "/nonexistent",
                              "--base", "0.5"], capture_output=True, text=True)
        self.assertNotEqual(out.returncode, 0)
        self.assertIn("frozen", out.stderr)


class TestSafety(unittest.TestCase):
    def test_no_operator_variables(self):
        w = runner("PFATE").world
        names = " ".join(vars(w).keys()).lower()
        for bad in ("operator", "shutdown", "stop", "host", "kill"):
            self.assertNotIn(bad, names)

    def test_seeds(self):
        import glob
        import importlib
        used = set()
        for path in glob.glob("run_*.py"):
            name = path[:-3]
            if name == "run_p1g_graded":
                continue
            with open(path) as fh:
                src = fh.read()
            if "FINAL_SEEDS" not in src and "CALIB_SEEDS" not in src:
                continue
            try:
                m = importlib.import_module(name)
            except Exception:            # an old runner with unavailable dependencies: skip
                continue
            used |= set(getattr(m, "FINAL_SEEDS", [])) | set(getattr(m, "CALIB_SEEDS", []))
        self.assertIn(3000, used)        # P1f's seeds are seen
        self.assertFalse(set(G.FINAL_SEEDS) & used)
        self.assertFalse(set(G.CALIB_SEEDS) & used)
        self.assertFalse(set(G.FINAL_SEEDS) & set(G.CALIB_SEEDS))
        self.assertEqual(len(G.FINAL_SEEDS), 28)


if __name__ == "__main__":
    unittest.main()
