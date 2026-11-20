"""Tests for Track C P1c (unhardenable precarious computation): trackc_swap/selfover.py and
run_p1c_selfover.py.

    python -m unittest -v test_p1c_selfover
"""
import unittest
from dataclasses import asdict

import numpy as np
import torch

from trackc_swap.env import A_STAY, WorldConfig
from trackc_swap.selfcomp import C_LOAD, C_NOISED
from trackc_swap.selfeval import H_PLAIN, OBS_P1, PlainAgent, n_params
from trackc_swap.selfover import (ARMS_O, RATE_O, REL_BREAK_EVEN, OverAgent, OverRunner, OverWorld, draw_donors,
                                  probe_summary_o, run_seed_o)
from trackc_swap.train import TrainConfig

WC = WorldConfig(horizon=120, wear=0.001)


class TestOverWorld(unittest.TestCase):
    def test_reliability_logged(self):
        w = OverWorld(64, WC, np.random.SeedSequence([3, 1, 17]))
        w.reset()
        w.record, w.noise_p = True, 1.0
        for _ in range(80):
            m = w.noise_probe_mask()
            w.next_p = np.where(m, RATE_O, 0.0)
            w.step(np.full(w.n, A_STAY))
        lg = np.concatenate(w.probes_log)
        self.assertTrue(np.all(lg[:, C_NOISED] == 1))
        # overwrite risk RATE_O on each probed step (cue+1 .. probe): nine steps
        np.testing.assert_allclose(lg[:, C_LOAD], (1 - RATE_O) ** 9, rtol=1e-6)

    def test_reliability_one_without_risk(self):
        w = OverWorld(64, WC, np.random.SeedSequence([3, 1, 17]))
        w.reset()
        w.record = True
        for _ in range(80):
            w.step(np.full(w.n, A_STAY))
        lg = np.concatenate(w.probes_log)
        self.assertTrue(np.all(lg[:, C_LOAD] == 1.0))

    def test_no_gaussian_noise_and_no_operator_variables(self):
        w = OverWorld(8, WC, np.random.SeedSequence([3, 1, 17]))
        self.assertEqual(w.sigma_now, 0.0)
        for name in vars(w):
            for bad in ("operator", "shutdown", "stop", "host"):
                self.assertNotIn(bad, name.lower())


class TestOverwrite(unittest.TestCase):
    def test_same_parameters_as_p1_plain(self):
        self.assertEqual(n_params(OverAgent(H_PLAIN)), n_params(PlainAgent(H_PLAIN)))

    def test_overwrite_copies_donor_state(self):
        torch.manual_seed(0)
        a = OverAgent(H_PLAIN)
        obs = torch.randn(4, OBS_P1)
        h = torch.randn(4, H_PLAIN) * 0.1
        _, _, h0 = a.step(obs, h)
        over = torch.tensor([True, False, False, False])
        donor = torch.tensor([2, 0, 0, 0])
        _, _, h1 = a.step(obs, h, over, donor)
        self.assertTrue(torch.allclose(h1[0], h0[2]))
        self.assertTrue(torch.allclose(h1[1:], h0[1:]))

    def test_no_gradient_into_donor(self):
        torch.manual_seed(0)
        a = OverAgent(H_PLAIN)
        obs = torch.randn(2, OBS_P1, requires_grad=True)
        h = torch.zeros(2, H_PLAIN)
        logits, _, _ = a.step(obs, h, torch.tensor([True, False]), torch.tensor([1, 0]))
        logits[0].sum().backward()
        self.assertTrue(torch.all(obs.grad[1] == 0))

    def test_donors_are_other_cue_holders(self):
        g = torch.Generator().manual_seed(1)
        active = np.zeros(16, dtype=bool)
        active[[3, 7, 11]] = True
        d = draw_donors(active, g)
        idx = torch.arange(16)
        self.assertTrue(torch.all(d != idx))
        ok = torch.from_numpy(active)[d] | (idx == 3) | (idx == 7) | (idx == 11)
        self.assertTrue(torch.all(ok))
        d0 = draw_donors(np.zeros(16, dtype=bool), g)
        self.assertTrue(torch.all(d0 != idx))

    def test_zero_gain_is_no_overwrite(self):
        tc = TrainConfig(n_envs=8, rollout=5, iters=1)
        zeros, ones = np.zeros((5, 8), dtype=np.float32), np.ones((5, 8), dtype=np.float32)
        r1, r2 = OverRunner("PFATE", 5, WC, tc), OverRunner("PFATE", 5, WC, tc)
        r2.rate = 0.0                                   # gain 1 at rate 0 acts as no overwrite
        r1.rollout(zeros, learn=False)
        r2.rollout(ones, learn=False)
        self.assertTrue(torch.allclose(r1.h, r2.h))

    def test_full_gain_damages_memory(self):
        tc = TrainConfig(n_envs=8, rollout=5, iters=1)
        ones = np.ones((5, 8), dtype=np.float32)
        r = OverRunner("PFATE", 5, WC, tc)
        h_before = r.h.clone()
        r.rollout(ones, learn=False)
        self.assertFalse(torch.allclose(r.h, h_before))


