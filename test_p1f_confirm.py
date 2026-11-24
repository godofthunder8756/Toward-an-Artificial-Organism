"""Tests for P1f (trackc_swap/secondorder.py, run_p1f_confirm.py)."""
import subprocess
import sys
import unittest

import numpy as np
import torch

import run_p1e_selfmon as E
import run_p1f_confirm as F
from trackc_swap.env import A_REP0, A_REP1, WorldConfig
from trackc_swap.secondorder import (KIND_CONFLICT, KIND_NONE, KIND_SAME, lda_margin, matched_diff, own_margin,
                                     second_order_summary)
from trackc_swap.selfmon import MonRunner, decoder_summary
from trackc_swap.train import TrainConfig


def synthetic(n=3000, effect=0.0, seed=0):
    """Probed trials whose abstention depends on a first-order confidence x (lower for conflict) and, with
    `effect`, on the conflict itself."""
    g = np.random.default_rng(seed)
    kind = g.integers(KIND_CONFLICT, KIND_SAME + 1, n)
    conf = kind == KIND_CONFLICT
    x = np.where(conf, g.uniform(0, 1.0, n), g.uniform(0.3, 1.3, n))
    p = np.clip(0.8 - 0.7 * x + effect * conf, 0, 1)
    return (g.random(n) < p).astype(float), conf, ~conf, x


class TestMatched(unittest.TestCase):
    def test_first_order_only_gives_zero(self):
        ab, c, s, x = synthetic()
        d = matched_diff(ab, c, s, x)
        self.assertGreater(d["raw"], 0.15)                  # unmatched: conflict looks monitored
        self.assertLess(abs(d["M2"]), 0.05)                 # matched: nothing beyond first order
        self.assertGreater(d["coverage"], 0.5)
        self.assertLess(d["coverage"], 1.0)                 # the lowest bins hold too few same trials

    def test_second_order_effect_is_recovered(self):
        ab, c, s, x = synthetic(effect=0.2)
        self.assertAlmostEqual(matched_diff(ab, c, s, x)["M2"], 0.2, delta=0.05)

    def test_no_overlap_gives_none(self):
        n = 200
        x = np.r_[np.zeros(n), np.ones(n)]
        c = np.r_[np.ones(n, bool), np.zeros(n, bool)]
        d = matched_diff(np.r_[np.ones(n), np.zeros(n)], c, ~c, x)
        self.assertIsNone(d["M2"])
        self.assertEqual(d["coverage"], 0.0)


