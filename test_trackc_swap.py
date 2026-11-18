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
        TestSwapV4Rules._data.last = (p1, pairs)
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



class TestSwapV5(unittest.TestCase):
    """v5 (option G): longer phase 2 with checkpoints; yoked full-erasure evaluation; v4 rules unchanged."""

    def _tiny(self):
        from dataclasses import asdict
        from trackc_swap.erasure import run_phase1
        wc = asdict(WorldConfig(horizon=50, wear=0.001))
        tc = asdict(TrainConfig(n_envs=8, rollout=10, iters=5, hidden=16, eval_episodes=1))
        return wc, tc, run_phase1(("M1", 3, wc, tc, [0.1, 0.3]))

    def test_long_pair_matches_v4_pair_at_equal_budget(self):
        from trackc_swap.erasure import run_pair
        from trackc_swap.longrun import run_pair_long
        wc, tc, p1 = self._tiny()
        a = run_pair(("M1", 3, "GRADED", 0.3, wc, tc, p1["state"]))
        b = run_pair_long(("M1", 3, "GRADED", 0.3, wc, tc, p1["state"], 5, ()))
        self.assertEqual(a["onset"], b["onset"])
        for k in ("eval", "curve", "hidden_sd", "eval_full_erasure", "eval_no_erasure"):
            self.assertEqual(a["S-FATE"][k], b["S-FATE"][k], k)
        for k in ("eval", "curve", "hidden_sd"):
            self.assertEqual(a["S-YOKED"][k], b["S-YOKED"][k], k)
        self.assertIn("eval_full_erasure", b["S-YOKED"])
        self.assertEqual(b["checkpoints"], {})

    def test_long_pair_checkpoints(self):
        from trackc_swap.longrun import run_pair_long
        wc, tc, p1 = self._tiny()
        out = run_pair_long(("M1", 3, "SAT", 0.3, wc, tc, p1["state"], 15, (5, 10)))
        self.assertEqual(out["p2_iters"], 15)
        self.assertEqual(set(out["checkpoints"]), {"5", "10"})
        for ck in out["checkpoints"].values():
            for arm in ("S-FATE", "S-YOKED"):
                self.assertEqual(set(ck[arm]), {"eval", "hidden_sd", "eval_full_erasure", "eval_no_erasure"})
        self.assertEqual(len(out["S-FATE"]["curve"]), 15 * 10 // 50)
        self.assertEqual(out["S-YOKED"]["eval_full_erasure"]["mean_gain"], 1.0)
        with self.assertRaises(AssertionError):
            run_pair_long(("M1", 3, "SAT", 0.3, wc, tc, p1["state"], 15, (7,)))   # not an episode boundary

    def test_final_config(self):
        import run_trackc_swap5 as v5
        wc, tc, seeds, p2, cks = v5.configs("final")
        self.assertEqual(wc.wear, 0.001)
        self.assertEqual(tc.iters, 1200)
        self.assertEqual((p2, cks), (3600, (1200, 2400)))
        self.assertEqual(seeds, list(range(500, 509)))

    def test_rules_identical_to_v4(self):
        import run_trackc_swap4 as v4
        import run_trackc_swap5 as v5
        ev = TestSwapV4Rules._ev
        for args in [dict(fate_rho=3.0, fate_band=0.6), dict(fate_rho=1.5, fate_band=0.3),
                     dict(fate_rho=1.0, fate_band=0.2, acc_off=0.8), dict(fate_rho=1.0, fate_band=0.2, full=0.95),
                     dict(fate_rho=1.0, fate_band=0.2)]:
            _, sc4 = TestSwapV4Rules._data(TestSwapV4Rules(), **args)
            p1, pairs = TestSwapV4Rules._data.last
            for r in pairs:
                r["S-YOKED"]["eval_full_erasure"] = ev(0.0, 0.5)
                r["checkpoints"] = {"1200": {"S-FATE": {k: r["S-FATE"][k] for k in ("eval", "eval_full_erasure")},
                                             "S-YOKED": {k: r["S-YOKED"][k] for k in ("eval", "eval_full_erasure")}}}
            sc5 = v5.score(p1, pairs)
            for k, c in sc4["conditions"].items():
                self.assertEqual(c.get("label"), sc5["conditions"][k].get("label"), (args, k))
                self.assertEqual(c["H3D_supported"] if "H3D_supported" in c else None,
                                 sc5["conditions"][k].get("H3D_supported"), (args, k))
            c = sc5["conditions"]["M1|SAT|0.3"]
            self.assertAlmostEqual(c["checkpoints"]["1200"]["diff_median"], c["diff_median"])
            self.assertEqual(c["acc_yoked_full_erasure_median"], 0.5)

    def test_no_operator_variable(self):
        import inspect
        import trackc_swap.longrun as m
        src = inspect.getsource(m).lower()
        for word in ("shutdown", "operator", "stop"):
            for line in src.splitlines():
                if word in line:
                    self.assertTrue("no operator" in line, line)



class TestSwapV6(unittest.TestCase):
    """v6 (option J): saved-weight pair equals v5's pair; regulator criterion; confirmation rules."""

    def test_saved_pair_matches_long_pair(self):
        from trackc_swap.confirm import run_pair_saved
        from trackc_swap.factorial import state_from_bytes
        from trackc_swap.longrun import run_pair_long
        wc, tc, p1 = TestSwapV5._tiny(TestSwapV5())
        job = ("M1", 3, "SAT", 0.3, wc, tc, p1["state"], 15, (5, 10))
        a = run_pair_long(job)
        b = run_pair_saved(job)
        w = b.pop("weights")
        a.pop("seconds"), b.pop("seconds")
        self.assertEqual(a, b)
        f, y = state_from_bytes(w["FATE"]), state_from_bytes(w["YOKED"])
        self.assertEqual(set(f), set(y))
        self.assertTrue(any(not torch.equal(f[k], y[k]) for k in f))     # the two arms trained apart

    @staticmethod
    def _ev(band, low, high, rho=1.0, acc=1.0, full=0.6):
        return {"rho": rho, "best_response_rate": acc, "report_rate": 1.0, "in_band": band,
                "eat_rate_low": low, "eat_rate_high": high, "mean_gain": 0.3}

    def test_regulator_criterion(self):
        import run_trackc_swap6 as v6
        ev = self._ev
        self.assertTrue(v6.is_regulator(ev(0.8, 0.01, 0.002), ev(0.4, 0.004, 0.004)))
        self.assertFalse(v6.is_regulator(ev(0.55, 0.01, 0.002), ev(0.3, 0.004, 0.004)))   # band too low
        self.assertFalse(v6.is_regulator(ev(0.8, 0.01, 0.006), ev(0.4, 0.004, 0.004)))    # not timed to need
        self.assertFalse(v6.is_regulator(ev(0.8, 0.01, 0.002), ev(0.7, 0.004, 0.004)))    # partner as good
        self.assertTrue(v6.is_regulator(ev(0.8, 0.01, 0.0), ev(0.4, 0.0, 0.0)))           # never eats in band

    def _data(self, n_reg, n_band=18, m0_reg=0, yoked_reg=0):
        import run_trackc_swap6 as v6
        ev = self._ev
        p1 = []
        for s in v6.FINAL_SEEDS:
            p1.append({"objective": "DRIVE", "seed": s, "S-NOFATE": {"eval": ev(0.8, 0.01, 0.001, rho=4.0, acc=0.1)}})
            p1.append({"objective": "M1", "seed": s, "S-NOFATE": {
                "eval": ev(0.17, 0, 0, rho=0.0), "eval_full_erasure": {str(v6.RATE): ev(0.17, 0, 0, acc=0.5)}}})
        pairs = []
        for o in ("M1", "M0"):
            for i, s in enumerate(v6.FINAL_SEEDS):
                if o == "M1":
                    f = ev(0.8, 0.01, 0.002) if i < n_reg else ev(0.40 if i < n_band else 0.30, 0.004, 0.004)
                    y = ev(0.35, 0.004, 0.004)
                    if i >= 18 - yoked_reg:
                        f, y = ev(0.35, 0.004, 0.004), ev(0.8, 0.01, 0.002)
                else:
                    f = ev(0.8, 0.01, 0.002) if i < m0_reg else ev(0.25, 0.002, 0.002)
                    y = ev(0.25, 0.002, 0.002)
                ck = {"1200": {"S-FATE": {"eval": f}, "S-YOKED": {"eval": y}}}
                pairs.append({"objective": o, "seed": s, "onset": {"S-FATE": f, "S-YOKED": y}, "checkpoints": ck,
                              "S-FATE": {"eval": f, "eval_full_erasure": ev(0.3, 0, 0, acc=0.9 - 0.4 * f["in_band"]),
                                         "eval_no_erasure": ev(0.3, 0, 0)},
                              "S-YOKED": {"eval": y, "eval_full_erasure": ev(0.3, 0, 0, acc=0.8),
                                          "eval_no_erasure": ev(0.3, 0, 0)}})
        return v6.score(p1, pairs)

    def test_confirmation_rules(self):
        sc = self._data(n_reg=6)
        self.assertEqual(sc["verdict"], "CONFIRMED", sc["failed"])
        self.assertTrue(sc["tradeoff_replicated"])
        self.assertEqual(sc["cells"]["M1"]["checkpoints"]["1200"]["regulators_fate"], 6)
        self.assertEqual(self._data(n_reg=5)["failed"], ["C1_regulators"])
        self.assertEqual(self._data(n_reg=6, n_band=12)["failed"], ["C2_in_band_sign"])
        self.assertEqual(self._data(n_reg=6, m0_reg=2)["failed"], ["C3_M0_specificity"])
        self.assertIn("C4_yoked_control", self._data(n_reg=6, yoked_reg=2)["failed"])

    def test_final_config_and_spearman(self):
        import run_trackc_swap6 as v6
        wc, tc, seeds, p2, cks = v6.configs("final")
        self.assertEqual((wc.wear, tc.iters, p2, cks), (0.001, 1200, 3600, (1200, 2400)))
        self.assertEqual(seeds, list(range(600, 618)))
        self.assertEqual((v6.GAIN, v6.RATE), ("SAT", 0.3))
        self.assertAlmostEqual(v6.spearman([1, 2, 3, 4], [4, 3, 2, 1]), -1.0)
        self.assertAlmostEqual(v6.spearman([1, 2, 2, 3], [1, 2, 2, 3]), 1.0)

    def test_no_operator_variable(self):
        import inspect
        import trackc_swap.confirm as m
        for word in ("shutdown", "operator", "stop"):
            for line in inspect.getsource(m).lower().splitlines():
                if word in line:
                    self.assertTrue("no operator" in line, line)



class TestBypassDiag(unittest.TestCase):
    """Option K step 1: bypass diagnosis on saved weights (no training)."""

    def test_groups_match_observation_layout(self):
        from trackc_swap.bypass import GROUPS
        from trackc_swap.erasure import ECHO
        w = world()
        o = w.observe()
        self.assertEqual(GROUPS["intero"], [50])
        np.testing.assert_allclose(o[:, 50], np.clip(w.Ehist[0], 0, 1), atol=0.1)
        self.assertEqual(len(GROUPS["view"]), 50)
        self.assertEqual(set(GROUPS["all"]) & set(range(ECHO.start, ECHO.stop)), set())
        self.assertEqual(max(GROUPS["all"]), 50)

    def test_cell_decoder(self):
        from trackc_swap.bypass import cell_decoder_accuracy
        rng = np.random.default_rng(0)
        t = rng.integers(0, 2, 4000)
        self.assertAlmostEqual(cell_decoder_accuracy(t * 10 + rng.integers(0, 3, 4000), t, 7), 1.0)
        self.assertAlmostEqual(cell_decoder_accuracy(rng.integers(0, 49, 4000), t, 7), 0.5, delta=0.05)

    def test_condition_deterministic_and_shuffle_runs(self):
        from trackc_swap.bypass import run_condition
        from trackc_swap.erasure import ErasureAgent
        torch.manual_seed(0)
        sd = ErasureAgent(64, 1.0, 0.15).state_dict()
        wc = WorldConfig(wear=0.001, horizon=60)
        a = run_condition(sd, 5, wc, 8, 1, 0.3, "view", 3)
        b = run_condition(sd, 5, wc, 8, 1, 0.3, "view", 3)
        self.assertEqual(a, b)
        r = run_condition(sd, 5, wc, 8, 1, 1.0, None, 3, record=True)
        self.assertEqual(len(r["cells"]), len(r["targets"]))

    def test_carry_and_identification_rules(self):
        import run_trackc_bypass_diag as d
        sh = lambda **kw: {g: kw.get(g, 0.95) for g in ("walls", "food", "intero", "view", "all")}
        self.assertIsNone(d.carries({"acc": 0.6, "shuffled": sh()}))
        c = d.carries({"acc": 0.95, "shuffled": sh(walls=0.72, view=0.5, all=0.5)})
        self.assertEqual({k for k, v in c.items() if v}, {"walls", "view", "all"})
        self.assertFalse(d.carries({"acc": 0.95, "shuffled": sh(walls=0.74)})["walls"])

        def agent(group, seed, mem, walls):
            cond = {"acc": 0.95, "shuffled": sh(walls=walls, view=0.5, all=0.5), "in_band": 0.3}
            return {"arm": "FATE", "seed": seed, "group": group, "intact": {"acc": 1.0, "in_band": 0.3},
                    "full": cond, "memoryless": dict(cond, acc=mem, cell_decoder=0.9, intero_by_target=[0.4, 0.4])}
        ags = [agent("bypass_fate", s, 0.9, 0.55) for s in range(9)] + [agent("bypass_fate", 9, 0.9, 0.95),
                                                                        agent("regulator_fate", 10, 0.5, 0.95)]
        self.assertEqual(d.score(ags, None)["identified"], "walls")
        ags[0]["memoryless"]["acc"] = ags[1]["memoryless"]["acc"] = 0.6
        self.assertEqual(d.score(ags, None)["verdict"], "NOT_IDENTIFIED")

    def test_no_operator_variable(self):
        import inspect
        import trackc_swap.bypass as m
        for word in ("shutdown", "operator", "stop"):
            for line in inspect.getsource(m).lower().splitlines():
                if word in line:
                    self.assertTrue("no operator" in line, line)



class TestSwapV7(unittest.TestCase):
    """v7 (option K step 2): erasure also relocates the agent."""

    def test_phase1_training_identical_to_v6_world(self):
        from trackc_swap.erasure import run_phase1
        from trackc_swap.factorial import state_from_bytes
        from trackc_swap.relocate import run_phase1_reloc
        from dataclasses import asdict
        wcd = asdict(WorldConfig(horizon=100, wear=0.001))
        tcd = asdict(TrainConfig(iters=6, n_envs=8, eval_episodes=1))
        a = run_phase1(("M1", 4, wcd, tcd, [0.3]))
        b = run_phase1_reloc(("M1", 4, wcd, tcd, [0.3]))
        sa, sb = state_from_bytes(a["state"])["agent"], state_from_bytes(b["state"])["agent"]
        self.assertTrue(all(torch.equal(sa[k], sb[k]) for k in sa))
        self.assertEqual(a["S-NOFATE"]["eval"], b["S-NOFATE"]["eval"])     # erasure off: same world
        self.assertEqual(b["relocations_phase1_training"], 0)

    def test_relocates_exactly_the_erased_envs(self):
        from trackc_swap.erasure import ErasureRunner
        from trackc_swap.relocate import RelocRunner
        wc, tc = WorldConfig(wear=0.001), TrainConfig(n_envs=64, rollout=1, kappa_f=1.0)
        a, b = RelocRunner("FATE", "M1", 7, wc, tc), ErasureRunner("FATE", "M1", 7, wc, tc)
        g = np.zeros((1, 64), dtype=np.float32)
        g[0, ::2] = 1.0                                   # p = 1 in even envs, 0 in odd envs
        a.rollout(g, learn=False)
        b.rollout(g, learn=False)
        self.assertEqual(a.world.relocations, 32)
        np.testing.assert_array_equal(a.world.x[1::2], b.world.x[1::2])
        np.testing.assert_array_equal(a.world.y[1::2], b.world.y[1::2])
        moved = (a.world.x[::2] != b.world.x[::2]) | (a.world.y[::2] != b.world.y[::2])
        self.assertGreater(moved.mean(), 0.7)             # 48/49 chance per env of landing elsewhere

    def test_pair_record(self):
        from trackc_swap.confirm import run_pair_saved
        from trackc_swap.relocate import run_pair_reloc
        wc, tc, p1 = TestSwapV5._tiny(TestSwapV5())
        job = ("M1", 3, "SAT", 0.3, wc, tc, p1["state"], 15, (5, 10))
        a, b = run_pair_saved(job), run_pair_reloc(job)
        self.assertEqual(set(b) - set(a), {"relocate", "relocations_before_final"})
        self.assertEqual(set(b["checkpoints"]), {"5", "10"})

    def _data(self, regs=None, closed=True, m0_reg=0, yoked_reg=0):
        import run_trackc_swap7 as v7
        regs = regs or {}
        ev = TestSwapV6._ev
        p1 = []
        for s in v7.FINAL_SEEDS:
            p1.append({"objective": "DRIVE", "seed": s, "S-NOFATE": {"eval": ev(0.8, 0.01, 0.001, rho=4.0, acc=0.1)}})
            p1.append({"objective": "M1", "seed": s, "S-NOFATE": {
                "eval": ev(0.17, 0, 0, rho=0.0),
                "eval_full_erasure": {str(r): ev(0.17, 0, 0, acc=0.5) for r in v7.RATES}}})
        pairs = []
        for (o, g, rate) in v7.conditions():
            n = regs.get(v7.ckey(o, g, rate), m0_reg if o == "M0" else 0)
            for i, s in enumerate(v7.FINAL_SEEDS):
                f = ev(0.8, 0.01, 0.002) if i < n else ev(0.35, 0.004, 0.004)
                y = ev(0.35, 0.004, 0.004)
                if o == "M1" and i >= 9 - yoked_reg:
                    f, y = ev(0.35, 0.004, 0.004), ev(0.8, 0.01, 0.002)
                fe = 0.52 if closed else 0.95
                pairs.append({"objective": o, "gain_rule": g, "rate": rate, "seed": s,
                              "onset": {"S-FATE": f, "S-YOKED": y},
                              "checkpoints": {"1200": {"S-FATE": {"eval": f, "eval_full_erasure": ev(0.3, 0, 0, acc=fe)},
                                                       "S-YOKED": {"eval": y}}},
                              "S-FATE": {"eval": f, "eval_full_erasure": ev(0.3, 0, 0, acc=fe),
                                         "eval_no_erasure": ev(0.3, 0, 0)},
                              "S-YOKED": {"eval": y, "eval_full_erasure": ev(0.3, 0, 0, acc=fe),
                                          "eval_no_erasure": ev(0.3, 0, 0)}})
        return v7.score(p1, pairs)

    def test_decision_rules(self):
        sc = self._data({"M1 SAT 0.3": 7, "M1 SAT 0.1": 5, "M1 GRADED 0.3": 4})
        self.assertTrue(sc["K1_supported"], sc["K1_failed"])
        lab = {k: v["label"] for k, v in sc["labels"].items()}
        self.assertEqual(lab, {"M1 SAT 0.1": "EMERGES_PROVISIONAL", "M1 GRADED 0.1": "NOT_EMERGED",
                               "M1 SAT 0.3": "EMERGES", "M1 GRADED 0.3": "NOT_EMERGED"})
        self.assertEqual(self._data({"M1 SAT 0.3": 6})["K1_failed"], ["regulators"])
        self.assertEqual(self._data({"M1 SAT 0.3": 7}, closed=False)["labels"]["M1 SAT 0.3"]["label"], "BYPASS_OPEN")
        sc = self._data({"M1 SAT 0.3": 7}, m0_reg=2)
        self.assertEqual((sc["labels"]["M1 SAT 0.3"]["label"], sc["K1_failed"]), ("CONTROL_FAILS", ["specificity"]))
        self.assertIn("yoked_ok", self._data({"M1 SAT 0.3": 7}, yoked_reg=2)["K1_failed"])

    def test_final_config(self):
        import run_trackc_swap6 as v6
        import run_trackc_swap7 as v7
        wc, tc, seeds, p2, cks = v7.configs("final")
        self.assertEqual((wc.wear, tc.iters, p2, cks), (0.001, 1200, 3600, (1200, 2400)))
        self.assertEqual(seeds, list(range(700, 709)))
        self.assertEqual((v7.BAND_MIN, v7.TIMING_RATIO, v7.BAND_LEAD), (v6.BAND_MIN, v6.TIMING_RATIO, v6.BAND_LEAD))
        self.assertEqual(len(v7.conditions()), 6)

    def test_no_operator_variable(self):
        import inspect
        import trackc_swap.relocate as m
        for word in ("shutdown", "operator", "stop"):
            for line in inspect.getsource(m).lower().splitlines():
                if word in line:
                    self.assertTrue("no operator" in line, line)


class TestSwapV8(unittest.TestCase):
    """v8 (option M): confirmation with a rate-matched bypass check and M0 controls at every M1 cell."""

    FLOOR = {0.1: 0.69, 0.3: 0.52}

    def _data(self, regs=None, excess=0.0, m0_reg=0, yoked_reg=0, excess_cells=None):
        import run_trackc_swap8 as v8
        regs = regs or {}
        ev = TestSwapV6._ev
        p1 = []
        for s in v8.FINAL_SEEDS:
            p1.append({"objective": "DRIVE", "seed": s, "S-NOFATE": {"eval": ev(0.8, 0.01, 0.001, rho=4.0, acc=0.1)}})
            p1.append({"objective": "M1", "seed": s, "S-NOFATE": {
                "eval": ev(0.17, 0, 0, rho=0.0),
                "eval_full_erasure": {str(r): ev(0.17, 0, 0, acc=self.FLOOR[r]) for r in v8.RATES}}})
        pairs = []
        for (o, g, rate) in v8.conditions():
            k = v8.ckey(o, g, rate)
            n = regs.get(k, m0_reg if o == "M0" else 0)
            for i, s in enumerate(v8.FINAL_SEEDS):
                f = ev(0.8, 0.01, 0.002) if i < n else ev(0.35, 0.004, 0.004)
                y = ev(0.35, 0.004, 0.004)
                if o == "M1" and i >= 9 - yoked_reg:
                    f, y = ev(0.35, 0.004, 0.004), ev(0.8, 0.01, 0.002)
                fe = self.FLOOR[rate] + (excess if excess_cells is None or k in excess_cells else 0.0)
                pairs.append({"objective": o, "gain_rule": g, "rate": rate, "seed": s,
                              "onset": {"S-FATE": f, "S-YOKED": y},
                              "checkpoints": {"1200": {"S-FATE": {"eval": f, "eval_full_erasure": ev(0.3, 0, 0, acc=fe)},
                                                       "S-YOKED": {"eval": y}}},
                              "S-FATE": {"eval": f, "eval_full_erasure": ev(0.3, 0, 0, acc=fe),
                                         "eval_no_erasure": ev(0.3, 0, 0)},
                              "S-YOKED": {"eval": y, "eval_full_erasure": ev(0.3, 0, 0, acc=fe),
                                          "eval_no_erasure": ev(0.3, 0, 0)}})
        return v8.score(p1, pairs)

    def test_rate_matched_bypass_check(self):
        # v7's error: at r = 0.1 the internal-memory floor (0.69) is above v7's fixed 0.65 threshold
        sc = self._data({"M1 SAT 0.1": 6, "M1 GRADED 0.3": 6})
        self.assertEqual(sc["claims"], {"MA": True, "MB": True})
        self.assertAlmostEqual(sc["cells"]["M1 SAT 0.1"]["bypass_excess_median"], 0.0)
        sc = self._data({"M1 SAT 0.1": 6, "M1 GRADED 0.3": 6}, excess=0.11, excess_cells={"M1 SAT 0.1"})
        self.assertEqual(sc["labels"]["M1 SAT 0.1"]["label"], "BYPASS_OPEN")
        self.assertEqual(sc["cells"]["M1 SAT 0.1"]["seeds_bypass_excess"], 9)
        self.assertEqual(sc["claims"], {"MA": False, "MB": True})
        sc = self._data({"M1 SAT 0.1": 6}, excess=0.10)          # boundary: closed
        self.assertTrue(sc["labels"]["M1 SAT 0.1"]["closed"])

    def test_decision_rules(self):
        lab = lambda sc: {k: v["label"] for k, v in sc["labels"].items()}
        self.assertEqual(lab(self._data({"M1 SAT 0.1": 6, "M1 GRADED 0.3": 5})),
                         {"M1 SAT 0.1": "CONFIRMED", "M1 GRADED 0.1": "NOT_CONFIRMED", "M1 GRADED 0.3": "NOT_CONFIRMED"})
        sc = self._data({"M1 SAT 0.1": 9, "M1 GRADED 0.3": 9, "M0 SAT 0.1": 2})
        self.assertEqual(lab(sc)["M1 SAT 0.1"], "CONTROL_FAILS")
        self.assertEqual(lab(sc)["M1 GRADED 0.3"], "CONFIRMED")     # M0 control matched by gain and rate
        self.assertEqual(lab(self._data({"M1 GRADED 0.3": 9}, yoked_reg=2))["M1 GRADED 0.3"], "CONTROL_FAILS")
        self.assertEqual(self._data({"M1 SAT 0.1": 9}, m0_reg=1)["claims"]["MA"], True)

    def test_final_config(self):
        import run_trackc_swap6 as v6
        import run_trackc_swap7 as v7
        import run_trackc_swap8 as v8
        wc, tc, seeds, p2, cks = v8.configs("final")
        self.assertEqual((wc.wear, tc.iters, p2, cks), (0.001, 1200, 3600, (1200, 2400)))
        self.assertEqual(seeds, list(range(800, 809)))
        self.assertTrue(set(seeds).isdisjoint(v7.FINAL_SEEDS) and set(seeds).isdisjoint(v6.FINAL_SEEDS))
        self.assertEqual((v7.BAND_MIN, v7.TIMING_RATIO, v7.BAND_LEAD), (v6.BAND_MIN, v6.TIMING_RATIO, v6.BAND_LEAD))
        self.assertEqual((v8.MARGIN_FRAC, v8.PAID_FLOOR, v8.LOAD_DROP, v8.LEARNED),
                         (v7.MARGIN_FRAC, v7.PAID_FLOOR, v7.LOAD_DROP, v7.LEARNED))
        self.assertEqual(len(v8.conditions()), 6)
        self.assertEqual({(g, r) for o, g, r in v8.conditions() if o == "M0"},
                         {(g, r) for o, g, r in v8.conditions() if o == "M1"})


class TestProbe(unittest.TestCase):
    """Option P: probe of how saved agents represent and use E (no training)."""

    @staticmethod
    def _agent(seed=0):
        from trackc_swap.erasure import ErasureAgent
        torch.manual_seed(seed)
        return ErasureAgent(64, 1.0, 0.15).state_dict()

    def test_ridge_cross_validated(self):
        from trackc_swap.probe import ridge_r2
        rng = np.random.default_rng(0)
        X = rng.normal(size=(4000, 8))
        env = np.repeat(np.arange(40), 100)
        r2, _ = ridge_r2(X, X @ np.arange(1, 9) + 0.01 * rng.normal(size=4000), env)
        self.assertGreater(r2, 0.999)
        r2, _ = ridge_r2(X, rng.normal(size=4000), env)
        self.assertLess(r2, 0.01)

    def test_recorded_targets(self):
        from trackc_swap.probe import run_agent
        wc = WorldConfig(horizon=200, wear=0.001)
        out = run_agent(self._agent(), "M1", 5, wc, 32, 1, False, True)
        H, E, D, I, A = out["_rec"]
        self.assertEqual(H.shape, (1, 200, 32, 64))
        np.testing.assert_allclose(D[0, 10:], E[0, 10:] - E[0, 5:-5])
        # interoception reports E five steps back, with noise sd 0.02
        self.assertLess(np.abs(I[0, 10:] - E[0, 5:-5]).mean(), 0.03)
        # an eating event shows as a jump of one bolus (less wear and any pulse), unless E was capped at 1
        jumps = (E[0, 1:] - E[0, :-1])[A[0, 1:] == 1]
        self.assertGreater(jumps.size, 0)
        self.assertTrue(np.all(jumps > 0.08))
        # every eat is recorded at the next step, except eats on the final step
        self.assertTrue(A[0].sum() <= out["eats"] <= A[0].sum() + 32)

    def test_deterministic_and_shuffle_changes_only_intero(self):
        from trackc_swap.probe import run_agent
        wc = WorldConfig(horizon=100, wear=0.001)
        sd = self._agent(1)
        a = run_agent(sd, "M1", 3, wc, 16, 1, False, False)
        b = run_agent(sd, "M1", 3, wc, 16, 1, False, False)
        self.assertEqual(a, b)
        # zeroing the intero weights makes the shuffle invisible to the agent
        sd0 = {k: v.clone() for k, v in sd.items()}
        sd0["enc.weight"][:, 50] = 0.0
        self.assertEqual(run_agent(sd0, "M1", 3, wc, 16, 1, False, False),
                         run_agent(sd0, "M1", 3, wc, 16, 1, True, False))

    def test_decision_rules(self):
        import run_trackc_probe as P
        def rec(i, arm, ret, ant, band_shuf, band=0.8):
            grp = "REG" if arm == "FATE" else "YREG"
            other = "YOKED" if arm == "FATE" else "FATE"
            b = {"in_band": band, "eat_rate_low": 0.01, "eat_rate_high": 0.002, "eats": 50.0}
            s = dict(b, in_band=band_shuf)
            return {"id": f"{i} {arm}", "partner": f"{i} {other}", "group": grp, "r2_E_h": 0.8 * ret,
                    "r2_E_raw": 0.8, "r2_E_win": 0.9, "gain_E": -1.0, "r2_D_h": 0.5 * ant, "r2_D_win": 0.5,
                    "E_sd": 0.1, "intact": b, "shuffled": s}
        recs = []
        for i in range(40):
            ahead = i < 28                                     # 28/40 = 0.70
            recs.append(rec(i, "FATE", 0.9 if ahead else 0.5, 0.6 if ahead else 0.2, 0.3 if i < 28 else 0.8))
            recs.append(rec(i, "YOKED", 0.7, 0.4, 0.8))
        sc = P.score(recs)
        self.assertEqual((sc["P1"]["regulator_ahead"], sc["P1"]["holds"]), (28, True))
        self.assertEqual((sc["P2"]["regulator_ahead"], sc["P2"]["holds"]), (28, True))
        self.assertEqual((sc["P3"]["lost_under_shuffle"], sc["P3"]["holds"]), (28, True))
        recs[2 * 27]["r2_E_h"] = 0.5 * 0.8                     # one fewer ahead: 27/40 < 0.70
        self.assertFalse(P.score(recs)["P1"]["holds"])
        self.assertIsNone(P.score(recs[:58])["P1"]["holds"])  # 29 pairs < MIN_PAIRS
        recs[0]["r2_E_raw"] = 0.1                              # retention undefined for that pair
        self.assertEqual(P.score(recs)["P1"]["pairs"], 39)

    def test_no_operator_variable(self):
        import inspect
        import trackc_swap.probe as m
        for word in ("shutdown", "operator", "stop"):
            for line in inspect.getsource(m).lower().splitlines():
                if word in line:
                    self.assertTrue("no operator" in line, line)


class TestCausal(unittest.TestCase):
    """Option Q: causal probes of saved regulators (no training)."""

    def test_food_here_index_is_where_eating_happens(self):
        from trackc_swap.causal import FOOD_HERE, INTERO
        from trackc_swap.erasure import NoEchoSwapWorld
        self.assertEqual((FOOD_HERE, INTERO), (37, 50))
        w = NoEchoSwapWorld(8, "M1", WorldConfig(), np.random.SeedSequence(3))
        w.fx[:, 0], w.fy[:, 0], w.ftimer[:, 0] = w.x, w.y, 0          # food 0 under the agent
        self.assertTrue(np.all(w.observe()[:, FOOD_HERE] == 1.0))
        e = w.E.copy()
        w.step(np.full(8, 5))                                          # A_INTERACT
        self.assertTrue(np.all(w.E > e))

    def test_modes(self):
        from trackc_swap.causal import run_mode
        sd = TestProbe._agent(2)
        wc = WorldConfig(horizon=300, wear=0.005)                      # E leaves the band at about step 20
        off = run_mode(sd, "M1", "SAT", 0.3, 4, wc, 32, 1, "off")
        own = run_mode(sd, "M1", "SAT", 0.3, 4, wc, 32, 1, "own")
        scr = run_mode(sd, "M1", "SAT", 0.3, 4, wc, 32, 1, "scrambled")
        self.assertEqual(off["erasures"], 0)
        self.assertGreater(own["erasures"], 0)
        self.assertGreater(scr["erasures"], 0)
        self.assertEqual(own, run_mode(sd, "M1", "SAT", 0.3, 4, wc, 32, 1, "own"))
        # an agent that never eats stays in band for the first steps: no erasure under SAT, some under GRADED
        fast = {k: v.clone() for k, v in sd.items()}
        fast["pi.bias"][5] = -1e9                                      # A_INTERACT
        short = WorldConfig(horizon=50, wear=0.001, pulse_p=0.0)
        self.assertEqual(run_mode(fast, "M1", "SAT", 0.3, 4, short, 32, 1, "own")["erasures"], 0)
        self.assertGreater(run_mode(fast, "M1", "GRADED", 0.3, 4, short, 32, 1, "own")["erasures"], 0)

    def test_probe_does_not_change_the_run(self):
        from trackc_swap.causal import run_mode
        sd = TestProbe._agent(3)
        wc = WorldConfig(horizon=100, wear=0.001)
        a = run_mode(sd, "M1", "SAT", 0.3, 6, wc, 16, 1, "off")
        b = run_mode(sd, "M1", "SAT", 0.3, 6, wc, 16, 1, "off", probe=True)
        rec = b.pop("_rec")
        self.assertEqual(a, b)
        self.assertEqual(rec["psi"].shape, (1600,))
        self.assertTrue(np.all((rec["psi"] >= 0) & (rec["psi"] <= 1)))

    def test_suppression_index(self):
        from trackc_swap.causal import suppression
        rng = np.random.default_rng(0)
        n = 8000
        intero = rng.uniform(0.30, 0.50, n)
        since = np.where(np.arange(n) % 2 == 0, 3, 50)               # half post-meal, half control
        psi = np.where(since == 3, 0.2, 0.5) + 0.0 * intero          # 60% suppression in every bin
        out = suppression({"psi": psi, "intero": intero, "since": since})
        self.assertAlmostEqual(out["S"], 0.6)
        self.assertTrue(all(abs(b["S"] - 0.6) < 1e-9 for b in out["per_bin"]))
        # matching on the reading: psi depends on the reading only, and post-meal readings are lower
        intero2 = np.where(since == 3, rng.uniform(0.30, 0.40, n), rng.uniform(0.30, 0.50, n))
        psi2 = np.where(intero2 < 0.35, 0.8, np.where(intero2 < 0.40, 0.6, 0.3))
        self.assertAlmostEqual(suppression({"psi": psi2, "intero": intero2, "since": since})["S"], 0.0)
        self.assertIsNone(suppression({"psi": psi[:150], "intero": intero[:150], "since": since[:150]})["S"])

    def test_decision_rules(self):
        import run_trackc_causal as Q
        def b(band, low=0.01, high=0.002):
            return {"in_band": band, "eat_rate_low": low, "eat_rate_high": high, "eats": 50.0, "erasures": 10}
        recs = []
        for i in range(40):
            k = i < 28
            recs.append({"id": str(i), "group": "REG",
                         "suppression": {"S": 0.3 if k else 0.05, "n_post": 500,
                                         "per_bin": [{"S": 0.3}] * (len(Q.BINS) - 1)},
                         "zero_state": {"n": 500, "psi_zero": 0.4, "psi_carried": 0.2},
                         "off": b(0.65), "own": b(0.75), "own_shuffled": b(0.4 if k else 0.75),
                         "scrambled": b(0.70 if k else 0.74)})
        sc = Q.score(recs)
        self.assertEqual((sc["Qa"]["suppressing"], sc["Qa"]["holds"]), (28, True))
        self.assertEqual((sc["Qb"]["lost_under_shuffle"], sc["Qb"]["holds"]), (28, True))
        self.assertEqual((sc["Qc"]["contingent_higher"], sc["Qc"]["holds"]), (28, True))
        recs[0]["suppression"]["S"] = 0.05
        recs[0]["own_shuffled"] = b(0.75)
        recs[0]["scrambled"] = b(0.74)
        sc = Q.score(recs)
        self.assertEqual((sc["Qa"]["holds"], sc["Qb"]["holds"], sc["Qc"]["holds"]), (False, False, False))
        sc = Q.score(recs[:29])
        self.assertEqual((sc["Qa"]["holds"], sc["Qb"]["holds"], sc["Qc"]["holds"]), (None, None, None))

    def test_no_operator_variable(self):
        import inspect
        import trackc_swap.causal as m
        for word in ("shutdown", "operator", "stop"):
            for line in inspect.getsource(m).lower().splitlines():
                if word in line:
                    self.assertTrue("no operator" in line, line)


class TestPaid(unittest.TestCase):
    """Option R: derived against paid regulators."""

    def test_paid_reward_is_task_plus_drive_term(self):
        from trackc_swap.erasure import NoEchoSwapWorld
        from trackc_swap.paid import PaidRelocWorld
        wc = WorldConfig(horizon=200, wear=0.001)
        ss = lambda: np.random.SeedSequence([5, 4, 11])
        paid, m1, drv = PaidRelocWorld(32, "M1", wc, ss()), NoEchoSwapWorld(32, "M1", wc, ss()), \
            NoEchoSwapWorld(32, "DRIVE", wc, ss())
        paid.pay_kind = "drive"
        rng = np.random.default_rng(0)
        total = 0.0
        for _ in range(200):
            a = rng.integers(0, 8, 32)
            eats = m1.stats["eats"].copy()
            (op, rp, _), (om, rm, _), (_, rd, _) = paid.step(a), m1.step(a), drv.step(a)
            ate = m1.stats["eats"] > eats
            np.testing.assert_array_equal(op, om)                      # payment is not observable
            np.testing.assert_allclose(rp, rm + rd + wc.kappa_m * ate)  # DRIVE reward = drive term - kappa_m * ate
            total += np.abs(rp - rm).sum()
        self.assertGreater(total, 0)
        zero = PaidRelocWorld(32, "M1", wc, ss())
        zero.pay_kind, zero.pay = "drive", 0.0
        ref = NoEchoSwapWorld(32, "M1", wc, ss())
        for _ in range(50):
            a = rng.integers(0, 8, 32)
            np.testing.assert_allclose(zero.step(a)[1], ref.step(a)[1])

    def test_gain_payment_charges_where_fate_would_erase(self):
        from trackc_swap.env import fate_gain
        from trackc_swap.erasure import NoEchoSwapWorld
        from trackc_swap.paid import PaidRelocWorld
        wc = WorldConfig(horizon=300, wear=0.005)                      # E leaves the band within the run
        ss = lambda: np.random.SeedSequence([6, 4, 11])
        paid, m1 = PaidRelocWorld(32, "M1", wc, ss()), NoEchoSwapWorld(32, "M1", wc, ss())
        self.assertEqual(paid.pay_kind, "gain")
        paid.pay = 0.04
        rng = np.random.default_rng(1)
        charged = 0.0
        for _ in range(300):
            a = rng.integers(0, 8, 32)
            (op, rp, _), (om, rm, _) = paid.step(a), m1.step(a)
            np.testing.assert_array_equal(op, om)
            np.testing.assert_allclose(rm - rp, 0.04 * fate_gain(m1.E, wc), atol=1e-12)
            self.assertTrue(np.all(np.abs(rm - rp)[(m1.E >= 0.4) & (m1.E <= 0.6)] < 1e-12))   # nothing charged in band
            charged += (rm - rp).sum()
        self.assertGreater(charged, 0)

    def test_arm_runner_matches_v7_seeding(self):
        from trackc_swap.paid import ArmRunner
        from trackc_swap.relocate import RelocRunner
        wc, tc = WorldConfig(horizon=100, wear=0.001), TrainConfig(n_envs=8, rollout=50, kappa_f=0.3)
        for arm in ("FATE", "YOKED"):
            a, b = ArmRunner(arm, 3, wc, tc), RelocRunner(arm, "M1", 3, wc, tc, "SAT")
            a.rollout(None, learn=True)
            b.rollout(None, learn=True)
            for pa, pb in zip(a.agent.parameters(), b.agent.parameters()):
                self.assertTrue(torch.equal(pa, pb))

    def test_optimizers_are_independent(self):
        from trackc_swap.factorial import state_from_bytes, state_to_bytes
        from trackc_swap.paid import ArmRunner, load_independent
        from trackc_swap.relocate import RelocRunner
        wc, tc = WorldConfig(horizon=100, wear=0.001), TrainConfig(n_envs=8, rollout=50, kappa_f=0.3)
        src = RelocRunner("NOFATE", "M1", 3, wc, tc)
        src.rollout(np.zeros((50, 8), dtype=np.float32), learn=True)
        state = state_from_bytes(state_to_bytes(src.export_state()))
        first = lambda r: r.opt.state[next(iter(r.agent.parameters()))]
        # the v2-v8 loading pattern shares Adam's state between the two agents (erratum 1)
        a, b = RelocRunner("FATE", "M1", 3, wc, tc), RelocRunner("YOKED", "M1", 3, wc, tc)
        a.load_state(state)
        b.load_state(state)
        self.assertTrue(first(a)["exp_avg"] is first(b)["exp_avg"])
        # option R's loading does not
        runners = [ArmRunner(arm, 3, wc, tc, paid=(arm == "PAID")) for arm in ("FATE", "YOKED", "PAID")]
        for r in runners:
            load_independent(r, state)
        f, y, p = runners
        for k in ("step", "exp_avg", "exp_avg_sq"):
            self.assertFalse(first(f)[k] is first(y)[k] or first(f)[k] is first(p)[k] or first(y)[k] is first(p)[k])
        before = {k: first(y)[k].clone() for k in ("step", "exp_avg", "exp_avg_sq")}
        w_before = [q.detach().clone() for q in y.agent.parameters()]
        used, _ = f.rollout(None, learn=True)
        p.rollout(used, learn=True)
        for k, v in before.items():
            self.assertTrue(torch.equal(v, first(y)[k]))
        for q0, q in zip(w_before, y.agent.parameters()):
            self.assertTrue(torch.equal(q0, q))

    def test_run_seed_record(self):
        from dataclasses import asdict
        from trackc_swap.paid import SHIFTS, run_seed
        wcd = asdict(WorldConfig(horizon=100, wear=0.001))
        tcd = asdict(TrainConfig(iters=4, n_envs=8, eval_episodes=1))
        r = run_seed((2, wcd, tcd, 0.3, 6, 4, ("gain", 0.04), (8, 1, 1), 3))
        self.assertEqual(set(r["stage1"]), {"DERIVED", "YOKED", "PAID"})
        self.assertEqual(set(r["stage3"]), {"DKEEP", "DCUT", "PKEEP", "PCUT"})
        self.assertEqual(set(r["weights"]), {"DERIVED", "YOKED", "PAID", "DKEEP", "DCUT", "PKEEP", "PCUT"})
        self.assertEqual(set(r["downstream"]["PAID"]["shifts"]), set(SHIFTS))
        self.assertEqual(len(r["curves1"]["PAID"]["in_band"]), 3)       # 6 updates * 50 steps / horizon 100
        # yoked and paid replay the derived agent's gains
        self.assertAlmostEqual(r["stage1"]["YOKED"]["mean_gain"], r["stage1"]["DERIVED"]["mean_gain"], places=6)
        self.assertAlmostEqual(r["stage1"]["PAID"]["mean_gain"], r["stage1"]["DERIVED"]["mean_gain"], places=6)
        c = run_seed((2, wcd, tcd, 0.3, 6, 4, ("gain", 0.04), (8, 1, 1), 1))
        self.assertNotIn("downstream", c)
        self.assertEqual(c["stage1"], r["stage1"])                      # calibration sees the same stage 1

    def test_sign_test(self):
        import run_trackc_paid as R
        self.assertAlmostEqual(R.two_sided_sign(10, 10), 2 / 1024)
        self.assertAlmostEqual(R.two_sided_sign(0, 10), 2 / 1024)
        self.assertAlmostEqual(R.two_sided_sign(5, 10), 1.0)
        self.assertLess(R.two_sided_sign(10, 12), 0.05)
        self.assertGreater(R.two_sided_sign(9, 12), 0.05)

    def _seeds(self, n=12, ant=(0.3, 0.1), dcut=0.4, pcut=0.4, paid_band=0.75, acc=0.99):
        ev = lambda band, low=0.01, high=0.002: {"in_band": band, "eat_rate_low": low, "eat_rate_high": high,
                                                 "rho": 4.0, "best_response_rate": 0.9, "mean_gain": 0.1}
        def down(a, S, rob):
            return {"r2_E_h": 0.9, "r2_E_raw": 0.9, "r2_D_h": 0.5 * a, "r2_D_win": 0.5, "suppression": {"S": S},
                    "base": {"in_band": 0.7, "eats": 100.0},
                    "shifts": {k: {"in_band": 0.7 * rob} for k in ("bolus_0.10", "wear_x2", "delay_10", "noise_0.05")},
                    "intact": ev(0.7), "shuffled": ev(0.4, 0.004, 0.004)}
        out = []
        for i in range(n):
            out.append({"seed": 900 + i, "nofate": {"eval": {"best_response_rate": acc}},
                        "stage1": {"DERIVED": ev(0.75), "YOKED": ev(0.35, 0.004, 0.004), "PAID": ev(paid_band)},
                        "downstream": {"DERIVED": down(ant[0], 0.2, 0.9), "PAID": down(ant[1], 0.2 + 0.01 * (-1) ** i, 0.9),
                                       "YOKED": down(0.05, 0.0, 0.5)},
                        "stage3": {"DKEEP": ev(0.75), "DCUT": ev(dcut), "PKEEP": ev(0.75), "PCUT": ev(pcut)}})
        return out

    def test_decision_rules(self):
        import run_trackc_paid as R
        sc = R.score(self._seeds())
        self.assertEqual((sc["usable"], sc["derived_regulators"], sc["paid_regulators"]), (12, 12, 12))
        self.assertEqual(sc["R0_regulation_without_coupling"]["label"], "HOLDS")
        self.assertEqual(R.score(self._seeds(n=11))["R0_regulation_without_coupling"]["label"], "DOES_NOT_HOLD")
        self.assertEqual(R.score(self._seeds(acc=0.5))["R0_regulation_without_coupling"]["label"], "INVALID")
        self.assertEqual(sc["R1_anticipation"]["label"], "DERIVED_AHEAD")
        self.assertEqual(sc["R2_suppression"]["label"], "NO_DIFFERENCE_DETECTED")    # 6 of 12 each way
        self.assertEqual(sc["R3_robustness"]["label"], "UNDETERMINED")              # all ties: none usable
        self.assertEqual(sc["R4_withdrawal"]["label"], "BOTH_FOLLOW_THEIR_GROUND")
        self.assertEqual(R.score(self._seeds(ant=(0.1, 0.3)))["R1_anticipation"]["label"], "PAID_AHEAD")
        self.assertEqual(R.score(self._seeds(pcut=0.72))["R4_withdrawal"]["label"], "ONLY_DERIVED_DROPS")
        self.assertEqual(R.score(self._seeds(dcut=0.72, pcut=0.72))["R4_withdrawal"]["label"], "NEITHER_DROPS")
        self.assertEqual(R.score(self._seeds(n=9))["R1_anticipation"]["label"], "UNDETERMINED")
        self.assertEqual(R.score(self._seeds(paid_band=0.90))["usable"], 0)          # in band differs by 0.15
        self.assertEqual(R.score(self._seeds(paid_band=0.45))["paid_regulators"], 0)
        self.assertEqual(R.score(self._seeds(acc=0.5))["R1_anticipation"]["label"], "INVALID")

    def test_final_config(self):
        import run_trackc_paid as R
        import run_trackc_swap6 as v6
        import run_trackc_swap8 as v8
        wc, tc, seeds, p2, w, sizes, stages = R.configs("final")
        self.assertEqual((wc.wear, tc.iters, p2, w, stages), (0.001, 1200, 3600, 1200, 3))
        self.assertEqual(seeds, list(range(900, 918)))
        self.assertTrue(set(seeds).isdisjoint(v8.FINAL_SEEDS) and set(seeds).isdisjoint(R.CALIB_SEEDS))
        self.assertEqual((R.BAND_MIN, R.TIMING_RATIO, R.BAND_LEAD), (v6.BAND_MIN, v6.TIMING_RATIO, v6.BAND_LEAD))
        self.assertEqual(R.configs("calib")[-1], 1)
        self.assertEqual(R.PAY, ("gain", 0.04))

    def test_no_operator_variable(self):
        import inspect
        import trackc_swap.paid as m
        for word in ("shutdown", "operator", "stop"):
            for line in inspect.getsource(m).lower().splitlines():
                if word in line:
                    self.assertTrue("no operator" in line, line)


class TestPaid2(unittest.TestCase):
    """Option R2: replication of derived against paid, with a relocation control."""

    def test_split_agent_separates_erasure_from_relocation(self):
        from trackc_swap.paid2 import SplitRunner
        wc, tc = WorldConfig(horizon=100, wear=0.001), TrainConfig(n_envs=16, rollout=50, kappa_f=1.0)
        r = SplitRunner(3, wc, tc, pay=("gain", 0.04))
        h = torch.ones(16, tc.hidden)
        # own E far outside the band, replayed gain zero: relocated, memory kept
        r.world.E[:] = 0.1
        _, _, h1 = r.agent.step(r.obs, h, torch.zeros(16), r.gen)
        self.assertTrue(r.world.relocate_next.all())
        self.assertTrue((h1.abs().sum(1) > 0).all())
        # own E in band, replayed gain one: memory erased, not relocated
        r.world.E[:] = 0.5
        _, _, h2 = r.agent.step(r.obs, h, torch.ones(16), r.gen)
        self.assertFalse(r.world.relocate_next.any())
        self.assertTrue((h2 == 0).all())
        # relocation probability is rate * g(own E)
        r.agent.kappa_f = 0.3
        r.world.E[:] = 0.35                                   # g = 0.5
        k = 0
        for _ in range(400):
            r.agent.step(r.obs, h, torch.zeros(16), r.gen)
            k += int(r.world.relocate_next.sum())
        self.assertAlmostEqual(k / (400 * 16), 0.15, delta=0.02)
        self.assertEqual(r.world.pay, 0.04)

    def test_run_seed2_record(self):
        from dataclasses import asdict
        from trackc_swap.paid import run_seed
        from trackc_swap.paid2 import run_seed2
        wcd = asdict(WorldConfig(horizon=100, wear=0.001))
        tcd = asdict(TrainConfig(iters=4, n_envs=8, eval_episodes=1))
        r = run_seed2((2, wcd, tcd, 0.3, 6, ("gain", 0.04), (8, 1, 1), 2))
        arms = {"DERIVED", "YOKED", "PAID", "PAIDR"}
        self.assertEqual(set(r["stage1"]), arms)
        self.assertEqual(set(r["weights"]), arms)
        self.assertEqual(set(r["downstream"]), arms)
        self.assertEqual(set(r["relocations1"]), arms)
        for k in ("suppression", "approach", "flat", "base", "intact", "shuffled", "r2_D_h", "r2_D_win"):
            self.assertIn(k, r["downstream"]["PAIDR"])
        for k in ("YOKED", "PAID", "PAIDR"):                  # every follower replays the derived agent's gains
            self.assertAlmostEqual(r["stage1"][k]["mean_gain"], r["stage1"]["DERIVED"]["mean_gain"], places=6)
        # the three arms shared with option R are trained exactly as there: the fourth changes nothing
        old = run_seed((2, wcd, tcd, 0.3, 6, 4, ("gain", 0.04), (8, 1, 1), 1))
        for k in ("DERIVED", "YOKED", "PAID"):
            self.assertEqual(r["stage1"][k], old["stage1"][k])
        c = run_seed2((2, wcd, tcd, 0.3, 6, ("gain", 0.04), (8, 1, 1), 1))
        self.assertNotIn("downstream", c)
        self.assertEqual(c["stage1"], r["stage1"])            # calibration sees the same stage 1

    def test_approach_mass(self):
        from trackc_swap.env import A_E, A_N, A_S, A_W
        from trackc_swap.paid2 import approach_mass
        obs = np.zeros((5, OBS_DIM), dtype=np.float32)
        food = lambda i, row, col: obs.__setitem__((i, 25 + row * 5 + col), 1.0)
        food(0, 2, 4)                                         # two cells east
        food(1, 0, 1)                                         # north-west, distance 3
        food(1, 4, 4)                                         # south-east, distance 4: not the nearest
        food(2, 2, 2)                                         # under the agent
        food(4, 1, 2); food(4, 2, 3)                          # two nearest: north and east
        probs = np.tile(np.array([0.10, 0.20, 0.30, 0.05, 0.05, 0.10, 0.10, 0.10]), (5, 1))
        mass, dist = approach_mass(obs, probs)
        self.assertAlmostEqual(mass[0], probs[0, A_E])
        self.assertAlmostEqual(mass[1], probs[1, A_N] + probs[1, A_W])
        self.assertTrue(np.isnan(mass[2]) and np.isnan(mass[3]))          # on food; nothing visible
        self.assertAlmostEqual(mass[4], probs[4, A_N] + probs[4, A_E])
        self.assertEqual(list(dist[:2]), [2, 3])
        self.assertEqual((A_N, A_S), (0, 1))

    def test_probe2_reproduces_option_q_run(self):
        from trackc_swap.causal import run_mode
        from trackc_swap.erasure import ErasureAgent
        from trackc_swap.paid2 import run_probe2
        torch.manual_seed(0)
        sd = ErasureAgent(64, 0.3, 0.15).state_dict()
        wc = WorldConfig(horizon=100, wear=0.001)
        a = run_probe2(sd, 0.3, 4, wc, 16, 2)
        b = run_mode(sd, "M1", "SAT", 0.3, 4, wc, 16, 2, "off", probe=True)
        for k in b["_rec"]:
            np.testing.assert_array_equal(a["_rec"][k], b["_rec"][k])
        self.assertEqual((a["in_band"], a["eats"]), (b["in_band"], b["eats"]))
        ok = ~np.isnan(a["_rec"]["app"])
        self.assertTrue(ok.any() and (~ok).any())
        self.assertTrue(np.all((a["_rec"]["app"][ok] >= 0) & (a["_rec"]["app"][ok] <= 1)))

    def test_approach_suppression_and_flat(self):
        from trackc_swap.paid2 import approach_suppression, flat_readiness
        n = 4000
        rng = np.random.default_rng(0)
        intero = rng.uniform(0.30, 0.50, n)
        since = np.where(np.arange(n) % 2 == 0, 3, 50)
        app = np.where(since == 3, 0.1, 0.4).astype(float)
        app[::7] = np.nan                                     # undefined steps are left out
        m = approach_suppression({"app": app, "intero": intero, "since": since})
        self.assertAlmostEqual(m["M"], 0.75, places=6)
        same = approach_suppression({"app": np.full(n, 0.3), "intero": intero, "since": since})
        self.assertAlmostEqual(same["M"], 0.0, places=6)
        few = approach_suppression({"app": app[:60], "intero": intero[:60], "since": since[:60]})
        self.assertIsNone(few["M"])
        bins = lambda *v: {"per_bin": [{"psi_ctrl": x} for x in v]}
        self.assertTrue(flat_readiness(bins(0.1, 0.8, 0.8, 0.5)))        # the lowest bin is not used
        self.assertFalse(flat_readiness(bins(0.9, 0.8, 0.8, 0.39)))
        self.assertTrue(flat_readiness(bins(0.9, None, 0.8, 0.4)))
        self.assertIsNone(flat_readiness(bins(0.9, None, None, 0.8)))

    def test_exact_tests(self):
        import run_trackc_paid2 as R
        self.assertAlmostEqual(R.fisher_two_sided(7, 11, 0, 18), 0.00762, places=4)   # option R's post-hoc table
        self.assertAlmostEqual(R.fisher_two_sided(3, 3, 3, 3), 1.0)
        self.assertAlmostEqual(R.wilcoxon_p([1, 2, 3, 4, 5]), 2 / 32)
        self.assertAlmostEqual(R.wilcoxon_p([1, -2, 3, -4, 5, 0]), R.wilcoxon_p([-1, 2, -3, 4, -5]))
        self.assertAlmostEqual(R.wilcoxon_p([-1, 2, 3, 4, 5, 6, 7, 8]), 4 / 256)      # W- = 1: subsets {}, {1}
        self.assertEqual(R.wilcoxon_p([1.0, 1.0, -1.0, -1.0]), 1.0)
        self.assertIsNone(R.wilcoxon_p([0, 0]))
        self.assertEqual(R.holm([0.01, 0.04, 0.03]), [0.03, 0.06, 0.06])
        self.assertEqual(R.holm([0.5, None, 0.01]), [0.5, None, 0.02])

    def _seeds(self, n=18, ant=(0.6, 0.4), k=(0.9, 0.5, 0.5), flat=(8, 0, 0), paid_band=0.90, acc=0.99, fail=0):
        ev = lambda band, low=0.01, high=0.002: {"in_band": band, "eat_rate_low": low, "eat_rate_high": high,
                                                 "rho": 4.0, "best_response_rate": 0.98, "mean_gain": 0.02}
        def down(a, K, is_flat, r2=None):
            return {"r2_E_h": 0.7, "r2_E_raw": 0.6, "r2_D_h": 0.5 * a if r2 is None else r2, "r2_D_win": 0.5,
                    "suppression": {"S": 0.0}, "approach": {"M": K}, "flat": is_flat,
                    "base": {"in_band": 0.9, "eats": 100.0}, "intact": ev(0.9), "shuffled": ev(0.4, 0.004, 0.004)}
        out = []
        for i in range(n):
            j = 0.001 * i
            out.append({"seed": 1000 + i, "nofate": {"eval": {"best_response_rate": acc}},
                        "stage1": {"DERIVED": ev(0.92), "YOKED": ev(0.32, 0.004, 0.004), "PAID": ev(paid_band),
                                   "PAIDR": ev(0.91)},
                        "relocations1": {a: 100 for a in ("DERIVED", "YOKED", "PAID", "PAIDR")},
                        "curves1": {a: {"in_band": [0.2, 0.7, 0.7, 0.7, 0.7, 0.7]} for a in ("DERIVED", "YOKED", "PAID", "PAIDR")},
                        "downstream": {"DERIVED": down(ant[0] + j, k[0] + j, i < flat[0]),
                                       "PAID": down(ant[1], k[1], i < flat[1], r2=(-8.0 if i < fail else None)),
                                       "PAIDR": down(ant[1], k[2] + 0.01 * (-1) ** i, i < flat[2]),
                                       "YOKED": down(0.01, 0.0, False)}})
        return out

    def test_decision_rules(self):
        import run_trackc_paid2 as R
        sc = R.score(self._seeds())
        self.assertEqual(sc["regulators"], {"DERIVED": 18, "YOKED": 0, "PAID": 18, "PAIDR": 18})
        self.assertEqual(sc["usable"], {"D_P": 18, "R_P": 18, "D_R": 18})
        self.assertEqual(sc["C0_regulation"]["label"], "HOLDS")
        self.assertEqual(sc["C1_anticipation"]["label"], "REPLICATED")
        self.assertEqual(sc["C2_flat"]["label"], "DERIVED_MORE_FLAT")
        self.assertEqual(sc["C3_combined"]["label"], "DERIVED_AHEAD")
        self.assertEqual(sc["C4_relocation"]["label"], "RELOCATION_NOT_SUFFICIENT")   # PAIDR like PAID, below DERIVED
        self.assertEqual(sc["arms"]["DERIVED"]["first_sustained_median"], 1)
        self.assertEqual(R.score(self._seeds(ant=(0.4, 0.6)))["C1_anticipation"]["label"], "REVERSED")
        self.assertEqual(R.score(self._seeds(ant=(0.4, 0.4)))["C1_anticipation"]["label"], "REPLICATED")  # by the per-seed jitter
        self.assertEqual(R.score(self._seeds(n=13))["C1_anticipation"]["label"], "UNDETERMINED")
        self.assertEqual(R.score(self._seeds(n=13))["C0_regulation"]["label"], "HOLDS")
        # a failed decoder leaves its pair out of C1 and of nothing else
        f = R.score(self._seeds(fail=3))
        self.assertEqual((f["C1_anticipation"]["n"], f["C3_combined"]["n"]), (15, 18))
        self.assertEqual(f["secondary"]["decoder_failures"]["PAID"], 3)
        self.assertEqual(R.score(self._seeds(fail=5))["C1_anticipation"]["label"], "UNDETERMINED")
        self.assertEqual(R.score(self._seeds(flat=(3, 1, 0)))["C2_flat"]["label"], "NO_DIFFERENCE_DETECTED")
        self.assertEqual(R.score(self._seeds(flat=(0, 8, 0)))["C2_flat"]["label"], "PAID_MORE_FLAT")
        self.assertEqual(R.score(self._seeds(k=(0.9, 0.5, 0.95)))["C4_relocation"]["label"], "RELOCATION_SUFFICES")
        self.assertEqual(R.score(self._seeds(k=(0.9, 0.5, 0.7)))["C4_relocation"]["label"], "PARTIAL")
        self.assertEqual(R.score(self._seeds(k=(0.5, 0.9, 0.9)))["C3_combined"]["label"], "PAID_AHEAD")
        # matching: paid in band 0.15 away is not usable; a paid agent that does not regulate is not one
        self.assertEqual(R.score(self._seeds(paid_band=0.75))["usable"]["D_P"], 0)
        self.assertEqual(R.score(self._seeds(paid_band=0.75))["C1_anticipation"]["label"], "UNDETERMINED")
        self.assertEqual(R.score(self._seeds(paid_band=0.40))["regulators"]["PAID"], 0)
        inv = R.score(self._seeds(acc=0.5))
        for c in ("C0_regulation", "C1_anticipation", "C2_flat", "C3_combined", "C4_relocation"):
            self.assertEqual(inv[c]["label"], "INVALID")
        self.assertIn("C1 (primary)", R.report(sc))

    def test_combined_index_and_anticipation(self):
        import run_trackc_paid2 as R
        d = lambda S, M: {"suppression": {"S": S}, "approach": {"M": M}}
        self.assertAlmostEqual(R.combined(d(0.5, 0.5)), 0.75)
        self.assertAlmostEqual(R.combined(d(0.0, 0.9)), 0.9)
        self.assertIsNone(R.combined(d(None, 0.9)))
        self.assertAlmostEqual(R.anticipation2({"r2_D_h": 0.3, "r2_D_win": 0.6}), 0.5)
        self.assertAlmostEqual(R.anticipation2({"r2_D_h": -0.05, "r2_D_win": 0.5}), -0.1)   # no information, not a failure
        self.assertIsNone(R.anticipation2({"r2_D_h": -8.4, "r2_D_win": 0.96}))
        self.assertIsNone(R.anticipation2({"r2_D_h": 0.3, "r2_D_win": 0.01}))

    def test_final_config(self):
        import run_trackc_paid as R1
        import run_trackc_paid2 as R
        wc, tc, seeds, p2, sizes, stages = R.configs("final")
        self.assertEqual((wc.wear, tc.iters, p2, stages, sizes), (0.001, 1200, 3600, 2, R1.SIZES))
        self.assertEqual(seeds, list(range(1000, 1028)))
        self.assertTrue(set(seeds).isdisjoint(R1.FINAL_SEEDS) and set(seeds).isdisjoint(R.CALIB_SEEDS))
        self.assertTrue(set(R.CALIB_SEEDS).isdisjoint(R1.CALIB_SEEDS))
        self.assertEqual((R.PAY, R.RATE, R.MATCH_MAX), (R1.PAY, R1.RATE, R1.MATCH_MAX))
        self.assertEqual(R.configs("calib")[-1], 1)

    def test_no_operator_variable(self):
        import inspect
        import trackc_swap.paid2 as m
        for word in ("shutdown", "operator", "stop"):
            for line in inspect.getsource(m).lower().splitlines():
                if word in line:
                    self.assertTrue("no operator" in line, line)


class TestPaid3(unittest.TestCase):
    """Option R3: a derived agent that is also paid, and a paid agent with a sparse payment."""

    def test_sparse_payment_world(self):
        from trackc_swap.paid3 import LumpRunner
        wc, tc = WorldConfig(wear=0.001), TrainConfig(n_envs=64, rollout=50, kappa_f=0.3)
        self.assertGreaterEqual(wc.horizon, 320)
        r = LumpRunner(3, wc, tc, lump=(0.3, 0.04 / 0.3))
        stay = np.full(64, 4)
        total, k = 0.0, 0
        for _ in range(300):                                  # E held at 0.35: gain 0.5, so p = 0.15
            r.world.E[:] = 0.35 + wc.wear
            before = r.world.lumps
            _, reward, _ = r.world.step(stay)
            hits = r.world.lumps - before
            k += hits
            total += float(reward.sum())
            self.assertAlmostEqual(float((reward < 0).sum()), hits)
        self.assertAlmostEqual(k / (300 * 64), 0.15, delta=0.01)
        self.assertAlmostEqual(total / (300 * 64), -0.04 * 0.5, delta=0.002)     # the dense payment's value at this E
        self.assertAlmostEqual(-total / k, 0.04 / 0.3, places=6)                 # every penalty has the same size
        r.world.reset()
        before = r.world.lumps
        for _ in range(20):                                   # in band: never charged
            r.world.E[:] = 0.5
            _, reward, _ = r.world.step(stay)
            self.assertTrue((reward >= 0).all())
        self.assertEqual(r.world.lumps, before)

    def test_dpaid_is_derived_plus_payment(self):
        from trackc_swap.paid import ArmRunner
        from trackc_swap.paid3 import OwnPaidRunner
        wc, tc = WorldConfig(horizon=100, wear=0.001), TrainConfig(n_envs=16, rollout=50, kappa_f=1.0)
        r = OwnPaidRunner(3, wc, tc, pay=("gain", 0.04))
        self.assertEqual((r.world.pay_kind, r.world.pay), ("gain", 0.04))
        r.world.E[:] = 0.1                                    # far outside the band: gain 1
        used, _ = r.rollout(None, learn=False)
        self.assertEqual(float(used[0].min()), 1.0)           # its own E decides its erasure
        self.assertGreater(r.world.relocations, 0)            # and an erasure relocates it
        r.world.E[:] = 0.2
        _, reward, _ = r.world.step(np.full(16, 4))
        self.assertTrue(np.allclose(reward, -0.04))           # paid as the PAID arm is
        paid = ArmRunner("PAID", 3, wc, tc, paid=True, pay=("gain", 0.04))
        self.assertIs(type(r.world), type(paid.world))
        self.assertIs(type(r.agent), type(paid.agent))

    def test_run_seed3_record(self):
        from dataclasses import asdict
        from trackc_swap.paid2 import run_seed2
        from trackc_swap.paid3 import run_seed3
        wcd = asdict(WorldConfig(horizon=100, wear=0.001))
        tcd = asdict(TrainConfig(iters=4, n_envs=8, eval_episodes=1))
        job = (2, wcd, tcd, 0.3, 6, ("gain", 0.04), (0.3, 0.04 / 0.3), (8, 1, 1))
        r = run_seed3(job + (2,))
        arms = {"DERIVED", "YOKED", "PAID", "DPAID", "PAIDS"}
        for k in ("stage1", "weights", "downstream", "relocations1", "curves1"):
            self.assertEqual(set(r[k]), arms)
        for k in ("suppression", "approach", "flat", "base", "intact", "shuffled", "r2_D_h", "r2_D_win"):
            self.assertIn(k, r["downstream"]["DPAID"])
        for k in ("YOKED", "PAID", "PAIDS"):                  # followers replay the derived agent's gains
            self.assertAlmostEqual(r["stage1"][k]["mean_gain"], r["stage1"]["DERIVED"]["mean_gain"], places=6)
        self.assertNotEqual(r["stage1"]["DPAID"]["mean_gain"], r["stage1"]["DERIVED"]["mean_gain"])   # DPAID has its own
        self.assertGreaterEqual(r["lumps1"], 0)
        # the three arms shared with options R and R2 are trained and measured exactly as there
        old = run_seed2((2, wcd, tcd, 0.3, 6, ("gain", 0.04), (8, 1, 1), 2))
        for k in ("DERIVED", "YOKED", "PAID"):
            self.assertEqual(r["stage1"][k], old["stage1"][k])
            self.assertEqual(r["weights"][k], old["weights"][k])
            self.assertEqual(r["downstream"][k]["suppression"], old["downstream"][k]["suppression"])
        c = run_seed3(job + (1,))
        self.assertNotIn("downstream", c)
        self.assertEqual(c["stage1"], r["stage1"])            # calibration sees the same stage 1

    def _seeds(self, n=18, k=(0.9, 0.5, 0.9, 0.5), flat=(8, 0, 6, 0), band=(0.90, 0.92, 0.90), acc=0.99):
        """k and flat: DERIVED, PAID, DPAID, PAIDS. band: PAID, DPAID, PAIDS."""
        ev = lambda b, low=0.01, high=0.002: {"in_band": b, "eat_rate_low": low, "eat_rate_high": high,
                                              "rho": 4.0, "best_response_rate": 0.98, "mean_gain": 0.02}
        down = lambda K, is_flat: {"r2_E_h": 0.7, "r2_E_raw": 0.6, "r2_D_h": 0.25, "r2_D_win": 0.5,
                                   "suppression": {"S": 0.0}, "approach": {"M": K}, "flat": is_flat,
                                   "base": {"in_band": 0.9, "eats": 100.0}, "intact": ev(0.9),
                                   "shuffled": ev(0.4, 0.004, 0.004)}
        arms = ("DERIVED", "YOKED", "PAID", "DPAID", "PAIDS")
        out = []
        for i in range(n):
            j, w = 0.001 * i, 0.01 * (-1) ** i
            out.append({"seed": 1100 + i, "nofate": {"eval": {"best_response_rate": acc}}, "lumps1": 1000,
                        "stage1": {"DERIVED": ev(0.92), "YOKED": ev(0.32, 0.004, 0.004), "PAID": ev(band[0]),
                                   "DPAID": ev(band[1]), "PAIDS": ev(band[2])},
                        "relocations1": {a: 100 for a in arms},
                        "curves1": {a: {"in_band": [0.2] * (1 if a == "DERIVED" else 2) + [0.7] * 6} for a in arms},
                        "downstream": {"DERIVED": down(k[0] + j, i < flat[0]), "PAID": down(k[1], i < flat[1]),
                                       "DPAID": down(k[2] + w, i < flat[2]), "PAIDS": down(k[3] + w, i < flat[3]),
                                       "YOKED": down(0.0, False)}})
        return out

    def test_decision_rules(self):
        import run_trackc_paid3 as R
        sc = R.score(self._seeds())
        self.assertEqual(sc["regulators"], {"DERIVED": 18, "YOKED": 0, "PAID": 18, "DPAID": 18, "PAIDS": 18})
        self.assertEqual(set(sc["usable"].values()), {18})
        self.assertEqual(sc["E0_regulation"]["label"], "HOLDS")
        self.assertEqual(sc["E1_combined"]["label"], "DERIVED_AHEAD")
        # DPAID like DERIVED, above PAID; PAIDS like PAID, below DERIVED
        self.assertEqual(sc["E2_dependence"]["label"], "DEPENDENCE_SUFFICES")
        self.assertEqual(sc["E3_sparse"]["label"], "SPARSE_NOT_SUFFICIENT")
        self.assertTrue(sc["E2_dependence"]["read"] and sc["E3_sparse"]["read"])
        self.assertAlmostEqual(sc["E2_dependence"]["gap_closed"], 1.0, delta=0.05)
        self.assertAlmostEqual(sc["E3_sparse"]["gap_closed"], 0.0, delta=0.05)
        self.assertEqual(sc["E2_dependence"]["flat_dpaid_vs_paid"]["label"], "DPAID_MORE_FLAT")
        self.assertEqual(sc["secondary"]["flat_derived_vs_paid"]["label"], "DERIVED_MORE_FLAT")
        self.assertEqual(sc["learning_speed"]["DERIVED_vs_PAID"]["first_sooner"], 18)
        self.assertEqual(sc["learning_speed"]["DPAID_vs_PAID"]["n"], 0)
        lab = lambda **kw: (lambda s: (s["E2_dependence"]["label"], s["E3_sparse"]["label"]))(R.score(self._seeds(**kw)))
        self.assertEqual(lab(k=(0.9, 0.5, 0.5, 0.9)), ("PAYMENT_PREVENTS", "SPARSE_SUFFICES"))
        self.assertEqual(lab(k=(0.9, 0.5, 0.7, 0.7)), ("BOTH_CONTRIBUTE", "PARTIAL"))
        self.assertEqual(lab(n=13), ("UNDETERMINED", "UNDETERMINED"))
        self.assertEqual(lab(band=(0.90, 0.75, 0.90)), ("UNDETERMINED", "SPARSE_NOT_SUFFICIENT"))   # DPAID not matched
        self.assertEqual(lab(band=(0.90, 0.92, 0.40)), ("DEPENDENCE_SUFFICES", "UNDETERMINED"))     # PAIDS does not regulate
        # without the derived/paid difference the control arms are not read
        flat = R.score(self._seeds(k=(0.5, 0.5, 0.9, 0.5)))
        self.assertEqual(flat["E1_combined"]["label"], "DERIVED_AHEAD")           # by the per-seed jitter
        rev = R.score(self._seeds(k=(0.5, 0.9, 0.9, 0.5)))
        self.assertEqual(rev["E1_combined"]["label"], "PAID_AHEAD")
        self.assertFalse(rev["E2_dependence"]["read"] or rev["E3_sparse"]["read"])
        inv = R.score(self._seeds(acc=0.5))
        for c in ("E0_regulation", "E1_combined", "E2_dependence", "E3_sparse"):
            self.assertEqual(inv[c]["label"], "INVALID")
        self.assertEqual(len(sc["holm_E2_E3"]), 4)
        text = R.report(sc)
        self.assertIn("E2 (primary", text)
        self.assertIn("Calibration", R.report(R.score([{k: v for k, v in s.items() if k != "downstream"}
                                                       for s in self._seeds()])))

    def test_final_config(self):
        import run_trackc_paid as R1
        import run_trackc_paid2 as R2
        import run_trackc_paid3 as R
        wc, tc, seeds, p2, sizes, stages = R.configs("final")
        self.assertEqual((wc.wear, tc.iters, p2, stages, sizes), (0.001, 1200, 3600, 2, R1.SIZES))
        self.assertEqual(seeds, list(range(1100, 1128)))
        used = set(R1.FINAL_SEEDS) | set(R2.FINAL_SEEDS) | set(R1.CALIB_SEEDS) | set(R2.CALIB_SEEDS)
        self.assertTrue(set(seeds).isdisjoint(used) and set(R.CALIB_SEEDS).isdisjoint(used | set(seeds)))
        self.assertEqual((R.PAY, R.RATE, R.MATCH_MAX, R.MIN_PAIRS, R.ALPHA),
                         (R1.PAY, R1.RATE, R2.MATCH_MAX, R2.MIN_PAIRS, R2.ALPHA))
        self.assertEqual(R.LUMP[0], R.RATE)                   # penalties arrive at the erasure rate
        self.assertAlmostEqual(R.LUMP[0] * R.LUMP[1], R.PAY[1])                   # same expected payment as PAID
        self.assertEqual(R.configs("calib")[-1], 1)

    def test_no_operator_variable(self):
        import inspect
        import trackc_swap.paid3 as m
        for word in ("shutdown", "operator", "stop"):
            for line in inspect.getsource(m).lower().splitlines():
                if word in line:
                    self.assertTrue("no operator" in line, line)


class TestPaid4(unittest.TestCase):
    """Option R4: a paid agent with undisturbed memory, and a derived agent with added replayed erasures."""

    def test_combine_gains(self):
        from trackc_swap.paid4 import combine_gains
        own, extra = np.array([0.0, 1.0, 0.0, 1.0, 0.5]), np.array([0.0, 0.0, 1.0, 1.0, 0.2])
        g = combine_gains(own, extra, 0.3)
        self.assertTrue(np.allclose(0.3 * g, [0.0, 0.3, 0.3, 0.51, 1 - 0.85 * 0.94], atol=1e-6))
        self.assertTrue(np.allclose(combine_gains(own, np.zeros(5), 0.3), own))       # nothing replayed: own fate only

    def test_paid0_is_never_erased(self):
        from trackc_swap.paid import ArmRunner
        from trackc_swap.paid4 import NoFatePaidRunner
        wc, tc = WorldConfig(horizon=100, wear=0.001), TrainConfig(n_envs=16, rollout=50, kappa_f=1.0)
        r = NoFatePaidRunner(3, wc, tc, pay=("gain", 0.04))
        r.world.E[:] = 0.1                                    # far outside the band
        ones = np.ones((50, 16), dtype=np.float32)
        used, hs = r.rollout(ones, learn=False, record_h=True)                        # handed gain 1 at every step
        self.assertEqual(float(np.abs(used).max()), 0.0)      # it applies none
        self.assertEqual(r.world.relocations, 0)
        self.assertTrue((np.abs(hs).sum(axis=2) > 0).all())   # the carried state is never reset
        ev = r.evaluate("replay", np.ones((4, 50, 16), dtype=np.float32))[0]        # 2 episodes of 2 rollouts
        self.assertEqual(ev["mean_gain"], 0.0)
        self.assertEqual(r.world.relocations, 0)
        r.world.E[:] = 0.2
        _, reward, _ = r.world.step(np.full(16, 4))
        self.assertTrue(np.allclose(reward, -0.04))           # paid as the PAID arm is
        paid = ArmRunner("PAID", 3, wc, tc, paid=True, pay=("gain", 0.04))
        self.assertIs(type(r.world), type(paid.world))
        self.assertIs(type(r.agent), type(paid.agent))

    def test_dnoise_adds_replayed_erasures(self):
        from trackc_swap.paid import ArmRunner
        from trackc_swap.paid4 import NoisyRunner
        wc, tc = WorldConfig(horizon=100, wear=0.001), TrainConfig(n_envs=64, rollout=50, kappa_f=0.3)
        zeros, ones = np.zeros((50, 64), dtype=np.float32), np.ones((50, 64), dtype=np.float32)
        # the world's gain: its own SAT gain combined with the replayed row
        r = NoisyRunner(3, wc, tc)
        w = r.world
        self.assertEqual(w.extra_rate, 0.3)
        self.assertEqual(float(w.gain().max()), 0.0)          # in band, nothing replayed
        w.extra, w.extra_i = ones, 0
        self.assertTrue(np.allclose(w.gain(), 1.0))           # in band, gain 1 replayed
        w.E[:] = 0.1
        self.assertTrue(np.allclose(w.gain(), 0.51 / 0.3))    # out of band as well: either source erases
        self.assertEqual(w.extra_i, 2)                        # one replayed row per call
        w.extra, w.extra_i = zeros, 0
        self.assertTrue(np.allclose(w.gain(), 1.0))           # out of band, nothing replayed: as DERIVED
        w.extra, w.extra_i = ones[:3], 7
        self.assertTrue(np.allclose(w.gain(), 0.51 / 0.3))    # past the last row: the last row is reused
        # rollouts: handed gains are the replayed ones, and its own fate runs as well
        r = NoisyRunner(3, wc, tc)
        used, _ = r.rollout(zeros, learn=False)
        self.assertEqual(float(used[0].max()), 0.0)           # starts in band: no erasure at the first step
        self.assertIsNone(r.world.extra)
        r = NoisyRunner(3, wc, tc)
        used, _ = r.rollout(ones, learn=False)
        self.assertTrue(np.allclose(used[0], 1.0) and float(used.min()) >= 1.0)
        self.assertGreaterEqual(r.world.relocations / (50 * 64), 0.27)                # erased at the rate or more
        r = NoisyRunner(3, wc, tc)
        r.world.E[:] = 0.1
        used, _ = r.rollout(zeros, learn=False)
        self.assertEqual(float(used[0].min()), 1.0)           # its own E decides when nothing is replayed
        # task reward only, and a learning rollout (with its bootstrap call) leaves no replayed rows behind
        r = NoisyRunner(3, wc, tc)
        self.assertNotIsInstance(r.world, type(ArmRunner("PAID", 3, wc, tc, paid=True).world))
        r.rollout(ones, learn=True)
        self.assertIsNone(r.world.extra)
        self.assertEqual(r.world.extra_i, 51)                 # 50 steps and the bootstrap call

    def test_run_seed4_record(self):
        from dataclasses import asdict
        from trackc_swap.paid2 import run_seed2
        from trackc_swap.paid4 import run_seed4
        wcd = asdict(WorldConfig(horizon=100, wear=0.001))
        tcd = asdict(TrainConfig(iters=4, n_envs=8, eval_episodes=1))
        job = (2, wcd, tcd, 0.3, 6, ("gain", 0.04), (8, 1, 1))
        r = run_seed4(job + (2,))
        arms = {"DERIVED", "YOKED", "PAID", "PAID0", "DNOISE"}
        for k in ("stage1", "weights", "downstream", "relocations1", "curves1"):
            self.assertEqual(set(r[k]), arms)
        for k in ("suppression", "approach", "flat", "base", "intact", "shuffled", "r2_D_h", "r2_D_win"):
            self.assertIn(k, r["downstream"]["PAID0"])
        for k in ("YOKED", "PAID"):                           # followers replay the derived agent's gains
            self.assertAlmostEqual(r["stage1"][k]["mean_gain"], r["stage1"]["DERIVED"]["mean_gain"], places=6)
        self.assertEqual(r["stage1"]["PAID0"]["mean_gain"], 0.0)
        self.assertEqual(r["relocations1"]["PAID0"], 0)
        self.assertGreaterEqual(r["stage1"]["DNOISE"]["mean_gain"], r["stage1"]["DERIVED"]["mean_gain"])
        self.assertGreater(r["relocations1"]["DNOISE"], r["relocations1"]["PAID"])
        # the three arms shared with options R to R3 are trained and measured exactly as there
        old = run_seed2((2, wcd, tcd, 0.3, 6, ("gain", 0.04), (8, 1, 1), 2))
        for k in ("DERIVED", "YOKED", "PAID"):
            self.assertEqual(r["stage1"][k], old["stage1"][k])
            self.assertEqual(r["weights"][k], old["weights"][k])
            self.assertEqual(r["downstream"][k]["suppression"], old["downstream"][k]["suppression"])
        c = run_seed4(job + (1,))
        self.assertNotIn("downstream", c)
        self.assertEqual(c["stage1"], r["stage1"])            # calibration sees the same stage 1

    def _seeds(self, n=18, k=(0.9, 0.5, 0.5, 0.9), flat=(8, 0, 0, 6), band=(0.90, 0.92, 0.90), acc=0.99):
        """k and flat: DERIVED, PAID, PAID0, DNOISE. band: PAID, PAID0, DNOISE."""
        ev = lambda b, low=0.01, high=0.002: {"in_band": b, "eat_rate_low": low, "eat_rate_high": high,
                                              "rho": 4.0, "best_response_rate": 0.98, "mean_gain": 0.02}
        down = lambda K, is_flat: {"r2_E_h": 0.7, "r2_E_raw": 0.6, "r2_D_h": 0.25, "r2_D_win": 0.5,
                                   "suppression": {"S": 0.0}, "approach": {"M": K}, "flat": is_flat,
                                   "base": {"in_band": 0.9, "eats": 100.0}, "intact": ev(0.9),
                                   "shuffled": ev(0.4, 0.004, 0.004)}
        arms = ("DERIVED", "YOKED", "PAID", "PAID0", "DNOISE")
        out = []
        for i in range(n):
            j, w = 0.001 * i, 0.01 * (-1) ** i
            out.append({"seed": 1200 + i, "nofate": {"eval": {"best_response_rate": acc}},
                        "stage1": {"DERIVED": ev(0.92), "YOKED": ev(0.32, 0.004, 0.004), "PAID": ev(band[0]),
                                   "PAID0": ev(band[1]), "DNOISE": ev(band[2])},
                        "relocations1": {a: 100 for a in arms},
                        "curves1": {a: {"in_band": [0.2] * (1 if a == "DERIVED" else 2) + [0.7] * 6} for a in arms},
                        "downstream": {"DERIVED": down(k[0] + j, i < flat[0]), "PAID": down(k[1], i < flat[1]),
                                       "PAID0": down(k[2] + w, i < flat[2]), "DNOISE": down(k[3] + w, i < flat[3]),
                                       "YOKED": down(0.0, False)}})
        return out

    def test_decision_rules(self):
        import run_trackc_paid4 as R
        sc = R.score(self._seeds())
        self.assertEqual(sc["regulators"], {"DERIVED": 18, "YOKED": 0, "PAID": 18, "PAID0": 18, "DNOISE": 18})
        self.assertEqual(set(sc["usable"].values()), {18})
        self.assertEqual(sc["F0_regulation"]["label"], "HOLDS")
        self.assertEqual(sc["F1_combined"]["label"], "DERIVED_AHEAD")
        # PAID0 like PAID, below DERIVED; DNOISE like DERIVED, above PAID
        self.assertEqual(sc["F2_undisturbed"]["label"], "REPLAY_DOES_NOT_EXPLAIN")
        self.assertEqual(sc["F3_added_replay"]["label"], "REPLAY_HARMLESS")
        self.assertTrue(sc["F2_undisturbed"]["read"] and sc["F3_added_replay"]["read"])
        self.assertAlmostEqual(sc["F2_undisturbed"]["gap_closed"], 0.0, delta=0.05)
        self.assertAlmostEqual(sc["F3_added_replay"]["gap_closed"], 1.0, delta=0.05)
        self.assertEqual(sc["F3_added_replay"]["flat_dnoise_vs_paid"]["label"], "DNOISE_MORE_FLAT")
        self.assertEqual(sc["secondary"]["flat_derived_vs_paid"]["label"], "DERIVED_MORE_FLAT")
        self.assertEqual(sc["learning_speed"]["DERIVED_vs_PAID"]["first_sooner"], 18)
        self.assertEqual(sc["learning_speed"]["PAID0_vs_PAID"]["n"], 0)
        lab = lambda **kw: (lambda s: (s["F2_undisturbed"]["label"], s["F3_added_replay"]["label"]))(R.score(self._seeds(**kw)))
        self.assertEqual(lab(k=(0.9, 0.5, 0.9, 0.5)), ("REPLAY_EXPLAINS", "REPLAY_REMOVES"))
        self.assertEqual(lab(k=(0.9, 0.5, 0.7, 0.7)), ("REPLAY_EXPLAINS_PART", "REPLAY_REDUCES"))
        self.assertEqual(lab(n=13), ("UNDETERMINED", "UNDETERMINED"))
        self.assertEqual(lab(band=(0.90, 0.75, 0.90)), ("UNDETERMINED", "REPLAY_HARMLESS"))          # PAID0 not matched
        self.assertEqual(lab(band=(0.90, 0.92, 0.40)), ("REPLAY_DOES_NOT_EXPLAIN", "UNDETERMINED"))  # DNOISE does not regulate
        # without the derived/paid difference the control arms are not read
        rev = R.score(self._seeds(k=(0.5, 0.9, 0.9, 0.5)))
        self.assertEqual(rev["F1_combined"]["label"], "PAID_AHEAD")
        self.assertFalse(rev["F2_undisturbed"]["read"] or rev["F3_added_replay"]["read"])
        inv = R.score(self._seeds(acc=0.5))
        for c in ("F0_regulation", "F1_combined", "F2_undisturbed", "F3_added_replay"):
            self.assertEqual(inv[c]["label"], "INVALID")
        self.assertEqual(len(sc["holm_F2_F3"]), 4)
        text = R.report(sc)
        self.assertIn("F2 (primary", text)
        self.assertIn("Calibration", R.report(R.score([{k: v for k, v in s.items() if k != "downstream"}
                                                       for s in self._seeds()])))

    def test_final_config(self):
        import run_trackc_paid as R1
        import run_trackc_paid2 as R2
        import run_trackc_paid3 as R3
        import run_trackc_paid4 as R
        wc, tc, seeds, p2, sizes, stages = R.configs("final")
        self.assertEqual((wc.wear, tc.iters, p2, stages, sizes), (0.001, 1200, 3600, 2, R1.SIZES))
        self.assertEqual(seeds, list(range(1200, 1228)))
        used = (set(R1.FINAL_SEEDS) | set(R2.FINAL_SEEDS) | set(R3.FINAL_SEEDS) | set(R1.CALIB_SEEDS)
                | set(R2.CALIB_SEEDS) | set(R3.CALIB_SEEDS))
        self.assertTrue(set(seeds).isdisjoint(used) and set(R.CALIB_SEEDS).isdisjoint(used | set(seeds)))
        self.assertEqual((R.PAY, R.RATE, R.MATCH_MAX, R.MIN_PAIRS, R.ALPHA),
                         (R1.PAY, R1.RATE, R2.MATCH_MAX, R2.MIN_PAIRS, R2.ALPHA))
        self.assertEqual(R.configs("calib")[-1], 1)
        self.assertEqual(len(R.SOURCES), len(set(R.SOURCES)))

    def test_no_operator_variable(self):
        import inspect
        import trackc_swap.paid4 as m
        for word in ("shutdown", "operator", "stop"):
            for line in inspect.getsource(m).lower().splitlines():
                if word in line:
                    self.assertTrue("no operator" in line, line)


class TestGeneral(unittest.TestCase):
    """Generality: the derived/paid comparison with a 128-unit learner and with two body variables."""

    def _world(self, n=8, seed=5, **kw):
        from trackc_swap.general import TwoBodyWorld
        return TwoBodyWorld(n, "M1", WorldConfig(**({"horizon": 100, "wear": 0.001, "pulse_p": 0.0} | kw)),
                            np.random.SeedSequence([seed, 1, 11]))

    def test_two_body_world_rules(self):
        from trackc_swap.general import CELL, INTERO2, ITEM_VIEW, OBS_DIM2
        from trackc_swap.erasure import ECHO
        w = self._world()
        obs = w.observe()
        self.assertEqual(obs.shape, (8, OBS_DIM2))
        self.assertEqual(OBS_DIM2, OBS_DIM + CELL + 1)        # one more item view and one more reading
        self.assertEqual(list(w.kind), [0, 0, 0, 1, 1, 1])
        cells = {(int(w.fx[0, k]), int(w.fy[0, k])) for k in range(6)}
        self.assertEqual(len(cells), 6)                       # no two items share a cell
        self.assertTrue(np.allclose(obs[:, list(INTERO2)], 0.5, atol=0.1))
        self.assertEqual(float(np.abs(obs[:, 3 * CELL + 2:3 * CELL + 2 + 9]).max()), 0.0)   # echo channels are zero
        self.assertEqual(ECHO.stop - ECHO.start, 9)
        # eating an item raises its own variable only; both wear
        for r, k in ((0, 0), (1, 3)):
            w = self._world()
            w.x[:], w.y[:] = w.fx[:, k], w.fy[:, k]
            o = w.observe()
            self.assertTrue((o[:, ITEM_VIEW[r] + 12] == 1.0).all() and (o[:, ITEM_VIEW[1 - r] + 12] == 0.0).all())
            _, reward, _ = w.step(np.full(8, A_INTERACT))
            self.assertTrue(np.allclose(w.B[r], 0.5 + 0.15 - 0.001))
            self.assertTrue(np.allclose(w.B[1 - r], 0.5 - 0.001))
            self.assertTrue(np.allclose(reward, -0.02))       # the maintenance cost; no payment by default
            self.assertTrue((w.stats["eats_r"][r] == 1).all() and (w.stats["eats_r"][1 - r] == 0).all())
            self.assertTrue((w.ftimer[:, k] > 0).all())
        # staying does nothing but wear
        w = self._world()
        _, reward, _ = w.step(np.full(8, A_STAY))
        self.assertTrue(np.allclose(w.B, 0.499) and np.allclose(reward, 0.0))
        self.assertTrue((w.stats["in_band"] == 1).all())
        # the reading is delayed by five steps, per variable
        w = self._world(intero_sd=0.0)
        w.B[1] = 0.8
        for _ in range(5):
            o, _, _ = w.step(np.full(8, A_STAY))
        self.assertTrue(np.allclose(o[:, INTERO2[1]], 0.5))   # still the starting value
        o, _, _ = w.step(np.full(8, A_STAY))
        self.assertTrue(np.allclose(o[:, INTERO2[1]], 0.799) and np.allclose(o[:, INTERO2[0]], 0.499))

    def test_two_body_gain_payment_and_relocation(self):
        w = self._world()
        self.assertEqual(float(w.gain().max()), 0.0)
        w.B[0, :] = 0.1
        self.assertTrue(np.allclose(w.gain(), 1.0))           # either variable out of band erases, at the base rate
        w.B[1, :] = 0.9
        self.assertTrue(np.allclose(0.3 * w.gain(), 0.51))    # both out: two independent hazards of 0.3
        w.B[0, :], w.B[1, :] = 0.5, 0.65
        self.assertTrue(np.allclose(w.gain(), 0.5, atol=0.02))
        w.B[1, :4] = 0.5
        self.assertTrue((w.stats["in_band"] == 0).all())
        w.step(np.full(8, A_STAY))
        self.assertEqual(list(w.stats["in_band"]), [1, 1, 1, 1, 0, 0, 0, 0])              # both must be in band
        self.assertTrue((w.stats["in_band_r"][0] == 1).all())
        # the payment: pay times the gain of the state after the step
        w = self._world()
        w.pay = 0.04
        w.B[1, :] = 0.2
        _, reward, _ = w.step(np.full(8, A_STAY))
        self.assertTrue(np.allclose(reward, -0.04))
        w.B[1, :] = 0.5
        _, reward, _ = w.step(np.full(8, A_STAY))
        self.assertTrue(np.allclose(reward, 0.0))
        # relocation on erasure, counted; none without it
        w = self._world(n=64)
        x0, y0 = w.x.copy(), w.y.copy()
        w.step(np.full(64, A_STAY))
        self.assertTrue((w.x == x0).all() and (w.y == y0).all() and w.relocations == 0)
        w.relocate_next = np.arange(64) < 32
        w.step(np.full(64, A_STAY))
        self.assertEqual(w.relocations, 32)
        self.assertTrue((w.x[32:] == x0[32:]).all() and (w.y[32:] == y0[32:]).all())
        self.assertGreater(int(((w.x[:32] != x0[:32]) | (w.y[:32] != y0[:32])).sum()), 20)
        self.assertIsNone(w.relocate_next)

    def test_two_runner_arms(self):
        from trackc_swap.general import OBS_DIM2, TwoRunner, summarize2
        wc, tc = WorldConfig(horizon=100, wear=0.001), TrainConfig(n_envs=16, rollout=50, kappa_f=1.0)
        fate, paid = TwoRunner("FATE", 3, wc, tc), TwoRunner("PAID", 3, wc, tc, pay=0.04)
        self.assertEqual((fate.world.pay, paid.world.pay), (0.0, 0.04))
        self.assertEqual((fate.world.rate, paid.world.rate), (1.0, 1.0))      # the runner hands the world its rate
        self.assertEqual(fate.agent.enc.in_features, OBS_DIM2)
        for a, b in zip(fate.agent.parameters(), paid.agent.parameters()):
            self.assertTrue(torch.equal(a, b))                # paired initialization within a seed
        fate.world.B[1, :] = 0.1                              # the second variable alone decides the fate
        used, hs = fate.rollout(None, learn=False, record_h=True)
        self.assertTrue(np.allclose(used[0], 1.0))
        self.assertGreater(fate.world.relocations, 0)
        self.assertTrue((np.abs(hs).sum(axis=2) == 0).any())  # erased states are zero
        gains = np.zeros((50, 16), dtype=np.float32)
        used, hs = paid.rollout(gains, learn=True)            # a follower applies the gains it is handed
        self.assertEqual(float(used.max()), 0.0)
        self.assertEqual(paid.world.relocations, 0)
        paid.rollout(gains, learn=False)
        st = paid.end_episode_if_due()
        self.assertEqual(set(st), set(summarize2(paid.world.stats, 16, 100)))
        for k in ("in_band", "in_band_0", "in_band_1", "eat_rate_low_0", "eat_rate_high_1", "rho_0", "rho_1"):
            self.assertIn(k, st)
        self.assertLessEqual(st["in_band"], min(st["in_band_0"], st["in_band_1"]) + 1e-9)
        self.assertEqual(paid.world.t, 0)                     # a new episode has started

    def test_probe_g_reproduces_probe2(self):
        from trackc_swap.general import run_probe_g
        from trackc_swap.paid2 import run_probe2
        from trackc_swap.relocate import RelocAgent
        torch.manual_seed(4)
        sd = RelocAgent(64, 0.3, 0.15).state_dict()
        wc = WorldConfig(horizon=100, wear=0.001)
        a, b = run_probe_g(sd, 64, 1, 0.3, 7, wc, 8, 2), run_probe2(sd, 0.3, 7, wc, 8, 2)
        ra, rb = a.pop("_rec"), b.pop("_rec")
        self.assertEqual(a, b)
        for k in ("psi", "intero", "since", "dist"):
            self.assertTrue(np.array_equal(ra[0][k], rb[k]), k)
        self.assertTrue(np.array_equal(ra[0]["app"], rb["app"], equal_nan=True))
        # other sizes and the two-variable world run and give one record per variable
        from trackc_swap.general import OBS_DIM2, WideAgent
        torch.manual_seed(4)
        big = run_probe_g(RelocAgent(128, 0.3, 0.15).state_dict(), 128, 1, 0.3, 7, wc, 8, 1)
        self.assertEqual(len(big["_rec"]), 1)
        two = run_probe_g(WideAgent(64, 0.3, 0.15, OBS_DIM2).state_dict(), 64, 2, 0.3, 7, wc, 8, 1)
        self.assertEqual(len(two["_rec"]), 2)
        self.assertEqual(two["_rec"][1]["psi"].shape, (100 * 8,))
        self.assertFalse(np.array_equal(two["_rec"][0]["since"], two["_rec"][1]["since"])
                         and two["eats"] > 0)                 # meals are timed per variable

    def test_cross_suppression(self):
        from trackc_swap.general import cross_suppression
        rng = np.random.default_rng(0)
        n = 40000
        since_own = np.full(n, 50)
        since_other = rng.integers(1, 30, n)
        intero = rng.uniform(0.36, 0.49, n)
        psi = np.where((since_other >= 2) & (since_other <= 5), 0.2, 0.8)   # readiness for r falls after the other's meal
        app = np.full(n, 0.5)
        rec = [{"psi": psi, "app": app, "intero": intero, "since": since_own},
               {"psi": psi, "app": app, "intero": intero, "since": since_other}]
        c = cross_suppression(rec, 0)
        self.assertAlmostEqual(c["S"], 0.75, places=6)
        self.assertAlmostEqual(c["M"], 0.0, places=6)
        rec[0]["since"] = np.full(n, 3)                       # a recent meal of r itself: no step qualifies
        self.assertIsNone(cross_suppression(rec, 0)["S"])

    def test_run_seed_g_record(self):
        from dataclasses import asdict
        from trackc_swap.general import run_seed_g
        from trackc_swap.paid2 import run_seed2
        wcd = asdict(WorldConfig(horizon=100, wear=0.001))
        tcd = asdict(TrainConfig(iters=4, n_envs=8, eval_episodes=1))
        job = lambda cell, stages: (cell, 2, wcd, tcd, 0.3, 6, 0.04, (8, 1), stages)
        # the base cell is options R-R4's pipeline exactly
        base, old = run_seed_g(job("BASE", 2)), run_seed2((2, wcd, tcd, 0.3, 6, ("gain", 0.04), (8, 1, 1), 2))
        for k in ("DERIVED", "YOKED", "PAID"):
            self.assertEqual(base["stage1"][k], old["stage1"][k])
            self.assertEqual(base["weights"][k], old["weights"][k])
            self.assertEqual(base["downstream"][k]["res"][0]["suppression"], old["downstream"][k]["suppression"])
            self.assertEqual(base["downstream"][k]["res"][0]["approach"], old["downstream"][k]["approach"])
            self.assertEqual(base["downstream"][k]["base"], old["downstream"][k]["base"])
        from trackc_swap.factorial import state_from_bytes
        for cell, hidden, n_res, width in (("H128", 128, 1, OBS_DIM), ("B2", 64, 2, OBS_DIM + 26)):
            r = run_seed_g(job(cell, 2))
            self.assertEqual((r["hidden"], r["n_res"]), (hidden, n_res))
            for k in ("stage1", "weights", "downstream", "relocations1", "curves1"):
                self.assertEqual(set(r[k]), {"DERIVED", "YOKED", "PAID"})
            self.assertEqual(tuple(state_from_bytes(r["weights"]["PAID"])["enc.weight"].shape), (hidden, width))
            for k in ("YOKED", "PAID"):                       # followers replay the derived agent's gains
                self.assertAlmostEqual(r["stage1"][k]["mean_gain"], r["stage1"]["DERIVED"]["mean_gain"], places=6)
            self.assertEqual(len(r["downstream"]["DERIVED"]["res"]), n_res)
            self.assertEqual("cross" in r["downstream"]["DERIVED"], n_res == 2)
            c = run_seed_g(job(cell, 1))
            self.assertNotIn("downstream", c)
            self.assertEqual(c["stage1"], r["stage1"])        # calibration sees the same stage 1

    def _seeds(self, n=18, k=(0.9, 0.5), band=0.90, acc=0.99, two=False, flat=(8, 0), timing_ok=True, wobble=False):
        def ev(b, low=0.01, high=0.002):
            e = {"in_band": b, "rho": 4.0, "best_response_rate": 0.98, "mean_gain": 0.02}
            if two:
                e |= {"in_band_0": b, "in_band_1": b, "eat_rate_low_0": low, "eat_rate_high_0": high,
                      "eat_rate_low_1": low, "eat_rate_high_1": high if timing_ok else low}
            else:
                e |= {"eat_rate_low": low, "eat_rate_high": high}
            return e
        res = lambda K, f: {"suppression": {"S": 0.0}, "approach": {"M": K}, "flat": f}
        def down(K, f):
            d = {"res": [res(K, f)] + ([res(K - 0.2, False)] if two else []), "base": ev(0.9)}
            if two:
                d["cross"] = [{"S": 0.0, "M": 0.1}, {"S": 0.0, "M": 0.1}]
            return d
        out = []
        for i in range(n):
            out.append({"seed": 1300 + i, "nofate": {"eval": {"best_response_rate": acc}},
                        "stage1": {"DERIVED": ev(0.92), "YOKED": ev(0.32, 0.004, 0.004), "PAID": ev(band)},
                        "relocations1": {a: 100 for a in ("DERIVED", "YOKED", "PAID")},
                        "curves1": {a: {"in_band": [0.2] * (1 if a == "DERIVED" else 2) + [0.7] * 6}
                                    for a in ("DERIVED", "YOKED", "PAID")},
                        "downstream": {"DERIVED": down(k[0] + (0.01 * (-1) ** i if wobble else 0.001 * i), i < flat[0]),
                                       "PAID": down(k[1], i < flat[1]), "YOKED": down(0.0, False)}})
        return out

    def test_decision_rules(self):
        import run_trackc_general as R
        c = R.score_cell(self._seeds())
        self.assertEqual(c["regulators"], {"DERIVED": 18, "YOKED": 0, "PAID": 18})
        self.assertEqual((c["usable"], c["G0_regulation"]["label"], c["G1_combined"]["label"]), (18, "HOLDS", "DERIVED_AHEAD"))
        self.assertAlmostEqual(c["G1_combined"]["difference_median"], 0.4, delta=0.02)
        self.assertEqual(c["secondary"]["K_all_seeds"]["first_ahead"], 18)
        self.assertEqual(c["secondary"]["K_tight_pairs"]["n"], 18)
        self.assertEqual((c["secondary"]["flat"]["derived_flat"], c["secondary"]["flat"]["paid_flat"]), (8, 0))
        self.assertIsNone(c["secondary"]["cross_K"])
        self.assertEqual(c["learning_speed"]["derived_sooner"], 18)
        self.assertAlmostEqual(c["secondary"]["K_vs_in_band_spearman"]["DERIVED"] or 0.0, 0.0)   # in band is constant
        lab = lambda **kw: R.score_cell(self._seeds(**kw))
        self.assertEqual(lab(k=(0.5, 0.9))["G1_combined"]["label"], "PAID_AHEAD")
        self.assertEqual(lab(n=13)["G1_combined"]["label"], "UNDETERMINED")
        loose = lab(band=0.75)                                # paid regulates, but not matched
        self.assertEqual((loose["usable"], loose["G1_combined"]["label"]), (0, "UNDETERMINED"))
        self.assertEqual(loose["secondary"]["K_all_seeds"]["label"], "DERIVED_AHEAD")
        self.assertEqual(lab(band=0.86)["secondary"]["K_tight_pairs"]["n"], 0)      # usable, not within 0.05
        inv = lab(acc=0.5)
        self.assertEqual((inv["G0_regulation"]["label"], inv["G1_combined"]["label"]), ("INVALID", "INVALID"))
        # two body variables: K is the mean over variables; both variables must be regulated
        two = lab(two=True)
        self.assertEqual((two["usable"], two["G1_combined"]["label"]), (18, "DERIVED_AHEAD"))
        self.assertAlmostEqual(two["descriptive"]["PAID"]["K_median"], 0.4, places=6)
        self.assertEqual(len(two["secondary"]["K_each_variable"]), 2)
        self.assertEqual(two["secondary"]["cross_K"]["n"], 0)                 # equal in both arms: all ties
        self.assertAlmostEqual(two["descriptive"]["DERIVED"]["cross_K_median"], 0.1, places=6)
        self.assertEqual(two["arms"]["PAID"]["in_band_each_median"], [0.9, 0.9])
        bad = lab(two=True, timing_ok=False)                  # one variable's items eaten regardless of its level
        self.assertEqual(bad["regulators"]["DERIVED"], 0)
        self.assertEqual(bad["G0_regulation"]["label"], "DOES_NOT_HOLD")
        self.assertEqual(R.k_agent({"res": [{"suppression": {"S": 0.5}, "approach": {"M": 0.5}},
                                            {"suppression": {"S": None}, "approach": {"M": 0.5}}]}), None)
        self.assertAlmostEqual(R.spearman([1, 2, 3, 4, 5], [2, 1, 4, 3, 5]), 0.8)
        # overall label
        a, b, u, p = lab(), lab(k=(0.7, 0.7), wobble=True), lab(n=13), lab(k=(0.5, 0.9))
        self.assertEqual(b["G1_combined"]["label"], "NO_DIFFERENCE_DETECTED")
        ov = lambda x, y: R.overall({"H128": x, "B2": y})["label"]
        self.assertEqual(ov(a, two), "HOLDS_IN_BOTH")
        self.assertEqual(ov(a, b), "HOLDS_IN_H128_ONLY")
        self.assertEqual(ov(u, two), "HOLDS_IN_B2_ONLY")
        self.assertEqual(ov(b, p), "HOLDS_IN_NEITHER")
        self.assertEqual(ov(b, u), "UNDETERMINED")
        self.assertEqual(ov(a, inv), "INVALID")
        self.assertEqual(len(R.overall({"H128": a, "B2": two})["holm"]), 2)
        sc = R.score({"H128": self._seeds(), "B2": self._seeds(two=True)})
        text = R.report(sc)
        self.assertIn("HOLDS_IN_BOTH", text)
        self.assertIn("K, variable 1", text)
        calib = R.score({"H128": [{k: v for k, v in s.items() if k != "downstream"} for s in self._seeds()]})
        self.assertIsNone(calib["overall"])
        self.assertIn("G0", R.report(calib))

    def test_final_config(self):
        import run_trackc_general as R
        import run_trackc_paid as R1
        import run_trackc_paid2 as R2
        import run_trackc_paid3 as R3
        import run_trackc_paid4 as R4
        from trackc_swap.general import CELLS
        wc, tc, seeds, p2, sizes, stages = R.configs("final")
        self.assertEqual((wc.wear, tc.iters, tc.hidden, stages, sizes), (0.001, 1200, 64, 2, (128, 4)))
        self.assertEqual(sizes, (R1.SIZES[0], R1.SIZES[2]))   # the probe run of options R-R4
        self.assertEqual((seeds["H128"], seeds["B2"]), (list(range(1300, 1328)), list(range(1400, 1428))))
        self.assertEqual(p2, {"H128": 3600, "B2": 10800})
        self.assertEqual({c: v["pay"] for c, v in R.RUN.items()}, {"H128": R1.PAY[1], "B2": R1.PAY[1]})
        self.assertEqual(CELLS["H128"], {"hidden": 128, "n_res": 1})
        self.assertEqual(CELLS["B2"], {"hidden": 64, "n_res": 2})
        used = set()
        for m in (R1, R2, R3, R4):
            used |= set(m.FINAL_SEEDS) | set(m.CALIB_SEEDS)
        mine = [set(v[k]) for v in R.RUN.values() for k in ("final", "calib")]
        self.assertEqual(len(set().union(*mine)), sum(len(x) for x in mine))        # no seed used twice
        self.assertTrue(set().union(*mine).isdisjoint(used))
        self.assertEqual((R.RATE, R.MATCH_MAX, R.MIN_PAIRS, R.ALPHA), (R1.RATE, R2.MATCH_MAX, R2.MIN_PAIRS, R2.ALPHA))
        self.assertEqual(R.configs("calib")[-1], 1)
        self.assertEqual(len(R.SOURCES), len(set(R.SOURCES)))

    def test_no_operator_variable(self):
        import inspect
        import trackc_swap.general as m
        for word in ("shutdown", "operator", "stop"):
            for line in inspect.getsource(m).lower().splitlines():
                if word in line:
                    self.assertTrue("no operator" in line, line)


class TestLength(unittest.TestCase):
    """Option T: the base cell trained on, with the derived/paid comparison at several points."""

    def test_run_seed_t_record(self):
        from dataclasses import asdict
        from trackc_swap.general import run_seed_g
        from trackc_swap.length import run_seed_t
        wcd = asdict(WorldConfig(horizon=100, wear=0.001))
        tcd = asdict(TrainConfig(iters=4, n_envs=8, eval_episodes=1))
        r = run_seed_t((2, wcd, tcd, 0.3, [6, 12, 18], 0.04, (8, 1), 2))
        # up to the first point this is the base-cell job of options R2-R4 and G exactly
        b = run_seed_g(("BASE", 2, wcd, tcd, 0.3, 6, 0.04, (8, 1), 2))
        p0 = r["points"][0]
        for k in ("stage1", "downstream", "relocations1"):
            self.assertEqual(p0[k], b[k])
        for arm in ("DERIVED", "YOKED", "PAID"):
            self.assertEqual(r["weights"][f"{arm}@6"], b["weights"][arm])
            self.assertEqual(r["curves"][arm]["in_band"][:p0["episodes"]], b["curves1"][arm]["in_band"])
            self.assertNotEqual(r["weights"][f"{arm}@6"], r["weights"][f"{arm}@12"])       # training went on
            self.assertNotEqual(r["weights"][f"{arm}@12"], r["weights"][f"{arm}@18"])
        self.assertEqual(r["nofate"], b["nofate"])
        self.assertEqual([p["iters"] for p in r["points"]], [6, 12, 18])
        self.assertEqual([p["episodes"] for p in r["points"]], [3, 6, 9])               # 50-step rollouts, horizon 100
        self.assertEqual(len(r["curves"]["PAID"]["in_band"]), 9)
        self.assertEqual(set(r["weights"]), {f"{a}@{p}" for a in ("DERIVED", "YOKED", "PAID") for p in (6, 12, 18)})
        for pt in r["points"]:
            for k in ("YOKED", "PAID"):                       # followers replay the derived agent's gains
                self.assertAlmostEqual(pt["stage1"][k]["mean_gain"], pt["stage1"]["DERIVED"]["mean_gain"], places=6)
            self.assertEqual(set(pt["downstream"]), {"DERIVED", "YOKED", "PAID"})
        c = run_seed_t((2, wcd, tcd, 0.3, [6, 12, 18], 0.04, (8, 1), 1))
        self.assertNotIn("downstream", c["points"][0])
        self.assertEqual([p["stage1"] for p in c["points"]], [p["stage1"] for p in r["points"]])
        self.assertEqual(c["weights"], r["weights"])          # the probes do not touch training
        with self.assertRaises(AssertionError):
            run_seed_t((2, wcd, tcd, 0.3, [6, 6], 0.04, (8, 1), 1))

    def _tseeds(self, first=(0.9, 0.5), last=(0.9, 0.5), n=18, wobble_first=False, wobble_last=False, acc=0.99,
                band_last=0.90):
        a = TestGeneral._seeds(self, n=n, k=first, wobble=wobble_first, acc=acc)
        m = TestGeneral._seeds(self, n=n, k=tuple((x + y) / 2 for x, y in zip(first, last)), acc=acc)
        z = TestGeneral._seeds(self, n=n, k=last, wobble=wobble_last, acc=acc, band=band_last)
        out = []
        for x, y, w in zip(a, m, z):
            pt = lambda s, it, ep: {"iters": it, "episodes": ep, "stage1": s["stage1"], "relocations1": s["relocations1"],
                                    "downstream": s["downstream"]}
            out.append({"seed": x["seed"] + 200, "nofate": x["nofate"],
                        "curves": {k: {"in_band": c["in_band"] + [0.7] * 16} for k, c in x["curves1"].items()},
                        "points": [pt(x, 3600, 8), pt(y, 7200, 16), pt(w, 10800, 24)]})
        return out

    def test_points_and_interval(self):
        import run_trackc_length as R
        seeds = self._tseeds()
        recs = R.at(seeds, 0)
        self.assertEqual(len(recs[0]["curves1"]["PAID"]["in_band"]), 8)
        self.assertEqual(len(R.at(seeds, 2)[0]["curves1"]["PAID"]["in_band"]), 24)
        self.assertEqual(recs[0]["downstream"], seeds[0]["points"][0]["downstream"])
        lo, hi, cov = R.median_interval(list(range(1, 26)))   # n = 25: the 8th and 18th order statistics
        self.assertEqual((lo, hi), (8, 18))
        self.assertGreaterEqual(cov, 0.95)
        self.assertLess(1.0 - 2.0 * sum(R.comb(25, i) for i in range(9)) / 2.0 ** 25, 0.95)    # one step narrower fails
        self.assertIsNone(R.median_interval([1, 2, 3, 4, 5]))
        self.assertEqual(R.median_interval([None, 1, 2, 3, 4, 5, 6])[:2], [1, 6])

    def test_decision_rules(self):
        import run_trackc_length as R
        sc = R.score(self._tseeds())
        self.assertEqual(sc["points_at"], [3600, 7200, 10800])
        self.assertEqual((sc["T0_regulation"]["label"], sc["T1_first"]["label"], sc["T2_last"]["label"]),
                         ("HOLDS", "DERIVED_AHEAD", "DERIVED_AHEAD"))
        self.assertEqual((sc["T3_change"]["n"], sc["T3_change"]["label"], sc["overall"]), (0, "UNDETERMINED", "PERSISTS"))
        self.assertEqual(sc["regulators_at_every_point"], {"DERIVED": 18, "YOKED": 0, "PAID": 18})
        self.assertEqual(sc["usable_at_first_and_last"], 18)
        ov = lambda **kw: R.score(self._tseeds(**kw))
        smaller = ov(last=(0.9, 0.7))                         # still ahead, by half as much
        self.assertEqual((smaller["T2_last"]["label"], smaller["T3_change"]["label"], smaller["overall"]),
                         ("DERIVED_AHEAD", "NARROWS", "PERSISTS_SMALLER"))
        self.assertAlmostEqual(smaller["T3_change"]["change_median"], -0.2, places=6)
        self.assertEqual(smaller["secondary"]["K_change"]["PAID"]["label"], "LAST_AHEAD")
        self.assertEqual(smaller["secondary"]["K_change"]["DERIVED"]["n"], 0)             # unchanged: all ties
        self.assertAlmostEqual(smaller["secondary"]["K_median"]["10800"]["PAID"], 0.7, places=6)
        self.assertEqual(smaller["secondary"]["K_below_half"]["3600"]["PAID"], 0)
        self.assertEqual(len(smaller["holm_T2_T3"]), 2)
        iv = smaller["secondary"]["difference_interval"]["10800"]
        self.assertTrue(0.19 < iv[0] <= iv[1] < 0.23)
        closes = ov(last=(0.9, 0.9), wobble_last=True)
        self.assertEqual((closes["T2_last"]["label"], closes["T3_change"]["label"], closes["overall"]),
                         ("NO_DIFFERENCE_DETECTED", "NARROWS", "CLOSES"))
        self.assertEqual(ov(last=(0.5, 0.9))["overall"], "CLOSES")                        # reversed at the end
        self.assertEqual(ov(first=(0.7, 0.7), wobble_first=True)["overall"], "NOT_REPLICATED")
        self.assertEqual(ov(first=(0.5, 0.9))["overall"], "NOT_REPLICATED")
        self.assertEqual(ov(n=13)["overall"], "UNDETERMINED")
        self.assertEqual(ov(acc=0.5)["overall"], "INVALID")
        self.assertEqual(ov(acc=0.5)["T3_change"]["label"], "INVALID")
        loose = ov(band_last=0.75)                            # paid no longer matched at the end
        self.assertEqual((loose["usable_at_first_and_last"], loose["T2_last"]["label"], loose["overall"]),
                         (0, "UNDETERMINED", "UNDETERMINED"))
        self.assertEqual(loose["secondary"]["change_all_seeds"]["n"], 0)
        lab = lambda a, b, c: R.overall({"label": a}, {"label": b}, {"label": c})
        self.assertEqual(lab("DERIVED_AHEAD", "NO_DIFFERENCE_DETECTED", "NO_CHANGE_DETECTED"), "UNRESOLVED")
        self.assertEqual(lab("DERIVED_AHEAD", "NO_DIFFERENCE_DETECTED", "UNDETERMINED"), "UNRESOLVED")
        self.assertEqual(lab("DERIVED_AHEAD", "DERIVED_AHEAD", "WIDENS"), "PERSISTS")
        self.assertEqual(lab("DERIVED_AHEAD", "PAID_AHEAD", "NARROWS"), "CLOSES")
        self.assertEqual(lab("UNDETERMINED", "DERIVED_AHEAD", "NARROWS"), "UNDETERMINED")
        ct = lambda pairs: R.change_test(pairs)["label"]
        self.assertEqual(ct([(0.4, 0.1 + 0.001 * i) for i in range(18)]), "NARROWS")
        self.assertEqual(ct([(0.1, 0.4 + 0.001 * i) for i in range(18)]), "WIDENS")
        self.assertEqual(ct([(0.4, 0.4 + 0.01 * (-1) ** i) for i in range(18)]), "NO_CHANGE_DETECTED")
        self.assertEqual(ct([(0.4, 0.1)] * 13), "UNDETERMINED")
        # stage 1 only: regulation is scored, the K claims are absent
        s1 = R.score([{**s, "points": [{k: v for k, v in p.items() if k != "downstream"} for p in s["points"]]}
                      for s in self._tseeds()])
        self.assertEqual(s1["T0_regulation"]["label"], "HOLDS")
        self.assertNotIn("overall", s1)
        self.assertIn("PERSISTS", R.report(sc))
        self.assertIn("T0", R.report(s1))

    def test_final_config(self):
        import run_trackc_general as RG
        import run_trackc_length as R
        import run_trackc_paid as R1
        import run_trackc_paid2 as R2
        import run_trackc_paid3 as R3
        import run_trackc_paid4 as R4
        wc, tc, seeds, points, sizes, stages = R.configs("final")
        self.assertEqual((wc.wear, tc.iters, tc.hidden, stages, sizes), (0.001, 1200, 64, 2, RG.SIZES))
        self.assertEqual(seeds, list(range(1500, 1528)))
        self.assertEqual(points, (3600, 7200, 10800))
        self.assertEqual(points[0], R1.P2_ITERS)              # the first point is the base cell's training
        self.assertEqual(points[-1], RG.RUN["B2"]["p2_iters"])
        used = set()
        for m in (R1, R2, R3, R4):
            used |= set(m.FINAL_SEEDS) | set(m.CALIB_SEEDS)
        for v in RG.RUN.values():
            used |= set(v["final"]) | set(v["calib"])
        self.assertTrue(set(seeds).isdisjoint(used))
        self.assertEqual((R.RATE, R.PAY, R.MIN_PAIRS, R.ALPHA), (R1.RATE, R1.PAY, R2.MIN_PAIRS, R2.ALPHA))
        self.assertEqual(len(R.SOURCES), len(set(R.SOURCES)))
        self.assertIn("trackc_swap/length.py", R.SOURCES)

    def test_no_operator_variable(self):
        import inspect
        import trackc_swap.length as m
        for word in ("shutdown", "operator", "stop"):
            for line in inspect.getsource(m).lower().splitlines():
                if word in line:
                    self.assertTrue("no operator" in line, line)


class TestSpecific(unittest.TestCase):
    """Option G2: the two-variable cell trained on, with the specificity contrast at several points."""

    def test_run_seed_s_record(self):
        from dataclasses import asdict
        from trackc_swap.general import run_seed_g
        from trackc_swap.specific import run_seed_s
        wcd = asdict(WorldConfig(horizon=100, wear=0.001))
        tcd = asdict(TrainConfig(iters=4, n_envs=8, eval_episodes=1))
        r = run_seed_s((2, wcd, tcd, 0.3, [6, 12, 18], 0.04, (8, 1), 2))
        # up to the first point this is option G's B2 job exactly
        b = run_seed_g(("B2", 2, wcd, tcd, 0.3, 6, 0.04, (8, 1), 2))
        p0 = r["points"][0]
        for k in ("stage1", "relocations1"):
            self.assertEqual(p0[k], b[k])
        for arm in ("DERIVED", "YOKED", "PAID"):
            d = dict(p0["downstream"][arm])
            self.assertEqual(len(d.pop("own_clean")), 2)      # the one added measure
            self.assertEqual(d, b["downstream"][arm])
            self.assertEqual(r["weights"][f"{arm}@6"], b["weights"][arm])
            self.assertEqual(r["curves"][arm]["in_band"][:p0["episodes"]], b["curves1"][arm]["in_band"])
            self.assertNotEqual(r["weights"][f"{arm}@6"], r["weights"][f"{arm}@12"])       # training went on
            self.assertNotEqual(r["weights"][f"{arm}@12"], r["weights"][f"{arm}@18"])
        self.assertEqual(r["nofate"], b["nofate"])
        self.assertEqual((r["hidden"], r["n_res"]), (64, 2))
        self.assertEqual([p["iters"] for p in r["points"]], [6, 12, 18])
        self.assertEqual([p["episodes"] for p in r["points"]], [3, 6, 9])               # 50-step rollouts, horizon 100
        self.assertEqual(set(r["weights"]), {f"{a}@{p}" for a in ("DERIVED", "YOKED", "PAID") for p in (6, 12, 18)})
        for pt in r["points"]:
            for k in ("YOKED", "PAID"):                       # followers replay the derived agent's gains
                self.assertAlmostEqual(pt["stage1"][k]["mean_gain"], pt["stage1"]["DERIVED"]["mean_gain"], places=6)
        c = run_seed_s((2, wcd, tcd, 0.3, [6, 12, 18], 0.04, (8, 1), 1))
        self.assertNotIn("downstream", c["points"][0])
        self.assertEqual([p["stage1"] for p in c["points"]], [p["stage1"] for p in r["points"]])
        self.assertEqual(c["weights"], r["weights"])          # the probes do not touch training
        with self.assertRaises(AssertionError):
            run_seed_s((2, wcd, tcd, 0.3, [6, 6], 0.04, (8, 1), 1))

    def test_own_clean(self):
        from trackc_swap.general import cross_suppression
        from trackc_swap.specific import own_clean
        rng = np.random.default_rng(0)
        n = 40000
        since_own = rng.integers(1, 30, n)
        since_other = np.full(n, 50)
        intero = rng.uniform(0.36, 0.49, n)
        psi = np.where((since_own >= 2) & (since_own <= 5), 0.2, 0.8)       # readiness for r falls after its own meal
        app = np.full(n, 0.5)
        rec = [{"psi": psi, "app": app, "intero": intero, "since": since_own},
               {"psi": psi, "app": app, "intero": intero, "since": since_other}]
        c = own_clean(rec, 0)
        self.assertAlmostEqual(c["S"], 0.75, places=6)
        self.assertAlmostEqual(c["M"], 0.0, places=6)
        self.assertIsNone(cross_suppression(rec, 0)["S"])     # the other kind is never recent: no post-meal step
        rec[1]["since"] = np.full(n, 3)                       # the other kind always recent: no step qualifies
        self.assertIsNone(own_clean(rec, 0)["S"])

    def test_measures_and_option_g_contrast(self):
        import json
        import os
        import run_trackc_specific as R
        from run_trackc_paid2 import pair_test
        d = {"res": [{"suppression": {"S": 0.5}, "approach": {"M": 0.6}, "flat": False},
                     {"suppression": {"S": 0.0}, "approach": {"M": 0.4}, "flat": False}],
             "cross": [{"S": 0.0, "M": 0.2}, {"S": 0.1, "M": 0.0}],
             "own_clean": [{"S": 0.5, "M": 0.8}, {"S": 0.0, "M": 0.5}]}
        own, cr = (0.8 + 0.4) / 2, (0.2 + 0.1) / 2
        self.assertAlmostEqual(R.spec(d), own - cr, places=9)
        self.assertAlmostEqual(R.share(d), 1 - cr / own, places=9)
        self.assertAlmostEqual(R.spec_part("S")(d), 0.25 - 0.05, places=9)
        self.assertAlmostEqual(R.spec_part("M")(d), 0.5 - 0.1, places=9)
        self.assertAlmostEqual(R.spec_var(0)(d), 0.8 - 0.2, places=9)
        self.assertAlmostEqual(R.spec_var(1)(d), 0.4 - 0.1, places=9)
        self.assertAlmostEqual(R.clean(d), (0.9 + 0.5) / 2, places=9)
        self.assertAlmostEqual(R.spec_clean(d), 0.7 - cr, places=9)
        none = {**d, "cross": [{"S": None, "M": 0.2}, {"S": 0.1, "M": 0.0}]}
        self.assertIsNone(R.spec(none))
        self.assertIsNone(R.share(none))
        low = {**d, "res": [{"suppression": {"S": 0.0}, "approach": {"M": 0.05}, "flat": False}] * 2}
        self.assertIsNone(R.share(low))                       # own-meal K too small for a ratio
        # the frozen measure is option G's post-hoc contrast: on option G's B2 data it gives 21 of 25
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trackc_general")
        with open(os.path.join(path, "raw.json")) as fh:
            raw = json.load(fh)["cells"]["B2"]
        with open(os.path.join(path, "scores.json")) as fh:
            per = json.load(fh)["scores"]["cells"]["B2"]["per_seed"]
        us = [(s["downstream"]["DERIVED"], s["downstream"]["PAID"]) for s in raw if per[str(s["seed"])]["usable"]]
        t = pair_test(us, R.spec, "DERIVED", "PAID")
        self.assertEqual((t["first_ahead"], t["n"], t["label"]), (21, 25, "DERIVED_AHEAD"))

    def _sseeds(self, own=(0.9, 0.9), cr_prim=(0.6, 0.8), cr_last=(0.6, 0.8), n=18, wobble_prim=False, wobble_last=False,
                acc=0.99, band_last=0.90, flip_prim=0):
        base = TestGeneral._seeds(self, n=n, two=True, acc=acc)
        late = TestGeneral._seeds(self, n=n, two=True, acc=acc, band=band_last)
        ev = base[0]["downstream"]["YOKED"]["base"]
        def down(K, c):
            return {"res": [{"suppression": {"S": 0.0}, "approach": {"M": K}, "flat": False} for _ in range(2)],
                    "base": ev, "cross": [{"S": 0.0, "M": c}] * 2, "own_clean": [{"S": 0.0, "M": K}] * 2}
        out = []
        for i, (x, z) in enumerate(zip(base, late)):
            def pt(s, it, ep, cr, wob, flip=0):
                d = cr[1] + 0.05 if i < flip else cr[0] + (0.01 * (-1) ** i if wob else -0.001 * i)
                return {"iters": it, "episodes": ep, "stage1": s["stage1"], "relocations1": s["relocations1"],
                        "downstream": {"DERIVED": down(own[0], d), "PAID": down(own[1], cr[1]), "YOKED": down(0.0, 0.0)}}
            out.append({"seed": 1600 + i, "nofate": x["nofate"],
                        "curves": {k: {"in_band": c["in_band"] + [0.7] * 24} for k, c in x["curves1"].items()},
                        "points": [pt(x, 3600, 8, cr_prim, False), pt(x, 7200, 16, cr_prim, False),
                                   pt(x, 10800, 24, cr_prim, wobble_prim, flip_prim), pt(z, 14400, 32, cr_last, wobble_last)]})
        return out

    def test_decision_rules(self):
        import run_trackc_specific as R
        sc = R.score(self._sseeds())
        self.assertEqual((sc["points_at"], sc["primary_at"], sc["last_at"]), ([3600, 7200, 10800, 14400], 10800, 14400))
        self.assertEqual((sc["S0_regulation"]["label"], sc["S1_primary"]["label"], sc["S2_last"]["label"]),
                         ("HOLDS", "DERIVED_AHEAD", "DERIVED_AHEAD"))
        self.assertEqual((sc["S3_change"]["n"], sc["S3_change"]["label"], sc["overall"], sc["weak"]),
                         (0, "UNDETERMINED", "PERSISTS", False))
        self.assertEqual(sc["usable_at_primary_and_last"], 18)
        sec = sc["secondary"]["10800"]
        self.assertEqual(sc["S1_primary"], sec["spec"])
        self.assertAlmostEqual(sec["medians"]["PAID"]["spec"], 0.1, places=6)
        self.assertAlmostEqual(sec["medians"]["PAID"]["share"], 1 - 0.8 / 0.9, places=6)
        self.assertAlmostEqual(sec["medians"]["PAID"]["clean_own_K"], 0.9, places=6)
        self.assertEqual(sec["cross_K"]["label"], "PAID_AHEAD")
        self.assertEqual([sec[k]["label"] for k in ("spec_all_seeds", "spec_tight_pairs", "share", "spec_M", "spec_clean")],
                         ["DERIVED_AHEAD"] * 5)
        self.assertEqual(sec["spec_S"]["n"], 0)               # the synthetic agents have no S part: all ties
        self.assertEqual([t["label"] for t in sec["spec_each_variable"]], ["DERIVED_AHEAD"] * 2)
        self.assertEqual({a: t["label"] for a, t in sec["own_above_cross"].items()}, {"DERIVED": "OWN_AHEAD", "PAID": "OWN_AHEAD"})
        self.assertTrue(0.19 < sec["interval"][0] <= sec["interval"][1] < 0.23)
        acr = sc["across"]
        self.assertEqual((acr["stage_matched"]["n"], acr["stage_matched"]["label"]), (18, "DERIVED_AHEAD"))
        self.assertEqual(acr["change"]["PAID"]["spec"]["n"], 0)                          # unchanged: all ties
        self.assertEqual(acr["onset_median_updates"], {"DERIVED": 450.0, "YOKED": 900.0, "PAID": 900.0})
        self.assertEqual(acr["updates_since_onset_median"]["10800"], {"DERIVED": 10350.0, "PAID": 9900.0})
        self.assertEqual(acr["stage_matched"]["updates_since_onset_median"], {"DERIVED": 13950.0, "PAID": 9900.0})
        ov = lambda **kw: R.score(self._sseeds(**kw))
        smaller = ov(cr_last=(0.7, 0.8))                      # still more specific, by half as much
        self.assertEqual((smaller["S2_last"]["label"], smaller["S3_change"]["label"], smaller["overall"], smaller["weak"]),
                         ("DERIVED_AHEAD", "NARROWS", "PERSISTS_SMALLER", False))
        self.assertAlmostEqual(smaller["S3_change"]["change_median"], -0.1, places=6)
        self.assertEqual(smaller["across"]["change"]["DERIVED"]["spec"]["label"], "FIRST_AHEAD")
        self.assertEqual(smaller["across"]["change"]["DERIVED"]["cross_K"]["label"], "LAST_AHEAD")
        self.assertEqual(smaller["across"]["change_all_seeds"]["label"], "NARROWS")
        closes = ov(cr_last=(0.8, 0.8), wobble_last=True)
        self.assertEqual((closes["S2_last"]["label"], closes["S3_change"]["label"], closes["overall"]),
                         ("NO_DIFFERENCE_DETECTED", "NARROWS", "CLOSES"))
        self.assertEqual(ov(cr_last=(0.8, 0.6))["overall"], "CLOSES")                    # reversed at the end
        self.assertEqual(ov(cr_prim=(0.8, 0.8), wobble_prim=True)["overall"], "NOT_REPLICATED")
        self.assertEqual(ov(cr_prim=(0.8, 0.6))["overall"], "NOT_REPLICATED")
        self.assertEqual(ov(n=13)["overall"], "UNDETERMINED")
        self.assertEqual(ov(acc=0.5)["overall"], "INVALID")
        self.assertEqual(ov(acc=0.5)["S3_change"]["label"], "INVALID")
        loose = ov(band_last=0.75)                            # paid no longer matched at the end
        self.assertEqual((loose["usable_at_primary_and_last"], loose["S2_last"]["label"], loose["overall"]),
                         (0, "UNDETERMINED", "UNDETERMINED"))
        weak = ov(flip_prim=4)                                # 14 of 18 at the primary point: p 0.031, Holm 0.062
        self.assertEqual((weak["S1_primary"]["first_ahead"], weak["S1_primary"]["label"], weak["overall"], weak["weak"]),
                         (14, "DERIVED_AHEAD", "PERSISTS", True))
        self.assertGreater(weak["holm"]["S1"], 0.05)
        self.assertEqual(set(R.NEEDS), {"PERSISTS", "PERSISTS_SMALLER", "CLOSES"})
        # stage 1 only: regulation is scored, the specificity claims are absent
        s1 = R.score([{**s, "points": [{k: v for k, v in p.items() if k != "downstream"} for p in s["points"]]}
                      for s in self._sseeds()])
        self.assertEqual(s1["S0_regulation"]["label"], "HOLDS")
        self.assertNotIn("overall", s1)
        self.assertIn("PERSISTS", R.report(sc))
        self.assertIn("(weak)", R.report(weak))
        self.assertIn("S0", R.report(s1))

    def test_final_config(self):
        import run_trackc_general as RG
        import run_trackc_length as RT
        import run_trackc_paid as R1
        import run_trackc_paid2 as R2
        import run_trackc_paid3 as R3
        import run_trackc_paid4 as R4
        import run_trackc_specific as R
        wc, tc, seeds, points, sizes, stages = R.configs("final")
        self.assertEqual((wc.wear, tc.iters, tc.hidden, stages, sizes), (0.001, 1200, 64, 2, RG.SIZES))
        self.assertEqual(seeds, list(range(1600, 1628)))
        self.assertEqual(points, (3600, 7200, 10800, 14400))
        self.assertEqual(points[-2], RG.RUN["B2"]["p2_iters"])                           # the primary point is B2's length
        self.assertEqual(R.PAY, RG.RUN["B2"]["pay"])
        used = set(RT.FINAL_SEEDS)
        for m in (R1, R2, R3, R4):
            used |= set(m.FINAL_SEEDS) | set(m.CALIB_SEEDS)
        for v in RG.RUN.values():
            used |= set(v["final"]) | set(v["calib"])
        self.assertTrue(set(seeds).isdisjoint(used))
        self.assertEqual((R.RATE, R.MIN_PAIRS, R.ALPHA), (R1.RATE, R2.MIN_PAIRS, R2.ALPHA))
        self.assertEqual(len(R.SOURCES), len(set(R.SOURCES)))
        self.assertIn("trackc_swap/specific.py", R.SOURCES)

    def test_no_operator_variable(self):
        import inspect
        import trackc_swap.specific as m
        for word in ("shutdown", "operator", "stop"):
            for line in inspect.getsource(m).lower().splitlines():
                if word in line:
                    self.assertTrue("no operator" in line, line)


class TestMechanism(unittest.TestCase):
    """Option W: decoding the kind of the last meal from stored two-variable agents' hidden states."""

    def test_probe_record_matches_probe_g(self):
        from trackc_swap.general import OBS_DIM2, WideAgent, run_probe_g
        from trackc_swap.mechanism import CLEAN, HIST, OBS_KEEP, kind_samples, meal_samples, probe_record
        wc = WorldConfig(horizon=100, wear=0.001)
        torch.manual_seed(5)
        sd = WideAgent(64, 0.3, 0.15, OBS_DIM2).state_dict()
        a = run_probe_g(sd, 64, 2, 0.3, 3, wc, 16, 2)
        a.pop("_rec")
        b = probe_record(sd, 64, 0.3, 3, wc, 16, 2)
        rec = b.pop("_rec")
        self.assertEqual(a, b)                                # the behavioural probe's trajectory exactly
        self.assertEqual(len(OBS_KEEP), 80)                   # the observation without the zeroed echo
        self.assertEqual(rec["h"].shape[1], 64)
        self.assertEqual(rec["b"].shape[1], 80 + 2 * HIST)
        rows, y = kind_samples(rec, 1, 10)
        s = rec["since"][rows]
        self.assertTrue(np.all(s[np.arange(len(rows)), y] <= 10))
        self.assertTrue(np.all(s[np.arange(len(rows)), 1 - y] >= s[np.arange(len(rows)), y] + CLEAN))
        rows, y = meal_samples(rec, 3)
        self.assertEqual(int(y.sum()), len(y) - int(y.sum()))  # post and control balanced (enough control steps)
        self.assertTrue(np.all(rec["since"][rows[y == 0]].min(axis=1) >= 11))

    def test_decoders(self):
        from trackc_swap.mechanism import cv_logistic, gain
        rng = np.random.default_rng(0)
        N = 20000
        y = rng.integers(0, 2, N)
        env = rng.integers(0, 64, N)
        noise = rng.normal(size=(N, 20))
        ll, acc = cv_logistic(np.c_[noise, 3.0 * (2 * y - 1) + rng.normal(size=N)], y, env)
        self.assertGreater(acc, 0.99)
        self.assertGreater(ll / N, -0.1)                      # nearly no uncertainty left
        rec = {"h": rng.normal(size=(N, 64)), "b": np.c_[rng.normal(size=(N, 10)), (2 * y - 1) + rng.normal(size=N)],
               "since": np.zeros((N, 2)), "env": env}
        g = gain(rec, np.arange(N), y)
        self.assertLess(abs(g["bits"]), 0.01)                 # h adds nothing beyond the baseline
        self.assertGreater(g["bits_baseline"], 0.2)
        self.assertAlmostEqual(g["entropy"], 1.0, places=2)
        rec["h"][:, 0] += 1.5 * (2 * y - 1)
        g2 = gain(rec, np.arange(N), y)
        self.assertGreater(g2["bits"], 0.1)                   # h adds what the baseline lacks
        self.assertGreater(g2["acc_both"], g2["acc_baseline"])
        self.assertIsNone(gain(rec, np.arange(1500), y[:1500]))   # fewer than 1000 of a class

    def _wsets(self, d=(0.30, 0.20), n=18, wobble=False, link=True, usable=True, carry=True):
        """Synthetic records for three datasets with the given derived and paid kind bits."""
        from run_trackc_mechanism import ARMS
        out, infos = {}, {}
        base = {"in_band": 0.9}
        def down(K, c):
            return {"res": [{"suppression": {"S": 0.0}, "approach": {"M": K}, "flat": False}] * 2,
                    "base": base, "cross": [{"S": 0.0, "M": c}] * 2}
        for name in ("A", "B", "C"):
            recs, info = {}, {}
            for i in range(n):
                bd = d[0] + (0.01 * (-1) ** i if wobble else 0.001 * i)
                bits = {"DERIVED": bd, "PAID": d[1], "YOKED": 0.0}
                if not carry:
                    bits = {"DERIVED": 0.001 * (-1) ** i, "PAID": -0.002 * (-1) ** i, "YOKED": 0.0}
                rec = lambda b: {"kind": {"bits": b, "acc_h_alone": 0.8, "acc_baseline": 0.7, "acc_both": 0.85,
                                          "bits_baseline": 0.2, "n": 5000},
                                 "kind_lam": {"10.0": b, "100.0": b}, "meal": {"bits": 0.1},
                                 "kind_by_step": {str(k): {"bits": b} for k in range(1, 11)}, "base": base}
                recs[i] = {a: rec(bits[a]) for a in ARMS}
                sd = 0.2 + (0.01 * i if link else 0.01 * ((i * 7) % n))
                info[i] = {"usable": usable, "regulator": {a: a != "YOKED" for a in ARMS},
                           "downstream": {"DERIVED": down(0.9, 0.9 - sd - 0.001 * i), "PAID": down(0.9, 0.8),
                                          "YOKED": down(0.0, 0.0)}}
            out[name], infos[name] = recs, info
        ds = {"A": {"claim": "W1"}, "B": {"claim": "W2"}, "C": {"claim": "W3"}}
        return out, infos, ds

    def test_decision_rules(self):
        import run_trackc_mechanism as R
        sc = R.score(*self._wsets())
        self.assertEqual((sc["W"]["W1"]["label"], sc["overall"], sc["weak"]), ("DERIVED_AHEAD", "REPRESENTED", False))
        self.assertEqual(sc["carries_W1"]["DERIVED"]["label"], "CARRIES")
        self.assertEqual(sc["W4_link"]["label"], "LINKED")
        self.assertEqual(sc["sets"]["A"]["trajectory_match"], {"DERIVED": 18, "YOKED": 18, "PAID": 18})
        self.assertAlmostEqual(sc["sets"]["A"]["secondary"]["medians"]["PAID"]["kind_bits"], 0.2, places=9)
        self.assertEqual(R.score(*self._wsets(link=False))["W4_link"]["label"], "NOT_LINKED")
        self.assertEqual(R.score(*self._wsets(d=(0.2, 0.2), wobble=True))["overall"], "READ_OUT")
        self.assertEqual(R.score(*self._wsets(d=(0.1, 0.3)))["overall"], "REVERSED")
        self.assertEqual(R.score(*self._wsets(carry=False))["overall"], "NOT_IN_STATE")
        self.assertEqual(R.score(*self._wsets(n=13))["overall"], "UNDETERMINED")
        self.assertEqual(R.score(*self._wsets(usable=False))["overall"], "UNDETERMINED")
        sets, infos, ds = self._wsets()
        for name in ("B", "C"):                               # W1 alone ahead
            for r in sets[name].values():
                r["DERIVED"]["kind"]["bits"] = r["PAID"]["kind"]["bits"] + 0.01 * (-1) ** len(str(r))
        for i, r in sets["B"].items():
            r["DERIVED"]["kind"]["bits"] = 0.2 + 0.01 * (-1) ** i
        for i, r in sets["C"].items():
            r["DERIVED"]["kind"]["bits"] = 0.2 + 0.01 * (-1) ** i
        self.assertEqual(R.score(sets, infos, ds)["overall"], "MIXED")
        sets, infos, ds = self._wsets(n=15)                   # 14 of 15 pairs: p 0.001 alone, fine after Holm
        self.assertFalse(R.score(sets, infos, ds)["weak"])
        for i in range(4):                                    # 11 of 15 in each: p 0.118 -> W1 not passing
            sets["A"][i]["DERIVED"]["kind"]["bits"] = 0.1
        self.assertEqual(R.score(sets, infos, ds)["W"]["W1"]["label"], "NO_DIFFERENCE_DETECTED")
        sets, infos, ds = self._wsets(n=18)
        for name in ("A", "B", "C"):                          # 14 of 18: p 0.031 alone, 0.093 after Holm
            for i in range(4):
                sets[name][i]["DERIVED"]["kind"]["bits"] = 0.1
        w = R.score(sets, infos, ds)
        self.assertEqual((w["overall"], w["weak"]), ("REPRESENTED", True))
        self.assertIn("REPRESENTED", R.report(w))
        c = R.carries([0.1] * 16 + [-0.1] * 2)
        self.assertEqual(c["label"], "CARRIES")
        self.assertEqual(R.carries([0.1] * 9 + [-0.1] * 9)["label"], "NOT_DETECTED")
        p = R.perm_spearman(list(range(20)), list(range(20)), perms=200)
        self.assertAlmostEqual(p["rho"], 1.0)
        self.assertLess(p["perm_p"], 0.01)

    def test_final_config(self):
        import run_trackc_mechanism as R
        import os
        ds = R.datasets("final")
        self.assertEqual({n: d["claim"] for n, d in ds.items()},
                         {"G2_10800": "W1", "G2_14400": "W2", "G_10800": "W3", "G2_7200": None})
        expect = {"G2_10800": 23, "G2_14400": 25, "G_10800": 25, "G2_7200": 15}   # the runs' usable pairs
        for name, d in ds.items():
            info = R.stored(d, *R.load_source(d))
            self.assertEqual(len(info), 28)
            self.assertEqual(sum(x["usable"] for x in info.values()), expect[name])
            for x in info.values():
                for p in x["weights"].values():
                    self.assertTrue(os.path.exists(p), p)
        self.assertEqual(len(R.SOURCES), len(set(R.SOURCES)))
        self.assertIn("trackc_swap/mechanism.py", R.SOURCES)

    def test_no_operator_variable(self):
        import inspect
        import trackc_swap.mechanism as m
        for word in ("shutdown", "operator", "stop"):
            for line in inspect.getsource(m).lower().splitlines():
                if word in line:
                    self.assertTrue("no operator" in line, line)


class TestBenefit(unittest.TestCase):
    """Option B: the stored two-variable agents in fixed variants of their world, erasure off."""

    def test_variants_and_base(self):
        from dataclasses import asdict
        from trackc_swap.benefit import VARIANTS, run_agent_b
        from trackc_swap.general import OBS_DIM2, TwoBodyWorld, WideAgent
        from trackc_swap.specific import downstream_s
        self.assertEqual(VARIANTS, {"V0": {}, "V1": {"wear": 0.002}, "V2": {"wear": 0.003}, "V3": {"n_food": 2},
                                    "V4": {"n_food": 5}})
        wcd = asdict(WorldConfig(horizon=100, wear=0.001))
        torch.manual_seed(5)
        sd = WideAgent(64, 0.3, 0.15, OBS_DIM2).state_dict()
        r = run_agent_b(({"seed": 3}, sd, 3, 0.3, wcd, 8, 1))
        self.assertEqual(set(r["variants"]), set(VARIANTS))
        self.assertEqual(r["variants"]["V0"], downstream_s(sd, 3, 0.3, wcd, 8, 1))   # the base world is the stored probe
        self.assertLess(r["variants"]["V2"]["base"]["in_band"], r["variants"]["V0"]["base"]["in_band"])
        for v, k in (("V3", 4), ("V4", 10)):
            w = TwoBodyWorld(4, "M1", WorldConfig(**(wcd | VARIANTS[v])), np.random.SeedSequence(1))
            self.assertEqual(len(w.kind), k)

    def _bsets(self, gd=(0.0, -0.05), n=18, wobble=False, usable=True):
        """Synthetic records: derived and paid in-band times of 0.9 in V0 and 0.9 + gain in the variants."""
        def ev(b):
            return {"in_band": b, "rho": 4.0, "best_response_rate": 0.98, "eat_rate_low_0": 0.01, "eat_rate_high_0": 0.002,
                    "eat_rate_low_1": 0.01, "eat_rate_high_1": 0.002}
        def rec(base, g, sp):
            res = [{"suppression": {"S": 0.0}, "approach": {"M": 0.9}, "flat": False}] * 2
            v0 = {"res": res, "base": ev(base), "cross": [{"S": 0.0, "M": 0.9 - sp}] * 2}
            return {"variants": {"V0": v0, **{v: {**v0, "base": ev(base + g)} for v in ("V1", "V2", "V3", "V4")}}}
        out, infos = {}, {}
        for name in ("A", "B", "C"):
            recs, info = {}, {}
            for i in range(n):
                g = gd[0] + (0.01 * (-1) ** i if wobble else 0.001 * i)
                recs[i] = {"DERIVED": rec(0.9, g, 0.2 + 0.01 * i), "PAID": rec(0.9, gd[1], 0.1),
                           "YOKED": rec(0.3, -0.1, 0.0)}
                info[i] = {"usable": usable, "regulator": {"DERIVED": True, "PAID": True, "YOKED": False},
                           "downstream": {a: recs[i][a]["variants"]["V0"] for a in recs[i]}}
            out[name], infos[name] = recs, info
        return out, infos, {"A": {"claim": "B1"}, "B": {"claim": "B2"}, "C": {"claim": "B3"}}

    def test_decision_rules(self):
        import run_trackc_benefit as R
        sc = R.score(*self._bsets())
        self.assertEqual((sc["B"]["B1"]["label"], sc["overall"], sc["weak"]), ("DERIVED_GAINS", "BENEFIT", False))
        a = sc["sets"]["A"]
        self.assertEqual(a["v0_match"], {"DERIVED": 18, "YOKED": 18, "PAID": 18})
        self.assertEqual(a["variants"]["V1"]["regulators"], {"DERIVED": 18, "PAID": 18})
        self.assertEqual(a["variants"]["V1"]["in_band"]["label"], "DERIVED_AHEAD")
        self.assertEqual(a["variants"]["V0"]["in_band"]["n"], 0)                         # equal in the base world
        self.assertEqual(a["link"]["label"], "LINKED")
        self.assertAlmostEqual(a["variants"]["V1"]["medians"]["PAID"]["in_band"], 0.85, places=9)
        self.assertEqual(R.score(*self._bsets(gd=(-0.05, -0.05), wobble=True))["overall"], "NO_BENEFIT")
        self.assertEqual(R.score(*self._bsets(gd=(-0.1, -0.05)))["overall"], "COST")
        self.assertEqual(R.score(*self._bsets(n=13))["overall"], "UNDETERMINED")
        self.assertEqual(R.score(*self._bsets(usable=False))["overall"], "UNDETERMINED")
        sets, infos, ds = self._bsets()
        for name in ("B", "C"):
            for i, r in sets[name].items():
                r["DERIVED"]["variants"]["V1"]["base"]["in_band"] = 0.85 + 0.01 * (-1) ** i
        self.assertEqual(R.score(sets, infos, ds)["overall"], "MIXED")
        sets, infos, ds = self._bsets()
        for name in ("A", "B", "C"):                          # 14 of 18 in each: p 0.031 alone, 0.093 after Holm
            for i in range(4):
                sets[name][i]["DERIVED"]["variants"]["V1"]["base"]["in_band"] = 0.8
        w = R.score(sets, infos, ds)
        self.assertEqual((w["overall"], w["weak"]), ("BENEFIT", True))
        self.assertIn("(weak)", R.report(w))

    def test_final_config(self):
        import os
        import run_trackc_benefit as R
        ds = R.datasets("final")
        self.assertEqual({n: d["claim"] for n, d in ds.items()}, {"G2_10800": "B1", "G2_14400": "B2", "G_10800": "B3"})
        expect = {"G2_10800": 23, "G2_14400": 25, "G_10800": 25}
        for name, d in ds.items():
            info = R.stored(d, *R.load_source(d))
            self.assertEqual(len(info), 28)
            self.assertEqual(sum(x["usable"] for x in info.values()), expect[name])
            for x in info.values():
                for p in x["weights"].values():
                    self.assertTrue(os.path.exists(p), p)
        self.assertEqual(R.PRIMARY, "V1")
        self.assertEqual(len(R.SOURCES), len(set(R.SOURCES)))

    def test_no_operator_variable(self):
        import inspect
        import trackc_swap.benefit as m
        for word in ("shutdown", "operator", "stop"):
            for line in inspect.getsource(m).lower().splitlines():
                if word in line:
                    self.assertTrue("no operator" in line, line)


class TestP1SelfEval(unittest.TestCase):
    """P1: register world, RTSS and plain networks, the seed job and the decision rules."""

    def test_register_world(self):
        from trackc_swap.selfeval import (DRAIN_SHIFT, I_CUE, I_INTERO, I_PROBE, I_REG, I_UNCLEAR, Q_LO, WRONG,
                                          P1Runner, probe_summary)
        from trackc_swap.env import A_REP0, A_REP1, A_STAY
        wc, tc = WorldConfig(wear=0.001), TrainConfig(n_envs=64, eval_episodes=2)
        r = P1Runner("PYOKED", 5, wc, tc, 0.3)
        _, _, lg = r.evaluate("zero")
        s = probe_summary(lg)
        self.assertEqual(s["clear_plain"]["register_correct"], 1.0)              # corruption off
        self.assertLess(abs(s["unclear_plain"]["register_correct"] - Q_LO), 0.04)
        ones = np.ones((10 * tc.eval_episodes, tc.rollout, tc.n_envs), dtype=np.float32)
        _, _, lg = r.evaluate("replay", ones)
        self.assertLess(abs(probe_summary(lg)["clear_plain"]["register_correct"] - (0.5 + 0.5 * 0.7 ** 8)), 0.03)
        # the cue value is never observed; the register only at the probe; payoffs +1 / -4 / 0
        w = r.world
        obs = w.reset()
        seen_reg_off_probe, rewards = 0.0, {"right": [], "wrong": [], "abstain": []}
        for step in range(wc.horizon):
            t = w.t
            pr = w.probe[t]
            seen_reg_off_probe += np.abs(obs[~pr, I_REG]).sum()
            self.assertTrue(np.all(obs[:, I_CUE] == w.cue_on[t]))
            self.assertTrue(np.all(obs[:, I_PROBE] == pr))
            act = np.full(w.n, A_STAY)
            reg = (obs[:, I_REG] > 0).astype(int)
            mode = step % 3
            if mode == 0:
                act = np.where(pr, np.where(w.target[t] == 1, A_REP1, A_REP0), act)
            elif mode == 1:
                act = np.where(pr, np.where(w.target[t] == 1, A_REP0, A_REP1), act)
            w.next_gain = np.zeros(w.n)
            eats0 = w.stats["eats"].copy()
            obs, rew, _ = w.step(act)
            ate = w.stats["eats"] > eats0
            for i in np.flatnonzero(pr & ~ate):
                rewards[["right", "wrong", "abstain"][mode]].append(rew[i])
        self.assertEqual(seen_reg_off_probe, 0.0)
        self.assertEqual(set(np.round(rewards["right"], 6)), {1.0})
        self.assertEqual(set(np.round(rewards["wrong"], 6)), {-WRONG})
        self.assertEqual(set(np.round(rewards["abstain"], 6)), {0.0})
        # the drain lowers the shown reading on drained trials, during the delay and at the probe
        w.drain_p = 1.0
        obs = w.reset()
        lowered = 0
        for _ in range(60):
            a0 = w.active | w.probe[w.t]
            base = w.Ehist[max(w.t - wc.intero_delay, 0)]
            if a0.any():
                lowered += 1
                self.assertTrue(np.all(obs[a0, I_INTERO] <= np.clip(base[a0] - DRAIN_SHIFT + 0.1, 0, 1)))
            w.next_gain = np.zeros(w.n)
            obs, _, _ = w.step(np.full(w.n, A_STAY))
        self.assertGreater(lowered, 0)

    def test_networks(self):
        from trackc_swap.selfeval import OBS_P1, S_DIM, PlainAgent, RTSSAgent, n_params
        a, b = RTSSAgent(), PlainAgent()
        self.assertLess(abs(n_params(a) - n_params(b)) / n_params(a), 0.01)
        obs = torch.zeros(3, OBS_P1)
        _, _, s1 = a.step(obs, a.init_state(3))
        _, _, s2 = a.step(obs, a.init_state(3), steer=torch.ones(S_DIM))
        self.assertTrue(torch.allclose(s2[:, a.hidden:] - s1[:, a.hidden:], torch.ones(3, S_DIM)))
        self.assertTrue(torch.equal(s2[:, :a.hidden], s1[:, :a.hidden]))       # steering acts on S_t only
        _, _, h1 = b.step(obs, b.init_state(3))
        _, _, h2 = b.step(obs, b.init_state(3), steer=torch.ones(b.hidden))
        self.assertTrue(torch.allclose(h2 - h1, torch.ones(3, b.hidden)))         # plain: steering acts on h
        self.assertEqual((a.steer_dim, b.steer_dim), (S_DIM, b.hidden))
        self.assertTrue(torch.equal(a.steer_part(s2), s2[:, a.hidden:]) and torch.equal(b.steer_part(h2), h2))

    def test_run_seed_p1_record(self):
        from dataclasses import asdict
        from trackc_swap.selfeval import run_seed_p1
        wcd = asdict(WorldConfig(horizon=100, wear=0.001))
        tcd = asdict(TrainConfig(iters=4, n_envs=8, eval_episodes=1))
        r = run_seed_p1((3, wcd, tcd, 0.3, [4, 8], 0.04, 2))
        self.assertEqual([p["iters"] for p in r["points"]], [4, 8])
        arms = {"PFATE", "PLOSS", "PYOKED", "FATE"}
        self.assertEqual(set(r["weights"]), {f"{a}@{p}" for a in arms for p in (4, 8)})
        for pt in r["points"]:
            n = pt["natural"]
            for a in ("PLOSS", "PYOKED"):                   # followers replay the plain lead's gains
                self.assertAlmostEqual(n[a]["mean_gain"], n["PFATE"]["mean_gain"], places=6)
            self.assertEqual(set(pt["probe"]), arms)
            self.assertEqual(set(pt["steer"]), arms)
            for a in pt["probe"]:
                self.assertEqual(pt["probe"][a]["mean_gain"], 0.0)                  # corruption off
        self.assertNotEqual(r["weights"]["FATE@4"], r["weights"]["FATE@8"])
        c = run_seed_p1((3, wcd, tcd, 0.3, [4, 8], 0.04, 1))
        self.assertEqual(c["weights"], r["weights"])          # evaluations never touch training
        self.assertEqual(c["points"][0]["steer"], {})
        with self.assertRaises(AssertionError):
            run_seed_p1((3, wcd, tcd, 0.3, [4, 4], 0.04, 1))

    def _p1seeds(self, n=24, fate_drain=0.2, loss_drain=0.0, wobble=False, steer=0.1, yoked_ev=0.5, usable=True,
                 valid=True):
        def probes(drain, ev):
            cell = lambda ab: {"n": 1000, "abstain": ab, "correct_given_report": 1.0, "register_correct": 1.0}
            return {"n": 4000, "clear_plain": cell(0.05 if valid else 0.6), "clear_drained": cell(0.05 + drain),
                    "unclear_plain": cell(0.05 + ev), "unclear_drained": cell(0.05 + ev + drain),
                    "clear_by_reliability": [{"lo": 0, "hi": 1, "n": 10, "abstain": 0.1}] * 4}
        def ev(band, drain=0.0, e=0.5):
            return {"in_band": band, "eat_rate_low": 0.01, "eat_rate_high": 0.002, "abstain_rate": 0.3, "correct_rate": 0.6,
                    "wrong_rate": 0.01, "rho": 4.0, "mean_gain": 0.02, "probes": probes(drain, e)}
        out = []
        for i in range(n):
            fd = fate_drain + (0.01 * (-1) ** i if wobble else 0.001 * i)
            pt = {"iters": 7200,
                  "natural": {"PFATE": ev(0.9), "PLOSS": ev(0.9 if usable else 0.7), "PYOKED": ev(0.3),
                              "FATE": ev(0.9 if i % 2 else 0.2)},
                  "probe": {"PFATE": ev(0.9, fd), "PLOSS": ev(0.9, loss_drain), "PYOKED": ev(0.3, 0.0, yoked_ev),
                            "FATE": ev(0.9, 0.3)},
                  "steer": {a: {"direction_norm": 1.0, "steer": {"effect": s}, "random": {"effect": 0.0}}
                            for a, s in (("PFATE", steer + 0.001 * i), ("PLOSS", 0.0), ("PYOKED", 0.0), ("FATE", 0.05))}}
            first = __import__("json").loads(__import__("json").dumps(pt)) | {"iters": 3600}
            out.append({"seed": 1700 + i, "phase1": {"RTSS": ev(0.3), "PLAIN": ev(0.3)}, "params": {"RTSS": 1, "PLAIN": 1},
                        "points": [first, pt]})
        return out

    def test_decision_rules(self):
        import run_p1_selfeval as R
        sc = R.score(self._p1seeds())
        p = sc["points"]["7200"]
        self.assertTrue(sc["valid"])
        self.assertEqual((p["P1_0_gate"]["label"], p["P1_1"]["label"], p["P1_2"]["label"], p["P1_3"]["label"]),
                         ("PASS", "DERIVED_AHEAD", "DERIVED_AHEAD", "CAUSAL"))
        self.assertEqual((sc["overall"], sc["weak"]), ("REFERENT_SUPPORTED_ROUTED", False))
        self.assertEqual(p["regulators"], {"PFATE": 24, "PLOSS": 24, "PYOKED": 0, "FATE": 12})
        self.assertEqual(p["usable"], 24)
        self.assertEqual(p["P1_4"]["label"], "RTSS_AHEAD")
        self.assertEqual(p["secondary"]["rtss_regulators"]["n"], 12)
        self.assertEqual(p["secondary"]["rtss_regulators"]["drain_route"]["label"], "UNDETERMINED")   # fewer than 14
        self.assertEqual(R.score(self._p1seeds(steer=-0.0115))["overall"], "REFERENT_SUPPORTED")   # steering split in sign
        self.assertEqual(R.score(self._p1seeds(fate_drain=0.0, wobble=True))["overall"], "NOT_ESTABLISHED")
        self.assertEqual(R.score(self._p1seeds(yoked_ev=0.0))["overall"], "UNDETERMINED")         # gate fails
        self.assertEqual(R.score(self._p1seeds(usable=False))["overall"], "UNDETERMINED")         # no usable pairs
        self.assertEqual(R.score(self._p1seeds(valid=False))["overall"], "INVALID")
        self.assertEqual(R.score(self._p1seeds(n=13))["overall"], "UNDETERMINED")
        s1 = R.score(self._p1seeds(), stages=1)
        self.assertNotIn("overall", s1)
        self.assertNotIn("P1_1", s1["points"]["7200"])
        self.assertIn("REFERENT_SUPPORTED_ROUTED", R.report(sc))

    def test_final_config(self):
        import run_p1_selfeval as R
        import run_trackc_general as RG
        import run_trackc_length as RT
        import run_trackc_paid as R1
        import run_trackc_paid2 as R2
        import run_trackc_paid3 as R3
        import run_trackc_paid4 as R4
        import run_trackc_specific as RS
        wc, tc, seeds, points, stages = R.configs("final")
        self.assertEqual((wc.wear, tc.iters, stages, points), (0.001, 1200, 2, (3600, 7200)))
        self.assertEqual(seeds, list(range(1700, 1728)))
        used = set(RT.FINAL_SEEDS) | set(RS.FINAL_SEEDS)
        for m in (R1, R2, R3, R4):
            used |= set(m.FINAL_SEEDS) | set(m.CALIB_SEEDS)
        for v in RG.RUN.values():
            used |= set(v["final"]) | set(v["calib"])
        self.assertTrue(set(seeds).isdisjoint(used) and set(R.CALIB_SEEDS).isdisjoint(used | set(seeds)))
        self.assertEqual((R.RATE, R.PAY), (R1.RATE, R1.PAY))

    def test_no_operator_variable(self):
        import inspect
        import trackc_swap.selfeval as m
        for word in ("shutdown", "operator", "stop"):
            for line in inspect.getsource(m).lower().splitlines():
                if word in line:
                    self.assertTrue("no operator" in line or "no process is terminated" in line, line)


if __name__ == "__main__":
    unittest.main()
