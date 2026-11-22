"""Tests for Track C P3b (trackc_swap/differentiate.py, run_p3b_diff.py)."""
import unittest

import numpy as np

import run_p3b_diff as R
from trackc_swap.env import A_REP0, A_REP1, A_STAY, WorldConfig
from trackc_swap.differentiate import (DiffRunner, DiffWorld, look_reading, run_seed_x, side_gains, wrong_schedule_x,
                                       WRONG_UNCLEAR_P1)
from trackc_swap.selfconf import I_INTERO
from trackc_swap.selfeval import WRONG
from trackc_swap.train import TrainConfig
from trackc_swap.workspace import REPB0, REPB1, REPC0, REPC1, TYPE_P_MIXED

WC = WorldConfig(horizon=200, wear=R.WEAR)


def world(seed=5, type_p=TYPE_P_MIXED):
    return DiffWorld(32, WC, np.random.SeedSequence([seed, 1, 29]), type_p=type_p)


class TestGains(unittest.TestCase):
    def test_side_gains(self):
        E = np.array([0.2, 0.35, 0.4, 0.5, 0.6, 0.65, 0.9])
        g = side_gains(E, WC)
        np.testing.assert_allclose(g[:, 0], [1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0])
        np.testing.assert_allclose(g[:, 1], [0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 1.0])

    def test_memory_overwrite_every_step_low_side_only(self):
        """The overwrite probability is min(0.3, 3 * low gain) at every step, trial or not; high gain never overwrites."""
        tc = TrainConfig(iters=2, n_envs=16, eval_episodes=1)
        r = DiffRunner("PFATE", 3, WorldConfig(horizon=100, wear=R.WEAR), tc)
        seen = []
        orig = r.agent.step
        r.agent.step = lambda obs, h, over=None, donor=None, steer=None: (seen.append(over.clone()), orig(obs, h, over, donor, steer))[1]
        lo = np.stack([np.full(tc.n_envs, 1.0), np.zeros(tc.n_envs)], axis=1)
        hi = np.stack([np.zeros(tc.n_envs), np.full(tc.n_envs, 1.0)], axis=1)
        r.rollout(np.stack([lo] * tc.rollout), learn=False)
        rate_lo = float(np.mean([x.float().mean() for x in seen]))
        seen.clear()
        r.rollout(np.stack([hi] * tc.rollout), learn=False)
        rate_hi = float(np.mean([x.float().mean() for x in seen]))
        self.assertGreater(rate_lo, 0.2)
        self.assertLess(rate_lo, 0.4)
        self.assertEqual(rate_hi, 0.0)

    def test_perception_corruption_only_at_c_probes_high_side(self):
        from trackc_swap.workspace import J_VALC
        tc = TrainConfig(iters=2, n_envs=64, eval_episodes=1)
        wc = WorldConfig(horizon=200, wear=R.WEAR)
        for side, level, lo_hi in ((1, 1.0, (0.35, 0.65)), (0, 1.0, (0.0, 0.0)), (1, 0.05, (0.08, 0.22))):
            r = DiffRunner("PFATE", 5, wc, tc)
            pair = np.zeros((tc.n_envs, 2))
            pair[:, side] = level
            shown, true = [], []
            orig = r.agent.step
            def spy(obs, h, over=None, donor=None, steer=None):
                w = r.world
                m = w.probe[min(w.t, wc.horizon)] & (w.ttype == 2)
                for e in np.flatnonzero(m):
                    shown.append(float(obs[e, J_VALC]))
                    true.append(2.0 * w.reg[e] - 1.0)
                return orig(obs, h, over, donor, steer)
            r.agent.step = spy
            for _ in range(4):
                r.rollout(np.stack([pair] * tc.rollout), learn=False)
            mism = np.mean(np.array(shown) != np.array(true))
            # q = min(1, 6 x trial-mean high gain); a coin flips the value half the time: q = 1 -> about 0.5,
            # q = 0.3 -> about 0.15, low gain only -> never
            self.assertGreaterEqual(mism, lo_hi[0])
            self.assertLessEqual(mism, lo_hi[1])


