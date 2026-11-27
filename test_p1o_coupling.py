"""Tests for P1o (trackc_swap/coupling.py, run_p1o_coupling.py)."""
import dataclasses
import unittest

import numpy as np
import torch

import run_p1g_graded as G
import run_p1o_coupling as O
from run_trackc_paid import PAY, WEAR
from trackc_swap.access import ACCESS_TAG, STEER_TAG_L
from trackc_swap.coupling import P1O_TAG, CoupleRunner, foraging, room
from trackc_swap.env import A_E, A_INTERACT, A_STAY, A_W, N_ACT, WorldConfig
from trackc_swap.gradmon import EVAL_TAG_G
from trackc_swap.necessity import NECESS_TAG, LesionRunner
from trackc_swap.selfmon import EARLY, SPLIT_P
from trackc_swap.steerint import STEER_TAG
from trackc_swap.train import TrainConfig
from trackc_swap.transfer import TRANSFER_TAG


def _run(cls, frec=False):
    wc = WorldConfig(wear=WEAR)
    tc = dataclasses.replace(TrainConfig(), eval_episodes=1)
    torch.manual_seed(0)
    c = cls("PFATE", 11, wc, tc, PAY[1], tag_offset=P1O_TAG, base=G.BASE_F)
    c.agent.eval()
    c.agent.op = "donor"
    if frec:
        c.frec = []
    _, _, _, col = c.evaluate_g("zero", drain_p=0.0, split_p=SPLIT_P, split_at=EARLY, collect=True,
                                probe_ks=c.ks, base_on=False)
    return col, c


class TestCoupling(unittest.TestCase):
    def test_recording_reproduces_lesionrunner(self):
        a, _ = _run(LesionRunner)
        b, c = _run(CoupleRunner, frec=True)
        for k in ("h", "val", "kind", "damaged", "k", "said"):
            self.assertTrue(np.array_equal(a[k], b[k]), k)
        self.assertGreater(len(c.frec), 0)
        self.assertNotIn("step", c.agent.__dict__)          # the wrapper is removed after the rollout

    def test_foraging(self):
        grid = 7
        x, y = np.array([0, 0, 3, 3]), np.array([0, 0, 3, 3])
        fx = np.array([[2, 6], [2, 6], [3, 0], [3, 0]])
        fy = np.array([[0, 6], [0, 6], [3, 0], [3, 0]])
        avail = np.array([[True, True], [True, True], [True, True], [False, False]])
        p = np.zeros((4, N_ACT))
        p[0, A_E] = 1.0          # toward the food at (2, 0): +1
        p[1, A_W] = 1.0          # into the wall: no move, 0
        p[2, A_INTERACT] = 1.0   # on food, eats: 1
        p[3, A_STAY] = 1.0       # no food available: NaN
        f = foraging(p, x, y, fx, fy, avail, grid)
        self.assertEqual(f[0], 1.0)
        self.assertEqual(f[1], 0.0)
        self.assertEqual(f[2], 1.0)
        self.assertTrue(np.isnan(f[3]))
        p2 = np.zeros((1, N_ACT))
        p2[0, A_W] = 0.5
        p2[0, A_E] = 0.5         # half away (-1), half toward (+1)
        self.assertAlmostEqual(foraging(p2, x[:1] + 1, y[:1], fx[:1], fy[:1], avail[:1], grid)[0], 0.0)

    def test_room(self):
        rng = np.random.default_rng(5)
        n = 40000
        shown = rng.random(n)
        out = rng.random(n) < 0.2
        base = dict(shown=shown, out=out, pre_damaged=np.zeros(n, bool), since=np.full(n, 3))
        ev_inf = rng.random(n) < np.where(out, 0.3, 0.012)       # informative events
        ev_ind = rng.random(n) < 0.05                             # events independent of the body
        r1 = room([dict(base, ev=ev_inf)])["room"]
        r0 = room([dict(base, ev=ev_ind)])["room"]
        self.assertGreater(r1, 0.5)
        self.assertLess(abs(r0), 0.03)

    def test_labels(self):
        mk = lambda a, b, c, valid=True: {"valid": valid, "P1O_1": {"label": a}, "P1O_2": {"label": b},
                                          "P1O_3": {"label": c}}
        self.assertEqual(O.overall(mk("PRESENT", "FATE_AHEAD", "PRESENT")), "PRECARITY_COUPLES_MONITOR")
        self.assertEqual(O.overall(mk("PRESENT", "FATE_AHEAD", "NOT_DETECTED")), "COUPLED_NOT_CAUSAL")
        self.assertEqual(O.overall(mk("PRESENT", "NO_DIFFERENCE_DETECTED", "PRESENT")), "COUPLED_NOT_PRECARITY")
        self.assertEqual(O.overall(mk("NOT_DETECTED", "FATE_AHEAD", "PRESENT")), "NO_COUPLING")
        self.assertEqual(O.overall(mk("REVERSED", "YOKED_AHEAD", "NOT_DETECTED")), "NO_COUPLING")
        self.assertEqual(O.overall(mk("UNDETERMINED", "FATE_AHEAD", "PRESENT")), "UNDETERMINED")
        self.assertEqual(O.overall(mk("PRESENT", "FATE_AHEAD", "PRESENT", valid=False)), "INVALID")

    def test_streams_and_sets(self):
        import run_p1n_supplied as N
        self.assertEqual(len({P1O_TAG, N.P1N_TAG, NECESS_TAG, ACCESS_TAG, STEER_TAG_L, TRANSFER_TAG, STEER_TAG,
                              EVAL_TAG_G}), 8)
        import run_p1i_calib as I
        self.assertEqual(O.CONFIRM_SET, I.FINAL_SEEDS)
        self.assertEqual(O.DISCOVERY_SET, list(range(3200, 3228)))


if __name__ == "__main__":
    unittest.main()
