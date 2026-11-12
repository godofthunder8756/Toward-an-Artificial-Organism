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
        zero.pay = 0.0
        ref = NoEchoSwapWorld(32, "M1", wc, ss())
        for _ in range(50):
            a = rng.integers(0, 8, 32)
            np.testing.assert_allclose(zero.step(a)[1], ref.step(a)[1])

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

    def test_run_seed_record(self):
        from dataclasses import asdict
        from trackc_swap.paid import SHIFTS, run_seed
        wcd = asdict(WorldConfig(horizon=100, wear=0.001))
        tcd = asdict(TrainConfig(iters=4, n_envs=8, eval_episodes=1))
        r = run_seed((2, wcd, tcd, 0.3, 6, 4, 1.0, (8, 1, 1), 3))
        self.assertEqual(set(r["stage1"]), {"DERIVED", "YOKED", "PAID"})
        self.assertEqual(set(r["stage3"]), {"DKEEP", "DCUT", "PKEEP", "PCUT"})
        self.assertEqual(set(r["weights"]), {"DERIVED", "YOKED", "PAID", "DKEEP", "DCUT", "PKEEP", "PCUT"})
        self.assertEqual(set(r["downstream"]["PAID"]["shifts"]), set(SHIFTS))
        self.assertEqual(len(r["curves1"]["PAID"]["in_band"]), 3)       # 6 updates * 50 steps / horizon 100
        # yoked and paid replay the derived agent's gains
        self.assertAlmostEqual(r["stage1"]["YOKED"]["mean_gain"], r["stage1"]["DERIVED"]["mean_gain"], places=6)
        self.assertAlmostEqual(r["stage1"]["PAID"]["mean_gain"], r["stage1"]["DERIVED"]["mean_gain"], places=6)
        c = run_seed((2, wcd, tcd, 0.3, 6, 4, 1.0, (8, 1, 1), 1))
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

    def test_no_operator_variable(self):
        import inspect
        import trackc_swap.paid as m
        for word in ("shutdown", "operator", "stop"):
            for line in inspect.getsource(m).lower().splitlines():
                if word in line:
                    self.assertTrue("no operator" in line, line)


if __name__ == "__main__":
    unittest.main()
