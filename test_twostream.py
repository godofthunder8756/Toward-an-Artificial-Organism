"""Exact-arithmetic tests for the two-stream certificate.

Run from the repository root:

    python -m unittest -v test_twostream

These tests cover the frozen generator, the chart, hand-checked one-step
updates, and agreement of the three code paths on horizons shorter than the
admission horizon. They do not encode the eight-reading gate values.
"""

import ast
import unittest
from fractions import Fraction
from pathlib import Path

from twostream_alias import audit_stages, interpretation, min_marginal_separation
from twostream_chart import belief_from_chart, forecasts, frechet_contains, marginals_covariance
from twostream_constants import (
    A,
    BX,
    BY,
    DX,
    DY,
    E,
    ETA,
    G,
    latent_observed_bit,
    phase_mask,
    state_index,
    variable_at,
)
from twostream_enumerate import enumerate_horizon
from twostream_filter import fraction_transition, initial_belief, observe, transit
from twostream_moments import observe_moments, transit_moments
from twostream_replay import (
    TRANSITION_DENOMINATOR,
    enumerate_joint_numerators,
    integer_transition,
)
from twostream_score import (
    XOR_EXCESS_THRESHOLD,
    classify_run,
    current_only_terminal,
    decimal_truncation,
    expected_squared_error,
    factorized_xor,
    gate_i_pass,
    gate_ii_pass,
    gate_iii_pass,
    intervention_mass,
    xor_forecasts,
)

ROOT = Path(__file__).resolve().parent


class FrozenGenerator(unittest.TestCase):
    def test_decision_parameters_and_read_order(self):
        self.assertEqual(G, Fraction(1, 5))
        self.assertEqual(DX, Fraction(1, 50))
        self.assertEqual(DY, Fraction(1, 40))
        self.assertEqual(E, Fraction(1, 5))
        self.assertEqual(A, Fraction(3, 5))
        self.assertEqual(BX, Fraction(24, 25))
        self.assertEqual(BY, Fraction(19, 20))
        self.assertEqual(ETA, Fraction(3, 5))
        self.assertEqual([variable_at(t) for t in range(8)], list("XYXYXYXY"))

    def test_thresholds_are_the_decision_values(self):
        self.assertEqual(XOR_EXCESS_THRESHOLD, Fraction(1, 1000))
        self.assertTrue(gate_ii_pass(Fraction(1, 1000)))
        self.assertFalse(gate_ii_pass(Fraction(1, 1600)))
        self.assertTrue(gate_iii_pass(Fraction(1, 4), True))
        self.assertFalse(gate_iii_pass(Fraction(1, 4), False))
        self.assertFalse(gate_i_pass(Fraction(0)))
        self.assertTrue(gate_i_pass(Fraction(1, 100)))

    def test_protocol_keeps_the_numerical_gates(self):
        text = (ROOT / "TWOSTREAM_PROTOCOL_v1.md").read_text(encoding="utf-8")
        self.assertIn("1/1000", text)
        self.assertIn("1/20", text)
        self.assertIn("1/4", text)
        self.assertIn("one-component", text)
        self.assertIn("X, Y, X, Y, X, Y, X, Y", text)
        self.assertIn("ADMIT", text)
        self.assertIn("REJECT", text)
        self.assertIn("UNRESOLVED", text)


