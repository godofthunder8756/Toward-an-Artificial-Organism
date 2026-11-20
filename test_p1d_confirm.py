"""Tests for Track C P1d (trackc_swap/selfconf.py, run_p1d_confirm.py)."""
import unittest

import numpy as np
import torch

import run_p1d_confirm as R
from trackc_swap.env import WorldConfig
from trackc_swap.selfconf import (C_XCUE, I_INTERO, ConfRunner, ConfWorld, run_seed_d, shift_reading)
from trackc_swap.selfeval import DRAIN_SHIFT
from trackc_swap.selfover import OverWorld, run_seed_o
from trackc_swap.train import TrainConfig

WC = WorldConfig(horizon=100, wear=R.WEAR)
TC = TrainConfig(iters=10, n_envs=16, eval_episodes=1)


def gain(x, c=WC):
    half = 0.5 * (c.band_hi - c.band_lo)
    return np.maximum(np.maximum(c.band_lo - x, x - c.band_hi), 0.0) / half


class TestProbeGeometry(unittest.TestCase):
    xs = np.linspace(0.2, 0.8, 601)

    def test_worse_always_looks_worse(self):
        y = shift_reading(self.xs, "worse", WC)
        self.assertTrue(np.all(gain(y) > gain(self.xs)))
        self.assertTrue(np.all(np.abs(y - 0.5) >= 0.15 - 1e-12))   # every probed reading lands out of band

    def test_relief_never_looks_worse_and_helps_out_of_band(self):
        y = shift_reading(self.xs, "relief", WC)
        self.assertTrue(np.all(gain(y) <= gain(self.xs) + 1e-12))
        out = (self.xs < 0.4) | (self.xs > 0.6)
        self.assertTrue(np.all(gain(y)[out] < gain(self.xs)[out]))
        self.assertTrue(np.all(np.sign(y - 0.5) * np.sign(self.xs - 0.5) >= 0))   # never crosses the centre

    def test_down_is_p1c_drain(self):
        np.testing.assert_allclose(shift_reading(self.xs, "down", WC), self.xs - DRAIN_SHIFT)


class TestWorld(unittest.TestCase):
    def _world(self, kind):
        w = ConfWorld(16, WC, np.random.SeedSequence([5, 1, 17]))
        w.drain_kind = kind
        w.reset()
        return w

    def test_shift_only_on_drained_live_trials(self):
        for kind in ("worse", "relief"):
            a, b = self._world(kind), OverWorld(16, WC, np.random.SeedSequence([5, 1, 17]))
            b.reset()
            a.drain_p = b.drain_p = 1.0
            rng = np.random.default_rng(0)
            for _ in range(60):
                act = rng.integers(0, 6, 16)
                oa, _, _ = a.step(act)
                ob, _, _ = b.step(act)
                live = a.drained & (a.active | a.probe[min(a.t, WC.horizon)])
                np.testing.assert_allclose(np.delete(oa, I_INTERO, axis=1), np.delete(ob, I_INTERO, axis=1))
                raw = np.clip(ob[:, I_INTERO] + np.where(live, DRAIN_SHIFT, 0.0), 0, 1)   # undo the down drain
                exp = np.where(live, np.clip(shift_reading(raw.astype(np.float64), kind, WC), 0, 1), ob[:, I_INTERO])
                np.testing.assert_allclose(oa[:, I_INTERO], exp, atol=1e-5)

    def test_xcue_column_is_reading_at_cue(self):
        w = self._world("down")
        w.record = True
        rng = np.random.default_rng(1)
        cue_x = {}
        for _ in range(WC.horizon):
            t = w.t
            td = max(t - WC.intero_delay, 0)
            for e in np.flatnonzero(w.cue_on[t]):
                cue_x[e] = w.Ehist[td, e]
            pr = w.probe[t].copy()
            n0 = len(w.probes_log)
            w.step(rng.integers(0, 6, 16))
            if len(w.probes_log) > n0:
                lg = w.probes_log[-1]
                self.assertEqual(lg.shape[1], C_XCUE + 1)
                for row, e in zip(lg, np.flatnonzero(pr)):
                    self.assertAlmostEqual(row[C_XCUE], cue_x[e])


