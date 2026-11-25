"""Tests for P1j (trackc_swap/steerint.py, run_p1j_steer.py)."""
import dataclasses
import unittest

import numpy as np
import torch

import run_p1g_graded as G
import run_p1j_steer as J
from run_trackc_paid import PAY, WEAR
from trackc_swap.env import A_REP0, A_REP1, N_ACT, WorldConfig
from trackc_swap.gradmon import EVAL_TAG_G, GradRunner
from trackc_swap.selfmon import EARLY, KIND_CONFLICT, KIND_NONE, KIND_SAME, SPLIT_P
from trackc_swap.steerint import (C_D, C_NONE, C_R, STEER_TAG, SteerRunner, directions, steer_summary)
from trackc_swap.train import TrainConfig


def _small():
    tc = dataclasses.replace(TrainConfig(), eval_episodes=1)
    return WorldConfig(wear=WEAR), tc


def _run(cls, setup=None):
    wc, tc = _small()
    torch.manual_seed(0)
    c = cls("PFATE", 11, wc, tc, PAY[1], tag_offset=STEER_TAG, base=G.BASE_F)
    c.agent.eval()
    if setup:
        setup(c)
    _, _, _, col = c.evaluate_g("zero", drain_p=0.0, split_p=SPLIT_P, split_at=EARLY, collect=True,
                                probe_ks=c.ks, base_on=False)
    return col


class StubAgent:
    """pi(h): logits with REP1 - REP0 = h[:, 0] and an abstain logit 0."""

    def pi(self, h):
        n = h.shape[0]
        out = torch.full((n, N_ACT), -50.0)
        out[:, A_REP1] = 0.5 * h[:, 0]
        out[:, A_REP0] = -0.5 * h[:, 0]
        out[:, [i for i in range(N_ACT) if i not in (A_REP0, A_REP1)][0]] = 0.0
        return out


class TestSteer(unittest.TestCase):
    def test_reproduces_gradrunner(self):
        a = _run(GradRunner)
        b = _run(SteerRunner)
        for k in a:
            self.assertTrue(np.array_equal(a[k], b[k]), k)

    def test_zero_push_changes_nothing(self):
        a = _run(SteerRunner)

        def setup(c):
            c.mode, c.dirs = "push", {"d": np.zeros(c.agent.hidden), "r": np.zeros(c.agent.hidden)}
            c.gen_steer = np.random.default_rng(1)
        b = _run(SteerRunner, setup)
        for k in a:
            if k != "cond":
                self.assertTrue(np.array_equal(a[k], b[k]), k)
        self.assertTrue(set(np.unique(b["cond"])) <= {-1, C_NONE, C_D, C_R})
        self.assertTrue((b["cond"] >= 0).any())

    def test_directions_synthetic(self):
        rng = np.random.default_rng(0)
        n, D = 4000, 12
        val = rng.integers(0, 2, n)
        kind = rng.choice([KIND_NONE, KIND_SAME, KIND_CONFLICT], n)
        unclear = rng.random(n) < 0.3
        dam = kind != KIND_NONE
        e = np.eye(D)
        H = 0.3 * rng.standard_normal((n, D)) + np.outer(2 * val - 1, e[0])
        H -= 0.4 * np.outer((kind == KIND_CONFLICT) * (2 * val - 1), e[0])   # content weakening (signed)
        H += 0.7 * np.outer(kind == KIND_CONFLICT, e[3])                     # content-free conflict shift
        H += 0.5 * np.outer(unclear, e[5])                                   # ambiguity shift
        rec = {"h": H, "val": val, "kind": kind, "damaged": dam, "unclear": unclear, "drained": np.zeros(n, bool)}
        d = directions(rec, 0)
        self.assertTrue(d["ok"])
        dv = d["d"] / np.linalg.norm(d["d"])
        self.assertGreater(abs(dv[3]), 0.97)
        self.assertAlmostEqual(np.linalg.norm(d["r"]), np.linalg.norm(d["d"]), places=6)
        self.assertLess(abs(d["r"] @ d["d"]), 1e-8)

    def _col(self, push):
        rng = np.random.default_rng(1)
        n = 6000
        val = rng.integers(0, 2, n)
        kind = rng.choice([KIND_SAME, KIND_CONFLICT, KIND_NONE], n)
        cond = rng.integers(0, 3, n)
        z = (2 * val - 1) * (3.0 + rng.standard_normal(n))
        z = push(z, val, kind, cond)
        H = np.zeros((n, 4))
        H[:, 0] = z
        return {"h": H, "val": val, "kind": kind, "damaged": kind != KIND_NONE, "unclear": np.zeros(n, bool),
                "drained": np.zeros(n, bool), "cond": cond}

    def test_constant_shift_is_not_a_discount(self):
        col = self._col(lambda z, v, k, c: z + np.where((k == KIND_SAME) & (c == C_D), 1.5, 0.0))
        s = steer_summary(StubAgent(), col)
        self.assertLess(abs(s["induce"]), 0.15)

    def test_gain_reduction_is_a_discount(self):
        col = self._col(lambda z, v, k, c: z * np.where((k == KIND_SAME) & (c == C_D), 0.6, 1.0))
        s = steer_summary(StubAgent(), col)
        self.assertGreater(s["induce"], 1.0)
        self.assertGreater(s["induce_abs"], 0.0)

    def test_labels(self):
        base = {"valid": True, "content": {"confounded_induce": False, "confounded_rescue": False}}
        mk = lambda a, b, c: dict(base, P1J_1={"label": a}, P1J_2={"label": b}, P1J_3={"label": c})
        self.assertEqual(J.overall(mk("PRESENT", "PRESENT", "DERIVED_AHEAD")), "CAUSAL_INTEGRITY_SIGNAL")
        self.assertEqual(J.overall(mk("PRESENT", "PRESENT", "NO_DIFFERENCE_DETECTED")), "CAUSAL_NOT_LEARNED")
        self.assertEqual(J.overall(mk("PRESENT", "NOT_DETECTED", "DERIVED_AHEAD")), "ONE_WAY")
        self.assertEqual(J.overall(mk("NOT_DETECTED", "REVERSED", "HOST_AHEAD")), "NO_CAUSAL_SIGNAL")
        self.assertEqual(J.overall(mk("UNDETERMINED", "PRESENT", "DERIVED_AHEAD")), "UNDETERMINED")
        c = mk("PRESENT", "PRESENT", "DERIVED_AHEAD")
        c["content"] = {"confounded_induce": True, "confounded_rescue": False}
        self.assertEqual(J.overall(c), "CONTENT_CONFOUNDED")
        self.assertEqual(J.overall(dict(c, valid=False)), "INVALID")

    def test_streams_and_seeds(self):
        self.assertNotEqual(STEER_TAG, EVAL_TAG_G)
        self.assertFalse(set(J.DISCOVERY_SEEDS) & set(J.CONFIRM_SEEDS))
        self.assertEqual(J.DISCOVERY_SEEDS, list(range(3200, 3228)))
        self.assertEqual(J.CONFIRM_SEEDS, list(range(3400, 3428)))


if __name__ == "__main__":
    unittest.main()
