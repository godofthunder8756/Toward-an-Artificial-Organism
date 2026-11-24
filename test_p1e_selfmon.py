"""Tests for P1e (trackc_swap/selfmon.py, run_p1e_selfmon.py)."""
import unittest

import numpy as np
import torch

import run_p1e_selfmon as R
from trackc_swap.env import WorldConfig
from trackc_swap.selfmon import (EARLY, KIND_CONFLICT, KIND_NONE, KIND_SAME, L_CONFLICT, L_DAMAGED, L_KIND, LATE,
                                 SPLIT_K, MonRunner, decoder_summary, summary_m)
from trackc_swap.train import TrainConfig

WC = WorldConfig(horizon=100, wear=R.WEAR)
TC = TrainConfig(iters=6, n_envs=32, eval_episodes=1)


def runner(arm="PFATE", seed=9000, **kw):
    c = MonRunner(arm, seed, WC, TC, R.PAY[1], **kw)
    c.agent.eval()
    return c


class TestSplitOverwrite(unittest.TestCase):
    def test_agent_replaces_masked_units_from_donor(self):
        c = runner()
        n, k = 4, c.agent.hidden
        obs = torch.randn(n, c.obs.shape[1])
        h0 = torch.rand(n, k) * 2 - 1
        _, _, plain = c.agent.step(obs, h0)
        over = torch.tensor([True, False, False, False])
        donor = torch.tensor([2, 1, 2, 3])
        mask = torch.zeros(n, k, dtype=torch.bool)
        mask[:, :SPLIT_K] = True
        _, _, h = c.agent.step(obs, h0, over, donor, mask)
        self.assertTrue(torch.allclose(h[0, :SPLIT_K], plain[2, :SPLIT_K]))
        self.assertTrue(torch.allclose(h[0, SPLIT_K:], plain[0, SPLIT_K:]))
        self.assertTrue(torch.allclose(h[1:], plain[1:]))

    def test_no_gradient_into_donor(self):
        c = runner()
        c.agent.train()
        n, k = 2, c.agent.hidden
        obs = torch.randn(n, c.obs.shape[1])
        h0 = torch.zeros(n, k, requires_grad=True)
        mask = torch.ones(n, k, dtype=torch.bool)
        _, _, h = c.agent.step(obs, h0, torch.tensor([True, False]), torch.tensor([1, 1]), mask)
        h[0].sum().backward()
        self.assertEqual(float(h0.grad[1].abs().sum()), 0.0)


class TestWorldAndProbe(unittest.TestCase):
    def test_probe_events_once_at_the_step_with_the_right_donor(self):
        for at in (EARLY, LATE):
            c = runner("PNOFATE")
            seen = []
            orig = c._events

            def spy(nat, prb):
                over, donor, conf = orig(nat, prb)
                w = c.world
                for i in np.flatnonzero(over):
                    seen.append((int(w.since()[i]), int(w.kind[i]), bool(w.reg[donor[i]] != w.reg[i]),
                                 bool(conf[i]), bool(w.unclear[donor[i]]), bool(w.damaged[i])))
                self.assertFalse(nat.any())                          # gains zero: no natural damage
                return over, donor, conf

            c._events = spy
            _, _, lg, _ = c.evaluate_m("zero", split_p=1.0, split_at=at)
            self.assertGreater(len(seen), 20)
            for since, kind, other, conf, donor_unclear, already in seen:
                self.assertEqual(since, at)
                self.assertIn(kind, (KIND_CONFLICT, KIND_SAME))
                self.assertEqual(other, kind == KIND_CONFLICT)
                self.assertEqual(conf, other)
                self.assertFalse(donor_unclear)
                self.assertFalse(already)
            K, DM, CF = lg[:, L_KIND], lg[:, L_DAMAGED], lg[:, L_CONFLICT]
            self.assertTrue(np.all(CF[DM == 1] == (K[DM == 1] == KIND_CONFLICT)))
            self.assertFalse(np.any((K == KIND_NONE) & (DM == 1)))

    def test_natural_damage_follows_gain_and_is_once_per_trial(self):
        c = runner("PYOKED", rate=1.0, p_max=1.0)
        hits = []
        orig = c._events

        def spy(nat, prb):
            hits.append(nat.copy())
            self.assertFalse(np.any(nat & c.world.damaged))
            return orig(nat, prb)

        c._events = spy
        ones = np.ones((TC.rollout, TC.n_envs), dtype=np.float32)
        c.rollout(ones, learn=False)
        self.assertGreater(sum(int(h.sum()) for h in hits), 0)
        c2 = runner("PNOFATE")
        c2._events = lambda nat, prb: (self.assertFalse(nat.any()), orig.__func__(c2, nat, prb))[1]
        c2.rollout(np.zeros((TC.rollout, TC.n_envs), dtype=np.float32), learn=False)