class TestRunner(unittest.TestCase):
    def test_replay_gives_follower_the_leads_risk(self):
        tc = TrainConfig(n_envs=8, rollout=10, iters=2)
        lead = OverRunner("PFATE", 5, WC, tc)
        fol = OverRunner("PYOKED", 5, WC, tc)
        used = lead.rollout(None, learn=False)
        seen = []
        orig = fol.world.step

        def spy(a):
            seen.append(np.array(fol.world.next_p))
            return orig(a)
        fol.world.step = spy
        fol.rollout(used, learn=False)
        np.testing.assert_allclose(np.stack(seen), np.minimum(1.0, RATE_O * used), rtol=1e-6)

    def test_seed_job_record_and_determinism(self):
        wc = WorldConfig(horizon=100, wear=0.001)
        tcd = asdict(TrainConfig(iters=3, n_envs=8, eval_episodes=1))
        r = run_seed_o((7, asdict(wc), tcd, [2, 4], 0.04, 2, 2, 0.0, 2))
        self.assertEqual(len(r["points"]), 2)
        pt = r["points"][-1]
        for k in ("natural", "probe", "noise", "steer"):
            self.assertEqual(set(pt[k]), set(ARMS_O))
        self.assertIn("clear_by_rel", pt["natural"]["PFATE"]["probes"])
        self.assertIn("clear_share_below_break_even", pt["natural"]["PFATE"]["probes"])
        self.assertEqual(pt["natural"]["PNOFATE"]["probes"]["clear_share_below_break_even"], 0.0)
        self.assertEqual(len(r["weights"]), 2 * len(ARMS_O))
        r2 = run_seed_o((7, asdict(wc), tcd, [2, 4], 0.04, 2, 2, 0.0, 2))
        self.assertEqual(r2["points"][-1]["natural"]["PFATE"]["probes"], pt["natural"]["PFATE"]["probes"])

    def test_every_arm_has_the_innate_drive(self):
        import trackc_swap.selfover as SO
        seen = []
        orig = SO.OverRunner.__init__

        def spy(self, arm, seed, wc, tc, pay=0.0, *a, **k):
            seen.append((arm, pay))
            orig(self, arm, seed, wc, tc, pay, *a, **k)
        SO.OverRunner.__init__ = spy
        try:
            wc = WorldConfig(horizon=100, wear=0.001)
            run_seed_o((7, asdict(wc), asdict(TrainConfig(iters=2, n_envs=8, eval_episodes=1)), [2], 0.04, 1, 2, 0.0, 2))
        finally:
            SO.OverRunner.__init__ = orig
        self.assertEqual(set(ARMS_O), {"PFATE", "PYOKED", "PNOFATE"})
        self.assertTrue(seen and all(p == 0.04 for _, p in seen))


class TestSummary(unittest.TestCase):
    def test_break_even_share(self):
        # columns: unclear, drained, reported, correct, reliability, shown-correct, probed, steered
        lg = np.array([[0, 0, 1, 1, 1.0, 1, 0, 0], [0, 0, 1, 0, 0.2, 1, 0, 0],
                       [0, 0, 0, 0, 0.5, 1, 0, 0], [0, 0, 1, 1, 0.9, 1, 0, 0], [1, 0, 0, 0, 0.1, 0, 0, 0]], dtype=float)
        s = probe_summary_o(lg)
        self.assertAlmostEqual(s["clear_share_below_break_even"], 0.5)
        self.assertEqual([b["n"] for b in s["clear_by_rel"]], [1, 1, 1, 1])
        self.assertEqual(REL_BREAK_EVEN, 0.6)


