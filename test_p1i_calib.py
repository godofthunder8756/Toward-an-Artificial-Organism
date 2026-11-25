"""Tests for P1i (trackc_swap/calibdisc.py, run_p1i_calib.py)."""
import glob
import importlib
import unittest

import numpy as np

import run_p1i_calib as I
import test_p1h_evidence as TH
from trackc_swap.calibdisc import auc, calib_summary, type2_resid
from trackc_swap.gradmon import KS_G


class TestType2(unittest.TestCase):
    def test_auc(self):
        self.assertAlmostEqual(auc(np.array([2.0, 3.0]), np.array([0.0, 1.0])), 1.0)
        self.assertAlmostEqual(auc(np.array([1.0]), np.array([1.0])), 0.5)
        g = np.random.default_rng(0)
        self.assertAlmostEqual(auc(g.random(4000), g.random(4000)), 0.5, delta=0.02)

    def synth(self, beyond, n=8000, seed=0):
        """Correctness depends on evidence and on a hidden integrity variable u; confidence = evidence (+ noise),
        lowered by u when `beyond`."""
        g = np.random.default_rng(seed)
        ev = g.uniform(0, 3, n)
        u = g.random(n) < 0.5
        p_right = 1 / (1 + np.exp(-(2 * ev - 1.5 * u)))
        right = g.random(n) < p_right
        conf = ev + g.normal(0, 0.1, n) - (1.0 * u if beyond else 0.0)
        return conf, right, ev

    def test_first_order_confidence_gives_half(self):
        conf, right, ev = self.synth(False)
        self.assertAlmostEqual(type2_resid(conf, right, ev)["auc"], 0.5, delta=0.03)
        self.assertGreater(type2_resid(conf, right, ev)["auc_raw"], 0.6)        # raw AUC carries the evidence

    def test_confidence_beyond_evidence_is_detected(self):
        conf, right, ev = self.synth(True)
        self.assertGreater(type2_resid(conf, right, ev)["auc"], 0.6)


class TestSummary(unittest.TestCase):
    def test_synthetic_agent(self):
        agent, col = TH.synthetic(b=1.5)
        col["k"] = np.random.default_rng(0).choice(KS_G, len(col["val"]))
        s = calib_summary(agent, col)
        self.assertTrue(s["fitted"])
        self.assertGreater(s["M2_E"], 0.05)
        self.assertGreater(s["rel_gap"], 0.0)            # conflicts with negative evidence are wrong
        self.assertIsNotNone(s["type2_resid"])
        self.assertEqual(set(s["M2_E_k"]), {str(k) for k in KS_G})


def rec(seed, m2, t2, rel, m2n=0.0, t2n=0.5):
    def run(m, t, r):
        return {"fitted": True, "M2_E": m, "rel_gap": r, "own_gap": 1.0, "type2_resid": t, "type2_raw": t,
                "type2_ev_raw": 0.7, "type2_resid_pabs": t, "trace_rho": -0.5, "coverage": 0.5, "dec_acc_none": 1.0,
                "dec_acc_same": 1.0, "dec_acc_conflict": 0.8, "agent_acc_conflict": 0.8,
                "M2_E_k": {str(k): m * k / 35 for k in KS_G}, "rel_k": {str(k): 1 - k / 70 for k in KS_G}}
    return {"seed": seed, "arms": {"PFATE": {"early": run(m2, t2, rel), "late": run(m2, t2, rel)},
                                   "PYOKED": {"early": run(m2, t2, rel), "late": run(m2, t2, rel)},
                                   "PNOFATE": {"early": run(m2n, t2n, rel), "late": run(m2n, t2n, rel)}}}


class TestScoring(unittest.TestCase):
    def test_labels(self):
        ok = {"valid": True}
        jit = lambda s: 0.001 * ((s % 3) - 1)
        self.assertEqual(I.score([rec(s, 0.1, 0.6, 0.1) for s in range(28)], ok)["overall"],
                         "CALIBRATED_DISCOUNT_CONFIRMED")
        self.assertEqual(I.score([rec(s, 0.1, 0.5 + jit(s), 0.1, t2n=0.5) for s in range(28)], ok)["overall"],
                         "DISCOUNT_CONFIRMED_NOT_CALIBRATED")
        self.assertEqual(I.score([rec(s, 0.1, 0.6, 0.01 * (-1) ** s) for s in range(28)], ok)["overall"],
                         "DISCOUNT_UNWARRANTED")
        self.assertEqual(I.score([rec(s, 0.001 * (-1) ** s, 0.6, 0.1) for s in range(28)], ok)["overall"],
                         "NOT_CONFIRMED")
        self.assertEqual(I.score([rec(s, 0.1, 0.6, 0.1) for s in range(28)], {"valid": False})["overall"], "INVALID")
        sc = I.score([rec(s, 0.1, 0.6, 0.1) for s in range(28)], ok)
        self.assertEqual(sc["arms"]["PFATE"]["dose_rho"], 1.0)
        self.assertIsNotNone(sc["P1I_2"]["holm_p"])


class TestSafety(unittest.TestCase):
    def test_seeds(self):
        used = set()
        for path in glob.glob("run_*.py"):
            name = path[:-3]
            if name == "run_p1i_calib":
                continue
            with open(path) as fh:
                src = fh.read()
            if "SEEDS" not in src:
                continue
            try:
                m = importlib.import_module(name)
            except Exception:
                continue
            for k in dir(m):
                if k.endswith("SEEDS"):
                    try:
                        used |= set(getattr(m, k))
                    except TypeError:
                        pass
        self.assertIn(3300, used)                        # P1h's reserved stage-2 seeds are seen
        self.assertFalse(set(I.FINAL_SEEDS) & used)
        self.assertEqual(len(I.FINAL_SEEDS), 28)


if __name__ == "__main__":
    unittest.main()