class ChartAndHandUpdates(unittest.TestCase):
    def test_chart_round_trip_and_zero_covariance_box(self):
        samples = [
            (Fraction(0), Fraction(0), Fraction(0)),
            (Fraction(1), Fraction(1), Fraction(0)),
            (Fraction(1, 2), Fraction(1, 2), Fraction(0)),
            (Fraction(4, 5), Fraction(1, 5), Fraction(1, 25)),
            (Fraction(1, 3), Fraction(2, 3), Fraction(0)),
        ]
        for mx, my, cov in samples:
            self.assertTrue(frechet_contains(mx, my, Fraction(0)))
            belief = belief_from_chart(mx, my, cov)
            self.assertEqual(sum(belief), 1)
            self.assertEqual(marginals_covariance(belief), (mx, my, cov))

    def test_uniform_x_observation(self):
        belief, predictive = observe(initial_belief(), "X", 1)
        self.assertEqual(predictive, Fraction(1, 2))
        self.assertEqual(
            belief,
            [Fraction(1, 10), Fraction(2, 5), Fraction(1, 10), Fraction(2, 5)],
        )
        self.assertEqual(
            marginals_covariance(belief),
            (Fraction(4, 5), Fraction(1, 2), Fraction(0)),
        )

    def test_uniform_y_observation_zero(self):
        belief, predictive = observe(initial_belief(), "Y", 0)
        self.assertEqual(predictive, Fraction(1, 2))
        self.assertEqual(belief[state_index(0, 0)], Fraction(2, 5))
        self.assertEqual(belief[state_index(1, 0)], Fraction(2, 5))
        self.assertEqual(belief[state_index(0, 1)], Fraction(1, 10))
        self.assertEqual(belief[state_index(1, 1)], Fraction(1, 10))
        self.assertEqual(
            marginals_covariance(belief),
            (Fraction(1, 2), Fraction(1, 5), Fraction(0)),
        )

    def test_transition_after_first_x_reading(self):
        mx, my, cov = observe_moments(Fraction(1, 2), Fraction(1, 2), Fraction(0), "X", 1)
        mx, my, cov = transit_moments(mx, my, cov)
        self.assertEqual((mx, my, cov), (Fraction(841, 1250), Fraction(1, 2), Fraction(0)))
        belief, _predictive = observe(initial_belief(), "X", 1)
        moved = transit(belief, fraction_transition())
        self.assertEqual(marginals_covariance(moved), (mx, my, cov))

    def test_integer_and_fraction_transitions_agree(self):
        fractional = fraction_transition()
        integral = integer_transition()
        for src in range(4):
            self.assertEqual(sum(integral[src]), TRANSITION_DENOMINATOR)
            self.assertEqual(sum(fractional[src]), 1)
            for dst in range(4):
                self.assertGreater(integral[src][dst], 0)
                self.assertEqual(
                    Fraction(integral[src][dst], TRANSITION_DENOMINATOR),
                    fractional[src][dst],
                )

    def test_factorized_gap_is_twice_covariance(self):
        mx, my, cov = Fraction(2, 7), Fraction(3, 5), Fraction(1, 11)
        _qx, _qy, joint = forecasts(mx, my, cov)
        self.assertEqual(factorized_xor(mx, my) - joint, 2 * cov)
        self.assertEqual(xor_forecasts(mx, my, cov), joint)


class ReplayAgreement(unittest.TestCase):
    def test_one_step_weights_match_the_hand_posterior(self):
        weights, denominator = enumerate_joint_numerators(1)
        self.assertEqual(denominator, 20)
        self.assertEqual(weights[1], [1, 4, 1, 4])
        self.assertEqual(sum(weights[0]), 10)
        self.assertEqual(sum(sum(row) for row in weights), denominator)

    def test_two_step_matches_an_inline_trajectory_sum(self):
        history = 0b11  # reading 1 = X = 1, reading 2 = Y = 1
        trans = integer_transition()
        expected = [0, 0, 0, 0]
        for src in range(4):
            for dst in range(4):
                observation = 1
                if latent_observed_bit(src, 0) == 1:
                    observation *= 4
                if latent_observed_bit(dst, 1) == 1:
                    observation *= 4
                expected[dst] += trans[src][dst] * observation
        weights, denominator = enumerate_joint_numerators(2)
        self.assertEqual(weights[history], expected)
        self.assertEqual(denominator, 4 * TRANSITION_DENOMINATOR * 25)
        self.assertEqual(sum(sum(row) for row in weights), denominator)

    def test_three_paths_agree_through_horizon_three(self):
        for horizon in (1, 2, 3):
            payload = enumerate_horizon(horizon)
            self.assertEqual(len(payload["records"]), 1 << horizon)
            self.assertEqual(sum(row["prob"] for row in payload["records"]), 1)

    def test_posterior_averages_to_the_uniform_law(self):
        for horizon in (1, 2, 3):
            payload = enumerate_horizon(horizon)
            mean_mx = Fraction(0)
            mean_my = Fraction(0)
            mean_p11 = Fraction(0)
            for row in payload["records"]:
                mean_mx += row["prob"] * row["mx"]
                mean_my += row["prob"] * row["my"]
                mean_p11 += row["prob"] * (row["mx"] * row["my"] + row["c"])
            self.assertEqual(mean_mx, Fraction(1, 2))
            self.assertEqual(mean_my, Fraction(1, 2))
            self.assertEqual(mean_p11, Fraction(1, 4))

    def test_covariance_remains_zero_before_the_second_transition(self):
        for horizon in (1, 2):
            payload = enumerate_horizon(horizon)
            for row in payload["records"]:
                self.assertEqual(row["c"], 0)