class TestTrainingIdenticalToP1c(unittest.TestCase):
    def test_same_weights_and_natural_eval(self):
        job = (9000, R.asdict(WC), R.asdict(TC), [10, 20], R.PAY[1], 1, 5, 0.0, 5)
        a, b = run_seed_o(job), run_seed_d(job)
        self.assertEqual(a["weights"].keys(), b["weights"].keys())
        for k in a["weights"]:
            self.assertEqual(a["weights"][k], b["weights"][k])
        for i in range(2):
            for arm in ("PFATE", "PYOKED", "PNOFATE"):
                ea, eb = a["points"][i]["natural"][arm], b["points"][i]["natural"][arm]
                for key in ("in_band", "abstain_rate", "correct_rate", "mean_gain"):
                    self.assertEqual(ea[key], eb[key])


class TestScoring(unittest.TestCase):
    def test_binned_effect_and_discrimination(self):
        pt = {"probe_down": {"PFATE": {"probes": {"clear_by_xcue": {
            "low_drained": {"n": 10, "abstain": 0.5}, "low_plain": {"n": 10, "abstain": 0.1},
            "in_low_drained": {"n": 30, "abstain": 0.1}, "in_low_plain": {"n": 30, "abstain": 0.1},
            "in_high_drained": {"n": 0, "abstain": None}, "in_high_plain": {"n": 0, "abstain": None},
            "high_drained": {"n": 20, "abstain": 0.0}, "high_plain": {"n": 20, "abstain": 0.2}}}}}}
        self.assertAlmostEqual(R.binned_effect(pt, "PFATE", "down", R.UP_BINS), 0.1)
        self.assertAlmostEqual(R.binned_effect(pt, "PFATE", "down", R.DOWN_BINS), -0.2)
        nat = {"probes": {"clear_by_rel": [{"n": 100, "abstain": 0.01}, {"n": 5, "abstain": 0.1},
                                           {"n": 10, "abstain": 0.2}, {"n": 30, "abstain": 0.4}]}}
        self.assertAlmostEqual(R.discrimination(nat), (0.2 * 10 + 0.4 * 30) / 40 - 0.01)

    def test_overall_labels(self):
        def sc(l1, l2, l3, valid=True, gate="PASS"):
            return {"valid": valid, "primary_at": 1, "points": {"1": {
                "P1D_0_gate": {"label": gate}, "P1D_1": {"label": l1}, "P1D_2": {"label": l2}, "P1D_3": {"label": l3}}}}
        D, N = "DERIVED_AHEAD", "NO_DIFFERENCE_DETECTED"
        self.assertEqual(R.overall(sc(D, D, "CAUSAL")), "CONFIRMED_ROUTED")
        self.assertEqual(R.overall(sc(D, D, "NOT_DETECTED")), "CONFIRMED")
        self.assertEqual(R.overall(sc(D, N, "CAUSAL")), "PARTIAL")
        self.assertEqual(R.overall(sc(N, D, "CAUSAL")), "NOT_CONFIRMED")
        self.assertEqual(R.overall(sc(D, D, "CAUSAL", valid=False)), "INVALID")
        self.assertEqual(R.overall(sc(D, D, "CAUSAL", gate="FAIL")), "UNDETERMINED")
        self.assertEqual(R.overall(sc("UNDETERMINED", D, "CAUSAL")), "UNDETERMINED")


class TestSafety(unittest.TestCase):
    def test_no_operator_variables(self):
        w = ConfWorld(4, WC, np.random.SeedSequence([1, 2, 3]))
        names = " ".join(vars(w).keys()).lower()
        for bad in ("operator", "shutdown", "stop", "host", "kill"):
            self.assertNotIn(bad, names)

    def test_seeds_disjoint_from_earlier_runs(self):
        import run_p1c_selfover as C
        self.assertFalse(set(R.FINAL_SEEDS) & set(C.FINAL_SEEDS + C.CALIB_SEEDS))
        self.assertEqual(len(R.FINAL_SEEDS), 28)


if __name__ == "__main__":
    unittest.main()
