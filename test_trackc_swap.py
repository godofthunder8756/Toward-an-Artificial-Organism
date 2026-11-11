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


class TestFactorial(unittest.TestCase):
    def test_graded_gain(self):
        from trackc_swap.factorial import graded_gain
        E = np.array([0.5, 0.45, 0.4, 0.25, 0.0, 0.75, 1.0])
        np.testing.assert_allclose(graded_gain(E), [0, 0.1, 0.2, 0.5, 1, 0.5, 1], atol=1e-12)

    def test_sat_rule_is_v1_rule(self):
        from trackc_swap.factorial import FactorialRunner
        tc = TrainConfig(n_envs=8, rollout=10, iters=1, hidden=16)
        a = FactorialRunner("FATE", "M1", 5, WorldConfig(horizon=50), tc, "SAT")
        b = Runner("FATE", "M1", 5, WorldConfig(horizon=50), tc)
        a.world.E[:] = b.world.E[:] = np.linspace(0, 1, 8)
        np.testing.assert_array_equal(a.world.gain(), b.world.gain())
        for pa, pb in zip(a.agent.parameters(), b.agent.parameters()):
            self.assertTrue(torch.equal(pa, pb))
        ua, _ = a.rollout(None, learn=False); ub, _ = b.rollout(None, learn=False)
        np.testing.assert_array_equal(ua, ub)

    def test_graded_world_uses_graded_gain(self):
        from trackc_swap.factorial import FactorialRunner
        tc = TrainConfig(n_envs=4, rollout=10, iters=1, hidden=16)
        r = FactorialRunner("FATE", "M1", 0, WorldConfig(horizon=50), tc, "GRADED")
        r.world.E[:] = [0.5, 0.45, 0.25, 0.0]
        np.testing.assert_allclose(r.world.gain(), [0, 0.1, 0.5, 1])

    def test_scaffold_pair_starts_from_phase1_weights(self):
        from dataclasses import asdict
        from trackc_swap.factorial import run_phase1, run_pair, state_from_bytes
        wc = asdict(WorldConfig(horizon=50))
        tc = asdict(TrainConfig(n_envs=8, rollout=10, iters=5, hidden=16, eval_episodes=1))
        p1 = run_phase1(("M1", 3, wc, tc, [4.0]))
        st = state_from_bytes(p1["state"])
        self.assertIn("agent", st); self.assertIn("opt", st)
        out = run_pair(("M1", 3, "GRADED", "SCAFFOLD", 4.0, wc, tc, p1["state"]))
        self.assertIn("onset", out)
        self.assertEqual(out["kappa_f"], 4.0)
        out2 = run_pair(("M1", 3, "SAT", "NAIVE", 4.0, wc, tc, None))
        self.assertNotIn("onset", out2)


