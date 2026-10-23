"""Unit tests for the two-stream acquisition study.

Toy forwards and two-step updates only. The 4000-step study is not run here.
"""

from __future__ import annotations

import unittest
from fractions import Fraction

import numpy as np
import torch

from twostream_acquisition_metrics import (
    _repair,
    centered_ridge,
    component_excess,
    full_analysis,
    identity_checks,
    quantize_coordinates,
    round_ties_even,
)
from twostream_acquisition_models import build_model, eval_copy, parameter_counts, snapshot_state
from twostream_acquisition_oracle import filter_disagreements, load_world
from twostream_acquisition_spec import (
    B_GRID,
    DEVIATIONS,
    LR_FINAL,
    LR_INIT,
    PROTOCOL_SHA256,
    STEPS,
    Spec,
    cosine_lr,
    is_test_history,
    iter_specs,
)
from twostream_acquisition_study import sha256_file
from twostream_acquisition_study import ROOT
from twostream_acquisition_train import episodes_from_uniforms, sample_batch, train_model
from twostream_acquisition_verdicts import (
    BASE_CLAIM,
    assemble_claim,
    e1_label,
    e2_label,
    e3_label,
    study_verdict,
)


class ProtocolAndSplit(unittest.TestCase):
    def test_protocol_hash_is_the_reviewed_file(self):
        digest = sha256_file(ROOT / "TWOSTREAM_ACQUISITION_PROTOCOL_v1.md")
        self.assertEqual(digest, PROTOCOL_SHA256)

    def test_split_counts_and_prefix_exclusion(self):
        test = [h for h in range(256) if is_test_history(h)]
        train = [h for h in range(256) if not is_test_history(h)]
        self.assertEqual(len(test), 64)
        self.assertEqual(len(train), 192)
        for stage in (6, 7, 8):
            mask = (1 << stage) - 1
            overlap = {h & mask for h in test} & {h & mask for h in train}
            self.assertEqual(overlap, set(), stage)

    def test_run_count_and_kfr_scope(self):
        specs = list(iter_specs())
        self.assertEqual(len(specs), 120)
        self.assertEqual(len({spec.file_stem() for spec in specs}), 120)
        self.assertFalse(any(spec.arm == "K-FR" and spec.hidden == 2 for spec in specs))
        self.assertEqual(sum(1 for spec in specs if spec.arm == "K-FR"), 40)

    def test_cosine_endpoints(self):
        self.assertAlmostEqual(cosine_lr(0), LR_INIT)
        self.assertAlmostEqual(cosine_lr(STEPS - 1), LR_FINAL)

    def test_deviations_are_recorded(self):
        self.assertGreaterEqual(len(DEVIATIONS), 8)
        text = " ".join(DEVIATIONS)
        self.assertNotIn("consciousness is", text)


