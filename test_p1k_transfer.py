"""Tests for P1k (trackc_swap/transfer.py, run_p1k_transfer.py)."""
import dataclasses
import unittest

import numpy as np
import torch

import run_p1g_graded as G
import run_p1k_transfer as K
from run_trackc_paid import PAY, WEAR
from trackc_swap.env import WorldConfig
from trackc_swap.gradmon import EVAL_TAG_G
from trackc_swap.selfmon import EARLY, KIND_CONFLICT, KIND_NONE, KIND_SAME, SPLIT_P
from trackc_swap.steerint import STEER_TAG, SteerRunner
from trackc_swap.train import TrainConfig
from trackc_swap.transfer import TRANSFER_TAG, OpAgent, TransferRunner, activation, damaged_group


def _run(cls, op=None):
    wc = WorldConfig(wear=WEAR)
    tc = dataclasses.replace(TrainConfig(), eval_episodes=1)
    torch.manual_seed(0)
    c = cls("PFATE", 11, wc, tc, PAY[1], tag_offset=TRANSFER_TAG, base=G.BASE_F)
    c.agent.eval()
    if op:
        c.agent.op = op
        c.agent.gen_op = torch.Generator().manual_seed(3)
    _, _, _, col = c.evaluate_g("zero", drain_p=0.0, split_p=SPLIT_P, split_at=EARLY, collect=True,
                                probe_ks=c.ks, base_on=False)
    return col


class TestTransfer(unittest.TestCase):
    def test_donor_op_reproduces_steerrunner(self):
        a, b = _run(SteerRunner), _run(TransferRunner, "donor")
        for k in ("h", "val", "kind", "damaged", "k", "said", "unclear", "drained"):
            self.assertTrue(np.array_equal(a[k], b[k]), k)

    def test_operators(self):
        torch.manual_seed(1)
        ag = OpAgent(8)
        ag.gen_op = torch.Generator().manual_seed(0)
        obs = torch.zeros(3, ag.enc.in_features)
        h0 = torch.rand(3, 8) * 0.8 + 0.1
        over = torch.tensor([True, False, True])
        mask = torch.zeros(3, 8, dtype=torch.bool)
        mask[:, :4] = True
        ref = ag.core(torch.relu(ag.enc(obs)), h0)
        for op in ("zero", "noise", "scramble"):
            ag.op = op
            _, _, h = ag.step(obs, h0, over, torch.arange(3), mask)
            self.assertTrue(torch.allclose(h[1], ref[1]))                 # not damaged: untouched
            self.assertTrue(torch.allclose(h[:, 4:], ref[:, 4:]))         # unmasked units untouched
            if op == "zero":
                self.assertTrue((h[0, :4] == 0).all())
            if op == "noise":
                self.assertTrue((h[0, :4].abs() <= 1).all() and not torch.allclose(h[0, :4], ref[0, :4]))
            if op == "scramble":
                self.assertTrue(torch.allclose(h[0, :4].sort().values, ref[0, :4].sort().values))

    def test_novel_ops_damage_every_probe_kind(self):
        col = _run(TransferRunner, "zero")
        dm = col["damaged"].astype(bool)
        self.assertTrue((dm & (col["kind"] == KIND_SAME)).any() and (dm & (col["kind"] == KIND_CONFLICT)).any())
        self.assertFalse((dm & (col["kind"] == KIND_NONE)).any())
        g = damaged_group("zero", col["kind"], col["damaged"], col["unclear"])
        gd = damaged_group("donor", col["kind"], col["damaged"], col["unclear"])
        self.assertGreater(g.sum(), gd.sum())

    def test_activation_synthetic(self):
        rng = np.random.default_rng(0)
        n, D = 3000, 10
        val = rng.integers(0, 2, n)
        kind = rng.choice([KIND_NONE, KIND_SAME, KIND_CONFLICT], n)
        dam = kind != KIND_NONE
        d = np.eye(D)[2] * 1.5
        H = 0.3 * rng.standard_normal((n, D)) + np.outer(2 * val - 1, np.eye(D)[0]) + 0.8 * np.outer(dam, np.eye(D)[2])
        rec = {"h": H, "val": val, "kind": kind, "damaged": dam, "unclear": np.zeros(n, bool),
               "drained": np.zeros(n, bool), "k": np.where(dam, 35, 0)}
        a = activation(rec, "zero", d)
        self.assertAlmostEqual(a["act"], 0.8, delta=0.05)
        self.assertGreater(a["cos"], 0.9)
        rec["h"] = H - 0.8 * np.outer(dam, np.eye(D)[2]) + 0.8 * np.outer(dam, np.eye(D)[5])
        self.assertLess(abs(activation(rec, "zero", d)["act"]), 0.05)

    def test_labels(self):
        self.assertEqual(K.op_label("PRESENT", "PRESENT", False), "GENERALIZES")
        self.assertEqual(K.op_label("PRESENT", "PRESENT", True), "CONTENT_CONFOUNDED")
        self.assertEqual(K.op_label("PRESENT", "NOT_DETECTED", False), "ACTIVATES_NOT_USED")
        self.assertEqual(K.op_label("NOT_DETECTED", "PRESENT", False), "USED_NOT_ACTIVATED")
        self.assertEqual(K.op_label("REVERSED", "NOT_DETECTED", False), "NOT_GENERAL")
        self.assertEqual(K.op_label("UNDETERMINED", "PRESENT", False), "UNDETERMINED")
        mk = lambda labs, valid=True: {"valid": valid, "per_op": dict(zip(("scramble", "noise", "zero"), labs))}
        self.assertEqual(K.overall(mk(["GENERALIZES"] * 3)), "GENERAL_INTEGRITY_VARIABLE")
        self.assertEqual(K.overall(mk(["GENERALIZES", "NOT_GENERAL", "ACTIVATES_NOT_USED"])), "PARTIAL_GENERALITY")
        self.assertEqual(K.overall(mk(["NOT_GENERAL"] * 3)), "DONOR_SPECIFIC")
        self.assertEqual(K.overall(mk(["GENERALIZES", "UNDETERMINED", "NOT_GENERAL"])), "UNDETERMINED")
        self.assertEqual(K.overall(mk(["GENERALIZES"] * 3, valid=False)), "INVALID")

    def test_streams_and_sets(self):
        self.assertEqual(len({TRANSFER_TAG, STEER_TAG, EVAL_TAG_G}), 3)
        import run_p1i_calib as I
        self.assertEqual(K.CONFIRM_SET, I.FINAL_SEEDS)
        self.assertEqual(K.DISCOVERY_SET, list(range(3200, 3228)))


if __name__ == "__main__":
    unittest.main()
