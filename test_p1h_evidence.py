"""Tests for P1h (trackc_swap/evidence.py, run_p1h_evidence.py)."""
import glob
import importlib
import subprocess
import sys
import unittest

import numpy as np
import torch

import run_p1h_evidence as H
from trackc_swap.env import A_REP0, A_REP1, A_STAY
from trackc_swap.evidence import evidence_logit, evidence_summary, joint_nn, p_abstain
from trackc_swap.selfmon import KIND_CONFLICT, KIND_NONE, KIND_SAME


class StubAgent:
    """A linear policy head on a synthetic state: REP1 / REP0 logits +-a * d0 (signed evidence), STAY logit
    c + b * d1 (d1 an integrity trace present on conflicts only)."""

    def __init__(self, D, a=3.0, b=0.0, c=0.0):
        self.pi = torch.nn.Linear(D, 8)
        with torch.no_grad():
            self.pi.weight.zero_()
            self.pi.bias.fill_(-20.0)
            self.pi.weight[A_REP1, 0], self.pi.weight[A_REP0, 0] = a, -a
            self.pi.bias[A_REP1] = self.pi.bias[A_REP0] = 0.0
            self.pi.bias[A_STAY] = c
            self.pi.weight[A_STAY, 1] = b


def synthetic(b, n=6000, D=12, seed=0):
    g = np.random.default_rng(seed)
    kind = g.choice([KIND_NONE, KIND_SAME, KIND_CONFLICT], n)
    val = g.integers(0, 2, n)
    s = np.where(kind == KIND_CONFLICT, g.uniform(-0.6, 1.6, n), g.uniform(0.2, 2.0, n))   # evidence strength
    sign = np.where(val == 1, 1.0, -1.0)
    Hm = g.normal(0, 0.3, (n, D))
    Hm[:, 0] = sign * s + g.normal(0, 0.05, n)
    Hm[:, 1] = np.where(kind == KIND_CONFLICT, 1.0, 0.0) + g.normal(0, 0.3, n)                # integrity trace
    Hm[:, 2] = np.tanh(Hm[:, 0]) + g.normal(0, 0.05, n)                                       # non-linear copy
    agent = StubAgent(D, b=b)
    pab = p_abstain(agent, Hm)
    rep = g.random(n) >= pab
    col = {"h": Hm, "val": val, "unclear": np.zeros(n, bool), "drained": np.zeros(n, bool), "kind": kind,
           "damaged": kind != KIND_NONE, "rep": rep}
    return agent, col


class TestControls(unittest.TestCase):
    def test_first_order_only_gives_zero(self):
        agent, col = synthetic(b=0.0)
        s = evidence_summary(agent, col)
        self.assertTrue(s["fitted"])
        self.assertGreater(s["dec_acc_same"], 0.95)
        self.assertLess(abs(s["E"]["M2"]), 0.01)
        self.assertGreater(s["E"]["coverage"], 0.3)

    def test_second_order_signal_is_recovered(self):
        agent, col = synthetic(b=1.5)
        s = evidence_summary(agent, col)
        self.assertGreater(s["E"]["M2"], 0.05)
        self.assertGreater(s["trace"]["auc"], 0.9)

    def test_p_abstain(self):
        agent, col = synthetic(b=0.0, n=200)
        pab = p_abstain(agent, col["h"])
        self.assertTrue(np.all((pab >= 0) & (pab <= 1)))
        weak = np.abs(col["h"][:, 0]) < 0.1
        strong = np.abs(col["h"][:, 0]) > 1.5
        self.assertGreater(pab[weak].mean(), pab[strong].mean())


class TestDecoder(unittest.TestCase):
    def test_every_scored_trial_gets_one_out_of_fold_logit(self):
        _, col = synthetic(b=0.0, n=1000)
        k = col["kind"]
        fit, sc = k != KIND_CONFLICT, k == KIND_CONFLICT
        lg = evidence_logit(col["h"], col["val"], fit, sc, epochs=5)
        self.assertFalse(np.isnan(lg).any())
        lg2 = evidence_logit(col["h"], col["val"], fit, sc, epochs=5)
        self.assertTrue(np.array_equal(lg, lg2))          # deterministic

    def test_joint_match(self):
        g = np.random.default_rng(1)
        x1, x2 = g.random(2000), g.random(2000)
        c = g.random(2000) < 0.5
        out = joint_nn(np.where(c, 1.0, 0.0), c, ~c, [x1, x2])
        self.assertAlmostEqual(out["M2"], 1.0)
        self.assertGreater(out["coverage"], 0.5)


def rec(seed, m2_pf, m2_pn):
    run = lambda m2: {"fitted": True, **{v: {"M2": m2, "coverage": 0.4, "balance": 0.0} for v in H.VARIANTS},
                      "dec_acc_none": 1.0, "dec_acc_same": 1.0, "dec_acc_conflict": 0.8, "ev_conflict": 1.0,
                      "ev_same": 2.0, "pabs_conflict": 0.1, "pabs_same": 0.0, "pabs_none": 0.0,
                      "trace": {"auc": 0.9, "pair_auc": 0.8}}
    return {"seed": seed, "arms": {"PFATE": {"early": run(m2_pf), "late": run(m2_pf)},
                                   "PYOKED": {"early": run(m2_pf), "late": run(m2_pf)},
                                   "PNOFATE": {"early": run(m2_pn), "late": run(m2_pn)}}}


class TestScoring(unittest.TestCase):
    def test_labels(self):
        sc = H.score([rec(s, 0.01, 0.0001) for s in range(28)], {"runs": 1, "mismatches": 0})
        self.assertEqual(sc["overall"], "SECOND_ORDER_SURVIVES")
        sc = H.score([rec(s, 0.01 * (-1) ** s, 0.0) for s in range(28)], {"runs": 1, "mismatches": 0})
        self.assertEqual(sc["overall"], "EXPLAINED_BY_EVIDENCE")
        sc = H.score([rec(s, 0.01, 0.01 + 0.001 * (-1) ** s) for s in range(28)], {"runs": 1, "mismatches": 0})
        self.assertEqual(sc["overall"], "NOT_SPECIFIC")
        sc = H.score([rec(s, 0.01, 0.0001) for s in range(28)], {"runs": 1, "mismatches": 1})
        self.assertEqual(sc["overall"], "INVALID")
        self.assertIsNotNone(sc["P1H_1"]["holm_p"])

    def test_stage2_is_gated(self):
        out = subprocess.run([sys.executable, "run_p1h_evidence.py", "--stage", "2", "--out", "/nonexistent_p1h"],
                             capture_output=True, text=True)
        self.assertNotEqual(out.returncode, 0)


class TestSafety(unittest.TestCase):
    def test_seeds(self):
        used = set()
        for path in glob.glob("run_*.py"):
            name = path[:-3]
            if name == "run_p1h_evidence":
                continue
            with open(path) as fh:
                src = fh.read()
            if "FINAL_SEEDS" not in src and "CALIB_SEEDS" not in src:
                continue
            try:
                m = importlib.import_module(name)
            except Exception:
                continue
            used |= set(getattr(m, "FINAL_SEEDS", [])) | set(getattr(m, "CALIB_SEEDS", []))
        self.assertIn(3200, used)
        self.assertFalse(set(H.FINAL_SEEDS) & used)
        self.assertEqual(H.STAGE1_SEEDS, list(range(3200, 3228)))
        self.assertEqual(len(H.FINAL_SEEDS), 28)


if __name__ == "__main__":
    unittest.main()