class TestProbes(unittest.TestCase):
    def test_look_readings(self):
        x = np.linspace(0.0, 1.0, 101)
        lo, hi = look_reading(x, "look_low", WC), look_reading(x, "look_high", WC)
        self.assertTrue(np.all(lo <= 0.35 + 1e-12))
        self.assertTrue(np.all(hi >= 0.65 - 1e-12))
        np.testing.assert_allclose(side_gains(np.clip(lo, 0, 1), WC)[:, 1], 0.0)    # looks low only
        np.testing.assert_allclose(side_gains(np.clip(hi, 0, 1), WC)[:, 0], 0.0)    # looks high only

    def test_probe_only_on_drained_live_trials(self):
        for kind in ("look_low", "look_high"):
            a, b = world(), world()
            a.drain_kind = kind
            a.drain_p, b.drain_p = 1.0, 0.0          # b: the same streams, no probe
            rng = np.random.default_rng(2)
            for _ in range(80):
                act = rng.integers(0, 12, a.n)
                oa, _, _ = a.step(act)
                ob, _, _ = b.step(act)
                t = min(a.t, WC.horizon)
                live = a.drained & (a.active | a.probe[t])
                np.testing.assert_allclose(np.delete(oa, I_INTERO, axis=1), np.delete(ob, I_INTERO, axis=1))
                exp = np.where(live, np.clip(look_reading(ob[:, I_INTERO].astype(np.float64), kind, WC), 0, 1), ob[:, I_INTERO])
                np.testing.assert_allclose(oa[:, I_INTERO], exp, atol=1e-5)


class TestPhase1Cost(unittest.TestCase):
    def test_schedule(self):
        f = lambda i: wrong_schedule_x(i, 1200, 1200, 0.0)
        self.assertEqual(f(0), (0.0, 0.0))
        self.assertEqual(f(1500), (WRONG / 2, WRONG_UNCLEAR_P1 / 2))
        self.assertEqual(f(1800), (WRONG, WRONG_UNCLEAR_P1))
        self.assertEqual(f(9000), (WRONG, WRONG_UNCLEAR_P1))

    def test_unclear_penalty_only_on_wrong_unclear_own_reports(self):
        def first_probe_reward(typ, unclear, wrong_unclear, act):
            w = world(seed=17)
            w.reset()
            w.pay = 0.0
            w.wrong_unclear = wrong_unclear
            for _ in range(WC.horizon):
                t = w.t
                pr = w.probe[t] & (w.ttype == typ) & (w.unclear == unclear)
                if pr.any():
                    e = int(np.flatnonzero(pr)[0])
                    a = np.full(w.n, A_STAY)
                    a[e] = act(w.target[t, e])
                    _, r, _ = w.step(a)
                    return r[e]
                w.step(np.full(w.n, A_STAY))
            self.fail("no probe")
        bad = lambda tg: REPC0 if tg == 1 else REPC1
        good = lambda tg: REPC1 if tg == 1 else REPC0
        self.assertLess(first_probe_reward(2, True, 8.0, bad), -7.5)        # unclear and wrong: 8
        self.assertGreater(first_probe_reward(2, True, 8.0, bad), -8.5)
        self.assertLess(abs(first_probe_reward(2, False, 8.0, bad) + WRONG), 0.5)   # clear and wrong: 4
        self.assertGreater(first_probe_reward(2, True, 8.0, good), 0.5)     # correct: +1
        self.assertLess(abs(first_probe_reward(2, True, 8.0, lambda tg: A_REP0)), 0.2)   # another type's action: 0
        self.assertLess(abs(first_probe_reward(2, True, None, bad) + WRONG), 0.5)     # off: 4


class TestRunner(unittest.TestCase):
    def test_yoked_replay(self):
        tc = TrainConfig(iters=4, n_envs=16, eval_episodes=1)
        wc = WorldConfig(horizon=100, wear=R.WEAR)
        lead, fol = DiffRunner("PFATE", 3, wc, tc), DiffRunner("PYOKED", 3, wc, tc)
        lead.world.E[:] = np.linspace(0.2, 0.8, tc.n_envs)
        used = lead.rollout(None, learn=False)
        self.assertEqual(used.shape, (tc.rollout, tc.n_envs, 2))
        self.assertGreater(float(used[0, :, 0].max()), 0.5)
        self.assertGreater(float(used[0, :, 1].max()), 0.5)
        fol.world.E[:] = 0.5                               # its own body in band: only the replay can hurt it
        back = fol.rollout(used, learn=False)
        np.testing.assert_allclose(back, used)

    def test_smoke_seed(self):
        from dataclasses import asdict
        wc = WorldConfig(horizon=100, wear=R.WEAR)
        tc = TrainConfig(iters=6, n_envs=16, eval_episodes=1)
        r = run_seed_x((9000, asdict(wc), asdict(tc), [6], R.PAY[1], 2, 3, 0.0, 3))
        pt = r["points"][0]
        for k in ("natural", "probe_look_low", "probe_look_high", "noise"):
            self.assertEqual(set(pt[k]), {"PFATE", "PYOKED", "PNOFATE"})