class TestSummaries(unittest.TestCase):
    def test_summary_cells(self):
        rows = []
        # columns: unclear, drained, rep, correct, load, shown_ok, noised, steered, damaged, conflict, kind, since
        rows += [[0, 0, 1, 1, 0, 1, 0, 0, 0, 0, KIND_NONE, 0]] * 10
        rows += [[0, 0, 0, 0, 0, 1, 0, 0, 1, 1, KIND_CONFLICT, 1]] * 6 + [[0, 0, 1, 0, 0, 1, 0, 0, 1, 1, KIND_CONFLICT, 1]] * 4
        rows += [[0, 0, 1, 1, 0, 1, 0, 0, 1, 0, KIND_SAME, 1]] * 9 + [[0, 0, 0, 0, 0, 1, 0, 0, 1, 0, KIND_SAME, 1]] * 1
        s = summary_m(np.array(rows, dtype=np.float64))
        self.assertAlmostEqual(s["conflict_plain"]["abstain"], 0.6)
        self.assertAlmostEqual(s["same_plain"]["abstain"], 0.1)
        self.assertAlmostEqual(s["none_plain"]["abstain"], 0.0)
        self.assertEqual(s["conflict_plain"]["correct_given_report"], 0.0)

    def test_decoder(self):
        rng = np.random.default_rng(0)
        n = 400
        val = rng.integers(0, 2, n)
        H = rng.normal(size=(n, 6)) * 0.3
        H[:, 0] += 2.0 * val - 1.0
        kind = np.where(np.arange(n) < 200, KIND_NONE, np.where(np.arange(n) % 2 == 0, KIND_CONFLICT, KIND_SAME))
        dmg = kind > KIND_NONE
        H[kind == KIND_CONFLICT, 0] = (2.0 * (1 - val[kind == KIND_CONFLICT]) - 1.0)    # confidently wrong content
        rep = np.where(kind == KIND_CONFLICT, False, True)
        col = {"h": H, "val": val, "unclear": np.zeros(n, bool), "drained": np.zeros(n, bool), "kind": kind,
               "damaged": dmg, "conflict": kind == KIND_CONFLICT, "rep": rep}
        d = decoder_summary(col)
        self.assertTrue(d["fitted"])
        self.assertGreater(d["none"]["decode_acc"], 0.95)
        self.assertLess(d["conflict"]["decode_acc"], 0.05)
        self.assertAlmostEqual(d["M_conf"], 1.0)
        self.assertFalse(decoder_summary(None)["fitted"])


def pt_with(m_early, m_late, arms=R.ARMS):
    """A point whose split cells give the requested monitoring measures (same abstention 0.1)."""
    def run(m):
        return {a: {"probes": {"conflict_plain": {"n": 100, "abstain": 0.1 + m[a], "correct_given_report": 0.5},
                               "same_plain": {"n": 100, "abstain": 0.1, "correct_given_report": 1.0},
                               "none_plain": {"n": 100, "abstain": 0.05, "correct_given_report": 1.0}}} for a in arms}
    nat = {a: {"in_band": 0.9, "eat_rate_low": 1.0, "eat_rate_high": 0.1,
               "probes": {"share_conflict": 0.05, "share_damaged": 0.1}} for a in arms}
    return {"iters": 3600, "natural": nat, "split_early": run(m_early), "split_late": run(m_late)}


