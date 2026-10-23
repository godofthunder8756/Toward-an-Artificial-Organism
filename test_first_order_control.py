"""Freeze tests for first-order and isotropic controls. No phase A curve and no training."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

import numpy as np
import torch

from first_order_control_construct import construct_fo_paths, radius_quantities
from first_order_control_criteria import (
    d_family,
    eligibility_target,
    endpoint_counts,
    family_margin_report,
    fo_auc_from_dot,
    is_thin,
    joint_pass,
    m_flag,
    margin_sentence,
    percentage_undefined,
    rank_of_rev,
)
from first_order_control_draws import (
    concatenated_manifest_bytes,
    fo_generator_seed,
    fo_raw_draws,
    grad_generator_seed,
    grad_raw_draws,
    iso_generator_seed,
    iso_raw_draws,
    sha256_array,
)
from first_order_control_gradient import (
    bit_tensor,
    compute_gradient,
    fd_within_tolerance,
    finite_difference_report,
    l_prefix_torch,
    oracle_tensor,
    prefix_loss,
    untied_stage_gradients,
)
from first_order_control_report import assert_phase_a_text, render_phase_a, render_phase_b
from first_order_control_spec import (
    CLAIM_NOT_MET,
    CLAIM_SUCCESS,
    CLAIM_UNRESOLVED_E1,
    CLAIM_UNRESOLVED_INSUFFICIENT,
    CODE_FILES,
    CODE_VERSION,
    DISCLOSURE,
    EPS0,
    FAMILY_FO,
    FAMILY_ISO,
    FD_ABS_FLOOR,
    FD_REL,
    FREEZE_FILENAME,
    G_ZERO,
    MANIFEST_SEEDS,
    N_PATHS,
    PHASE_A_HEADLINE,
    PHASE_A_PREFIX,
    PRIMARY_NOT_MET,
    PRIMARY_REPLICATED,
    PROTOCOL_FILENAME,
    PROTOCOL_SHA256,
    RHO_COLLAPSE,
    SINGLE_BLOCK_SENTENCE,
    TIED_GRAD_ATOL,
    UNRESOLVED_E1,
    UNRESOLVED_INSUFFICIENT,
    fo_generator_seed as spec_fo_seed,
)
from first_order_control_study import approval_text_ok, load_freeze
from first_order_control_verdicts import (
    primary_label,
    robustness_applies,
    secondary_label,
    unevaluable_count,
    verdict_paragraph,
)
from graded_reversion_draws import draws_sha256
from graded_reversion_eval import module_from_state, weight_hh_f64
from graded_reversion_outcomes import auc, l_prefix
from graded_reversion_spec import ALPHAS, AUC_WEIGHTS, PROTOCOL_SHA256 as PR8_PROTOCOL_SHA256
from recurrent_core_transfer_models import CoreGRU, MatrixOverride, load_checkpoint
from recurrent_core_transfer_spec import CONTINUATION_STAGES
from twostream_acquisition_metrics import all_bits, continue_from, rollout
from twostream_acquisition_oracle import World

ROOT = Path(__file__).resolve().parent


def _child_env():
    env = os.environ.copy()
    env["OMP_NUM_THREADS"] = "1"
    env["MKL_NUM_THREADS"] = "1"
    env["OPENBLAS_NUM_THREADS"] = "1"
    env["PYTHONPATH"] = str(ROOT)
    return env


def _eye_block(scale, column):
    block = torch.zeros((8, 8), dtype=torch.float64)
    block[0, column] = scale
    return block


def _pack(r, z, n):
    matrix = torch.zeros((24, 8), dtype=torch.float64)
    matrix[0:8] = r
    matrix[8:16] = z
    matrix[16:24] = n
    return matrix


def _draws(seed=1):
    generator = torch.Generator().manual_seed(seed)
    return torch.randn((32, 24, 8), dtype=torch.float64, generator=generator)


def _ordinary_pair():
    generator = torch.Generator().manual_seed(11)
    d = torch.randn((8, 8), dtype=torch.float64, generator=generator)
    g = torch.randn((8, 8), dtype=torch.float64, generator=generator)
    return d, g


class ProtocolFreezeTest(unittest.TestCase):
    def test_protocol_sha256(self):
        digest = hashlib.sha256((ROOT / PROTOCOL_FILENAME).read_bytes()).hexdigest()
        self.assertEqual(digest, PROTOCOL_SHA256)
        self.assertEqual(digest, "0efce40bdf2cf55af61f8c70f817ec3fbf8fe3a79256025556a77a03f8347101")

    def test_pr8_protocol_is_untouched(self):
        digest = hashlib.sha256((ROOT / "GRADED_REVERSION_PROTOCOL_FINAL.md").read_bytes()).hexdigest()
        self.assertEqual(digest, PR8_PROTOCOL_SHA256)

    def test_strings_are_in_the_protocol(self):
        text = (ROOT / PROTOCOL_FILENAME).read_text(encoding="utf-8")
        for piece in (
            CLAIM_SUCCESS,
            CLAIM_NOT_MET,
            "Graded joint reversion against first-order-matched and isotropic controls was UNRESOLVED ([E1 not replicated | insufficient evaluable seeds]).",
            PRIMARY_REPLICATED,
            PRIMARY_NOT_MET,
            UNRESOLVED_E1,
            UNRESOLVED_INSUFFICIENT,
            DISCLOSURE,
            SINGLE_BLOCK_SENTENCE,
            PHASE_A_PREFIX,
            PHASE_A_HEADLINE,
            "abs(FD - dot(G, direction)) <= 1e-10 + 1e-6*norm(G)",
            "abs(norm(d_k)^2 - norm(p_k)^2 - r_k^2)",
        ):
            self.assertIn(piece, text)

    def test_approval_record(self):
        text = (ROOT / "FIRST_ORDER_CONTROL_PHASE_B_APPROVAL.md").read_text(encoding="utf-8")
        self.assertTrue(approval_text_ok(text))
        self.assertIn("widget t23s2", text)
        self.assertIn("1:05 AM ET", text)

    def test_freeze_manifest_matches_code_and_draws(self):
        manifest = load_freeze()
        self.assertEqual(manifest["protocol_sha256"], PROTOCOL_SHA256)
        self.assertTrue(manifest["status"].startswith("FREEZE"))
        self.assertEqual(manifest["code_version"], CODE_VERSION)
        self.assertIn("not executed", manifest["phase_B_training"])
        self.assertIn("not run", manifest["phase_A"])
        self.assertEqual(set(manifest["code_sha256"]), set(CODE_FILES))
        for name, digest in manifest["code_sha256"].items():
            self.assertEqual(hashlib.sha256((ROOT / name).read_bytes()).hexdigest(), digest, name)
        self.assertEqual(set(manifest["manifests"]), {str(seed) for seed in MANIFEST_SEEDS})
        for seed in (100, 209, 300, 309):
            item = manifest["manifests"][str(seed)]
            self.assertEqual(item["fo_sha256"], sha256_array(fo_raw_draws(seed)))
            self.assertEqual(item["iso_sha256"], sha256_array(iso_raw_draws(seed)))
            self.assertEqual(item["grad_sha256"], sha256_array(grad_raw_draws(seed)))

    def test_deviations_log_records_the_tied_gap_and_draw_shape(self):
        text = (ROOT / "first_order_control_DEVIATIONS_AND_AMBIGUITIES.md").read_text(encoding="utf-8")
        self.assertIn("1e-18", text)
        self.assertIn("torch.randn((24, 8), dtype=torch.float64)", text)
        self.assertIn("scratch/fo_control", text)


class DrawManifestTest(unittest.TestCase):
    def test_generator_seeds_and_phase_b_iso_range(self):
        self.assertEqual(iso_generator_seed(300), 70000)
        self.assertEqual(iso_generator_seed(309), 70900)
        self.assertEqual(fo_generator_seed(300), 1_030_000)
        self.assertEqual(spec_fo_seed(309), 1_030_900)
        self.assertEqual(grad_generator_seed(100), 2_010_000)
        self.assertEqual(grad_generator_seed(309), 2_030_900)
        training = []
        for seed in list(range(100, 110)) + list(range(200, 210)) + list(range(300, 310)):
            training.extend((seed, 1000 + seed, 5000 + seed))
        generators = []
        for seed in MANIFEST_SEEDS:
            generators.extend((iso_generator_seed(seed), fo_generator_seed(seed), grad_generator_seed(seed)))
        self.assertEqual(len(generators), len(set(generators)))
        self.assertTrue(set(training).isdisjoint(generators))

    def test_phase_a_iso_matches_pr8_manifest(self):
        pr8 = json.loads((ROOT / "GRADED_REVERSION_FREEZE_v1.json").read_text(encoding="utf-8"))
        for seed in (100, 109, 200, 209):
            self.assertEqual(sha256_array(iso_raw_draws(seed)), pr8["draw_sha256"][str(seed)])
            self.assertEqual(draws_sha256(seed), pr8["draw_sha256"][str(seed)])

    def test_two_processes_byte_identical(self):
        script = (
            "import sys\n"
            "from first_order_control_draws import concatenated_manifest_bytes\n"
            "sys.stdout.buffer.write(concatenated_manifest_bytes())\n"
        )
        env = _child_env()

        def raw():
            proc = subprocess.run(
                [sys.executable, "-c", script],
                cwd=ROOT,
                env=env,
                check=True,
                capture_output=True,
            )
            return proc.stdout

        first = raw()
        second = raw()
        self.assertEqual(first, second)
        self.assertEqual(hashlib.sha256(first).hexdigest(), hashlib.sha256(concatenated_manifest_bytes()).hexdigest())


class ConstructionTest(unittest.TestCase):
    def test_norm_derivative_and_radius_gate(self):
        d_r, g_r = _ordinary_pair()
        d_z, g_z = _ordinary_pair()
        d_n, g_n = _ordinary_pair()
        built = construct_fo_paths(_pack(d_r, d_z, g_n * 0 + d_n), _pack(g_r, g_z, g_n), _draws(3))
        self.assertTrue(built["ok"], built["reasons"])
        self.assertTrue(built["assembled_norm_ok"])
        self.assertTrue(built["assembled_fo_ok"])
        self.assertTrue(built["g_preserved"])
        for name in ("r", "z", "n"):
            info = built["blocks"][name]
            self.assertTrue(info["norm_ok"], name)
            self.assertTrue(info["fo_ok"], name)
            self.assertTrue(info["radius_ok"], name)
            self.assertTrue(info["orth_ok"], name)
            self.assertLessEqual(info["worst_norm_relative"], 1e-12)
            self.assertLessEqual(info["worst_fo_relative"], 1e-12)
            self.assertLessEqual(info["worst_orth_abs"], 1e-12)

    def test_cancellation_safe_radius_gate(self):
        generator = torch.Generator().manual_seed(0)
        found = None
        for _index in range(10000):
            g = torch.randn(64, dtype=torch.float64, generator=generator)
            noise = torch.randn(64, dtype=torch.float64, generator=generator)
            noise = noise - torch.dot(noise, g) / torch.dot(g, g) * g
            exponent = int(torch.randint(8, 16, (1,), generator=generator).item())
            d = g + noise * (10.0 ** (-exponent))
            radius = radius_quantities(d, g)
            if radius["sqrt_inside"] < 0.0 and radius["gate_ok"]:
                found = (d, g, radius)
                break
        self.assertIsNotNone(found)
        d_vec, g_vec, radius = found
        # The square-root form is negative and is not the gate.
        self.assertIsNone(radius["sqrt_form"])
        self.assertLessEqual(radius["gate_abs"], radius["gate_tol"])
        d_block = d_vec.reshape(8, 8)
        g_block = g_vec.reshape(8, 8)
        healthy_d, healthy_g = _ordinary_pair()
        built = construct_fo_paths(
            _pack(d_block, healthy_d, healthy_d),
            _pack(g_block, healthy_g, healthy_g),
            _draws(5),
        )
        self.assertTrue(built["blocks"]["r"]["radius_ok"])
        self.assertLess(built["blocks"]["r"]["sqrt_inside"], 0.0)
        self.assertTrue(built["ok"], built["reasons"])

    def test_exactly_zero_gradient_uses_isotropic_fallback(self):
        d_r = _eye_block(1.5, 0)
        g_r = torch.zeros((8, 8), dtype=torch.float64)
        d_z, g_z = _ordinary_pair()
        d_n, g_n = _ordinary_pair()
        draws = _draws(9)
        built = construct_fo_paths(_pack(d_r, d_z, d_n), _pack(g_r, g_z, g_n), draws)
        self.assertTrue(built["ok"], built["reasons"])
        info = built["blocks"]["r"]
        self.assertTrue(info["exactly_zero_gradient"])
        self.assertTrue(info["fallback_isotropic"])
        self.assertFalse(info["collapsed"])
        self.assertEqual(info["rho"], 1.0)
        paths = torch.from_numpy(built["paths"])
        for index in range(N_PATHS):
            block = paths[index, 0:8]
            self.assertAlmostEqual(float(torch.linalg.vector_norm(block)), 1.5, places=12)
            self.assertEqual(float(torch.sum(block * g_r)), 0.0)

    def test_tiny_nonzero_gradient_stays_on_the_projection(self):
        g_n = torch.zeros((8, 8), dtype=torch.float64)
        g_n[0, 1] = 1e-11
        d_n = torch.zeros((8, 8), dtype=torch.float64)
        d_n[0, 0] = 1.0
        d_r, g_r = _ordinary_pair()
        d_z, g_z = _ordinary_pair()
        built = construct_fo_paths(_pack(d_r, d_z, d_n), _pack(g_r, g_z, g_n), _draws(13))
        self.assertTrue(built["ok"], built["reasons"])
        info = built["blocks"]["n"]
        self.assertFalse(info["exactly_zero_gradient"])
        self.assertTrue(info["negligible_first_order_scale"])
        self.assertLessEqual(info["g_norm"] * info["d_norm"], G_ZERO)
        self.assertFalse(info["collapsed"])
        self.assertTrue(info["norm_ok"])
        self.assertTrue(info["fo_ok"])
        self.assertFalse(info["fallback_isotropic"])

    def test_collapsed_block_copies_displacement(self):
        d_r = _eye_block(2.0, 0)
        g_r = _eye_block(0.3, 0)
        d_z, g_z = _ordinary_pair()
        d_n, g_n = _ordinary_pair()
        built = construct_fo_paths(_pack(d_r, d_z, d_n), _pack(g_r, g_z, g_n), _draws(17))
        self.assertTrue(built["ok"], built["reasons"])
        info = built["blocks"]["r"]
        self.assertTrue(info["collapsed"])
        self.assertTrue(info["fixed"])
        self.assertLessEqual(info["rho"], RHO_COLLAPSE)
        self.assertIn("r", built["fixed_blocks"])
        paths = torch.from_numpy(built["paths"])
        for index in range(N_PATHS):
            self.assertTrue(torch.equal(paths[index, 0:8], d_r))

    def test_collapsed_primary_via_r_eff(self):
        d_r = _eye_block(10.0, 0)
        g_r = _eye_block(1.0, 0)
        d_z = _eye_block(10.0, 1)
        g_z = _eye_block(1.0, 1)
        d_n = torch.zeros((8, 8), dtype=torch.float64)
        d_n[0, 0] = (1.0 - 0.002 ** 2) ** 0.5
        d_n[0, 1] = 0.002
        g_n = _eye_block(1.0, 0)
        built = construct_fo_paths(_pack(d_r, d_z, d_n), _pack(g_r, g_z, g_n), _draws(19))
        self.assertTrue(built["ok"], built["reasons"])
        self.assertTrue(built["blocks"]["r"]["collapsed"])
        self.assertTrue(built["blocks"]["z"]["collapsed"])
        self.assertFalse(built["blocks"]["n"]["collapsed"])
        self.assertGreater(built["blocks"]["n"]["rho"], RHO_COLLAPSE)
        self.assertTrue(built["primary_collapsed"])
        self.assertLessEqual(built["R_eff_over_delta"], RHO_COLLAPSE)
        self.assertEqual(built["fixed_blocks"], ["r", "z"])

    def test_zero_block_and_negative_a(self):
        d_r = _eye_block(-1.0, 0)
        d_r[0, 1] = 0.5
        g_r = _eye_block(2.0, 0)
        d_z = torch.zeros((8, 8), dtype=torch.float64)
        g_z = _eye_block(1.0, 3)
        d_n, g_n = _ordinary_pair()
        built = construct_fo_paths(_pack(d_r, d_z, d_n), _pack(g_r, g_z, g_n), _draws(23))
        self.assertTrue(built["ok"], built["reasons"])
        self.assertLess(built["blocks"]["r"]["a_k"], 0.0)
        self.assertEqual(built["blocks"]["r"]["a_k_sign"], "negative")
        self.assertTrue(built["blocks"]["z"]["zero_displacement"])
        paths = torch.from_numpy(built["paths"])
        self.assertTrue(torch.all(paths[:, 8:16, :] == 0))

    def test_projection_failure_does_not_redraw(self):
        d_r, g_r = _ordinary_pair()
        d_z, g_z = _ordinary_pair()
        d_n, g_n = _ordinary_pair()
        draws = _draws(29)
        draws[:, 0:8, :] = g_r.reshape(1, 8, 8)
        first = construct_fo_paths(_pack(d_r, d_z, d_n), _pack(g_r, g_z, g_n), draws)
        second = construct_fo_paths(_pack(d_r, d_z, d_n), _pack(g_r, g_z, g_n), draws)
        self.assertFalse(first["ok"])
        self.assertIsNone(first["paths"])
        self.assertTrue(any("projection failure" in reason for reason in first["reasons"]))
        self.assertEqual(first["reasons"], second["reasons"])

    def test_source_does_not_draw(self):
        source = (ROOT / "first_order_control_construct.py").read_text(encoding="utf-8")
        self.assertNotIn("randn", source)


class CriterionTest(unittest.TestCase):
    def test_fo_auc_on_a_linear_curve(self):
        slope = 0.2
        deltas = [slope * alpha for alpha in ALPHAS]
        self.assertAlmostEqual(auc(deltas), 0.5 * slope, places=15)
        self.assertAlmostEqual(auc(deltas), fo_auc_from_dot(slope), places=15)
        self.assertAlmostEqual(sum(weight * alpha for weight, alpha in zip(AUC_WEIGHTS, ALPHAS)), 0.5, places=15)

    def test_directional_materiality_and_joint_rules(self):
        low = [1.0] * N_PATHS
        self.assertFalse(d_family(1.0, low))
        self.assertTrue(d_family(1.0 + 1e-9, low))
        self.assertFalse(d_family(1.0 + EPS0, [1.0 + EPS0] * N_PATHS))
        self.assertTrue(m_flag(0.3, 1.0))
        self.assertFalse(m_flag(0.2, 1.0))
        self.assertFalse(m_flag(1e-13, 1.0))
        self.assertTrue(joint_pass(True, True, True, True, True))
        self.assertFalse(joint_pass(True, True, True, False, True))
        self.assertFalse(joint_pass(False, True, True, True, True))
        self.assertFalse(joint_pass(True, False, True, True, True))
        eligible, reasons = eligibility_target(True, True, 1.0, 1.0, 1.0, True)
        self.assertFalse(eligible)
        self.assertIn("collapsed", reasons)

    def test_thin_margin_undefined_denominator_and_endpoint_ties(self):
        self.assertTrue(is_thin(True, 0.05, 1.0))
        self.assertFalse(is_thin(True, 0.2, 1.0))
        self.assertFalse(is_thin(True, 0.05, 0.0))
        self.assertFalse(is_thin(True, 0.05, -1.0))
        self.assertTrue(percentage_undefined(0.0))
        self.assertTrue(percentage_undefined(-0.2))
        self.assertFalse(percentage_undefined(0.1))
        family = [1.0] * 31 + [2.0]
        counts = endpoint_counts(1.0, family)
        self.assertEqual(counts["n_end_gt"], 1)
        self.assertEqual(counts["n_end_tie"], 31)
        self.assertFalse(counts["endpoint_D"])
        strict = endpoint_counts(1.0, [0.5] * N_PATHS)
        self.assertEqual(strict["n_end_gt"], 0)
        self.assertEqual(strict["n_end_tie"], 0)
        self.assertTrue(strict["endpoint_D"])
        self.assertEqual(rank_of_rev(1.0, [0.5] * 31 + [1.0]), 2)
        self.assertEqual(rank_of_rev(1.0, [0.5] * N_PATHS), 1)
        sentence = margin_sentence(1, 8, 2, 3, 1, 4, FAMILY_FO)
        self.assertIn("1 of 8 joint-passing seeds", sentence)
        self.assertIn("first-order-matched", sentence)
        self.assertIn("≤ eps0", sentence)
        self.assertIn("3/10", sentence)
        self.assertIn("isotropic", margin_sentence(0, 8, 0, 0, 0, 8, FAMILY_ISO))

    def test_verdict_precedence_and_exact_strings(self):
        e1_ok = [True] * 10
        e1_bad = [True] * 7 + [False] * 3
        valid = [False, False] + [True] * 8
        collapsed = [False, False, True, True] + [False] * 6
        joint = [False, False, False, False] + [True] * 6
        self.assertEqual(primary_label(e1_ok, valid, collapsed, joint), UNRESOLVED_INSUFFICIENT)
        self.assertEqual(verdict_paragraph(UNRESOLVED_INSUFFICIENT), CLAIM_UNRESOLVED_INSUFFICIENT)
        self.assertEqual(primary_label(e1_bad, [True] * 10, [False] * 10, [True] * 10), UNRESOLVED_E1)
        self.assertEqual(verdict_paragraph(UNRESOLVED_E1), CLAIM_UNRESOLVED_E1)
        replicated_valid = [False, False] + [True] * 8
        replicated_joint = [False, False] + [True] * 8
        self.assertEqual(
            primary_label(e1_ok, replicated_valid, [False] * 10, replicated_joint),
            PRIMARY_REPLICATED,
        )
        self.assertEqual(verdict_paragraph(PRIMARY_REPLICATED), CLAIM_SUCCESS)
        not_met_joint = [True] * 7 + [False] * 3
        self.assertEqual(primary_label(e1_ok, [True] * 10, [False] * 10, not_met_joint), PRIMARY_NOT_MET)
        self.assertEqual(verdict_paragraph(PRIMARY_NOT_MET), CLAIM_NOT_MET)
        both = [False] + [True] * 9
        collapsed_once = [True] + [False] * 9
        self.assertEqual(unevaluable_count(both, collapsed_once), 1)
        self.assertEqual(secondary_label("r", e1_ok, [True] * 10, [False] * 10, not_met_joint).startswith("Secondary (block-wise), r:"), True)
        thin_fo = [True, True] + [False] * 8
        thin_iso = [False] * 10
        joint_flags = [True] * 9 + [False]
        self.assertTrue(robustness_applies(PRIMARY_REPLICATED, joint_flags, thin_fo, thin_iso))
        self.assertFalse(robustness_applies(PRIMARY_NOT_MET, joint_flags, thin_fo, thin_iso))

    def test_phase_a_text_has_no_aggregate_and_phase_b_failure_is_verbatim(self):
        def fake(seed):
            summary = {
                "D_FO": False,
                "D_ISO": True,
                "D": False,
                "M": True,
                "joint": False,
                "collapsed": False,
                "residual_rev": 0.1,
                "eligible": True,
                "eligibility_reasons": [],
                "fo": {"margin": 0.01, "m_over_B": 0.1, "m_over_PD": 0.2, "m_over_max": "UNDEFINED", "rank": 4, "n_end_gt": 1, "n_end_tie": 0, "endpoint_D": False},
                "iso": {"margin": 0.2, "m_over_B": 0.3, "m_over_PD": 0.4, "m_over_max": 0.5, "rank": 1, "n_end_gt": 0, "n_end_tie": 2, "endpoint_D": True},
            }
            return {
                "seed": seed,
                "valid": True,
                "summary": {name: summary for name in ("weight_hh", "r", "z", "n")},
                "geometry": {
                    "G_dot_delta": -0.001,
                    "cos_G_delta": -0.2,
                    "FO_AUC": -0.0005,
                    "R_eff_over_delta": 0.9,
                    "fixed_blocks": [],
                    "negligible_blocks": [],
                },
                "targets": {name: {} for name in ("weight_hh", "r", "z", "n")},
            }

        text = render_phase_a([fake(100)], [fake(200)], {"protocol_sha256": PROTOCOL_SHA256, "freeze_commit": "abc", "appendix_b_note": "Autograd spans are listed per seed."})
        assert_phase_a_text(text)
        self.assertIn("100-109", text)
        self.assertIn("200-209", text)

        records = []
        for seed in range(300, 310):
            records.append(
                {
                    "seed": seed,
                    "e1_pass": True,
                    "evaluation": {
                        "valid": True,
                        "transfer_pass": True,
                        "primary_collapsed": False,
                        "block_collapsed": {"r": False, "z": False, "n": False},
                        "summary": {
                            name: {
                                "joint": False,
                                "eligible": True,
                                "eligibility_reasons": [],
                                "D_FO": False,
                                "D_ISO": True,
                                "D": False,
                                "M": True,
                                "collapsed": False,
                                "fo": {"thin": False, "percentage_undefined": False, "n_end_gt": 0, "n_end_tie": 0, "endpoint_D": False},
                                "iso": {"thin": False, "percentage_undefined": False, "n_end_gt": 0, "n_end_tie": 0, "endpoint_D": False},
                            }
                            for name in ("weight_hh", "r", "z", "n")
                        },
                        "geometry": {"G_dot_delta": 0.0, "cos_G_delta": 0.0, "FO_AUC": 0.0, "negligible_blocks": [], "fixed_blocks": []},
                        "targets": {"weight_hh": {}},
                    },
                }
            )
        report = render_phase_b(records, {"protocol_sha256": PROTOCOL_SHA256, "freeze_commit": "abc"})
        self.assertIn(CLAIM_NOT_MET, report)
        self.assertNotIn(CLAIM_SUCCESS, report)
        self.assertIn(PRIMARY_NOT_MET, report)
        self.assertIn("D_ISO", report)
        self.assertIn("D_FO", report)
        self.assertNotIn("explained by the gradient", report)
        self.assertNotIn("no causal effect", report)
        self.assertIn("Development history", report)


class GradientTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(1)
        torch.use_deterministic_algorithms(True)
        cls.world = World()
        cls.oracle = oracle_tensor(cls.world.q)
        cls.bits = bit_tensor()

    def _synthetic(self):
        torch.manual_seed(12345)
        model = CoreGRU(32).double().eval()
        for parameter in model.parameters():
            parameter.requires_grad_(False)
        trained = model.rnn.weight_hh_l0.detach().clone()
        return model, trained

    def test_fd_floor_predicate(self):
        self.assertTrue(fd_within_tolerance(FD_ABS_FLOOR, 0.0, 0.0))
        self.assertFalse(fd_within_tolerance(FD_ABS_FLOOR + 1e-8, 0.0, 0.0))
        self.assertTrue(fd_within_tolerance(FD_REL, 0.0, 1.0))
        self.assertFalse(fd_within_tolerance(FD_REL + 1e-4, 0.0, 1.0))

    def test_synthetic_autograd_matches_central_differences(self):
        model, trained = self._synthetic()
        gradient = compute_gradient(model, self.oracle, self.bits, trained)
        self.assertTrue(gradient["byte_identical"])
        self.assertTrue(gradient["finite"])
        again = compute_gradient(model, self.oracle, self.bits, trained)
        self.assertTrue(torch.equal(gradient["G"], again["G"]))
        delta = torch.randn((24, 8), dtype=torch.float64)
        raw = torch.randn((3, 24, 8), dtype=torch.float64)
        report = finite_difference_report(model, self.oracle, self.bits, trained, gradient["G"], delta, raw)
        self.assertTrue(report["ok"], report)
        untied = untied_stage_gradients(model, self.oracle, self.bits, trained)
        summed = untied[0] + untied[1] + untied[2] + untied[3]
        self.assertLessEqual(float(torch.max(torch.abs(summed - gradient["G"]))), TIED_GRAD_ATOL)

    def test_h4_is_detached_and_other_parameters_get_no_gradient(self):
        model, trained = self._synthetic()
        for parameter in model.parameters():
            parameter.requires_grad_(True)
        leaf = trained.detach().clone().requires_grad_(True)
        loss = prefix_loss(model, self.oracle, self.bits, leaf, detach_h4=True, freeze_parameters=True)
        loss.backward()
        self.assertIsNotNone(leaf.grad)
        for parameter in model.parameters():
            self.assertFalse(parameter.requires_grad)
            self.assertIsNone(parameter.grad)
        model.zero_grad(set_to_none=True)
        model.rnn.weight_hh_l0.requires_grad_(True)
        detached = trained.detach().clone().requires_grad_(True)
        loss = prefix_loss(model, self.oracle, self.bits, detached, detach_h4=True, freeze_parameters=False)
        loss.backward()
        early = model.rnn.weight_hh_l0.grad
        self.assertTrue(early is None or float(torch.linalg.vector_norm(early)) == 0.0)
        model.zero_grad(set_to_none=True)
        model.rnn.weight_hh_l0.requires_grad_(True)
        attached = trained.detach().clone().requires_grad_(True)
        loss = prefix_loss(model, self.oracle, self.bits, attached, detach_h4=False, freeze_parameters=False)
        loss.backward()
        self.assertIsNotNone(model.rnn.weight_hh_l0.grad)
        self.assertGreater(float(torch.linalg.vector_norm(model.rnn.weight_hh_l0.grad)), 0.0)

    def test_real_checkpoint_fd_and_checkpoint_bytes(self):
        path = ROOT / "recurrent_core_results_v1" / "checkpoints" / "s100_f_trained.ckpt"
        before = path.read_bytes()
        state = load_checkpoint(path)
        model = module_from_state(state)
        trained = weight_hh_f64(state)
        init = weight_hh_f64(load_checkpoint(ROOT / "recurrent_core_results_v1" / "checkpoints" / "s100_cand_init.ckpt"))
        delta = init - trained
        gradient = compute_gradient(model, self.oracle, self.bits, trained)
        self.assertTrue(gradient["byte_identical"])
        self.assertTrue(gradient["finite"])
        loss = prefix_loss(model, self.oracle, self.bits, trained.detach())
        predictions, _states = rollout(model, all_bits())
        self.assertEqual(float(loss.detach()), l_prefix(predictions, self.world.q))
        self.assertTrue(torch.equal(l_prefix_torch(torch.from_numpy(predictions), self.oracle), loss.detach()))
        raw = torch.from_numpy(grad_raw_draws(100))
        report = finite_difference_report(model, self.oracle, self.bits, trained, gradient["G"], delta, raw)
        self.assertTrue(report["ok"], report)
        for check in report["checks"]:
            self.assertLessEqual(check["gap"], FD_ABS_FLOOR + FD_REL * gradient["norm"])
        untied = untied_stage_gradients(model, self.oracle, self.bits, trained)
        summed = untied[0] + untied[1] + untied[2] + untied[3]
        self.assertLessEqual(float(torch.max(torch.abs(summed - gradient["G"]))), TIED_GRAD_ATOL)
        self.assertEqual(path.read_bytes(), before)
        block = (trained + 0.125 * delta).contiguous()
        full_pred, states = rollout(model, all_bits())
        model.override = MatrixOverride(CONTINUATION_STAGES, (0, 24), block)
        try:
            continued = continue_from(model, states[3], all_bits()[:, 4:], 4)
        finally:
            model.override = None
        reference = rollout_override(model, block)
        self.assertEqual(float(np.max(np.abs(continued - reference))), 0.0)
        self.assertEqual(float(np.max(np.abs(full_pred - rollout(model, all_bits())[0]))), 0.0)


def rollout_override(model, block):
    from graded_reversion_eval import _rollout_block

    return _rollout_block(model, block, (0, 24))


if __name__ == "__main__":
    unittest.main()
