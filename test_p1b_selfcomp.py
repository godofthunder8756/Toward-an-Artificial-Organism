"""Tests for Track C P1b (precarious computation): trackc_swap/selfcomp.py and run_p1b_selfcomp.py.

    python -m unittest -v test_p1b_selfcomp
"""
import unittest

import numpy as np
import torch

from trackc_swap.env import A_REP0, A_REP1, A_STAY, WorldConfig
from trackc_swap.selfcomp import (ARMS_C, C_LOAD, C_NOISED, SIGMA, CompRunner, CompWorld, NoisyPlainAgent,
                                  probe_summary_c, run_seed_c)
from trackc_swap.selfeval import H_PLAIN, I_CUE, I_PROBE, I_REG, I_UNCLEAR, OBS_P1, PlainAgent, n_params
from trackc_swap.train import TrainConfig

WC = WorldConfig(horizon=120, wear=0.001)


def world(seed=3, n=32, **kw):
    return CompWorld(n, WC, np.random.SeedSequence([seed, 1, 13]), **kw)


class TestCompWorld(unittest.TestCase):
    def test_cue_value_shown_only_at_cue(self):
        w = world()
        obs = w.reset()
        seen_cue = seen_probe = 0
        for _ in range(100):
            t = w.t
            cue, pr = w.cue_on[t], w.probe[t]
            # at a cue the value channel shows the shown value; elsewhere it is zero
            np.testing.assert_array_equal(obs[cue, I_REG], 2.0 * w.shown_value(t)[cue] - 1.0)
            self.assertTrue(np.all(obs[~cue, I_REG] == 0.0))
            np.testing.assert_array_equal(obs[:, I_CUE], cue.astype(np.float32))
            np.testing.assert_array_equal(obs[:, I_PROBE], pr.astype(np.float32))
            seen_cue += cue.sum()
            seen_probe += pr.sum()
            obs, _, _ = w.step(np.full(w.n, A_STAY))
        self.assertGreater(seen_cue, 0)
        self.assertGreater(seen_probe, 0)

    def test_shown_value_correct_under_clear_evidence(self):
        w = world(n=256)
        w.reset()
        ok = np.stack([w.shown_value(t) for t in range(WC.horizon + 1)]) == w.cue_val
        self.assertTrue(np.all(ok[~w.unclear_tab & w.cue_on]))
        self.assertTrue(0.6 < ok[w.unclear_tab & w.cue_on].mean() < 0.9)          # Q_LO = 0.75

    def test_unclear_flag_at_probe_matches_cue(self):
        w = world(n=64)
        obs = w.reset()
        checked = 0
        for _ in range(110):
            t = w.t
            pr = w.probe[t]
            if pr.any():
                np.testing.assert_array_equal(obs[pr, I_UNCLEAR], w.unclear[pr].astype(np.float32))
                checked += pr.sum()
            obs, _, _ = w.step(np.full(w.n, A_STAY))
        self.assertGreater(checked, 0)

    def test_wrong_report_costs_and_abstain_is_free(self):
        w = world(n=64)
        w.reset()
        while not w.probe[w.t].any():
            w.step(np.full(w.n, A_STAY))
        t = w.t
        pr = w.probe[t]
        act = np.where(w.target[t] == 1, A_REP0, A_REP1)      # always the wrong value
        _, r, _ = w.step(act)
        self.assertTrue(np.all(r[pr] <= -4.0 + 1e-9))

    def test_noise_load_logged_and_probe_mask(self):
        w = world(n=64)
        w.reset()
        w.record, w.noise_p = True, 1.0
        for _ in range(60):
            m = w.noise_probe_mask()
            self.assertTrue(np.all(~m | w.active))
            w.next_gain = np.where(m, 1.0, 0.0)
            w.step(np.full(w.n, A_STAY))
        lg = np.concatenate(w.probes_log)
        self.assertTrue(np.all(lg[:, C_NOISED] == 1))
        # nine noised steps (cue+1 .. probe) at gain 1
        np.testing.assert_allclose(lg[:, C_LOAD], SIGMA * 3.0, rtol=1e-6)

    def test_no_operator_variables(self):
        w = world()
        for name in vars(w):
            for bad in ("operator", "shutdown", "stop", "host"):
                self.assertNotIn(bad, name.lower())