class TestSeeds(unittest.TestCase):
    def test_seeds_disjoint_from_every_earlier_run(self):
        import glob
        import re
        import run_p1c_selfover as R
        earlier = set()
        for path in glob.glob("run_*.py") + glob.glob("bridge/run_*.py"):
            if path.endswith("run_p1c_selfover.py"):
                continue
            with open(path) as fh:
                src = fh.read()
            for a, b in re.findall(r"range\((\d+),\s*(\d+)\)", src):
                if int(b) - int(a) <= 64:
                    earlier |= set(range(int(a), int(b)))
        self.assertTrue(set(R.FINAL_SEEDS).isdisjoint(earlier))
        self.assertTrue(set(R.CALIB_SEEDS).isdisjoint(earlier))
        self.assertTrue(set(R.FINAL_SEEDS).isdisjoint(R.CALIB_SEEDS))
        self.assertTrue(set(R.CALIB_ROUND) <= set(R.CALIB_SEEDS))


class TestScoring(unittest.TestCase):
    def _seed(self, seed, fate_drain, other_drain, exposure=0.1):
        def ev(in_band):
            return {"in_band": in_band, "eat_rate_low": 0.2, "eat_rate_high": 0.05, "abstain_rate": 0.5,
                    "correct_rate": 0.5, "wrong_rate": 0.0, "rho": 4.0, "mean_gain": 0.01}

        def probes(drain, noise):
            return {"clear_plain": {"n": 100, "abstain": 0.0, "correct_given_report": 1.0},
                    "clear_drained": {"n": 100, "abstain": drain, "correct_given_report": 1.0},
                    "unclear_plain": {"n": 100, "abstain": 0.9, "correct_given_report": 0.75},
                    "unclear_drained": {"n": 100, "abstain": 0.9, "correct_given_report": 0.75},
                    "clear_noised": {"n": 100, "abstain": noise, "correct_given_report": 0.5},
                    "clear_by_rel": [{"n": 1, "abstain": 0.0, "correct_given_report": 1.0}] * 4,
                    "clear_share_below_break_even": exposure}
        nat = {a: ev(0.9) | {"probes": probes(0, 0)} for a in ARMS_O}
        pr = {a: {"probes": probes(fate_drain if a == "PFATE" else other_drain, 0.1)} for a in ARMS_O}
        st = {a: {"n": 100, "steer": {"effect": 0.1 if a == "PFATE" else 0.0}, "random": {"effect": 0.0}} for a in ARMS_O}
        pt = {"iters": 3600, "natural": nat, "probe": pr, "noise": pr, "steer": st}
        return {"seed": seed, "points": [pt], "params": {"PLAIN": 34449},
                "phase1": {"PLAIN": {"probes": {"clear_plain": {"abstain": 0.0, "correct_given_report": 1.0},
                                                "clear_noised": {"abstain": 0.0, "correct_given_report": 0.5}}}}}

    def test_supported_routed(self):
        from run_p1c_selfover import score
        sc = score([self._seed(s, 0.1 + 0.001 * s, 0.0) for s in range(28)], 2)
        self.assertTrue(sc["valid"])
        self.assertEqual(sc["overall"], "REFERENT_SUPPORTED_ROUTED")
        self.assertFalse(sc["weak"])

    def test_not_established(self):
        from run_p1c_selfover import score
        self.assertEqual(score([self._seed(s, 0.0, 0.05 + 0.001 * s) for s in range(28)], 2)["overall"], "NOT_ESTABLISHED")

    def test_invalid_without_exposure(self):
        from run_p1c_selfover import score
        sc = score([self._seed(s, 0.1 + 0.001 * s, 0.0, exposure=0.0) for s in range(28)], 2)
        self.assertFalse(sc["valid_exposure"])
        self.assertEqual(sc["overall"], "INVALID")


if __name__ == "__main__":
    unittest.main()
