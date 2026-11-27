"""Tests for P1p (trackc_swap/archswap.py, run_p1p_replication.py)."""
import dataclasses
import unittest

import numpy as np
import torch

import run_p1g_graded as G
import run_p1p_replication as P
from run_trackc_paid import PAY, WEAR
from trackc_swap import archswap
from trackc_swap.archswap import N_CELL, CIFGCore
from trackc_swap.env import WorldConfig
from trackc_swap.selfmon import EARLY, SPLIT_P
from trackc_swap.train import TrainConfig

archswap.uninstall()      # importing the run script installs the swap; each test installs it explicitly


class TestArchSwap(unittest.TestCase):
    def tearDown(self):
        archswap.uninstall()

    def test_cell_bounded(self):
        torch.manual_seed(1)
        core = CIFGCore(70, N_CELL)
        s = torch.zeros(64, 2 * N_CELL)
        for _ in range(200):
            with torch.no_grad():
                s = core(torch.randn(64, 70) * 5, s)
            self.assertLessEqual(float(s.abs().max()), 1.0)
        self.assertEqual(s.shape[1], 70)

    def test_install_swaps_every_runner(self):
        from trackc_swap import access, gradmon, necessity, selfmon, steerint, transfer
        wc, tc = WorldConfig(wear=WEAR), dataclasses.replace(TrainConfig(), eval_episodes=1, n_envs=32)
        archswap.install()
        archswap.install()                                    # idempotent: no double swap
        for cls in (selfmon.MonRunner, gradmon.GradRunner, steerint.SteerRunner, transfer.TransferRunner,
                    necessity.LesionRunner, access.SteerRunner, access.TransferRunner):
            r = cls("PFATE", 7, wc, tc, PAY[1]) if cls is selfmon.MonRunner else \
                cls("PFATE", 7, wc, tc, PAY[1], base=G.BASE_F)
            self.assertIsInstance(r.agent.core, CIFGCore, cls.__name__)
            self.assertEqual(cls.__mro__[1].__name__, cls.__name__[4:])      # one level of swapping
            self.assertTrue(all(p is q for p, q in zip(r.opt.param_groups[0]["params"], r.agent.parameters())))
        a = gradmon.GradRunner("PFATE", 7, wc, tc, PAY[1], base=G.BASE_F).agent.state_dict()
        b = gradmon.GradRunner("PFATE", 7, wc, tc, PAY[1], base=G.BASE_F).agent.state_dict()
        self.assertTrue(all(torch.equal(a[k], b[k]) for k in a))         # deterministic per seed
        archswap.uninstall()
        self.assertNotIsInstance(gradmon.GradRunner("PFATE", 7, wc, tc, PAY[1], base=G.BASE_F).agent.core, CIFGCore)

    def test_damage_and_probe_on_packed_state(self):
        from trackc_swap import necessity
        archswap.install()
        wc, tc = WorldConfig(wear=WEAR), dataclasses.replace(TrainConfig(), eval_episodes=1)
        c = necessity.LesionRunner("PFATE", 11, wc, tc, PAY[1], base=G.BASE_F)
        c.agent.eval()
        c.agent.op = "donor"
        _, _, _, col = c.evaluate_g("zero", drain_p=0.0, split_p=SPLIT_P, split_at=EARLY, collect=True,
                                    probe_ks=c.ks, base_on=False)
        self.assertEqual(col["h"].shape[1], 70)
        self.assertGreater(int(col["damaged"].sum()), 100)
        self.assertLessEqual(float(np.abs(col["h"]).max()), 1.0)

    def test_labels(self):
        def sc(p1g="DERIVED_AHEAD", valid=True, n=28, **lab):
            g = {"valid": valid, "n_seeds": n, "primary_at": 3600,
                 "points": {"3600": {"P1G_1": {"label": p1g}}}}
            out = {"P1g": g}
            for k in P.STUDIES:
                out[k] = {"overall": lab.get(k, P.GRU_LABELS[k])}
            return out
        self.assertEqual(P.overall(sc()), "BLOCK_REPLICATED")
        self.assertEqual(P.overall(sc(P1m="USED_NOT_NECESSARY")), "PARTIAL_REPLICATION")
        self.assertEqual(P.overall(sc(p1g="NO_DIFFERENCE_DETECTED")), "MONITOR_NOT_REPLICATED")
        self.assertEqual(P.overall(sc(valid=False)), "INVALID")
        self.assertEqual(P.overall(sc(n=8)), "UNDETERMINED")
        lab, match = P.summarize(sc(P1k="PARTIAL_GENERALITY"))
        self.assertFalse(match["P1k"])
        self.assertTrue(match["P1g"] and match["P1j"])

    def test_sets(self):
        import run_p1i_calib as I
        self.assertEqual(P.SETS["confirm"], I.FINAL_SEEDS)
        self.assertEqual(P.SETS["discovery"], list(range(3200, 3208)))


if __name__ == "__main__":
    unittest.main()
