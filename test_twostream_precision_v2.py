"""Checks for the corrected K-EXACT quantizer. No neural training."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

import numpy as np

from twostream_acquisition_metrics import _rho
from twostream_acquisition_oracle import load_world
from twostream_acquisition_precision_v2 import (
    FROZEN_METRICS_SHA256,
    exact_phase_overshoot,
    frozen_curve_matches_reference,
    frozen_metrics_sha256,
    kexact_precision_v2,
    quantized_exact_forecasts_v2,
)
from twostream_acquisition_spec import E3_COMPLEMENT_MIN

ROOT = Path(__file__).resolve().parent
REFERENCE = ROOT / "acquisition_results_v1" / "reference_arms.json"


class PrecisionV2Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.world = load_world()
        cls.report = kexact_precision_v2(cls.world)

    def test_t1_unbounded_ranges_match_oracle(self):
        ranges = [(np.full(3, -10.0), np.full(3, 10.0)) for _ in range(8)]
        forecasts, _repairs, clips, _overshoot, _preclip = quantized_exact_forecasts_v2(ranges, 52)
        self.assertEqual(clips, [0] * 8)
        self.assertLessEqual(float(np.max(np.abs(forecasts - self.world.q))), 1e-12)

    def test_t2_exact_post_observation_train_overshoot(self):
        overshoot = exact_phase_overshoot(self.world)["corrected_order"]["TRAIN"]
        self.assertEqual(len(overshoot), 8)
        self.assertTrue(all(value <= 1e-7 for value in overshoot))

    def test_t3_train_error_decreases_at_fine_precision(self):
        totals = [
            row["errors"]["TRAIN"]["total"]
            for row in self.report["curve"]
            if row["b"] in (8, 12, 16, 20, 24)
        ]
        self.assertEqual(len(totals), 5)
        self.assertTrue(all(totals[i] > totals[i + 1] for i in range(4)))
        self.assertLessEqual(totals[-1], 1e-12)

    def test_t4_frozen_function_matches_reference_arms(self):
        reference = json.loads(REFERENCE.read_text())
        self.assertTrue(frozen_curve_matches_reference(self.world, reference))
        frozen_b24 = reference["K-EXACT"]["precision"]["curve"][-1]
        self.assertEqual(frozen_b24["b"], 24)
        self.assertFalse(frozen_b24["train_afit"])
        self.assertAlmostEqual(frozen_b24["errors"]["TRAIN"]["total"], 0.0028588144953225346)

    def test_t5_frozen_metrics_hash(self):
        self.assertEqual(frozen_metrics_sha256(), FROZEN_METRICS_SHA256)

    def test_selection_is_four_bits_and_confirmed(self):
        self.assertEqual(self.report["smallest_passing_precision_train"], 4)
        self.assertEqual(self.report["smallest_passing_precision_test"], 4)
        self.assertEqual(self.report["b_sel_train"], 4)
        self.assertEqual(self.report["confirmation"], "CONFIRMED")
        self.assertEqual(self.report["charged_state_bits_nominal"], 12)
        self.assertEqual(self.report["charged_state_bits_stagewise"], [4, 8, 12, 12, 12, 12, 12, 12])
        row = next(item for item in self.report["curve"] if item["b"] == 24)
        self.assertLessEqual(row["errors"]["TRAIN"]["total"], 1e-12)
        self.assertLess(row["errors"]["TEST"]["total"], 0.001)

    def test_committed_v2_json_matches_rerun(self):
        committed = json.loads((ROOT / "acquisition_results_v1_errata" / "reference_arms_kexact_v2.json").read_text())
        self.assertEqual(committed["b_sel_train"], self.report["b_sel_train"])
        self.assertEqual(committed["confirmation"], self.report["confirmation"])
        self.assertEqual(
            committed["curve"][-1]["errors"],
            self.report["curve"][-1]["errors"],
        )

    def test_iterative_train_overshoot_exceeds_endpoint_rounding_below_24_bits(self):
        """Records a limit of the erratum's clip sentence. Not a phase-mismatch."""
        coarse = [row for row in self.report["curve"] if row["b"] < 24]
        self.assertTrue(any(max(row["max_clip_overshoot_train"]) > 1e-7 for row in coarse))
        fine = next(row for row in self.report["curve"] if row["b"] == 24)
        self.assertLessEqual(max(fine["max_clip_overshoot_train"]), 1e-7)


class E3DenominatorDefectTest(unittest.TestCase):
    def test_perfect_complement_is_undefined_and_cannot_pass(self):
        q_recipient = np.array([[0.2, 0.3, 0.4], [0.55, 0.45, 0.25]], dtype=np.float64)
        q_donor = np.array([[0.8, 0.15, 0.1], [0.35, 0.7, 0.2]], dtype=np.float64)
        forecast = q_recipient.copy()
        self.assertIsNone(_rho(forecast, q_donor, q_recipient, False))
        self.assertIsNone(_rho(forecast, q_donor, q_recipient, True))
        vector = _rho(forecast, q_donor, q_recipient, False)
        xor = _rho(forecast, q_donor, q_recipient, True)
        passes = (
            vector is not None
            and xor is not None
            and vector >= E3_COMPLEMENT_MIN
            and xor >= E3_COMPLEMENT_MIN
        )
        self.assertFalse(passes)


if __name__ == "__main__":
    unittest.main()