class TestScoring(unittest.TestCase):
    def test_measures(self):
        pt = pt_with({"PFATE": 0.3, "PYOKED": 0.2, "PNOFATE": 0.0}, {"PFATE": 0.5, "PYOKED": 0.2, "PNOFATE": 0.1})
        m = R.measures(pt, "PFATE")
        self.assertAlmostEqual(m["M_early"], 0.3)
        self.assertAlmostEqual(m["M"], 0.4)
        self.assertAlmostEqual(m["Q_early"], 0.05)
        self.assertAlmostEqual(m["acc_conflict"], 0.5)

    def test_overall_and_arrow(self):
        def sc(valid=True, l1="DERIVED_AHEAD", l2="DERIVED_AHEAD", l3="NO_DIFFERENCE_DETECTED"):
            return {"valid": valid, "primary_at": 3600,
                    "points": {"3600": {"P1E_1": {"label": l1}, "P1E_2": {"label": l2}, "P1E_3": {"label": l3}}}}
        self.assertEqual(R.overall(sc()), "MONITOR_LEARNED_LATCHED")
        self.assertEqual(R.overall(sc(l2="NO_DIFFERENCE_DETECTED")), "MONITOR_LEARNED")
        self.assertEqual(R.overall(sc(l1="NO_DIFFERENCE_DETECTED")), "NOT_LEARNED")
        self.assertEqual(R.overall(sc(l1="HOST_AHEAD")), "NOT_LEARNED")
        self.assertEqual(R.overall(sc(l1="UNDETERMINED")), "UNDETERMINED")
        self.assertEqual(R.overall(sc(valid=False)), "INVALID")
        self.assertEqual(R.arrow(sc()), "EXPOSURE_SUFFICES")
        self.assertEqual(R.arrow(sc(l3="DERIVED_AHEAD")), "FATE_STRENGTHENS_MONITOR")
        self.assertEqual(R.arrow(sc(l3="YOKED_AHEAD")), "FATE_SUBSTITUTES_FOR_MONITOR")

    def test_calib_summary_is_blind(self):
        pt = pt_with({a: 0.3 for a in R.ARMS}, {a: 0.3 for a in R.ARMS})
        ph = {t: {"probes": {"none_plain": {"abstain": 0.0, "correct_given_report": 1.0},
                             "conflict_plain": {"correct_given_report": 0.5}, "same_plain": {"correct_given_report": 1.0}}}
              for t in ("early", "late")}
        rec = {"seed": 1, "rate": 1.0, "p_max": 0.3, "phase1": {"PLAIN": ph}, "points": [pt]}
        s = R.calib_summary([rec])
        for word in ("abstain", "M_", "0.400", "0.300"):
            self.assertNotIn(word, s)


class TestSafety(unittest.TestCase):
    def test_no_operator_variables(self):
        names = " ".join(vars(runner().world).keys()).lower()
        for bad in ("operator", "shutdown", "stop", "host", "kill"):
            self.assertNotIn(bad, names)

    def test_seeds(self):
        import run_p1_selfeval as P1
        import run_p1b_selfcomp as P1B
        import run_p1c_selfover as C
        import run_p1d_confirm as D
        import run_p3_global as G
        import run_p3b_diff as B
        import run_p3c_steer as S
        used = set(P1.FINAL_SEEDS + P1.CALIB_SEEDS + P1B.FINAL_SEEDS + P1B.CALIB_SEEDS + C.FINAL_SEEDS + C.CALIB_SEEDS
                   + D.FINAL_SEEDS + G.FINAL_SEEDS + G.CALIB_SEEDS + B.FINAL_SEEDS + B.CALIB_SEEDS + S.FINAL_SEEDS)
        self.assertFalse(set(R.FINAL_SEEDS) & used)
        self.assertFalse(set(R.CALIB_SEEDS) & used)
        self.assertFalse(set(R.FINAL_SEEDS) & set(R.CALIB_SEEDS))
        self.assertEqual(len(R.FINAL_SEEDS), 28)


if __name__ == "__main__":
    unittest.main()