class ScoringConventions(unittest.TestCase):
    def test_rare_large_covariance_passes_ii_and_fails_iii(self):
        probabilities = [Fraction(1, 100), Fraction(99, 100)]
        covariances = [Fraction(1, 4), Fraction(0)]
        mx = my = Fraction(1, 2)
        factorized = [factorized_xor(mx, my), factorized_xor(mx, my)]
        joint = [xor_forecasts(mx, my, covariances[0]), xor_forecasts(mx, my, covariances[1])]
        excess = expected_squared_error(probabilities, factorized, joint)
        self.assertEqual(excess, Fraction(1, 400))
        self.assertTrue(gate_ii_pass(excess))
        self.assertEqual(intervention_mass(probabilities, covariances), Fraction(1, 100))
        self.assertFalse(gate_iii_pass(Fraction(1, 100), True))

    def test_boundary_mass_passes_iii_without_ii(self):
        probabilities = [Fraction(1, 4), Fraction(3, 4)]
        covariances = [Fraction(1, 40), Fraction(0)]
        excess = sum(
            (prob * 4 * cov * cov for prob, cov in zip(probabilities, covariances)),
            Fraction(0),
        )
        self.assertEqual(excess, Fraction(1, 1600))
        self.assertFalse(gate_ii_pass(excess))
        self.assertEqual(intervention_mass(probabilities, covariances), Fraction(1, 4))
        self.assertTrue(gate_iii_pass(Fraction(1, 4), True))

    def test_current_only_closed_form(self):
        self.assertEqual(
            current_only_terminal(1),
            (Fraction(1, 2), Fraction(4, 5), Fraction(0)),
        )
        self.assertEqual(
            current_only_terminal(0),
            (Fraction(1, 2), Fraction(1, 5), Fraction(0)),
        )

    def test_verdict_rule(self):
        passing = {"i": True, "ii": True, "iii": True, "iv": True}
        self.assertEqual(classify_run([], passing), "ADMIT")
        self.assertEqual(classify_run([], {"i": True, "ii": False, "iii": True, "iv": True}), "REJECT")
        self.assertEqual(classify_run(["replay mismatch"], passing), "UNRESOLVED")
        self.assertEqual(classify_run([], {"i": True, "ii": True, "iii": True, "iv": False}), "UNRESOLVED")

    def test_decimal_truncation_marks_a_remainder(self):
        self.assertEqual(decimal_truncation(Fraction(1, 2), 4), "0.5000")
        self.assertEqual(decimal_truncation(Fraction(1, 3), 4), "0.3333...")


