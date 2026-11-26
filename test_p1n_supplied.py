"""Tests for P1n (trackc_swap/supplied.py, run_p1n_supplied.py)."""
import dataclasses
import unittest

import numpy as np
import torch

import run_p1g_graded as G
import run_p1n_supplied as N
from run_trackc_paid import PAY, WEAR
from trackc_swap.env import WorldConfig
from trackc_swap.gradmon import GradRunner
from trackc_swap.selfmon import EARLY, SPLIT_P
from trackc_swap.supplied import N_FLAG, FlagRunner, pad_state
from trackc_swap.train import TrainConfig


def _cfg():
    return WorldConfig(wear=WEAR), dataclasses.replace(TrainConfig(), n_envs=32, eval_episodes=1)


class TestSupplied(unittest.TestCase):
    def test_flags_off_reproduce_pfate_training(self):
        wc, tc = _cfg()
        a = GradRunner("PFATE", 5, wc, tc, PAY[1], base=G.BASE_F)
        st = a.export_state()
        b = FlagRunner("PFATE", 5, wc, tc, PAY[1], base=G.BASE_F, flag_on=False)
        b.load_state(pad_state(st))
        for _ in range(3):
            a.rollout(None, learn=True)
            b.rollout(None, learn=True)
        sa, sb = a.agent.state_dict(), b.agent.state_dict()
        for k in sa:
            vb = sb[k][:, :sa[k].shape[1]] if k == "enc.weight" else sb[k]
            self.assertTrue(torch.equal(sa[k], vb), k)
        self.assertTrue(torch.equal(sb["enc.weight"][:, -N_FLAG:], torch.zeros(sa["enc.weight"].shape[0], N_FLAG)))
        self.assertTrue(torch.equal(a.h, b.h))

    def test_flags_report_damage(self):
        wc, tc = _cfg()
        c = FlagRunner("PFATE", 5, wc, tc, PAY[1], base=G.BASE_F, flag_on=True)
        c.agent.eval()
        seen = []
        orig = c.world.observe

        def obs():
            o = orig()
            w = c.world
            seen.append((o[:, -N_FLAG:].copy(), (w.damaged & w.active).copy(), w.conflict.copy(), w.dmg_k.copy()))
            return o
        c.world.observe = obs
        c.evaluate_g("zero", drain_p=0.0, split_p=SPLIT_P, split_at=EARLY, probe_ks=c.ks, base_on=False)
        any_flag = False
        for f, dm, cf, k in seen:
            self.assertTrue(np.array_equal(f[:, 0] > 0, dm))
            self.assertTrue(np.array_equal(f[:, 1] > 0, dm & cf))
            self.assertTrue(np.allclose(f[:, 2], np.where(dm, k / 70.0, 0.0)))
            any_flag |= bool(dm.any())
        self.assertTrue(any_flag)
        c.set_flag(False)
        seen.clear()
        c.evaluate_g("zero", drain_p=0.0, split_p=SPLIT_P, split_at=EARLY, probe_ks=c.ks, base_on=False)
        self.assertTrue(all((f == 0).all() for f, *_ in seen))

    def test_labels(self):
        mk = lambda a, b, c, valid=True: {"valid": valid, "P1N_1": {"label": a}, "P1N_2": {"label": b},
                                          "P1N_3": {"label": c}}
        self.assertEqual(N.overall(mk("SUPPLY_AHEAD", "ENDOGENOUS_AHEAD", "ENDOGENOUS_AHEAD")),
                         "SUPPLY_DISPLACES_MONITOR")
        self.assertEqual(N.overall(mk("SUPPLY_AHEAD", "ENDOGENOUS_AHEAD", "NO_DIFFERENCE_DETECTED")), "SUPPLY_FRAGILE")
        self.assertEqual(N.overall(mk("SUPPLY_AHEAD", "NO_DIFFERENCE_DETECTED", "ENDOGENOUS_AHEAD")),
                         "SUPPLY_NOT_FRAGILE")
        self.assertEqual(N.overall(mk("UNDETERMINED", "ENDOGENOUS_AHEAD", "ENDOGENOUS_AHEAD")), "UNDETERMINED")
        self.assertEqual(N.overall(mk("SUPPLY_AHEAD", "ENDOGENOUS_AHEAD", "ENDOGENOUS_AHEAD", valid=False)), "INVALID")

    def test_sets(self):
        import run_p1i_calib as I
        self.assertEqual(N.SETS["confirm"]["seeds"], I.FINAL_SEEDS)
        self.assertTrue(set(N.SETS["discovery"]["seeds"]) <= set(G.FINAL_SEEDS))
        self.assertFalse(set(N.SETS["discovery"]["seeds"]) & set(N.SETS["confirm"]["seeds"]))


if __name__ == "__main__":
    unittest.main()
