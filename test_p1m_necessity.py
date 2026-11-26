"""Tests for P1m (trackc_swap/necessity.py, run_p1m_necessity.py)."""
import dataclasses
import unittest

import numpy as np
import torch

import run_p1g_graded as G
import run_p1m_necessity as M
from run_trackc_paid import PAY, WEAR
from trackc_swap.access import ACCESS_TAG, STEER_TAG_L
from trackc_swap.env import WorldConfig
from trackc_swap.gradmon import EVAL_TAG_G
from trackc_swap.necessity import NECESS_TAG, LesionAgent, LesionRunner, v_star
from trackc_swap.selfmon import EARLY, SPLIT_P
from trackc_swap.steerint import STEER_TAG
from trackc_swap.train import TrainConfig
from trackc_swap.transfer import TRANSFER_TAG, TransferRunner


def _run(cls, lesion=None):
    wc = WorldConfig(wear=WEAR)
    tc = dataclasses.replace(TrainConfig(), eval_episodes=1)
    torch.manual_seed(0)
    c = cls("PFATE", 11, wc, tc, PAY[1], tag_offset=NECESS_TAG, base=G.BASE_F)
    c.agent.eval()
    c.agent.op = "donor"
    if lesion is not None:
        c.lesion = lesion
    _, _, _, col = c.evaluate_g("zero", drain_p=0.0, split_p=SPLIT_P, split_at=EARLY, collect=True,
                                probe_ks=c.ks, base_on=False)
    return col


class TestNecessity(unittest.TestCase):
    def test_no_lesion_reproduces_transferrunner(self):
        a, b = _run(TransferRunner), _run(LesionRunner)
        for k in ("h", "val", "kind", "damaged", "k", "said"):
            self.assertTrue(np.array_equal(a[k], b[k]), k)

    def test_lesion_changes_state(self):
        u = np.zeros(70)
        u[0] = 1.0
        b = _run(LesionRunner, {t: {"u": u, "mu": 0.25} for t in range(1, 10)})
        self.assertTrue(np.allclose(b["h"][:, 0], 0.25, atol=1e-6))      # clamped at the readout step

    def test_clamp(self):
        torch.manual_seed(0)
        ag = LesionAgent(6)
        obs = torch.zeros(4, ag.enc.in_features)
        h0 = torch.rand(4, 6) * 0.5
        u = torch.tensor([0.6, 0.8, 0, 0, 0, 0])
        ag.lesion_D = u.repeat(4, 1)
        ag.lesion_mu = torch.full((4,), 0.1)
        ag.lesion_on = torch.tensor([True, False, True, False])
        _, _, h = ag.step(obs, h0)
        ag.lesion_on = None
        _, _, ref = ag.step(obs, h0)
        self.assertTrue(torch.allclose((h[[0, 2]] * u).sum(1), torch.tensor([0.1, 0.1]), atol=1e-6))
        self.assertTrue(torch.allclose(h[[1, 3]], ref[[1, 3]]))
        perp = h[0] - (h[0] * u).sum() * u
        self.assertTrue(torch.allclose(perp, ref[0] - (ref[0] * u).sum() * u, atol=1e-6))

    def test_v_star(self):
        rng = np.random.default_rng(12345)              # not the fold seed of v_star
        n = 20000
        grp = rng.integers(0, 2, n)                       # group 1: unreliable at the same confidence
        x = rng.random(n)
        p = np.where(grp == 1, 0.5, 0.7 + 0.3 * x)
        right = rng.random(n) < p
        w = np.ones(n)
        v0 = v_star(x, right, w, 0)
        v1 = v_star(x, right, w, 0, groups=grp)
        self.assertGreater(v1, v0 + 0.05)                 # the flag earns where the confidence does not separate
        ideal = np.mean(np.where(grp == 1, 0.0, np.maximum(0, 5 * p - 4)))
        self.assertLess(abs(v1 - ideal), 0.02)

    def test_labels(self):
        base = {"valid": True, "content": {"confounded": False}, "room_ok": True}
        mk = lambda a, b, c, **kw: dict(base, P1M_1={"label": a}, P1M_2={"label": b}, P1M_3={"label": c}, **kw)
        self.assertEqual(M.overall(mk("PRESENT", "PRESENT", "DERIVED_AHEAD")), "VALUE_CREDITED")
        self.assertEqual(M.overall(mk("PRESENT", "NOT_DETECTED", "DERIVED_AHEAD")), "VALUE_CREDITED_NOT_AS_USED")
        self.assertEqual(M.overall(mk("PRESENT", "PRESENT", "NO_DIFFERENCE_DETECTED")), "VALUE_NOT_LEARNED")
        self.assertEqual(M.overall(mk("NOT_DETECTED", "PRESENT", "NO_DIFFERENCE_DETECTED")), "USED_NOT_NECESSARY")
        self.assertEqual(M.overall(mk("REVERSED", "NOT_DETECTED", "HOST_AHEAD")), "VARIABLE_COSTLY")
        self.assertEqual(M.overall(mk("NOT_DETECTED", "NOT_DETECTED", "NO_DIFFERENCE_DETECTED")), "NO_VALUE_DETECTED")
        self.assertEqual(M.overall(mk("NOT_DETECTED", "PRESENT", "NO_DIFFERENCE_DETECTED", room_ok=False)),
                         "NECESSITY_NOT_TESTABLE_USED")
        self.assertEqual(M.overall(mk("NOT_DETECTED", "NOT_DETECTED", "NO_DIFFERENCE_DETECTED", room_ok=False)),
                         "NECESSITY_NOT_TESTABLE")
        c = mk("PRESENT", "PRESENT", "DERIVED_AHEAD")
        c["content"] = {"confounded": True}
        self.assertEqual(M.overall(c), "CONTENT_CONFOUNDED")
        self.assertEqual(M.overall(dict(mk("PRESENT", "PRESENT", "DERIVED_AHEAD"), valid=False)), "INVALID")

    def test_streams_and_sets(self):
        self.assertEqual(len({NECESS_TAG, ACCESS_TAG, STEER_TAG_L, TRANSFER_TAG, STEER_TAG, EVAL_TAG_G}), 6)
        import run_p1i_calib as I
        self.assertEqual(M.CONFIRM_SET, I.FINAL_SEEDS)


if __name__ == "__main__":
    unittest.main()