class OracleAgreement(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.world = load_world()

    def test_filter_matches_results_json(self):
        self.assertEqual(filter_disagreements(self.world), [])

    def test_published_rounding(self):
        published = self.world.published
        self.assertAlmostEqual(round(float(published["oracle_brier"]["X"]), 6), 0.212406)
        self.assertAlmostEqual(round(float(published["oracle_brier"]["Y"]), 6), 0.155028)
        self.assertAlmostEqual(round(float(published["oracle_brier"]["XOR"]), 6), 0.214954)
        self.assertAlmostEqual(round(float(published["current_only_excess_total"]), 6), 0.077612)
        self.assertAlmostEqual(round(float(published["four_c2"]), 7), 0.0079539)
        self.assertEqual(published["alias_k1"], "A0")

    def test_split_references_are_not_the_unconditional_reweight(self):
        self.assertEqual(self.world.is_test.sum(), 64)
        self.assertNotAlmostEqual(float(self.world.e_cur["TEST"]["total"]), 0.077612, places=4)
        self.assertGreater(float(self.world.afit_threshold["TEST"]["total"]), 0)
        self.assertGreater(float(self.world.afit_threshold["TEST"]["XOR"]), 0)
        self.assertEqual(len(self.world.nearest_posterior), 16)
        self.assertTrue(all(int(self.world.nearest_posterior[i]) != i for i in range(16)))

    def test_exact_excess_of_oracle_is_zero(self):
        errors = component_excess(self.world.q, self.world)
        self.assertEqual(errors["TEST"]["total"], 0.0)
        self.assertEqual(errors["TRAIN"]["XOR"], 0.0)

    def test_reference_arms(self):
        from twostream_acquisition_metrics import reference_arm_report

        report = reference_arm_report(self.world)
        self.assertTrue(report["K-EXACT"]["afit_test"])
        self.assertGreater(report["K-CUR"]["errors"]["TEST"]["total"], 0.0)
        self.assertGreater(report["K-PROD*"]["errors"]["TEST"]["XOR"], 0.0)
        self.assertIn("precision", report["K-EXACT"])


class ParameterCounts(unittest.TestCase):
    def test_protocol_table(self):
        expected = {
            ("gru", 4, 3): (180, 259),
            ("gru", 8, 3): (456, 387),
            ("gru", 16, 3): (1296, 643),
            ("rnn", 8, 3): (152, 387),
            ("gru", 2, 3): (78, 195),
            ("mlp", 2, 3): (226, 195),
            ("gru", 8, 2): (456, 354),
        }
        for (cell, hidden, outputs), (recurrent, readout) in expected.items():
            model = build_model(Spec("CAND", cell, hidden, 0, outputs, False))
            counts = parameter_counts(model)
            self.assertEqual(counts["recurrent"], recurrent, (cell, hidden, outputs))
            self.assertEqual(counts["readout"], readout, (cell, hidden, outputs))

    def test_table_storage(self):
        model = build_model(Spec("K-TAB", "table", 0, 0, 3, False))
        self.assertEqual(parameter_counts(model)["readout"], 768)
        self.assertTrue(torch.equal(model.logits, torch.zeros(256, 3)))


class QuantizerAndRidge(unittest.TestCase):
    def test_ties_to_even(self):
        self.assertEqual(int(round_ties_even(np.array([0.5]), 1)[0]), 0)
        self.assertEqual(int(round_ties_even(np.array([1.5]), 3)[0]), 2)
        lo = np.array([0.0])
        hi = np.array([1.0])
        recon, outside, constant = quantize_coordinates(np.array([0.5]), lo, hi, 1)
        self.assertEqual(recon[0], 0.0)
        self.assertFalse(bool(outside[0]))
        self.assertFalse(bool(constant[0]))
        recon, _outside, _constant = quantize_coordinates(np.array([0.5]), lo, hi, 2)
        self.assertAlmostEqual(recon[0], 2.0 / 3.0)

    def test_clip_and_constant(self):
        lo = np.array([0.0, 1.0])
        hi = np.array([1.0, 1.0])
        recon, outside, constant = quantize_coordinates(np.array([-0.2, 3.0]), lo, hi, 2)
        self.assertTrue(bool(outside[0]))
        self.assertTrue(bool(constant[1]))
        self.assertGreaterEqual(recon[0], 0.0)
        self.assertLessEqual(recon[0], 1.0)
        self.assertEqual(recon[1], 1.0)

    def test_frechet_repair(self):
        mx, my, c, changed = _repair(1.2, -0.1, 0.5)
        self.assertEqual((mx, my, c), (1.0, 0.0, 0.0))
        self.assertTrue(changed)
        mx, my, c, changed = _repair(0.5, 0.5, 0.0)
        self.assertFalse(changed)

    def test_centered_ridge_normal_equation(self):
        rng = np.random.default_rng(0)
        states = rng.normal(size=(8, 4))
        targets = rng.normal(size=(8, 3))
        weight, _intercept, _z_mean, _y_mean = centered_ridge(states, targets, 1e-3)
        centered_z = states - states.mean(0)
        centered_y = targets - targets.mean(0)
        gram = centered_z.T @ centered_z + 1e-3 * np.eye(4)
        residual = gram @ weight - centered_z.T @ centered_y
        self.assertLess(np.linalg.norm(residual), 1e-8)


class SamplingAndTraining(unittest.TestCase):
    def test_uniform_layout(self):
        # U=0.99 is above every protocol probability, so every Bernoulli draw is 0.
        high = torch.full((1, 31), 0.99, dtype=torch.float64)
        _bits, labels, history = episodes_from_uniforms(high)
        self.assertEqual(int(history[0]), 0)
        self.assertEqual(int(labels.sum()), 0)
        self.assertTrue(is_test_history(0))
        # Latent bits 1 (U<1/2), no channel flips and no transitions (U>=1/5).
        uniforms = torch.full((1, 31), 0.5, dtype=torch.float64)
        uniforms[0, 0] = 0.0
        uniforms[0, 1] = 0.0
        bits, labels, history = episodes_from_uniforms(uniforms)
        self.assertEqual(int(history[0]), 255)
        self.assertFalse(is_test_history(255))
        self.assertTrue(torch.equal(bits, torch.ones(1, 8)))
        self.assertEqual([int(labels[0, i]) for i in range(3)], [1, 1, 0])

    def test_rejection_stays_in_train(self):
        generator = torch.Generator().manual_seed(1000)
        bits, labels = sample_batch(generator, 64)
        self.assertEqual(tuple(bits.shape), (64, 8))
        history = (bits.long() * (2 ** torch.arange(8))).sum(dim=1)
        self.assertTrue(all(not is_test_history(int(h)) for h in history))
        self.assertTrue(torch.all((labels == 0) | (labels == 1)))

    def test_step_matches_fused_forward(self):
        torch.manual_seed(0)
        bits = torch.randint(0, 2, (16, 8)).double()
        for spec in (
            Spec("CAND", "gru", 8, 0, 3, False),
            Spec("K-PCO", "gru", 8, 0, 2, False),
            Spec("K-2D-MLP", "mlp", 2, 0, 3, False),
        ):
            model = build_model(spec).double().eval()
            fused = model(bits)
            state = model.initial_state(16, torch.float64, bits.device)
            for stage in range(8):
                state = model.step(state, bits[:, stage], stage)
            stepped = model.readout(state)
            gap = torch.max(torch.abs(fused - stepped)).item()
            self.assertLess(gap, 1e-8, spec.configuration())

    def test_paired_init_and_two_step_determinism(self):
        def once(freeze):
            torch.manual_seed(3)
            spec = Spec("K-FR" if freeze else "CAND", "gru", 8, 3, 3, freeze)
            model = build_model(spec)
            initial = snapshot_state(model)
            info = train_model(model, spec, steps=2, batch=32)
            return initial, snapshot_state(model), info

        init_a, _final_a, info_a = once(False)
        init_b, final_b, info_b = once(True)
        for key in init_a:
            self.assertTrue(torch.equal(init_a[key], init_b[key]))
        self.assertTrue(info_a["integrity_training"])
        self.assertTrue(info_b["integrity_training"])
        for key in final_b:
            if key.startswith("rnn."):
                self.assertTrue(torch.equal(init_b[key], final_b[key]))
            if key.startswith("readout_"):
                self.assertFalse(torch.equal(init_b[key], final_b[key]))
        _init_c, final_c, _info_c = once(False)
        _init_d, final_d, _info_d = once(False)
        for key in final_c:
            self.assertTrue(torch.equal(final_c[key], final_d[key]))

    def test_toy_execute_serializes(self):
        import json

        from twostream_acquisition_study import execute, to_jsonable

        record = execute(Spec("CAND", "gru", 4, 0, 3, False), load_world(), steps=2)
        json.dumps(to_jsonable(record))
        self.assertTrue(record["complete"])
        self.assertEqual(record["training"]["steps_completed"], 2)
        self.assertTrue(record["integrity"])


class UntrainedIntegrity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.world = load_world()

    def _analyze(self, spec: Spec):
        torch.manual_seed(spec.seed)
        model = build_model(spec)
        init_state = snapshot_state(model)
        copied = eval_copy(model)
        from twostream_acquisition_metrics import predict_only

        init_eval = predict_only(model, self.world)
        identity = identity_checks(copied, init_eval["predictions"], init_eval["states"])
        self.assertTrue(identity["ok"], identity)
        self.assertLessEqual(identity["whole_state_max_abs"], 1e-9)
        train_info = {"integrity_training": True, "steps_completed": 0, "final_loss": None, "failure_step": None}
        record = full_analysis(model, spec, self.world, init_state, init_eval, train_info)
        self.assertTrue(record["integrity"], record["identity"])
        self.assertIn("final", record)
        return record

    def test_gru8_untrained_analysis(self):
        record = self._analyze(Spec("CAND", "gru", 8, 0, 3, False))
        self.assertTrue(record["interventions"]["applicable"])
        self.assertIn("ratios", record["interventions"])
        self.assertIn("b", record["precision"]["curve"][0])
        self.assertEqual([row["b"] for row in record["precision"]["curve"]], list(B_GRID))
        self.assertTrue(record["chart_probe"]["applicable"])

    def test_table_and_two_dimensional_untrained(self):
        table = self._analyze(Spec("K-TAB", "table", 0, 0, 3, False))
        self.assertFalse(table["interventions"]["applicable"])
        self.assertEqual(table["precision"]["b_sel"], "exact index; logits unquantized")
        low = self._analyze(Spec("K-2D", "gru", 2, 1, 3, False))
        self.assertTrue(low["interventions"]["descriptive_only"])
        mlp = self._analyze(Spec("K-2D-MLP", "mlp", 2, 1, 3, False))
        self.assertTrue(mlp["integrity"])
        product = self._analyze(Spec("K-PCO", "gru", 8, 2, 2, False))
        self.assertTrue(product["final"]["outputs_valid"])


class VerdictRules(unittest.TestCase):
    def test_e1_boundaries(self):
        def row(afit, alearn, integrity):
            return {"afit": afit, "alearn": alearn, "integrity": integrity}

        shown = [row(True, True, True) for _ in range(8)] + [row(False, True, True), row(False, True, True)]
        self.assertEqual(e1_label(shown), "SHOWN")
        not_shown = [row(True, True, True), row(True, True, True)] + [row(False, True, True) for _ in range(8)]
        self.assertEqual(e1_label(not_shown), "NOT SHOWN")
        mixed = [row(True, True, True) for _ in range(5)] + [row(False, True, True) for _ in range(5)]
        self.assertEqual(e1_label(mixed), "UNRESOLVED")
        self.assertEqual(study_verdict("SHOWN", 8), "ADMIT")
        self.assertEqual(study_verdict("NOT SHOWN", 8), "REJECT")
        self.assertEqual(study_verdict("SHOWN", 7), "UNRESOLVED")
        self.assertEqual(study_verdict("UNRESOLVED", 10), "UNRESOLVED")

    def test_e2_and_e3_labels(self):
        supported = [
            {"intact": True, "tie": False, "ratio_le_half": True, "kfr_afit": False} for _ in range(8)
        ] + [{"intact": True, "tie": False, "ratio_le_half": False, "kfr_afit": False} for _ in range(2)]
        self.assertEqual(e2_label(supported), "RECURRENT ADAPTATION SUPPORTED")
        frozen = [
            {"intact": True, "tie": False, "ratio_le_half": False, "kfr_afit": True} for _ in range(8)
        ] + [{"intact": True, "tie": True, "ratio_le_half": False, "kfr_afit": True} for _ in range(2)]
        self.assertEqual(e2_label(frozen), "FROZEN-RECURRENCE READOUT SUFFICIENT AT THIS BUDGET")
        unclear = [
            {"intact": True, "tie": False, "ratio_le_half": False, "kfr_afit": False} for _ in range(10)
        ]
        self.assertEqual(e2_label(unclear), "READOUT-ONLY INSUFFICIENT, RECURRENT CONTRIBUTION UNCLEAR")
        localized = [{"localized": True, "coverage_ok": True, "rank_ok": True} for _ in range(8)]
        localized += [{"localized": False, "coverage_ok": True, "rank_ok": True} for _ in range(2)]
        self.assertEqual(e3_label(localized), "LOCALIZED BY THE CHART-DECODER INTERVENTION")
        broken = [{"localized": True, "coverage_ok": False, "rank_ok": True} for _ in range(10)]
        self.assertEqual(e3_label(broken), "UNRESOLVED")
        absent = [{"localized": False, "coverage_ok": True, "rank_ok": True} for _ in range(10)]
        self.assertEqual(e3_label(absent), "NOT LOCALIZED BY THIS INTERVENTION")

    def test_claim_uses_the_protocol_base_only_on_admit(self):
        claim = assemble_claim(
            "ADMIT",
            "FROZEN-RECURRENCE READOUT SUFFICIENT AT THIS BUDGET",
            "UNRESOLVED",
            False,
            [],
        )
        self.assertIn(BASE_CLAIM, claim)
        self.assertIn("not established by this comparison", claim)
        rejected = assemble_claim("REJECT", "UNRESOLVED", "UNRESOLVED", False, [])
        self.assertNotIn(BASE_CLAIM, rejected)
        self.assertIn("was not shown", rejected)


if __name__ == "__main__":
    unittest.main()
