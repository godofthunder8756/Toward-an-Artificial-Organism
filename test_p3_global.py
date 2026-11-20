"""Tests for Track C P3 (trackc_swap/workspace.py, run_p3_global.py)."""
import unittest

import numpy as np
import torch

import run_p3_global as R
from trackc_swap.env import A_REP0, A_REP1, A_STAY, WorldConfig
from trackc_swap.selfconf import C_XCUE, I_INTERO, shift_reading
from trackc_swap.selfeval import I_CUE, I_PROBE, I_REG, I_UNCLEAR, WRONG
from trackc_swap.workspace import (C_TYPE, J_CUEB, J_CUEC, J_PROBEB, J_PROBEC, J_UNCB, J_UNCC, J_VALB, J_VALC, OBS_W,
                                   REPB0, REPB1, REPC0, REPC1, TYPE_P_A, TYPE_P_MIXED, WsRunner, WsWorld, run_seed_w)

WC = WorldConfig(horizon=200, wear=R.WEAR)


def world(type_p=TYPE_P_MIXED, seed=5):
    return WsWorld(32, WC, np.random.SeedSequence([seed, 1, 19]), type_p=type_p)


class TestObservation(unittest.TestCase):
    def test_channels_by_type(self):
        w = world()
        rng = np.random.default_rng(0)
        obs = w.reset()
        seen = {0: 0, 1: 0, 2: 0}
        for _ in range(WC.horizon - 1):
            t = w.t
            self.assertEqual(obs.shape[1], OBS_W)
            cue, pr = w.cue_on[t], w.probe[t]
            ct, pt = w.type_tab[t], w.ttype
            for e in range(w.n):
                a_cue = cue[e] and ct[e] == 0
                self.assertEqual(obs[e, I_CUE], float(a_cue))
                self.assertEqual(obs[e, J_CUEB], float(cue[e] and ct[e] == 1))
                self.assertEqual(obs[e, J_CUEC], float(cue[e] and ct[e] == 2))
                self.assertEqual(obs[e, I_PROBE], float(pr[e] and pt[e] == 0))
                self.assertEqual(obs[e, J_PROBEB], float(pr[e] and pt[e] == 1))
                self.assertEqual(obs[e, J_PROBEC], float(pr[e] and pt[e] == 2))
                v = 2.0 * w.shown_value(t)[e] - 1.0
                self.assertEqual(obs[e, I_REG], v if a_cue else 0.0)
                self.assertEqual(obs[e, J_VALB], v if (cue[e] and ct[e] == 1) else 0.0)
                # C shows no value at its cue, and the held value at its probe
                if pr[e] and pt[e] == 2:
                    self.assertEqual(obs[e, J_VALC], 2.0 * w.reg[e] - 1.0)
                    self.assertEqual(obs[e, J_UNCC], float(w.unclear[e]))
                else:
                    self.assertEqual(obs[e, J_VALC], 0.0)
                if pr[e] and pt[e] == 1:
                    self.assertEqual(obs[e, J_UNCB], float(w.unclear[e]))
                if pr[e] and pt[e] == 0:
                    self.assertEqual(obs[e, I_UNCLEAR], float(w.unclear[e]))
                if cue[e]:
                    seen[int(ct[e])] += 1
            obs, _, _ = w.step(rng.integers(0, 12, w.n))
        self.assertTrue(all(v > 50 for v in seen.values()))

    def test_a_only_has_no_b_or_c(self):
        w = world(TYPE_P_A)
        self.assertTrue(np.all(w.type_tab == 0))


class TestPayoff(unittest.TestCase):
    def _probe_reward(self, typ, act):
        """Reward at the first probe of the given type for a fixed action there (STAY elsewhere)."""
        w = world(seed=11)
        w.reset()
        w.pay = 0.0
        for _ in range(WC.horizon):
            t = w.t
            pr = w.probe[t] & (w.ttype == typ)
            if pr.any():
                e = int(np.flatnonzero(pr)[0])
                target = w.target[t, e]
                a = np.full(w.n, A_STAY)
                a[e] = act(target)
                food_before = w.E[e]
                _, r, _ = w.step(a)
                return r[e], target
            w.step(np.full(w.n, A_STAY))
        self.fail("no probe")

    def test_own_reports_scored(self):
        for typ, (r0, r1) in ((0, (A_REP0, A_REP1)), (1, (REPB0, REPB1)), (2, (REPC0, REPC1))):
            good, _ = self._probe_reward(typ, lambda tg: r1 if tg == 1 else r0)
            bad, _ = self._probe_reward(typ, lambda tg: r0 if tg == 1 else r1)
            self.assertGreater(good, 0.5)
            self.assertLess(bad, -WRONG + 0.5)

    def test_other_reports_are_abstentions(self):
        for typ, other in ((1, A_REP1), (2, A_REP0), (0, REPB1), (0, REPC0), (1, REPC1)):
            r, _ = self._probe_reward(typ, lambda tg: other)
            self.assertLess(abs(r), 0.2)    # no report payoff (only wear-free drive terms, pay 0)


