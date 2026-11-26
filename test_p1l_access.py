"""Tests for P1l (trackc_swap/access.py, run_p1l_access.py)."""
import unittest

import numpy as np

import run_p1l_access as L
from trackc_swap.access import ACCESS_TAG, STEER_TAG_L, fit_readout, score_readout, vb_auc
from trackc_swap.gradmon import EVAL_TAG_G
from trackc_swap.steerint import STEER_TAG
from trackc_swap.transfer import TRANSFER_TAG


class TestAccess(unittest.TestCase):
    def test_readout_finds_content_free_signal(self):
        rng = np.random.default_rng(0)
        n, D = 4000, 10
        val = rng.integers(0, 2, n)
        y = rng.random(n) < 0.3
        H = 0.5 * rng.standard_normal((n, D))
        H[:, 0] += 2.0 * (2 * val - 1)                  # content (value-signed)
        H[:, 3] += 1.0 * y                              # content-free corruption signal
        ro = fit_readout(H[:2000], y[:2000].astype(np.int64))
        s = score_readout(ro, H[2000:])
        a = vb_auc(s, val[2000:], y[2000:], ~y[2000:])
        self.assertGreater(a, 0.8)
        w = ro["w"] / ro["sd"]
        self.assertGreater(abs(w[3]) / np.linalg.norm(w), 0.9)

    def test_readout_cannot_use_signed_content(self):
        rng = np.random.default_rng(1)
        n, D = 4000, 6
        val = rng.integers(0, 2, n)
        y = rng.random(n) < 0.5
        H = 0.5 * rng.standard_normal((n, D))
        H[:, 0] += (2 * val - 1) * np.where(y, 0.5, 2.0)  # corruption only weakens the signed content
        ro = fit_readout(H[:2000], y[:2000].astype(np.int64))
        a = vb_auc(score_readout(ro, H[2000:]), val[2000:], y[2000:], ~y[2000:])
        self.assertLess(abs(a - 0.5), 0.1)                # a linear read-out cannot detect signed weakening alone

    def test_labels(self):
        mk = lambda a, b, c, valid=True: {"valid": valid, "P1L_1": {"label": a}, "P1L_2": {"label": b},
                                          "P1L_3": {"label": c}}
        self.assertEqual(L.overall(mk("PRESENT", "DERIVED_AHEAD", "PRESENT")), "SHARED_GENERAL_ACCESS")
        self.assertEqual(L.overall(mk("PRESENT", "NO_DIFFERENCE_DETECTED", "PRESENT")), "SHARED_ACCESS_NOT_LEARNED")
        self.assertEqual(L.overall(mk("PRESENT", "DERIVED_AHEAD", "NOT_DETECTED")), "GENERAL_ACCESS_SEPARATE_ROUTE")
        self.assertEqual(L.overall(mk("PRESENT", "HOST_AHEAD", "REVERSED")), "GENERAL_ACCESS_NOT_LEARNED")
        self.assertEqual(L.overall(mk("NOT_DETECTED", "DERIVED_AHEAD", "PRESENT")), "NOT_GENERAL")
        self.assertEqual(L.overall(mk("PRESENT", "UNDETERMINED", "PRESENT")), "UNDETERMINED")
        self.assertEqual(L.overall(mk("PRESENT", "DERIVED_AHEAD", "PRESENT", valid=False)), "INVALID")

    def test_streams_and_sets(self):
        self.assertEqual(len({ACCESS_TAG, STEER_TAG_L, TRANSFER_TAG, STEER_TAG, EVAL_TAG_G}), 5)
        import run_p1i_calib as I
        self.assertEqual(L.CONFIRM_SET, I.FINAL_SEEDS)
        self.assertEqual(L.DISCOVERY_SET, list(range(3200, 3228)))


if __name__ == "__main__":
    unittest.main()
