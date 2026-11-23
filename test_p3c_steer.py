"""Tests for P3c (trackc_swap/steerdiff.py, run_p3c_steer.py)."""
import json
import unittest
from dataclasses import asdict

import numpy as np
import torch

import run_p3b_diff as R3B
import run_p3c_steer as R
from trackc_swap.differentiate import DiffRunner, run_seed_x
from trackc_swap.env import WorldConfig
from trackc_swap.selfcomp import C_STEERED
from trackc_swap.steerdiff import TYPE_IDX, collect_h, cos, direction, run_seed_s, steer_effects
from trackc_swap.train import TrainConfig

WC = WorldConfig(horizon=100, wear=R.WEAR)
TC = TrainConfig(iters=6, n_envs=16, eval_episodes=1)


def runner(seed=9000, tag=0):
    c = DiffRunner("PFATE", seed, WC, TC, R.PAY[1], tag_offset=tag)
    c.agent.eval()
    return c


class TestCollect(unittest.TestCase):
    def test_counts_only_clear_live_trials_and_restores_step(self):
        c = runner()
        seen = []
        orig = c.agent.step

        def spy(obs, h, *a, **kw):
            w = c.world
            seen.append(sum(int((w.active & ~w.unclear & (w.ttype == ti)).sum()) for ti in TYPE_IDX.values()))
            return orig(obs, h, *a, **kw)

        c.agent.step = spy
        acc = collect_h(c, "look_low")
        self.assertIs(c.agent.step, spy)                 # an existing wrapper is put back
        del c.agent.step
        n = sum(acc[("n", t, d)] for t in TYPE_IDX for d in (0, 1))
        self.assertEqual(n, sum(seen))
        self.assertGreater(min(acc[("n", t, d)] for t in TYPE_IDX for d in (0, 1)), 0)
        self.assertNotIn("step", vars(c.agent))
        collect_h(c, "look_high")
        self.assertNotIn("step", vars(c.agent))          # collect_h's own wrapper is removed
        self.assertEqual(c.world.drain_kind, "down")

    def test_direction_and_cos(self):
        acc = {("A", 1): torch.tensor([4.0, 0.0], dtype=torch.float64), ("n", "A", 1): 2,
               ("A", 0): torch.tensor([0.0, 3.0], dtype=torch.float64), ("n", "A", 0): 3}
        d = direction(acc, "A")
        self.assertTrue(torch.allclose(d, torch.tensor([2.0, -1.0])))
        self.assertAlmostEqual(cos(d, -d), -1.0, places=6)
        acc[("n", "A", 0)] = 0
        self.assertIsNone(direction(acc, "A"))


class TestSteering(unittest.TestCase):
    def test_zero_vector_changes_nothing(self):
        a, b = runner(tag=7), runner(tag=7)
        b.agent.load_state_dict(a.agent.state_dict())
        _, _, la = a.evaluate("zero")
        _, _, lb = b.evaluate("zero", steer=torch.zeros(a.agent.hidden))
        cols = [k for k in range(la.shape[1]) if k != C_STEERED]
        self.assertTrue(np.array_equal(la[:, cols], lb[:, cols]))
        self.assertGreater(lb[:, C_STEERED].sum(), 0)    # half the trials are marked steered

    def test_steer_only_on_live_steered_envs(self):
        c = runner()
        c.world.reset()
        c.steer = torch.ones(c.agent.hidden)
        w = c.world
        w.active[:] = False
        w.steered[:] = True
        w.active[:3] = True
        s = c._steer_now()
        self.assertTrue(torch.all(s[:3] == 1) and torch.all(s[3:] == 0))
        c.steer = None

    def test_effect_fields(self):
        c = runner()
        e = steer_effects(c, torch.zeros(c.agent.hidden))
        self.assertEqual(set(e), {"A", "C"})
        for t in "AC":
            self.assertIn("effect", e[t])


class TestTrainingUnchanged(unittest.TestCase):
    def test_run_seed_s_is_p3b_training_plus_steering(self):
        job = (9000, asdict(WC), asdict(TC), [6], R.PAY[1], 2, 3, 0.0, 3)
        a = run_seed_x(job)
        b = run_seed_s(job + (1.0,))
        pa, pb = a["points"][0], {k: v for k, v in b["points"][0].items() if k != "steer"}
        pa = {k: v for k, v in pa.items() if k != "seconds_training"}
        pb = {k: v for k, v in pb.items() if k != "seconds_training"}
        self.assertEqual(json.dumps(pa, sort_keys=True, default=float), json.dumps(pb, sort_keys=True, default=float))
        self.assertEqual(a["weights"], b["weights"])
        self.assertEqual(set(b["points"][0]["steer"]), {"PFATE", "PYOKED", "PNOFATE"})
        st = b["points"][0]["steer"]["PFATE"]["steer"]
        self.assertEqual(set(st), {"+u_A", "-u_A", "+u_C", "-u_C", "+v_C", "-v_C",
                                   "+rand_u_A", "-rand_u_A", "+rand_u_C", "-rand_u_C"})


