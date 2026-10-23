"""E3-v2 ratio rule and the saved-run audit. No training."""

from __future__ import annotations

import math
import unittest
from pathlib import Path

from twostream_acquisition_e3_v2 import (
    UNAUDITABLE_FROM_SAVED,
    UNDEFINED,
    audit_saved_runs,
    e3_v2_from_saved,
    e3_v2_meets,
    e3_v2_ratio,
)

RUNS = Path(__file__).resolve().parent / "acquisition_results_v1" / "runs"


class E3V2RuleTest(unittest.TestCase):
    def test_large_numerator_and_tiny_denominator_is_infinite(self):
        self.assertEqual(e3_v2_ratio(1.0, 0.0), math.inf)
        self.assertEqual(e3_v2_ratio(1e-12 + 1e-15, 1e-12), math.inf)
        self.assertTrue(e3_v2_meets(math.inf, 0.75, at_least=True))
        self.assertFalse(e3_v2_meets(math.inf, 0.5, at_least=False))

    def test_both_tiny_is_undefined_and_never_passes(self):
        self.assertIs(e3_v2_ratio(0.0, 0.0), UNDEFINED)
        self.assertIs(e3_v2_ratio(1e-12, 1e-12), UNDEFINED)
        self.assertIs(e3_v2_ratio(1e-12, 0.0), UNDEFINED)
        self.assertFalse(e3_v2_meets(UNDEFINED, 0.75, at_least=True))
        self.assertFalse(e3_v2_meets(UNDEFINED, 0.5, at_least=False))

    def test_ordinary_quotient(self):
        denominator = math.nextafter(1e-12, math.inf)
        self.assertEqual(e3_v2_ratio(2.0, denominator), 2.0 / denominator)
        self.assertEqual(e3_v2_ratio(1.0, 4.0), 0.25)
        self.assertTrue(e3_v2_meets(0.25, 0.5, at_least=False))
        self.assertFalse(e3_v2_meets(0.25, 0.75, at_least=True))

    def test_saved_finite_ratio_is_already_the_v2_value(self):
        self.assertEqual(e3_v2_from_saved(0.1512214552042085), 0.1512214552042085)
        self.assertIs(e3_v2_from_saved(None), UNAUDITABLE_FROM_SAVED)
        self.assertFalse(e3_v2_meets(UNAUDITABLE_FROM_SAVED, 0.75, at_least=True))


class E3V2AuditTest(unittest.TestCase):
    def test_saved_runs_do_not_change_any_label(self):
        report = audit_saved_runs(RUNS)
        self.assertEqual(report["label"], "DESCRIPTIVE AUDIT, NOT A VERDICT CHANGE")
        self.assertEqual(report["runs"], 120)
        self.assertEqual(report["ratio_components"], 2400)
        self.assertEqual(report["unauditable_from_saved"], [])
        self.assertEqual(report["localized_flags"], 300)
        self.assertEqual(report["localized_flags_that_differ"], 0)
        self.assertFalse(report["any_label_would_differ"])
        self.assertEqual(report["gru8_cand_saved_e3"], "NOT LOCALIZED BY THIS INTERVENTION")
        self.assertEqual(report["gru8_cand_e3v2_e3"], "NOT LOCALIZED BY THIS INTERVENTION")
        self.assertEqual(report["gru8_kfr_saved_e3"], "UNRESOLVED")
        self.assertEqual(report["gru8_kfr_e3v2_e3"], "UNRESOLVED")
        self.assertEqual(report["localized_flag_sources"]["saved ratios"], 290)
        self.assertEqual(
            report["localized_flag_sources"]["no saved ratio block; flag left as recorded"],
            10,
        )


if __name__ == "__main__":
    unittest.main()