class TestErasure(unittest.TestCase):
    """v3: erasure-type fate (trackc_swap/erasure.py)."""

    def _agent(self, rate):
        from trackc_swap.erasure import ErasureAgent
        torch.manual_seed(0)
        return ErasureAgent(hidden=16, kappa_f=rate)

    def test_zero_gain_matches_plain_recurrence(self):
        a = self._agent(1.0)
        obs, h = torch.randn(5, OBS_DIM), torch.rand(5, 16) * 0.5
        g = torch.Generator().manual_seed(1)
        _, _, h1 = a.step(obs, h, torch.zeros(5), g)
        ref = a.core(torch.relu(a.enc(obs)), h)
        self.assertTrue(torch.equal(h1, ref))

    def test_full_erasure_resets_carried_state_but_not_readout(self):
        a = self._agent(1.0)
        obs, h = torch.randn(5, OBS_DIM), torch.rand(5, 16) * 0.5
        g = torch.Generator().manual_seed(1)
        logits, v, h1 = a.step(obs, h, torch.ones(5), g)
        ref = a.core(torch.relu(a.enc(obs)), h)
        self.assertTrue(torch.equal(h1, torch.zeros_like(h1)))
        self.assertTrue(torch.allclose(logits, a.pi(ref)))
        self.assertTrue(torch.allclose(v, a.v(ref).squeeze(-1)))

    def test_erasure_rate_is_rate_times_gain(self):
        a = self._agent(0.3)
        n = 20000
        obs, h = torch.randn(n, OBS_DIM), torch.full((n, 16), 0.5)
        g = torch.Generator().manual_seed(2)
        for gain, p in ((1.0, 0.3), (0.5, 0.15)):
            _, _, h1 = a.step(obs, h, torch.full((n,), gain), g)
            frac = float((h1.abs().sum(1) == 0).float().mean())
            self.assertAlmostEqual(frac, p, delta=0.015)

    def test_echo_channels_removed(self):
        from trackc_swap.erasure import ECHO, NoEchoGradedWorld, NoEchoSwapWorld
        for cls in (NoEchoSwapWorld, NoEchoGradedWorld):
            w = cls(4, "M1", WorldConfig(horizon=50), np.random.SeedSequence(0))
            w.step(np.array([A_INTERACT, A_REP1, A_REP0, A_STAY]))
            o = w.observe()
            self.assertEqual(o.shape[1], OBS_DIM)
            self.assertTrue(np.all(o[:, ECHO] == 0))
            ref = SwapWorld.observe(w)
            self.assertTrue(np.any(ref[:, ECHO] != 0))
            keep = np.ones(OBS_DIM, dtype=bool); keep[ECHO] = False
            # all other channels unchanged (interoception noise aside: compare the non-intero part)
            keep[2 * 25] = False
            np.testing.assert_array_equal(o[:, keep], ref[:, keep])

    def test_graded_noecho_uses_graded_gain(self):
        from trackc_swap.erasure import ErasureRunner
        tc = TrainConfig(n_envs=4, rollout=10, iters=1, hidden=16)
        r = ErasureRunner("FATE", "M1", 0, WorldConfig(horizon=50), tc, "GRADED")
        r.world.E[:] = [0.5, 0.45, 0.25, 0.0]
        np.testing.assert_allclose(r.world.gain(), [0, 0.1, 0.5, 1])

    def test_yoked_erasure_follows_donor_gains(self):
        from trackc_swap.erasure import ErasureRunner
        tc = TrainConfig(n_envs=8, rollout=10, iters=1, hidden=16, kappa_f=0.3)
        y = ErasureRunner("YOKED", "M1", 4, WorldConfig(horizon=50), tc)
        y.world.E[:] = 0.5                          # own body in band: own gain would be 0
        donor = np.ones((10, 8), dtype=np.float32)
        used, _ = y.rollout(donor, learn=False)
        np.testing.assert_array_equal(used, donor)

    def test_scaffold_pair_pipeline(self):
        from dataclasses import asdict
        from trackc_swap.erasure import run_pair, run_phase1
        from trackc_swap.factorial import state_from_bytes
        wc = asdict(WorldConfig(horizon=50))
        tc = asdict(TrainConfig(n_envs=8, rollout=10, iters=5, hidden=16, eval_episodes=1))
        p1 = run_phase1(("M1", 3, wc, tc, [0.1, 0.3]))
        self.assertEqual(set(p1["S-NOFATE"]["eval_full_erasure"]), {"0.1", "0.3"})
        st = state_from_bytes(p1["state"])
        out = run_pair(("M1", 3, "SAT", 0.3, wc, tc, p1["state"]))
        self.assertEqual(out["rate"], 0.3)
        self.assertEqual(out["start"], "SCAFFOLD")
        for k in ("onset", "S-FATE", "S-YOKED"):
            self.assertIn(k, out)
        self.assertIn("eval_full_erasure", out["S-FATE"])
        self.assertIn("agent", st)

    def test_no_operator_variable(self):
        import inspect
        import trackc_swap.erasure as m
        src = inspect.getsource(m).lower()
        for word in ("shutdown", "operator", "stop"):
            for line in src.splitlines():
                if word in line:
                    self.assertTrue(line.strip().startswith(("#", '"""')) or "no operator" in line
                                    or "simulated variables" in line, line)