def sp_record(eff):
    """A steer record with given effects: eff[(key, type)] -> effect."""
    keys = {k for k, _ in eff}
    st = {k: {t: {"effect": eff.get((k, t), 0.0), "correct_on": 1.0, "abstain_off": 0.0} for t in "AC"} for k in keys}
    return {"steer": st, "cos": {"u_A,u_C": 0.5}, "split_half_cos": {"u_A": 0.9, "u_C": 0.8}}


class TestScoring(unittest.TestCase):
    def test_signs(self):
        eff = {("+u_A", "A"): 0.3, ("-u_A", "A"): -0.1, ("+u_C", "C"): -0.2, ("-u_C", "C"): 0.1,
               ("+u_A", "C"): -0.05, ("-u_A", "C"): 0.0, ("+u_C", "A"): 0.02, ("-u_C", "A"): 0.0,
               ("+v_C", "C"): 0.1, ("-v_C", "C"): 0.0, ("+v_C", "A"): 0.0, ("-v_C", "A"): 0.0,
               ("+rand_u_A", "A"): 0.04, ("-rand_u_A", "A"): 0.02, ("+rand_u_C", "C"): 0.01, ("-rand_u_C", "C"): 0.03}
        m = R.steer_measures(sp_record(eff))
        self.assertAlmostEqual(m["S_A"], 0.4)
        self.assertAlmostEqual(m["S_C"], 0.3)       # release counts positive
        self.assertAlmostEqual(m["X_AC"], 0.05)
        self.assertAlmostEqual(m["X_CA"], 0.02)
        self.assertAlmostEqual(m["V_C"], 0.1)
        self.assertAlmostEqual(m["R_A"], 0.02)
        self.assertAlmostEqual(m["P_A"], 0.03)
        self.assertAlmostEqual(m["P_C"], 0.02)

    def test_structure(self):
        lab = lambda x: {"label": x}
        sp = {"SA": lab("CAUSAL"), "SC": lab("CAUSAL"), "secondary": {"X_AC_PFATE": lab("CAUSAL"), "X_CA_PFATE": lab("CAUSAL")}}
        self.assertEqual(R.structure(sp), "ONE_DIRECTION_TWO_READOUTS")
        sp["secondary"]["X_CA_PFATE"] = lab("NOT_DETECTED")
        self.assertEqual(R.structure(sp), "PARTLY_SHARED")
        sp["secondary"]["X_AC_PFATE"] = lab("NOT_DETECTED")
        self.assertEqual(R.structure(sp), "SEPARATE_DIRECTIONS")
        sp["secondary"]["X_AC_PFATE"] = lab("REVERSED_CAUSAL")
        self.assertEqual(R.structure(sp), "PARTLY_SHARED")
        sp["SC"] = lab("NOT_DETECTED")
        self.assertEqual(R.structure(sp), "NOT_APPLICABLE")

    def test_overall(self):
        def sc(valid=True, n=27, gate="PASS", b1="DERIVED_AHEAD", b2="DERIVED_AHEAD", sa="CAUSAL", s_c="CAUSAL"):
            p = {"gate": {"label": gate}, "P3C_B1": {"label": b1}, "P3C_B2": {"label": b2},
                 "P3C_SA": {"label": sa}, "P3C_SC": {"label": s_c}}
            return {"valid": valid, "n_usable": n, "primary_at": 3600, "points": {"3600": p}}
        self.assertEqual(R.overall(sc()), "CONFIRMED_CAUSAL")
        self.assertEqual(R.overall(sc(s_c="NOT_DETECTED")), "CONFIRMED_BEHAVIOURAL")
        self.assertEqual(R.overall(sc(sa="UNDETERMINED")), "CONFIRMED_BEHAVIOURAL")
        self.assertEqual(R.overall(sc(b2="NO_DIFFERENCE_DETECTED")), "NOT_CONFIRMED")
        self.assertEqual(R.overall(sc(b2="YOKED_AHEAD")), "NOT_CONFIRMED")
        self.assertEqual(R.overall(sc(b2="UNDETERMINED")), "UNDETERMINED")
        self.assertEqual(R.overall(sc(b1="NO_DIFFERENCE_DETECTED")), "UNDETERMINED")
        self.assertEqual(R.overall(sc(gate="FAIL")), "UNDETERMINED")
        self.assertEqual(R.overall(sc(n=13)), "UNDETERMINED")
        self.assertEqual(R.overall(sc(valid=False)), "INVALID")


class TestSafety(unittest.TestCase):
    def test_no_operator_variables(self):
        names = " ".join(vars(runner().world).keys()).lower()
        for bad in ("operator", "shutdown", "stop", "host", "kill"):
            self.assertNotIn(bad, names)

    def test_seeds(self):
        import run_p1c_selfover as C
        import run_p1d_confirm as D
        import run_p3_global as G
        used = set(C.FINAL_SEEDS + C.CALIB_SEEDS + D.FINAL_SEEDS + G.FINAL_SEEDS + G.CALIB_SEEDS
                   + R3B.FINAL_SEEDS + R3B.CALIB_SEEDS)
        self.assertFalse(set(R.FINAL_SEEDS) & used)
        self.assertEqual(len(R.FINAL_SEEDS), 28)
        self.assertTrue(set(R.CALIB_NETS) <= set(R3B.FINAL_SEEDS))


if __name__ == "__main__":
    unittest.main()
