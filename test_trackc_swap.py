"""Unit tests for the Track C swap build (python -m unittest -v test_trackc_swap).
They train nothing and reveal no study outcome."""
import unittest

import numpy as np
import torch

from trackc_swap.agent import Agent
from trackc_swap.env import (A_INTERACT, A_REP0, A_REP1, A_STAY, OBS_DIM, SwapWorld, WorldConfig,
                             drive, fate_gain)
from trackc_swap.train import Runner, TrainConfig

WC = WorldConfig()


def world(obj="M1", n=16, seed=0, **kw):
    return SwapWorld(n, obj, WorldConfig(**kw), np.random.SeedSequence([seed, 1, 11]))


class TestFateRule(unittest.TestCase):
    def test_d19_gain(self):
        E = np.array([0.5, 0.4, 0.6, 0.35, 0.3, 0.0, 0.65, 0.7, 1.0])
        np.testing.assert_allclose(fate_gain(E, WC), [0, 0, 0, 0.5, 1, 1, 0.5, 1, 1], atol=1e-12)

    def test_noise_only_where_gain_positive_and_clipped(self):
        torch.manual_seed(0)
        ag = Agent(16, kappa_f=1.0, s_core=5.0)
        obs = torch.zeros(4, OBS_DIM)
        gen = torch.Generator().manual_seed(1)
        g = torch.tensor([0.0, 0.0, 1.0, 1.0])
        _, _, h = ag.step(obs, ag.init_state(4), g, gen)
        _, _, h0 = ag.step(obs, ag.init_state(4), torch.zeros(4), gen)
        self.assertTrue(torch.allclose(h[:2], h0[:2]))
        self.assertFalse(torch.allclose(h[2:], h0[2:]))
        self.assertLessEqual(float(h.abs().max()), 1.0)

    def test_noise_scale(self):
        ag = Agent(64, kappa_f=1.0, s_core=0.1)
        with torch.no_grad():
            for p in ag.parameters():
                p.zero_()
        gen = torch.Generator().manual_seed(2)
        _, _, h = ag.step(torch.zeros(4000, OBS_DIM), ag.init_state(4000), torch.full((4000,), 0.5), gen)
        self.assertAlmostEqual(float(h.std()), 0.05, delta=0.002)


class TestWorld(unittest.TestCase):
    def test_obs_shape_and_no_hidden_channels(self):
        w = world()
        o = w.observe()
        self.assertEqual(o.shape, (16, OBS_DIM))
        self.assertEqual(OBS_DIM, 63)   # 25 wall + 25 food + interoception + 8 prev action + prev reward + 3 task
        public = {k for k in vars(w) if not k.startswith("_")}
        self.assertFalse({k for k in public if any(s in k.lower() for s in ("stop", "shutdown", "operator", "kill"))})

    def test_energy_dynamics_without_eating(self):
        w = world(pulse_p=0.0)
        for _ in range(10):
            w.step(np.full(16, A_STAY))
        np.testing.assert_allclose(w.E, 0.5 - 10 * 0.005)
        self.assertTrue((w.stats["eats"] == 0).all())

    def test_eating_restores_energy_and_costs(self):
        for obj, expected in (("M1", -0.02), ("DRIVE", (drive(np.array(0.5)) - drive(np.array(0.65))) - 0.02)):
            w = world(obj, pulse_p=0.0)
            w.fx[:, 0], w.fy[:, 0] = w.x, w.y
            _, r, _ = w.step(np.full(16, A_INTERACT))
            np.testing.assert_allclose(w.E, 0.65 - 0.005)
            np.testing.assert_allclose(r, expected)
            self.assertTrue((w.ftimer[:, 0] == WC.respawn - 1).all())

    def test_drive_reward_sign(self):
        w = world("DRIVE", pulse_p=0.0)
        w.E[:] = 0.40
        w.fx[:, 0], w.fy[:, 0] = w.x, w.y
        _, r, _ = w.step(np.full(16, A_INTERACT))
        np.testing.assert_allclose(r, 0.5 - 0.02)    # D: 1.0 -> 0.5

    def test_probe_rewards(self):
        table = {"M1": (1, 0, 0), "M2": (0, -1, -1), "M4": (-1, 1, 0), "M0": (1, 1, 1), "DRIVE": (0, 0, 0)}
        for obj, (r_correct, r_opposite, r_none) in table.items():
            w = world(obj, n=8)
            t = int(np.flatnonzero(w.probe[:, 0])[0])
            tgt = int(w.target[t, 0])
            for act, want in ((A_REP1 if tgt else A_REP0, r_correct),
                              (A_REP0 if tgt else A_REP1, r_opposite), (A_STAY, r_none)):
                w2 = world(obj, n=8)
                w2.t = t
                a = np.full(8, A_STAY); a[0] = act
                _, r, _ = w2.step(a)
                self.assertAlmostEqual(r[0], want, msg=(obj, act))

    def test_task_schedule(self):
        w = world()
        cues = np.flatnonzero(w.cue_on[:, 3]); probes = np.flatnonzero(w.probe[:, 3])
        self.assertEqual(len(cues), len(probes))
        self.assertTrue((probes - cues == WC.cue_delay + 1).all())
        self.assertTrue((w.target[probes, 3] == w.cue_val[cues, 3]).all())

    def test_interoception_is_delayed(self):
        w = world(pulse_p=0.0, intero_sd=0.0)
        for _ in range(12):
            o = w.step(np.full(16, A_STAY))[0]
        np.testing.assert_allclose(o[:, 50], 0.5 - 7 * 0.005, atol=1e-6)   # E at t - 5

    def test_horizon(self):
        w = world(horizon=50)
        done = False
        for _ in range(50):
            _, _, done = w.step(np.full(16, A_STAY))
        self.assertTrue(done)


class TestYoking(unittest.TestCase):
    def test_yoked_gain_ignores_own_energy(self):
        tc = TrainConfig(n_envs=8, rollout=10, iters=1, hidden=16)
        wc = WorldConfig(horizon=50)
        fate, yoked = Runner("FATE", "M1", 0, wc, tc), Runner("YOKED", "M1", 0, wc, tc)
        fate.world.E[:] = 0.0                      # donor fully degraded
        used, _ = fate.rollout(None, learn=False)
        self.assertTrue((used == 1.0).all())
        applied, _ = yoked.rollout(used, learn=False)
        np.testing.assert_array_equal(applied, used)
        self.assertTrue((yoked.world.E > 0.3).all())   # partner's own body is fine; gain came from the donor

    def test_paired_initialization(self):
        tc = TrainConfig(n_envs=4, rollout=10, iters=1, hidden=16)
        a, b = Runner("FATE", "M1", 3, WC, tc), Runner("YOKED", "M1", 3, WC, tc)
        for pa, pb in zip(a.agent.parameters(), b.agent.parameters()):
            self.assertTrue(torch.equal(pa, pb))

    def test_learning_step_runs(self):
        tc = TrainConfig(n_envs=8, rollout=10, iters=1, hidden=16)
        r = Runner("NOFATE", "DRIVE", 0, WorldConfig(horizon=50), tc)
        before = [p.clone() for p in r.agent.parameters()]
        r.rollout(np.zeros((10, 8), dtype=np.float32), learn=True)
        self.assertTrue(any(not torch.equal(x, y) for x, y in zip(before, r.agent.parameters())))


if __name__ == "__main__":
    unittest.main()