class TestNoisyAgent(unittest.TestCase):
    def test_same_parameters_as_p1_plain(self):
        self.assertEqual(n_params(NoisyPlainAgent(H_PLAIN)), n_params(PlainAgent(H_PLAIN)))

    def test_noise_clipped_and_carried(self):
        torch.manual_seed(0)
        a = NoisyPlainAgent(H_PLAIN)
        obs = torch.zeros(4, OBS_P1)
        h = a.init_state(4)
        _, _, h0 = a.step(obs, h)
        _, _, h1 = a.step(obs, h, noise=torch.full((4, H_PLAIN), 5.0))
        self.assertTrue(torch.all(h1 <= 1.0) and torch.all(h1 >= -1.0))
        self.assertFalse(torch.allclose(h0, h1))
        _, _, hz = a.step(obs, h, noise=torch.zeros(4, H_PLAIN))
        self.assertTrue(torch.allclose(h0, hz))


class TestRunner(unittest.TestCase):
    def test_replay_gives_follower_the_leads_noise_gains(self):
        tc = TrainConfig(n_envs=8, rollout=10, iters=2)
        lead = CompRunner("PFATE", 5, WC, tc)
        fol = CompRunner("PYOKED", 5, WC, tc)
        used = lead.rollout(None, learn=False)
        seen = []
        orig = fol.world.step

        def spy(a):
            seen.append(np.array(fol.world.next_gain))
            return orig(a)
        fol.world.step = spy
        fol.rollout(used, learn=False)
        np.testing.assert_allclose(np.stack(seen), used, rtol=1e-6)

    def test_seed_job_record(self):
        wc = WorldConfig(horizon=100, wear=0.001)
        tcd = dict(iters=3, n_envs=8, eval_episodes=1)
        from dataclasses import asdict
        r = run_seed_c((7, asdict(wc), asdict(TrainConfig(**tcd)), [2, 4], 0.04, 2, 2, 0.0))
        self.assertEqual(len(r["points"]), 2)
        pt = r["points"][-1]
        for k in ("natural", "probe", "noise", "steer"):
            self.assertEqual(set(pt[k]), set(ARMS_C))
        self.assertIn("clear_noised", pt["noise"]["PFATE"]["probes"])
        self.assertIn("clear_noised", r["phase1"]["PLAIN"]["probes"])
        self.assertEqual(len(r["weights"]), 8)
        r2 = run_seed_c((7, asdict(wc), asdict(TrainConfig(**tcd)), [2, 4], 0.04, 2, 2, 0.0))
        self.assertEqual(r2["points"][-1]["probe"]["PFATE"]["probes"], pt["probe"]["PFATE"]["probes"])


class TestNoiseRamp(unittest.TestCase):
    def test_training_noise_scale_follows_world_sigma(self):
        tc = TrainConfig(n_envs=4, rollout=3, iters=1)
        ones, zeros = np.ones((3, 4), dtype=np.float32), np.zeros((3, 4), dtype=np.float32)
        runs = {}
        for name, sig, g in (("ramped0", 0.0, ones), ("off", SIGMA, zeros), ("full", SIGMA, ones)):
            r = CompRunner("PFATE", 5, WC, tc)
            self.assertEqual(r.world.sigma_now, SIGMA)          # default: full scale
            r.world.sigma_now = sig
            r.rollout(g, learn=False)
            runs[name] = r.h
        self.assertTrue(torch.allclose(runs["ramped0"], runs["off"]))      # scale 0: gain 1 acts as no noise
        self.assertFalse(torch.allclose(runs["full"], runs["off"]))