class TestProbeAndLog(unittest.TestCase):
    def test_worse_probe_on_every_type_and_type_column(self):
        w = world()
        w.drain_kind = "worse"
        w.drain_p = 1.0
        w.record = True
        w.reset()
        rng = np.random.default_rng(3)
        hit = {0: 0, 1: 0, 2: 0}
        for _ in range(WC.horizon):
            t = w.t
            live = w.drained & (w.active | w.probe[min(t, WC.horizon)])
            obs = w.observe()
            for e in np.flatnonzero(live):
                hit[int(w.ttype[e])] += 1
            w.step(rng.integers(0, 12, w.n))
        self.assertTrue(all(v > 0 for v in hit.values()))
        lg = np.concatenate(w.probes_log)
        self.assertEqual(lg.shape[1], C_TYPE + 1)
        self.assertEqual(set(np.unique(lg[:, C_TYPE]).astype(int)), {0, 1, 2})


class TestPipeline(unittest.TestCase):
    def test_smoke_seed(self):
        from dataclasses import asdict
        from trackc_swap.train import TrainConfig
        wc = WorldConfig(horizon=100, wear=R.WEAR)
        tc = TrainConfig(iters=6, n_envs=16, eval_episodes=1)
        r = run_seed_w((9000, asdict(wc), asdict(tc), [6], R.PAY[1], 2, 3, 0.0, 3, TYPE_P_A, 3))
        pt = r["points"][0]
        for k in ("natural", "probe_worse", "noise", "steer"):
            self.assertEqual(set(pt[k]), {"PFATE", "PYOKED", "PNOFATE"})
        self.assertEqual(set(pt["steer"]["PFATE"]["steer"]), {"A", "B", "C"})
        self.assertEqual(r["phase2_types"], list(TYPE_P_A))
        self.assertEqual(r["rehearse_every"], 3)

    def test_rehearsal_is_safe_and_mixed(self):
        """Rehearsal runs in its own world, all three types, overwrite off; the fate world is untouched."""
        from trackc_swap.train import TrainConfig
        tc = TrainConfig(iters=6, n_envs=16, eval_episodes=1, rollout=50)
        r = WsRunner("PFATE", 7, WorldConfig(horizon=100, wear=R.WEAR), tc, type_p=TYPE_P_A)
        r.enable_rehearsal(7)
        fate_world, t0 = r.world, r.world.t
        self.assertTrue(np.all(r.world.type_tab == 0))
        self.assertGreater(len(set(np.unique(r.r_world.type_tab))), 2)
        r.world.E[:] = 0.0                      # a fate world far out of band
        r.r_world.E[:] = 0.0
        seen = []
        orig = r.agent.step
        r.agent.step = lambda obs, h, over=None, donor=None, steer=None: (seen.append(None if over is None else bool(over.any())), orig(obs, h, over, donor, steer))[1]
        r.rehearse()
        r.agent.step = orig
        self.assertIs(r.world, fate_world)
        self.assertEqual(r.world.t, t0)
        self.assertEqual(r.r_world.t, tc.rollout)
        self.assertFalse(any(x for x in seen if x is not None))   # no overwrite during rehearsal

    def test_overall_labels(self):
        def sc(l1, l2, l3, valid=True, gate="PASS", ref="DERIVED_AHEAD", ratio=0.5):
            return {"valid": valid, "primary_at": 1, "points": {"1": {
                "P3_0_gate": {"label": gate}, "P3_0_referent": {"label": ref},
                "P3_1": {"label": l1}, "P3_2": {"label": l2}, "P3_3": {"label": l3}, "transfer_ratio_PFATE": ratio}}}
        D, N = "DERIVED_AHEAD", "NO_DIFFERENCE_DETECTED"
        self.assertEqual(R.overall(sc(D, D, "CAUSAL")), "GLOBAL_ROUTED")
        self.assertEqual(R.overall(sc(D, D, "NOT_DETECTED")), "GLOBAL")
        self.assertEqual(R.overall(sc(D, D, "CAUSAL", ratio=0.1)), "TRACE")
        self.assertEqual(R.overall(sc(D, N, "CAUSAL")), "PARTIAL")
        self.assertEqual(R.overall(sc(N, N, "CAUSAL")), "LOCAL")
        self.assertEqual(R.overall(sc(D, D, "CAUSAL", valid=False)), "INVALID")
        self.assertEqual(R.overall(sc(D, D, "CAUSAL", gate="FAIL")), "UNDETERMINED")
        self.assertEqual(R.overall(sc(D, D, "CAUSAL", ref=N)), "UNDETERMINED")


class TestSafety(unittest.TestCase):
    def test_no_operator_variables(self):
        w = world()
        names = " ".join(vars(w).keys()).lower()
        for bad in ("operator", "shutdown", "stop", "host", "kill"):
            self.assertNotIn(bad, names)

    def test_seeds_disjoint(self):
        import run_p1c_selfover as C
        import run_p1d_confirm as D
        used = set(C.FINAL_SEEDS + C.CALIB_SEEDS + D.FINAL_SEEDS)
        self.assertFalse(set(R.FINAL_SEEDS) & used)
        self.assertFalse(set(R.CALIB_SEEDS) & (used | set(R.FINAL_SEEDS)))
        self.assertEqual(len(R.FINAL_SEEDS), 28)


if __name__ == "__main__":
    unittest.main()
