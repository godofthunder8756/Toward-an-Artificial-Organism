"""Tests for P1q (run_p1q_symptom.py)."""
import unittest

import numpy as np

import run_p1q_symptom as Q
from trackc_swap.gradmon import GradWorld
from trackc_swap.selfeval import OBS_P1


class TestSymptom(unittest.TestCase):
    def test_blind_reading(self):
        n = 20000
        w = GradWorld(n, Q.world(), np.random.SeedSequence([1, 2, 3]))
        w.reset()
        E = np.random.default_rng(0).uniform(0.2, 0.8, n)
        w.Ehist[0] = E
        obs = w.observe()
        self.assertEqual(obs.shape[1], OBS_P1)
        r = obs[:, 2 * 25]                                     # the interoceptive column
        self.assertLess(abs(np.corrcoef(r, E)[0, 1]), 0.03)    # practically no information
        ref = GradWorld(n, Q.WorldConfig(wear=Q.WEAR), np.random.SeedSequence([1, 2, 3]))
        ref.reset()
        ref.Ehist[0] = E
        self.assertGreater(np.corrcoef(ref.observe()[:, 50], E)[0, 1], 0.9)   # the column is the reading

    def test_jobs_use_the_blind_world(self):
        self.assertEqual(Q.world().intero_sd, Q.INTERO_SD_Q)
        self.assertEqual(Q.world().wear, Q.WEAR)

    def test_invalid_when_p1g_invalid(self):
        orig_g, orig_o = Q.G.score, Q.O.score
        try:
            Q.G.score = lambda recs: {"valid": False}
            Q.O.score = lambda recs: {"valid": True, "P1O_1": {"label": "PRESENT"}, "P1O_2": {"label": "FATE_AHEAD"},
                                      "P1O_3": {"label": "PRESENT"}}
            self.assertEqual(Q.score_all({"train": [], "coupling": []})["overall"], "INVALID")
            Q.G.score = lambda recs: {"valid": True}
            self.assertEqual(Q.score_all({"train": [], "coupling": []})["overall"], "PRECARITY_COUPLES_MONITOR")
        finally:
            Q.G.score, Q.O.score = orig_g, orig_o

    def test_sets(self):
        import run_p1i_calib as I
        self.assertEqual(Q.SETS["confirm"], I.FINAL_SEEDS)
        self.assertEqual(Q.SETS["discovery"], list(range(3200, 3208)))


if __name__ == "__main__":
    unittest.main()