class AliasClassifier(unittest.TestCase):
    def test_accidental_terminal_alias_does_not_need_zero_mean(self):
        rows = {
            8: [
                self._row(0, Fraction(1, 3), Fraction(1, 3), Fraction(1, 10)),
                self._row(1, Fraction(1, 3), Fraction(1, 3), Fraction(1, 20)),
            ]
        }
        audit = audit_stages(rows, terminal_stage=8)
        self.assertEqual(audit["K1_outcome"], "A1")
        self.assertFalse(audit["T_PROJ"])
        self.assertFalse(audit["T_CLOSE"])
        self.assertEqual(audit["stages"][8]["pairs"][0]["mechanism"], "accidental")
        self.assertNotEqual(audit["stages"][8]["pairs"][0]["mu_x"], 0)
        self.assertEqual(min_marginal_separation(rows[8]), 0)

    def test_symmetry_pair_is_labeled_only_for_the_flip(self):
        mask = phase_mask(8, 0)
        rows = {
            8: [
                self._row(0, Fraction(1, 2), Fraction(1, 4), Fraction(1, 8)),
                self._row(mask, Fraction(1, 2), Fraction(1, 4), Fraction(-1, 8)),
            ]
        }
        audit = audit_stages(rows, terminal_stage=8)
        self.assertEqual(audit["stages"][8]["pairs"][0]["mechanism"], "symmetry-X")
        self.assertEqual(audit["symmetry_anomalies"], [])

    def test_prefix_alias_without_a_terminal_alias_is_A2(self):
        rows = {
            3: [
                self._row(0, Fraction(1, 5), Fraction(2, 5), Fraction(1, 50)),
                self._row(1, Fraction(1, 5), Fraction(2, 5), Fraction(1, 40)),
            ],
            8: [
                self._row(0, Fraction(1, 2), Fraction(1, 2), Fraction(0)),
                self._row(1, Fraction(1, 3), Fraction(1, 4), Fraction(0)),
            ],
        }
        audit = audit_stages(rows, terminal_stage=8)
        self.assertEqual(audit["K1_outcome"], "A2")
        self.assertTrue(audit["T_PROJ"])
        self.assertFalse(audit["T_CLOSE"])
        self.assertEqual(audit["same_phase_prefix_alias_count"], 1)
        self.assertEqual(audit["terminal_alias_count"], 0)

    def test_cross_stage_coincidence_is_not_a_covariance_witness(self):
        rows = {
            1: [self._row(0, Fraction(1, 2), Fraction(1, 2), Fraction(0))],
            2: [self._row(0, Fraction(1, 2), Fraction(1, 2), Fraction(1, 10))],
        }
        audit = audit_stages(rows, terminal_stage=2)
        self.assertEqual(audit["K1_outcome"], "A0")
        self.assertEqual(audit["K2_outcome"], "A3")
        self.assertEqual(audit["terminal_alias_count"], 0)
        self.assertEqual(audit["cross_stage"]["count"], 1)
        self.assertTrue(audit["cross_stage"]["pairs"][0]["covariance_differs"])
        self.assertIn("clockless", interpretation("A0", "A3"))

    def test_benign_merge_is_not_an_alias(self):
        rows = {
            4: [
                self._row(0, Fraction(1, 2), Fraction(1, 2), Fraction(1, 9)),
                self._row(2, Fraction(1, 2), Fraction(1, 2), Fraction(1, 9)),
            ]
        }
        audit = audit_stages(rows, terminal_stage=4)
        self.assertEqual(audit["stages"][4]["alias_pair_count"], 0)
        self.assertEqual(audit["stages"][4]["benign_merge_pair_count"], 1)
        self.assertIsNone(min_marginal_separation(rows[4]))

    def _row(self, history, mx, my, cov):
        return {
            "history": history,
            "mx": mx,
            "my": my,
            "c": cov,
            "prob": Fraction(1, 2),
        }


class SourceSeparation(unittest.TestCase):
    def test_filter_replay_and_moments_do_not_import_each_other(self):
        modules = {
            "twostream_filter.py": (ROOT / "twostream_filter.py").read_text(encoding="utf-8"),
            "twostream_replay.py": (ROOT / "twostream_replay.py").read_text(encoding="utf-8"),
            "twostream_moments.py": (ROOT / "twostream_moments.py").read_text(encoding="utf-8"),
        }
        for name, source in modules.items():
            tree = ast.parse(source)
            imported = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imported.extend(alias.name for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    imported.append(node.module)
            for other in modules:
                if other != name:
                    self.assertNotIn(other[:-3], imported)
            self.assertNotIn("numpy", imported)
            self.assertNotIn("float(", source)


if __name__ == "__main__":
    unittest.main()