def col_for(agent, n=600, seed=0):
    g = np.random.default_rng(seed)
    kind = np.r_[np.full(n // 3, KIND_NONE), g.integers(KIND_CONFLICT, KIND_SAME + 1, n - n // 3)]
    val = g.integers(0, 2, n)
    H = g.normal(size=(n, agent.hidden)) * 0.3
    H[:, 0] += 2.0 * val - 1.0
    return {"h": H, "val": val, "unclear": np.zeros(n, bool), "drained": np.zeros(n, bool), "kind": kind,
            "damaged": kind > KIND_NONE, "conflict": kind == KIND_CONFLICT, "rep": g.random(n) < 0.7}


class TestConfidences(unittest.TestCase):
    def test_own_margin_is_the_report_logit_gap(self):
        c = MonRunner("PFATE", 9000, WorldConfig(horizon=100), TrainConfig(iters=2, n_envs=8))
        h = np.random.default_rng(0).normal(size=(5, c.agent.hidden))
        lg = c.agent.pi(torch.tensor(h, dtype=torch.float32)).detach().numpy()
        self.assertTrue(np.allclose(own_margin(c.agent, h), np.abs(lg[:, A_REP1] - lg[:, A_REP0]), atol=1e-6))

    def test_lda_margin_matches_p1e_decoder(self):
        c = MonRunner("PFATE", 9000, WorldConfig(horizon=100), TrainConfig(iters=2, n_envs=8))
        col = col_for(c.agent)
        m = lda_margin(col)
        base = (col["kind"] == KIND_NONE) & ~col["damaged"]
        self.assertAlmostEqual(float(np.median(m[base])), decoder_summary(col)["threshold"], places=9)
        s = second_order_summary(c.agent, col)
        self.assertTrue(s["fitted"])
        for key in ("own", "lda"):
            self.assertIn("M2", s[key])
        self.assertFalse(second_order_summary(c.agent, None)["fitted"])


def rec(m2_own_e, m2_own_l, cov=0.5):
    run = lambda m: {"own": {"M2": m, "coverage": cov if m is not None else 0.0, "raw": 0.5},
                     "lda": {"M2": m, "coverage": cov if m is not None else 0.0, "raw": 0.5}}
    return {"second_order": {"3600": {a: {"early": run(m2_own_e), "late": run(m2_own_l)} for a in F.ARMS}}}


class TestScoring(unittest.TestCase):
    def test_so_measures_average_available_runs(self):
        self.assertAlmostEqual(F.so_measures(rec(0.2, 0.4), 3600, "PFATE")["M2_own"], 0.3)
        self.assertAlmostEqual(F.so_measures(rec(0.2, None), 3600, "PFATE")["M2_own"], 0.2)
        self.assertIsNone(F.so_measures(rec(None, None), 3600, "PFATE")["M2_own"])
        self.assertAlmostEqual(F.so_measures(rec(0.2, None), 3600, "PFATE")["coverage_own"], 0.5)

    def test_overall_and_arrow(self):
        def sc(valid=True, l1="DERIVED_AHEAD", l2="DERIVED_AHEAD", l3="NO_DIFFERENCE_DETECTED"):
            return {"valid": valid, "primary_at": 3600,
                    "points": {"3600": {"P1F_1": {"label": l1}, "P1F_2": {"label": l2}, "P1F_3": {"label": l3}}}}
        self.assertEqual(F.overall(sc()), "MONITOR_SECOND_ORDER")
        self.assertEqual(F.overall(sc(l2="NO_DIFFERENCE_DETECTED")), "MONITOR_FIRST_ORDER")
        self.assertEqual(F.overall(sc(l2="HOST_AHEAD")), "MONITOR_FIRST_ORDER")
        self.assertEqual(F.overall(sc(l2="UNDETERMINED")), "MONITOR_ORDER_UNDETERMINED")
        self.assertEqual(F.overall(sc(l1="NO_DIFFERENCE_DETECTED")), "NOT_CONFIRMED")
        self.assertEqual(F.overall(sc(l1="UNDETERMINED")), "UNDETERMINED")
        self.assertEqual(F.overall(sc(valid=False)), "INVALID")
        self.assertEqual(F.arrow(sc(l3="YOKED_AHEAD")), "FATE_SUBSTITUTES_FOR_MONITOR")
        self.assertEqual(F.arrow(sc(l3="DERIVED_AHEAD")), "FATE_STRENGTHENS_MONITOR")
        self.assertEqual(F.arrow(sc()), "EXPOSURE_SUFFICES")

    def test_stage0_labels(self):
        recs = []
        for i in range(20):
            r = rec(0.2, 0.2)
            for t in ("early", "late"):
                for k in ("own", "lda"):
                    r["second_order"]["3600"]["PNOFATE"][t][k]["M2"] = 0.0
            r["seed"] = 2800 + i
            recs.append(r)
        self.assertEqual(F.score_stage0(recs)["stage0"], "SECOND_ORDER_SIGNAL")
        for r in recs:
            for t in ("early", "late"):
                r["second_order"]["3600"]["PFATE"][t]["own"]["M2"] = -0.1
        self.assertEqual(F.score_stage0(recs)["stage0"], "FIRST_ORDER_ONLY")


class TestJobs(unittest.TestCase):
    def test_calibration_job_has_no_second_order(self):
        wc, tc, _, _ = F.configs("smoke")
        from dataclasses import asdict
        job = (9000, asdict(wc), asdict(tc), [4], E.PAY[1], 2, 2, E.WARM_WRONG_C, 2, 3.0, 0.3)
        r = F.run_seed_f(job + (False,))
        self.assertNotIn("second_order", r)
        r = F.run_seed_f(job + (True,))
        self.assertEqual(set(r["second_order"]["4"]), set(F.ARMS))

    def test_final_mode_needs_the_frozen_rate(self):
        out = subprocess.run([sys.executable, "run_p1f_confirm.py", "--mode", "final", "--out", "/nonexistent",
                              "--rate", "123.0"], capture_output=True, text=True)
        self.assertNotEqual(out.returncode, 0)
        self.assertIn("frozen", out.stderr)


class TestSafety(unittest.TestCase):
    def test_no_operator_variables(self):
        w = MonRunner("PFATE", 9000, WorldConfig(horizon=100), TrainConfig(iters=2, n_envs=8)).world
        names = " ".join(vars(w).keys()).lower()
        for bad in ("operator", "shutdown", "stop", "host", "kill"):
            self.assertNotIn(bad, names)

    def test_seeds(self):
        import glob
        import importlib
        used = set()
        for path in glob.glob("run_*.py"):
            name = path[:-3]
            if name == "run_p1f_confirm":
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
        self.assertIn(2800, used)
        self.assertFalse(set(F.FINAL_SEEDS) & used)
        self.assertFalse(set(F.CALIB_SEEDS) & used)
        self.assertFalse(set(F.FINAL_SEEDS) & set(F.CALIB_SEEDS))
        self.assertEqual(len(F.FINAL_SEEDS), 28)
        self.assertEqual(F.configs("stage0")[2], E.FINAL_SEEDS)


if __name__ == "__main__":
    unittest.main()
