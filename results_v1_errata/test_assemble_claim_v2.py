"""The frozen assembler still shows the bug. The v2 helper only formats it."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from recurrent_core_transfer_verdicts import assemble_claim
from results_v1_errata.assemble_claim_v2 import assemble_claim_v2

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "recurrent_core_results_v1" / "results.json"


def _recorded_inputs():
    summary = json.loads(RESULTS.read_text(encoding="utf-8"))["summary"]
    specific = {gate: summary["specific"][gate]["label"] for gate in ("r", "z", "n")}
    variation = {gate: summary["variation"][gate]["label"] for gate in ("r", "z", "n")}
    return (
        summary["e1"]["label"],
        summary["transfer"]["label"],
        specific,
        variation,
        summary["advantage"]["label"],
        summary["rival_afit"]["label"],
        summary["rival_afit"]["count"],
    )


class AssembleClaimV2Test(unittest.TestCase):
    def test_frozen_output_is_the_recorded_bug(self):
        summary = json.loads(RESULTS.read_text(encoding="utf-8"))["summary"]
        frozen = assemble_claim(*_recorded_inputs())
        self.assertEqual(frozen, summary["claim"])
        self.assertIn(". not met (0/10).", frozen)
        self.assertNotIn("TUNED FROZEN GRU-8 MEETS A-FIT AT THIS BUDGET: not met", frozen)
        self.assertFalse(frozen.endswith("."))

    def test_v2_names_the_rival_label_and_closes_the_paragraph(self):
        frozen = assemble_claim(*_recorded_inputs())
        repaired = assemble_claim_v2(*_recorded_inputs())
        self.assertTrue(repaired.endswith("."))
        self.assertIn(
            "TUNED FROZEN GRU-8 MEETS A-FIT AT THIS BUDGET: not met (0/10).",
            repaired,
        )
        self.assertNotIn(". not met (0/10).", repaired)
        self.assertTrue(repaired.startswith(frozen.split(" Tuned-rival results:")[0]))
        self.assertIn(
            "Variation results: r: selective variation reduction not demonstrated; "
            "z: selective variation reduction not demonstrated; "
            "n: selective variation reduction not demonstrated.",
            repaired,
        )

    def test_positive_rival_label_is_left_named(self):
        e1, transfer, specific, variation, advantage, _rival, _count = _recorded_inputs()
        rival = "TUNED FROZEN GRU-8 MEETS A-FIT AT THIS BUDGET"
        frozen = assemble_claim(e1, transfer, specific, variation, advantage, rival, 8)
        repaired = assemble_claim_v2(e1, transfer, specific, variation, advantage, rival, 8)
        self.assertEqual(repaired, frozen + ".")
        self.assertIn("TUNED FROZEN GRU-8 MEETS A-FIT AT THIS BUDGET (8/10).", repaired)


if __name__ == "__main__":
    unittest.main()