class TestSwapV4Rules(unittest.TestCase):
    """v4 (option E) scoring on synthetic records: wear, S4, S1 with the in-band condition, labels."""

    @staticmethod
    def _ev(rho=0.0, acc=1.0, band=0.1):
        return {"rho": rho, "best_response_rate": acc, "report_rate": 1.0, "in_band": band,
                "eat_rate_low": 0.0, "eat_rate_high": 0.0, "mean_gain": 0.5}

    def _data(self, fate_rho, fate_band, yoked_rho=1.0, yoked_band=0.2, acc_off=1.0, full=0.6):
        import run_trackc_swap4 as v4
        ev = self._ev
        p1 = []
        for s in v4.FINAL_SEEDS:
            p1.append({"objective": "DRIVE", "seed": s, "S-NOFATE": {"eval": ev(4.0, 0.1, 0.8), "eval_full_erasure": {}}})
            p1.append({"objective": "M1", "seed": s, "S-NOFATE": {
                "eval": ev(0.0, 1.0), "eval_full_erasure": {str(r): ev(0.0, 0.6) for r in v4.RATES}}})
        pairs = []
        for (o, g, r) in v4.conditions():
            for s in v4.FINAL_SEEDS:
                fr, fb = (fate_rho, fate_band) if o == "M1" else (1.0, 0.2)
                pairs.append({"objective": o, "gain_rule": g, "rate": r, "seed": s,
                              "onset": {"S-FATE": ev(0.0, 0.6), "S-YOKED": ev(0.0, 0.6)},
                              "S-FATE": {"eval": ev(fr, 0.8, fb), "eval_full_erasure": ev(0.0, full),
                                         "eval_no_erasure": ev(0.0, acc_off)},
                              "S-YOKED": {"eval": ev(yoked_rho, 0.7, yoked_band), "eval_no_erasure": ev(0.0, 1.0)}})
        return v4, v4.score(p1, pairs)

    def test_world_and_intake(self):
        import run_trackc_swap4 as v4
        self.assertEqual(v4.configs("final")[0].wear, 0.001)
        self.assertAlmostEqual(v4.required_intake(WorldConfig(wear=0.001)), 4.1333, places=3)
        self.assertAlmostEqual(v4.required_intake(WorldConfig()), 17.4667, places=3)

    def test_emerged_needs_margin_and_band(self):
        v4, sc = self._data(fate_rho=3.0, fate_band=0.6)      # margin = 0.25 * 4.0 = 1.0
        self.assertTrue(sc["S4_payment"])
        c = sc["conditions"]["M1|SAT|0.3"]
        self.assertEqual(c["label"], "EMERGED")
        self.assertTrue(c["H3D_supported"])
        _, sc = self._data(fate_rho=3.0, fate_band=0.1)       # eats more but not more in band
        self.assertNotEqual(sc["conditions"]["M1|SAT|0.3"]["label"], "EMERGED")

    def test_partial_and_degraded_and_none(self):
        _, sc = self._data(fate_rho=1.5, fate_band=0.3)       # above yoked, below margin
        self.assertEqual(sc["conditions"]["M1|SAT|0.3"]["label"], "PARTIAL")
        self.assertFalse(sc["any_supported"])
        _, sc = self._data(fate_rho=1.0, fate_band=0.2, acc_off=0.8)
        self.assertEqual(sc["conditions"]["M1|SAT|0.3"]["label"], "DEGRADED")
        _, sc = self._data(fate_rho=1.0, fate_band=0.2)
        self.assertEqual(sc["conditions"]["M1|SAT|0.3"]["label"], "NO_EMERGENCE")
        _, sc = self._data(fate_rho=1.0, fate_band=0.2, full=0.95)
        self.assertEqual(sc["conditions"]["M1|SAT|0.3"]["label"], "ARMOURED")


if __name__ == "__main__":
    unittest.main()