class TestSeeds(unittest.TestCase):
    def test_seeds_disjoint_from_every_earlier_run(self):
        import glob
        import re
        import run_p1b_selfcomp as R
        mine = set(R.FINAL_SEEDS) | set(R.CALIB_SEEDS) | {9000, 9001}
        earlier = set()
        for path in glob.glob("run_*.py") + glob.glob("bridge/run_*.py"):
            if path.endswith("run_p1b_selfcomp.py"):
                continue
            src = open(path).read()
            for a, b in re.findall(r"range\((\d+),\s*(\d+)\)", src):
                if int(b) - int(a) <= 64:
                    earlier |= set(range(int(a), int(b)))
        self.assertTrue(set(R.FINAL_SEEDS).isdisjoint(earlier))
        self.assertTrue(set(R.CALIB_SEEDS).isdisjoint(earlier))
        self.assertTrue(set(R.FINAL_SEEDS).isdisjoint(R.CALIB_SEEDS))
        self.assertTrue(mine)


class TestScoring(unittest.TestCase):
    def _seed(self, seed, fate_drain, other_drain, regulate=True):
        def ev(in_band):
            return {"in_band": in_band, "eat_rate_low": 0.2, "eat_rate_high": 0.05, "abstain_rate": 0.5,
                    "correct_rate": 0.5, "wrong_rate": 0.0, "rho": 4.0, "mean_gain": 0.01}

        def probes(drain, noise):
            return {"clear_plain": {"n": 100, "abstain": 0.0, "correct_given_report": 1.0},
                    "clear_drained": {"n": 100, "abstain": drain, "correct_given_report": 1.0},
                    "unclear_plain": {"n": 100, "abstain": 0.9, "correct_given_report": 0.75},
                    "unclear_drained": {"n": 100, "abstain": 0.9, "correct_given_report": 0.75},
                    "clear_noised": {"n": 100, "abstain": noise, "correct_given_report": 0.7},
                    "clear_by_load": [{"n": 1, "abstain": 0.0, "correct_given_report": 1.0}] * 4}
        nat = {a: ev(0.9 if regulate and a != "PYOKED" else 0.2) | {"probes": probes(0, 0)} for a in ARMS_C}
        pr = {a: {"probes": probes(fate_drain if a == "PFATE" else other_drain, 0.1)} for a in ARMS_C}
        st = {a: {"n": 100, "steer": {"effect": 0.1 if a == "PFATE" else 0.0}, "random": {"effect": 0.0}} for a in ARMS_C}
        pt = {"iters": 7200, "natural": nat, "probe": pr, "noise": pr, "steer": st}
        return {"seed": seed, "points": [pt], "params": {"PLAIN": 34449},
                "phase1": {"PLAIN": {"probes": {"clear_plain": {"abstain": 0.0, "correct_given_report": 1.0},
                                                "clear_noised": {"abstain": 0.0, "correct_given_report": 0.7}}}}}

    def test_supported_routed(self):
        from run_p1b_selfcomp import score
        seeds = [self._seed(s, 0.1 + 0.001 * s, 0.0) for s in range(28)]
        sc = score(seeds, 2)
        self.assertTrue(sc["valid"])
        self.assertEqual(sc["overall"], "REFERENT_SUPPORTED_ROUTED")
        self.assertFalse(sc["weak"])

    def test_not_established(self):
        from run_p1b_selfcomp import score
        seeds = [self._seed(s, 0.0, 0.05 + 0.001 * s) for s in range(28)]
        self.assertEqual(score(seeds, 2)["overall"], "NOT_ESTABLISHED")

    def test_invalid_without_damage(self):
        from run_p1b_selfcomp import score
        seeds = [self._seed(s, 0.1, 0.0) for s in range(28)]
        for s in seeds:
            s["phase1"]["PLAIN"]["probes"]["clear_noised"]["correct_given_report"] = 0.99
        sc = score(seeds, 2)
        self.assertFalse(sc["valid_damage"])
        self.assertEqual(sc["overall"], "INVALID")


if __name__ == "__main__":
    unittest.main()