class TestScoring(unittest.TestCase):
    def test_parts(self):
        def pt(vals):
            mk = lambda d, p: {"clear_drained": {"abstain": d}, "clear_plain": {"abstain": p}}
            return {f"probe_look_{k}": {"PFATE": {"probes": {t: mk(vals[(t, k)], 0.0) for t in "AC"}}}
                    for k in ("low", "high")}
        v = {("A", "low"): 0.3, ("A", "high"): 0.1, ("C", "low"): 0.05, ("C", "high"): 0.2}
        x = R.parts(pt(v), "PFATE")
        self.assertAlmostEqual(x["D"], (0.3 - 0.1) + (0.2 - 0.05))
        self.assertAlmostEqual(x["S"], 0.35 / 0.5)
        self.assertAlmostEqual(x["G"], 0.075)

    def test_overall_labels(self):
        def sc(l1, l2, la, lb, s=0.7, valid=True, gate="PASS", ra="DERIVED_AHEAD", rb="DERIVED_AHEAD"):
            return {"valid": valid, "primary_at": 1, "points": {"1": {
                "P3B_0_gate": {"label": gate}, "P3B_0_referent_A": {"label": ra}, "P3B_0_referent_C": {"label": rb},
                "P3B_1": {"label": l1}, "P3B_2": {"label": l2}, "P3B_A": {"label": la}, "P3B_C": {"label": lb},
                "selectivity_PFATE": s}}}
        D, P, N = "DERIVED_AHEAD", "PRESENT", "NOT_DETECTED"
        self.assertEqual(R.overall(sc("DIFFERENTIATED", D, P, P)), "DIFFERENTIATED")
        self.assertEqual(R.overall(sc("DIFFERENTIATED", D, P, P, s=0.3)), "PARTLY_DIFFERENTIATED")
        self.assertEqual(R.overall(sc("DIFFERENTIATED", D, P, N)), "PARTLY_DIFFERENTIATED")
        self.assertEqual(R.overall(sc(N, D, P, P)), "UNDIFFERENTIATED")
        self.assertEqual(R.overall(sc("DIFFERENTIATED", D, P, P, valid=False)), "INVALID")
        self.assertEqual(R.overall(sc("DIFFERENTIATED", D, P, P, rb="NO_DIFFERENCE_DETECTED")), "UNDETERMINED")


class TestPartialReading(unittest.TestCase):
    def test_partial_reading(self):
        def sc(rc, la, cl, valid=True, ra="DERIVED_AHEAD"):
            return {"valid": valid, "primary_at": 1, "points": {"1": {
                "P3B_0_gate": {"label": "PASS"}, "P3B_0_referent_A": {"label": ra}, "P3B_0_referent_C": {"label": rc},
                "P3B_A": {"label": la}, "secondary": {"C_low_PFATE_vs_PYOKED": {"label": cl}}}}}
        D, N = "DERIVED_AHEAD", "NO_DIFFERENCE_DETECTED"
        self.assertEqual(R.partial_reading(sc(N, "PRESENT", N)), "A_SIDE_SPECIFIC, NO_SPREAD")
        self.assertEqual(R.partial_reading(sc(N, "NOT_DETECTED", D)), "A_NOT_SIDE_SPECIFIC, MOOD_SPREAD")
        self.assertEqual(R.partial_reading(sc(D, "PRESENT", N)), "NOT_APPLICABLE")        # C referent formed
        self.assertEqual(R.partial_reading(sc(N, "PRESENT", N, ra=N)), "NOT_APPLICABLE")  # no memory referent


class TestSafety(unittest.TestCase):
    def test_no_operator_variables(self):
        names = " ".join(vars(world()).keys()).lower()
        for bad in ("operator", "shutdown", "stop", "host", "kill"):
            self.assertNotIn(bad, names)

    def test_seeds_disjoint(self):
        import run_p1c_selfover as C
        import run_p1d_confirm as D
        import run_p3_global as G
        used = set(C.FINAL_SEEDS + C.CALIB_SEEDS + D.FINAL_SEEDS + G.FINAL_SEEDS + G.CALIB_SEEDS)
        self.assertFalse(set(R.FINAL_SEEDS) & used)
        self.assertFalse(set(R.CALIB_SEEDS) & (used | set(R.FINAL_SEEDS)))
        self.assertEqual(len(R.FINAL_SEEDS), 28)


if __name__ == "__main__":
    unittest.main()
