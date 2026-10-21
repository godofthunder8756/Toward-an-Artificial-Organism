"""Freeze checks for graded joint recurrent reversion. No training and no phase A curve."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import unittest
from fractions import Fraction
from pathlib import Path

import numpy as np
import torch

from graded_reversion_appendix_a import (
    AppendixNotApproved,
    advantage_label,
    boundary_label,
    execute_appendix_a_training,
    is_boundary,
    rival_afit_label,
    rival_grid,
    run_appendix_a,
    select_rival,
)
from graded_reversion_draws import block_norm_errors, concatenated_draw_bytes, draws_sha256, raw_draws, rescale_draws
from graded_reversion_eval import endpoint_gaps, load_verified_checkpoint, probe_sham_restore, weight_hh_f64
from graded_reversion_outcomes import (
    auc,
    d_passes,
    eligibility,
    l_cont,
    l_prefix,
    l_prefix_components,
    l_prefix_probability,
    l_prefix_test,
    m_passes,
    pd_cd_components,
    saturation_index,
)
from graded_reversion_report import assert_phase_a_text, render_phase_a, render_phase_b
from graded_reversion_spec import (
    ALPHAS,
    AUC_DISCLAIMER,
    AUC_WEIGHTS,
    CLAIM_LIMITATION,
    CLAIM_NOT_MET,
    CLAIM_SUCCESS,
    CLAIM_UNRESOLVED_E1,
    CLAIM_UNRESOLVED_INVALID,
    CODE_FILES,
    CODE_VERSION,
    D_RULE,
    DENOMINATOR_RULE,
    DISPLACEMENT_RULE,
    DRAW_SEEDS,
    ENDPOINT_SENTENCE,
    EPS0,
    FREEZE_FILENAME,
    IDENTITY_TOL,
    N_RANDOM,
    PHASE_A_PREFIX,
    PRIMARY_NOT_MET,
    PRIMARY_REPLICATED,
    PROTOCOL_FILENAME,
    PROTOCOL_SHA256,
    READOUT_32_COUNT,
    READOUT_LIMITATION,
    RECURRENT_COUNT,
    SATURATION_RULE,
    TARGETS,
    TOTAL_843,
    UNDEFINED,
    UNRESOLVED,
    UNRESOLVED_E1,
)
from graded_reversion_train import approval_text_ok, missing_evaluation, refusal_reason
from graded_reversion_verdicts import claim_text, primary_label, secondary_label, transfer_label
from recurrent_core_transfer_models import CoreGRU, eval_copy, load_checkpoint, parameter_counts
from twostream_acquisition_oracle import World

ROOT = Path(__file__).resolve().parent

FROZEN_SHA256 = {
    "DEVIATIONS_AND_AMBIGUITIES.md": "bc734055ff4940921e7dcfcf0df774249a87a0563ab63c59ebf06cc7498b53c5",
    "recurrent_core_transfer_models.py": "6ec5ef187ae4dd417411d6b57b179e6a093a84264d9a91bd1d1ed676097aa5fa",
    "recurrent_core_transfer_train.py": "5cac4d077cdf48c5f7f21fc990c7d2afde66a342f103aaae6e857c990dfef12e",
    "recurrent_core_transfer_metrics.py": "c1a2e9ae9a381528afacc10693849c6387fcf95284332fa185afeefb62155d4b",
    "recurrent_core_results_v1/checkpoints/s100_f_trained.ckpt": "07096bc5ac83b579c84626d1caab73086363e6ddedf9a8bbe58394906f5175f8",
    "recurrent_core_results_v1/seeds/s100.json": "1c706c84d272e7189a4d3b922d4bc0ad9853c8ef0a016f1e7c834feda7d4b194",
}


def _child_env():
    env = os.environ.copy()
    env["OMP_NUM_THREADS"] = "1"
    env["MKL_NUM_THREADS"] = "1"
    env["OPENBLAS_NUM_THREADS"] = "1"
    env["PYTHONPATH"] = str(ROOT)
    return env


class ProtocolAndFreezeTest(unittest.TestCase):
    def test_protocol_bytes(self):
        digest = hashlib.sha256((ROOT / PROTOCOL_FILENAME).read_bytes()).hexdigest()
        self.assertEqual(digest, PROTOCOL_SHA256)

    def test_claim_strings_are_in_the_protocol(self):
        text = (ROOT / PROTOCOL_FILENAME).read_text(encoding="utf-8")
        for piece in (
            CLAIM_SUCCESS,
            CLAIM_LIMITATION,
            D_RULE,
            SATURATION_RULE,
            DENOMINATOR_RULE,
            ENDPOINT_SENTENCE,
            READOUT_LIMITATION,
            DISPLACEMENT_RULE,
            AUC_DISCLAIMER,
            PHASE_A_PREFIX,
            PRIMARY_REPLICATED,
            PRIMARY_NOT_MET,
        ):
            self.assertIn(piece, text, piece[:48])

    def test_freeze_manifest_matches_code_and_draws(self):
        path = ROOT / FREEZE_FILENAME
        self.assertTrue(path.exists(), "freeze manifest must exist before phase A")
        manifest = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(manifest["protocol_sha256"], PROTOCOL_SHA256)
        self.assertTrue(manifest["status"].startswith("FREEZE"))
        self.assertEqual(manifest["code_version"], CODE_VERSION)
        self.assertIn("not executed", manifest["phase_B_training"])
        self.assertIn("not approved", manifest["appendix_A"])
        for name in CODE_FILES:
            digest = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
            self.assertEqual(manifest["code_sha256"][name], digest, name)
        self.assertEqual(set(manifest["draw_sha256"]), {str(seed) for seed in DRAW_SEEDS})

    def test_approval_note(self):
        text = (ROOT / "GRADED_REVERSION_PHASE_B_APPROVAL.md").read_text(encoding="utf-8")
        self.assertTrue(approval_text_ok(text, PROTOCOL_SHA256))
        self.assertIn("does not approve Appendix A", text)
        self.assertIn("10:38 PM ET", text)

    def test_frozen_pr7_artifacts_unchanged(self):
        for name, digest in FROZEN_SHA256.items():
            actual = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
            self.assertEqual(actual, digest, name)

    def test_two_processes_byte_identical_draws(self):
        script = (
            "import json,sys\n"
            "from graded_reversion_draws import all_draw_sha256s, concatenated_draw_bytes\n"
            "if sys.argv[1] == 'sha':\n"
            "    print(json.dumps(all_draw_sha256s()))\n"
            "else:\n"
            "    sys.stdout.buffer.write(concatenated_draw_bytes())\n"
        )
        env = _child_env()

        def shas():
            proc = subprocess.run(
                [sys.executable, "-c", script, "sha"],
                cwd=ROOT,
                env=env,
                check=True,
                capture_output=True,
            )
            return json.loads(proc.stdout.decode("utf-8"))

        def raw():
            proc = subprocess.run(
                [sys.executable, "-c", script, "raw"],
                cwd=ROOT,
                env=env,
                check=True,
                capture_output=True,
            )
            return proc.stdout

        first = shas()
        second = shas()
        self.assertEqual(first, second)
        manifest = json.loads((ROOT / FREEZE_FILENAME).read_text(encoding="utf-8"))
        self.assertEqual(first, manifest["draw_sha256"])
        self.assertEqual(raw(), raw())
        self.assertEqual(hashlib.sha256(raw()).hexdigest(), hashlib.sha256(concatenated_draw_bytes()).hexdigest())

    def test_draw_sha_stable_after_deterministic_flag(self):
        before = draws_sha256(100)
        torch.use_deterministic_algorithms(True)
        after = draws_sha256(100)
        self.assertEqual(before, after)


class AlgebraTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.world = World()

    def test_parameter_counts(self):
        counts = parameter_counts(CoreGRU(32))
        self.assertEqual(counts["recurrent"], RECURRENT_COUNT)
        self.assertEqual(counts["readout"], READOUT_32_COUNT)
        self.assertEqual(counts["total"], TOTAL_843)
        self.assertEqual((456, 387, 843), (counts["recurrent"], counts["readout"], counts["total"]))
        self.assertEqual(tuple(CoreGRU(32).rnn.weight_hh_l0.shape), (24, 8))

    def test_trapezoid_weights_and_linear_auc(self):
        weights = (
            Fraction(1, 16),
            Fraction(1, 8),
            Fraction(3, 16),
            Fraction(1, 4),
            Fraction(1, 4),
            Fraction(1, 8),
        )
        self.assertEqual(sum(weights), 1)
        self.assertEqual(tuple(float(weight) for weight in weights), AUC_WEIGHTS)
        self.assertEqual(sum(AUC_WEIGHTS), 1.0)
        for dose in (0.0, 0.25, 1.0, -0.5):
            deltas = [dose * alpha for alpha in ALPHAS]
            self.assertAlmostEqual(auc(deltas), dose / 2.0, places=12)

    def test_l_prefix_identities(self):
        oracle = self.world.q
        self.assertEqual(l_prefix(oracle, oracle), 0.0)
        scale = pd_cd_components(oracle)
        self.assertAlmostEqual(scale["PD"], 0.013839, places=6)
        self.assertAlmostEqual(scale["PD_X"], 0.003046, places=6)
        self.assertAlmostEqual(scale["PD_Y"], 0.000697, places=6)
        self.assertAlmostEqual(scale["PD_XOR"], 0.010095, places=6)
        self.assertAlmostEqual(scale["CD"], 0.14172, places=5)
        generator = np.random.default_rng(0)
        continuation = generator.random((16, 3))
        blind = np.zeros_like(oracle)
        for prefix in range(16):
            for index in range(16):
                blind[prefix + 16 * index] = continuation[index]
        self.assertAlmostEqual(l_prefix(blind, oracle), scale["PD"], places=12)
        components = l_prefix_components(blind, oracle)
        self.assertAlmostEqual(components["X"] + components["Y"] + components["XOR"], scale["PD"], places=12)
        shifted = oracle.copy()
        for prefix in range(16):
            for index in range(16):
                shifted[prefix + 16 * index] = oracle[prefix + 16 * index] + continuation[index]
        self.assertLessEqual(abs(l_prefix(shifted, oracle)), 1e-20)
        self.assertLessEqual(abs(l_cont(oracle, oracle)), 1e-20)
        self.assertAlmostEqual(l_prefix_probability(oracle, oracle, self.world.probability), 0.0, places=15)
        self.assertAlmostEqual(l_prefix_test(oracle, oracle, self.world.is_test), 0.0, places=15)
        self.assertAlmostEqual(
            l_prefix_probability(blind, oracle, self.world.probability),
            l_prefix_probability(np.zeros_like(oracle), oracle, self.world.probability),
            places=12,
        )

    def test_baseline_signs_and_rules(self):
        pd_value = 0.02
        trained = 0.005
        init = 0.015
        b_prefix = init - trained
        c_prefix = pd_value - trained
        eligible, reasons = eligibility(True, True, b_prefix, c_prefix, 1.0)
        self.assertTrue(eligible)
        self.assertEqual(reasons, [])
        eligible, reasons = eligibility(True, True, -0.01, c_prefix, 1.0)
        self.assertFalse(eligible)
        self.assertIn("B_prefix", reasons)
        eligible, reasons = eligibility(True, True, b_prefix, -0.001, 1.0)
        self.assertFalse(eligible)
        self.assertIn("C_prefix", reasons)
        eligible, reasons = eligibility(True, True, EPS0, c_prefix, 1.0)
        self.assertFalse(eligible)
        self.assertIn("B_prefix", reasons)
        self.assertFalse(d_passes(1.0, [1.0 - EPS0] + [0.0] * (N_RANDOM - 1)))
        self.assertTrue(d_passes(1.0, [1.0 - EPS0 - 1e-9] + [0.0] * (N_RANDOM - 1)))
        self.assertTrue(d_passes(-0.1, [-0.2] * N_RANDOM))
        self.assertFalse(m_passes(EPS0, 0.0))
        self.assertTrue(m_passes(0.25, 1.0))
        self.assertTrue(m_passes(0.25, 1.0))
        self.assertFalse(m_passes(0.25 - 1e-12, 1.0))
        self.assertEqual(saturation_index(0.1, EPS0), UNDEFINED)
        self.assertEqual(saturation_index(0.1, EPS0 / 2), UNDEFINED)
        self.assertAlmostEqual(saturation_index(-0.25, 0.5), -0.5)
        self.assertIsInstance(saturation_index(-0.25, 0.5), float)

    def test_path_endpoints_and_checkpoints(self):
        generator = torch.Generator(device="cpu")
        generator.manual_seed(7)
        trained = torch.randn((24, 8), dtype=torch.float32, generator=generator).to(dtype=torch.float64)
        init = torch.randn((24, 8), dtype=torch.float32, generator=generator).to(dtype=torch.float64)
        gaps = endpoint_gaps(trained, init)
        self.assertTrue(gaps["w0_exact"])
        self.assertLessEqual(gaps["w1_max_abs"], EPS0)
        for seed in range(100, 110):
            directory = ROOT / "recurrent_core_results_v1"
            payload = json.loads((directory / "seeds" / ("s%d.json" % seed)).read_text(encoding="utf-8"))
            expected = {
                "f_trained": payload["f_trained"]["checkpoint_sha256"],
                "f_init": payload["f_init"]["checkpoint_sha256"],
                "cand_init": payload["cand"]["init_checkpoint_sha256"],
            }
            states = {}
            for key, filename in (
                ("f_trained", "s%d_f_trained.ckpt" % seed),
                ("f_init", "s%d_f_init.ckpt" % seed),
                ("cand_init", "s%d_cand_init.ckpt" % seed),
            ):
                state, ok, _file_sha = load_verified_checkpoint(
                    directory / "checkpoints" / filename, expected[key]
                )
                self.assertTrue(ok, "%s %s" % (seed, key))
                states[key] = state
            self.assertTrue(
                torch.equal(states["f_init"]["rnn.weight_hh_l0"], states["cand_init"]["rnn.weight_hh_l0"])
            )
            trained_hh = weight_hh_f64(states["f_trained"])
            init_hh = weight_hh_f64(states["cand_init"])
            gaps = endpoint_gaps(trained_hh, init_hh)
            self.assertTrue(gaps["w0_exact"], seed)
            self.assertLessEqual(gaps["w1_max_abs"], EPS0, seed)
            delta = (init_hh - trained_hh).numpy()
            full = float(np.linalg.norm(delta))
            self.assertGreater(full, 3.0)
            self.assertLess(full, 5.0)
            scaled, _info = rescale_draws(raw_draws(seed), delta)
            report = block_norm_errors(scaled, delta)
            self.assertTrue(report["ok"], report)
            self.assertLessEqual(report["worst_relative"], 1e-12)
            self.assertLessEqual(report["full_max_relative"], 1e-12)

    def test_zero_block_synthetic_delta(self):
        generator = np.random.default_rng(4)
        delta = np.zeros((24, 8), dtype=np.float64)
        delta[0:8] = generator.normal(size=(8, 8))
        delta[16:24] = generator.normal(size=(8, 8))
        delta[8:16] = 1e-14
        scaled, info = rescale_draws(raw_draws(101), delta)
        self.assertTrue(info[1]["zero"])
        self.assertTrue(np.all(scaled[:, 8:16, :] == 0))
        report = block_norm_errors(scaled, delta)
        self.assertTrue(report["ok"], report)
        self.assertGreater(report["blocks"]["r"]["target"], 0.1)
        self.assertGreater(report["blocks"]["n"]["target"], 0.1)

    def test_sham_restore_and_endpoint_identity(self):
        torch.manual_seed(1)
        synthetic = eval_copy(CoreGRU(32))
        probe = probe_sham_restore(synthetic)
        self.assertLessEqual(probe["sham_gap"], EPS0)
        self.assertLessEqual(probe["restore_gap"], IDENTITY_TOL)
        state = load_checkpoint(ROOT / "recurrent_core_results_v1" / "checkpoints" / "s100_f_trained.ckpt")
        model = CoreGRU(32)
        from recurrent_core_transfer_models import load_snapshot

        load_snapshot(model, state)
        copied = eval_copy(model)
        probe = probe_sham_restore(copied)
        self.assertLessEqual(probe["sham_gap"], EPS0)
        self.assertLessEqual(probe["restore_gap"], IDENTITY_TOL)
        init_state = load_checkpoint(ROOT / "recurrent_core_results_v1" / "checkpoints" / "s100_cand_init.ckpt")
        gaps = endpoint_gaps(weight_hh_f64(state), weight_hh_f64(init_state))
        self.assertTrue(gaps["ok"])


class VerdictTest(unittest.TestCase):
    def test_precedence_and_claim_strings(self):
        e1_fail = [True] * 7 + [False] * 3
        e1_ok = [True] * 10
        valid = [True] * 10
        joint = [True] * 10
        self.assertEqual(primary_label(e1_fail, valid, joint), UNRESOLVED_E1)
        self.assertEqual(claim_text(e1_fail, valid, joint, joint, joint, joint), CLAIM_UNRESOLVED_E1)
        invalid = [True] * 7 + [False] * 3
        self.assertEqual(primary_label(e1_ok, invalid, [True] * 7 + [False] * 3), UNRESOLVED)
        self.assertEqual(
            claim_text(e1_ok, invalid, [False] * 10, [False] * 10, [False] * 10, [False] * 10),
            CLAIM_UNRESOLVED_INVALID,
        )
        seven = [True] * 7 + [False] * 3
        self.assertEqual(primary_label(e1_ok, valid, seven), PRIMARY_NOT_MET)
        directional = [True] * 8 + [False] * 2
        material = [True] * 6 + [False] * 4
        eligible = [True] * 8 + [False] * 2
        text = claim_text(e1_ok, valid, seven, directional, material, eligible)
        self.assertEqual(text, CLAIM_NOT_MET % (7, 8, 6, 2))
        self.assertIn("7/10 seeds passed", text)
        self.assertNotIn("immaterial", text)
        eight_valid = [True] * 8 + [False] * 2
        eight_joint = [True] * 8 + [False] * 2
        self.assertEqual(primary_label(e1_ok, eight_valid, eight_joint), PRIMARY_REPLICATED)
        success = claim_text(e1_ok, eight_valid, eight_joint, eight_joint, eight_joint, eight_joint)
        self.assertEqual(success, CLAIM_SUCCESS + " " + CLAIM_LIMITATION)
        self.assertTrue(success.startswith(CLAIM_SUCCESS))
        secondary = secondary_label(e1_ok, valid, seven)
        self.assertTrue(secondary.startswith("Secondary (block-wise):"))
        self.assertIn(PRIMARY_NOT_MET, secondary)
        self.assertEqual(transfer_label(valid, [True] * 8 + [False] * 2), "TRANSFER SHOWN")
        self.assertEqual(transfer_label(valid, [True] * 7 + [False] * 3), "TRANSFER NOT SHOWN")
        self.assertEqual(transfer_label(invalid, [True] * 10), UNRESOLVED)

    def test_phase_a_text_has_no_aggregate_and_no_banned_words(self):
        records = []
        for seed in range(100, 110):
            target = {
                "auc_rev": 0.01 * (seed - 100),
                "auc_random_max": 0.004,
                "D": seed % 2 == 0,
                "M": seed % 3 == 0,
                "endpoint_delta_L_prefix": 0.02,
                "endpoint_E_TEST_total": 0.03,
                "endpoint_delta_E_TEST_total": 0.01,
                "endpoint_E_TEST_XOR": 0.004,
                "endpoint_delta_E_TEST_XOR": 0.001,
            }
            records.append(
                {
                    "seed": seed,
                    "L_prefix_f_trained": 0.002,
                    "L_prefix_f_trained_over_PD": 0.14,
                    "B_prefix": 0.01,
                    "B_prefix_over_PD": 0.7,
                    "C_prefix": 0.012,
                    "C_prefix_over_PD": 0.86,
                    "eligible": {name: True for name in TARGETS},
                    "eligibility_reasons": {name: [] for name in TARGETS},
                    "targets": {name: dict(target) for name in TARGETS},
                }
            )
        text = render_phase_a(
            records,
            {
                "protocol_sha256": PROTOCOL_SHA256,
                "freeze_manifest_sha256": "abc",
                "freeze_commit": "def",
            },
        )
        assert_phase_a_text(text)
        self.assertNotIn("verdict", text.lower())
        self.assertEqual(text.count("## Per-seed primary"), 1)

    def test_phase_b_report_uses_the_frozen_failure_wording(self):
        records = []
        for offset, seed in enumerate(range(200, 210)):
            evaluation = missing_evaluation(seed, [])
            evaluation["valid"] = True
            evaluation["curves_missing"] = False
            evaluation["transfer_pass"] = True
            evaluation["B_prefix"] = 0.02
            evaluation["C_prefix"] = 0.01
            evaluation["B_prefix_over_PD"] = 1.4
            evaluation["C_prefix_over_PD"] = 0.7
            evaluation["L_prefix_f_trained"] = 0.003
            evaluation["E_TEST_XOR_f_trained"] = 0.001
            evaluation["eligible"] = {name: True for name in TARGETS}
            evaluation["eligibility_reasons"] = {name: [] for name in TARGETS}
            joint = offset < 7
            evaluation["joint"] = {name: joint for name in TARGETS}
            target = {
                "auc_rev": 0.01 if joint else 0.001,
                "auc_random_max": 0.004,
                "D": joint,
                "M": joint,
                "L_cont_auc": 0.02,
                "L_prefix_XOR_auc": 0.005,
                "endpoint_E_TEST_XOR": 0.002,
                "endpoint_delta_E_TEST_total": 0.01,
                "endpoint_delta_L_prefix": 0.02,
                "saturation": UNDEFINED,
                "nondecreasing_steps": 3,
                "forecast_change_max_abs": 0.1,
            }
            evaluation["targets"] = {name: dict(target) for name in TARGETS}
            records.append(
                {
                    "seed": seed,
                    "e1_pass": True,
                    "evaluation": evaluation,
                }
            )
        from graded_reversion_verdicts import claim_text as build_claim

        e1 = [True] * 10
        valid = [True] * 10
        joint = [offset < 7 for offset in range(10)]
        claim = build_claim(e1, valid, joint, joint, joint, [True] * 10)
        text = render_phase_b(
            records,
            {"protocol_sha256": PROTOCOL_SHA256, "freeze_commit": "abc", "phase_a_dir": "graded_reversion_phaseA_exploratory"},
            claim,
        )
        self.assertIn(CLAIM_NOT_MET % (7, 7, 7, 0), text)
        self.assertIn("## Development history", text)
        self.assertIn("not pooled", text.lower())
        self.assertIn(PRIMARY_NOT_MET, text)

    def test_phase_b_guard_and_appendix_refusal(self):
        self.assertIn("approval", refusal_reason(False, True, {"blocking_engineering_issue": False, "code_version": CODE_VERSION}))
        self.assertIn("Freeze", refusal_reason(True, False, {"blocking_engineering_issue": False, "code_version": CODE_VERSION}))
        self.assertIn("Phase A", refusal_reason(True, True, None))
        self.assertIn(
            "engineering",
            refusal_reason(True, True, {"blocking_engineering_issue": True, "code_version": CODE_VERSION}),
        )
        self.assertIsNone(refusal_reason(True, True, {"blocking_engineering_issue": False, "code_version": CODE_VERSION}))
        with self.assertRaises(AppendixNotApproved):
            run_appendix_a()
        with self.assertRaises(AppendixNotApproved):
            execute_appendix_a_training([], {}, None, ROOT)
        rows = rival_grid()
        self.assertEqual(len(rows), 47)
        origins = {}
        for row in rows:
            origins[row["origin"]] = origins.get(row["origin"], 0) + 1
        self.assertEqual(origins, {"original": 5, "overlap": 4, "extension": 38})
        self.assertTrue(any(is_boundary(row["g"], row["b"]) and row["g"] == 8.0 for row in rows))
        self.assertTrue(any(row["b"] == -6.0 for row in rows))
        import math

        synthetic = [{"g": row["g"], "b": row["b"], "criterion": 5.0} for row in rows]
        synthetic[3]["criterion"] = -1.0
        chosen, tie = select_rival(synthetic)
        self.assertFalse(tie)
        self.assertEqual((chosen["g"], chosen["b"]), (synthetic[3]["g"], synthetic[3]["b"]))
        synthetic[4]["criterion"] = -1.0 + (EPS0 / 2.0)
        chosen, tie = select_rival(synthetic)
        self.assertTrue(tie)
        band = [row for row in synthetic if row["criterion"] - (-1.0) <= EPS0]
        expected = min(band, key=lambda row: (abs(math.log2(row["g"])), abs(row["b"]), row["b"], row["g"]))
        self.assertEqual((chosen["g"], chosen["b"]), (expected["g"], expected["b"]))
        self.assertEqual(boundary_label([(8.0, 0.0)] * 3 + [(1.0, 0.0)] * 7), "TUNED RIVAL STILL EDGE-LIMITED")
        self.assertIsNone(boundary_label([(1.0, 0.0)] * 10))
        self.assertIn("within the declared 47-configuration grid", advantage_label(True))
        self.assertIn("within the declared 47-configuration grid", rival_afit_label(False))


if __name__ == "__main__":
    unittest.main()
