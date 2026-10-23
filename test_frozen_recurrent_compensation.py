"""Freeze tests for frozen recurrent matrices with learned compensation.

Pairing uses seeds 400-409 for initialization only. Training in this file is the
synthetic fixture on seed 7. No consciousness claim.
"""

from __future__ import annotations

import ast
import json
import unittest
from pathlib import Path

import numpy as np
import torch

from frozen_recurrent_compensation_eval import evaluate_state
from frozen_recurrent_compensation_labels import (
    arm_counts,
    best_and_median,
    binding_frequencies,
    format_counts_block,
    paired_differences,
    render_report,
    stage1_final_reasons,
    statements_for_arm,
    status_from,
)
from frozen_recurrent_compensation_numpy_eval import pd_q
from frozen_recurrent_compensation_spec import (
    ACQUISITION_SENTENCE,
    BOUNDARY,
    CODE_FILES,
    EXISTENCE_NONE,
    EXISTENCE_NOT_REACHED,
    EXISTENCE_WITNESS,
    EXPECTED_COUNTS,
    FAIL,
    FINDING_1,
    FINDING_2,
    FINDING_4,
    INIT_WITNESS_SENTENCE,
    INVALID,
    PASS,
    PROTOCOL_FILENAME,
    PROTOCOL_SHA256,
    PUBLISHED_PD,
    REPRO_NO,
    REPRO_SENTENCE,
    REPRO_UNRESOLVED,
    REPRO_YES,
    SCOPE_SENTENCE,
    TAU_DISCLOSURE,
    WITNESS_SENTENCE,
    classify_T,
    code_tree_sha256,
    not_reached_sentence,
    protocol_sha256,
    values_agree,
)
from frozen_recurrent_compensation_study import (
    STAGE0_MANIFEST,
    assert_no_scores,
    reconcile_shared_inits,
)
from frozen_recurrent_compensation_train import (
    configure_runtime,
    draw_seed,
    episode_stream_digest,
    pairing_flags,
    run_synthetic_fixture,
    tensor_sha256,
    trainable_count,
)
from graded_reversion_outcomes import pd_cd_components
from recurrent_core_transfer_models import build_initialized, checkpoint_sha256, load_checkpoint, snapshot_state
from recurrent_core_transfer_spec import BATCH, GRAD_CLIP, STEPS
from recurrent_core_transfer_train import train_arm
from twostream_acquisition_oracle import World
from twostream_acquisition_spec import cosine_lr

import recurrent_core_transfer_train as rct_train

ROOT = Path(__file__).resolve().parent


def _run(seed, arm, final, init, reasons=None, init_reasons=None, t_final=0.5, binding=None):
    binding = binding or ["xor"]
    components = {"prefix": 0.2, "total": 0.3, "xor": t_final}

    def block(status, value):
        if status == INVALID:
            return {"evaluated": False, "binding_E1": None, "E1": None, "E2": None, "val_E1": None}
        metric = {
            "T": value,
            "L_prefix": 0.001,
            "components": {"prefix": 0.2, "total": 0.3, "xor": value},
        }
        return {
            "evaluated": True,
            "binding_E1": list(binding),
            "binding_E2": list(binding),
            "E1": metric,
            "E2": metric,
            "val_E1": {"total": 0.01, "XOR": 0.002},
        }

    return {
        "seed": seed,
        "arm": arm,
        "final_status": final,
        "init_status": init,
        "final_invalid_reasons": list(reasons or []),
        "init_invalid_reasons": list(init_reasons or []),
        "final_training_loss": 0.2,
        "steps_completed": 4000,
        "C_prefix_E1": 0.01,
        "G_prefix_E1": 0.02,
        "C_prefix_E2": 0.01,
        "G_prefix_E2": 0.02,
        "init": block(init, 2.0),
        "final": block(final, t_final),
    }


class ProtocolTextTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.protocol = (ROOT / PROTOCOL_FILENAME).read_text(encoding="utf-8")
        cls.approval = (ROOT / "FROZEN_RECURRENT_COMPENSATION_APPROVAL.md").read_text(encoding="utf-8")

    def test_protocol_sha256(self):
        self.assertEqual(protocol_sha256(), PROTOCOL_SHA256)
        self.assertEqual(PROTOCOL_SHA256, "eca2121c5972138580ebd8ababb1cd40879a4c20404e925e129becd7e778ea40")

    def test_verbatim_sentences_are_in_the_protocol(self):
        for sentence in (
            WITNESS_SENTENCE,
            ACQUISITION_SENTENCE,
            REPRO_SENTENCE,
            SCOPE_SENTENCE,
            TAU_DISCLOSURE,
            FINDING_4,
            FINDING_1,
            FINDING_2,
            not_reached_sentence("R-FIX-H"),
        ):
            self.assertIn(sentence, self.protocol)
        self.assertIn("NO VERIFIED WITNESS FOUND (u unresolved, i invalid).", self.protocol)
        self.assertIn("within-run prefix-loss improvement", self.protocol)

    def test_approval_quotes(self):
        question = (
            "Approve 30 CPU training runs for 'Frozen recurrent matrices with learned compensation': "
            "seeds 400-409, with CAND, R-FIX-32 and R-FIX-48 trained once per seed for 4000 steps "
            "under the PR #7 recipe, followed by the specified evaluation, once Astra's named edits "
            "are applied and the protocol and implementation are frozen? No appendices, restarts, "
            "searches or extra runs."
        )
        superseded = (
            "Approve fresh-seed GRU-8 training (seeds 400-409, 30 runs: normal plus two "
            "frozen-recurrent variants) for the frozen-recurrent compensation study once Astra clears the protocol?"
        )
        self.assertIn(question, self.approval)
        self.assertIn("Yes, approve the 30 runs", self.approval)
        self.assertIn("3:06 AM ET", self.approval)
        self.assertIn("2026-10-21", self.approval)
        self.assertIn("widget t28s1", self.approval)
        self.assertIn(superseded, self.approval)
        self.assertIn("never answered", self.approval)
        self.assertIn("t26s1", self.approval)

    def test_code_files_exist_and_hash_is_stable(self):
        for name in CODE_FILES:
            self.assertTrue((ROOT / name).is_file(), name)
        self.assertEqual(code_tree_sha256(), code_tree_sha256())

    def test_numpy_evaluator_does_not_import_torch_or_e1(self):
        source = (ROOT / "frozen_recurrent_compensation_numpy_eval.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        imported = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.extend(alias.name for alias in node.names)
            if isinstance(node, ast.ImportFrom) and node.module:
                imported.append(node.module)
        self.assertNotIn("torch", imported)
        self.assertNotIn("graded_reversion_outcomes", imported)
        self.assertNotIn("recurrent_core_transfer_metrics", imported)
        self.assertNotIn("evaluate_arm", source)
        self.assertNotIn("component_excess", source)


class RuleTests(unittest.TestCase):
    def test_recipe_constants(self):
        self.assertEqual(STEPS, 4000)
        self.assertEqual(BATCH, 256)
        self.assertEqual(GRAD_CLIP, 1.0)
        self.assertAlmostEqual(cosine_lr(0, 4000), 1e-3)
        self.assertAlmostEqual(cosine_lr(3999, 4000), 1e-4)

    def test_agreement_tolerance(self):
        self.assertTrue(values_agree(1.0, 1.0))
        self.assertTrue(values_agree(0.0, 1e-12))
        self.assertFalse(values_agree(0.0, 1e-12 + 1e-9))
        limit = 1e-12 + 1e-9 * 2.0
        self.assertTrue(values_agree(2.0, 2.0 + limit))
        self.assertFalse(values_agree(2.0, 2.0 + limit + 1e-9))
        self.assertFalse(values_agree(float("nan"), 1.0))

    def test_pass_fail_boundary(self):
        bound = 1e-9
        self.assertEqual(classify_T(1.0 - bound - 1e-12, 1.0 - bound - 1e-12, True), PASS)
        self.assertEqual(classify_T(1.0 - bound, 1.0 - bound, True), BOUNDARY)
        self.assertEqual(classify_T(1.0 + bound, 1.0 + bound, True), BOUNDARY)
        self.assertEqual(classify_T(1.0 + bound + 1e-12, 1.0 + bound + 1e-12, True), FAIL)
        self.assertEqual(classify_T(0.2, 2.0, True), BOUNDARY)
        self.assertEqual(classify_T(0.2, 0.2, False), "INTEGRITY_FAILURE")
        self.assertEqual(classify_T(float("nan"), 0.2, True), "INTEGRITY_FAILURE")

    def test_status_invalid_overrides_a_numeric_pass(self):
        self.assertEqual(status_from(PASS, ["identity"]), INVALID)
        self.assertEqual(status_from(PASS, []), PASS)
        self.assertEqual(status_from(None, ["stage2_sha"]), INVALID)

    def test_reproducible_eight_passes(self):
        runs = [_run(400 + i, "R-FIX-32", PASS if i < 8 else FAIL, FAIL) for i in range(10)]
        counts = arm_counts(runs)
        self.assertEqual(counts["final_verified_passes"], 8)
        self.assertEqual(counts["existence_label"], EXISTENCE_WITNESS)
        self.assertEqual(counts["reproducibility_label"], REPRO_YES)
        self.assertIn(REPRO_SENTENCE, statements_for_arm("R-FIX-32", counts))
        self.assertIn(WITNESS_SENTENCE, statements_for_arm("R-FIX-32", counts))

    def test_fewer_than_eight_is_criterion_not_met(self):
        runs = [_run(400 + i, "R-FIX-32", PASS if i < 7 else FAIL, FAIL) for i in range(10)]
        counts = arm_counts(runs)
        self.assertEqual(counts["reproducibility_label"], REPRO_NO)
        self.assertEqual(counts["existence_label"], EXISTENCE_WITNESS)

    def test_all_final_fails_is_not_reached(self):
        runs = [_run(400 + i, "R-FIX-48", FAIL, FAIL) for i in range(10)]
        counts = arm_counts(runs)
        self.assertEqual(counts["existence_label"], EXISTENCE_NOT_REACHED)
        self.assertEqual(counts["reproducibility_label"], REPRO_NO)
        text = "\n".join(statements_for_arm("R-FIX-48", counts))
        self.assertIn("TARGET NOT REACHED WITHIN DECLARED SEARCH", text)
        self.assertIn("not a necessity certificate", text)
        self.assertNotIn(WITNESS_SENTENCE, text)

    def test_boundary_below_the_unresolved_cutoff(self):
        runs = [_run(400 + i, "CAND", FAIL if i < 8 else BOUNDARY, FAIL) for i in range(10)]
        counts = arm_counts(runs)
        self.assertEqual(counts["boundary_runs"], 2)
        self.assertEqual(counts["existence_label"], EXISTENCE_NONE)
        self.assertEqual(counts["reproducibility_label"], REPRO_NO)
        text = "\n".join(statements_for_arm("R-FIX-32", counts))
        self.assertIn("NO VERIFIED WITNESS FOUND (2 unresolved, 0 invalid).", text)

    def test_more_than_two_unresolved(self):
        statuses = [FAIL] * 7 + [BOUNDARY] * 3
        runs = [_run(400 + i, "R-FIX-32", statuses[i], FAIL) for i in range(10)]
        counts = arm_counts(runs)
        self.assertEqual(counts["existence_label"], EXISTENCE_NONE)
        self.assertEqual(counts["reproducibility_label"], REPRO_UNRESOLVED)

    def test_init_witness_without_a_final_pass(self):
        runs = [_run(400 + i, "R-FIX-32", FAIL, PASS if i == 0 else FAIL) for i in range(10)]
        counts = arm_counts(runs)
        self.assertEqual(counts["initialization_witnesses"], 1)
        self.assertEqual(counts["final_verified_passes"], 0)
        self.assertEqual(counts["existence_label"], EXISTENCE_WITNESS)
        self.assertEqual(counts["acquisition_annotations"], 0)
        self.assertIn(INIT_WITNESS_SENTENCE, statements_for_arm("R-FIX-32", counts))
        self.assertNotIn(ACQUISITION_SENTENCE, statements_for_arm("R-FIX-32", counts))

    def test_acquisition_requires_verified_fail_then_pass(self):
        runs = [_run(400 + i, "R-FIX-32", PASS if i < 3 else FAIL, FAIL if i < 3 else BOUNDARY) for i in range(10)]
        counts = arm_counts(runs)
        self.assertEqual(counts["acquisition_annotations"], 3)
        self.assertIn(ACQUISITION_SENTENCE, statements_for_arm("R-FIX-32", counts))

    def test_boundary_init_does_not_annotate_acquisition(self):
        runs = [_run(400 + i, "R-FIX-32", PASS if i == 0 else FAIL, BOUNDARY if i == 0 else FAIL) for i in range(10)]
        counts = arm_counts(runs)
        self.assertEqual(counts["acquisition_annotations"], 0)
        self.assertEqual(counts["final_verified_passes"], 1)

    def test_invalid_final_does_not_erase_an_init_witness(self):
        runs = [_run(400 + i, "R-FIX-32", INVALID if i == 0 else FAIL, PASS if i == 0 else FAIL, reasons=["training_integrity"] if i == 0 else []) for i in range(10)]
        counts = arm_counts(runs)
        self.assertEqual(counts["invalid_runs"], 1)
        self.assertEqual(counts["initialization_witnesses"], 1)
        self.assertEqual(counts["existence_label"], EXISTENCE_WITNESS)
        self.assertEqual(counts["final_verified_passes"] + counts["final_verified_fails"] + counts["boundary_runs"] + counts["invalid_runs"], 10)

    def test_init_boundary_does_not_spoil_reproducibility(self):
        runs = [_run(400 + i, "CAND", PASS, BOUNDARY if i < 3 else FAIL) for i in range(10)]
        counts = arm_counts(runs)
        self.assertEqual(counts["reproducibility_label"], REPRO_YES)
        self.assertNotIn(WITNESS_SENTENCE, statements_for_arm("CAND", counts))

    def test_binding_frequencies_and_median(self):
        runs = []
        for i in range(10):
            binding = ["prefix", "xor"] if i == 0 else ["xor"]
            runs.append(_run(400 + i, "CAND", PASS, FAIL, t_final=float(i + 1), binding=binding))
        freq = binding_frequencies(runs, "final")
        self.assertEqual(freq["denominator_classified"], 10)
        self.assertEqual(freq["counts"]["xor"], 10)
        self.assertEqual(freq["counts"]["prefix"], 1)
        self.assertEqual(freq["ties"], 1)
        summary = best_and_median(runs)
        self.assertEqual(summary["best_seed"], 400)
        self.assertEqual(summary["best_T"], 1.0)
        self.assertEqual(summary["median_T"], 5.5)

    def test_stage1_reasons_do_not_double_count_an_early_stop(self):
        early = {
            "arm": "R-FIX-32",
            "integrity_training": True,
            "steps_completed": 12,
            "checkpoint_round_trip": True,
            "freezing_failure": "W0 bytes changed",
            "w0_matches_stage0_after_training": False,
            "w0_matches_stage0_after_reload": False,
            "batches_hashed": 12,
            "episode_digest_matches_stage0": None,
        }
        self.assertEqual(stage1_final_reasons(early), ["freezing_check"])
        digest = dict(early)
        digest.update(
            {
                "integrity_training": True,
                "steps_completed": 4000,
                "freezing_failure": None,
                "w0_matches_stage0_after_training": True,
                "w0_matches_stage0_after_reload": True,
                "batches_hashed": 4000,
                "episode_digest_matches_stage0": False,
            }
        )
        self.assertEqual(stage1_final_reasons(digest), ["episode_digest"])

    def test_stage1_schema_rejects_scores(self):
        assert_no_scores({"runs": [{"final_loss": 0.2, "steps_completed": 4000}]})
        with self.assertRaises(RuntimeError):
            assert_no_scores({"runs": [{"T": 0.2}]})

    def test_counts_block_lines(self):
        runs = [_run(400 + i, "R-FIX-32", PASS if i < 8 else FAIL, BOUNDARY) for i in range(10)]
        text = format_counts_block("R-FIX-32", arm_counts(runs))
        self.assertIn("final verified passes: 8/10", text)
        self.assertIn("initialization witnesses: 0", text)
        self.assertIn("acquisition annotations: 0", text)
        self.assertIn("invalid runs: 0", text)
        self.assertIn("boundary or numerically unresolved runs: 0", text)
        self.assertIn("existence label: WITNESS FOUND", text)
        self.assertIn("reproducibility label: TARGET REACHED REPRODUCIBLY", text)
        self.assertIn("counted once", text)

    def test_shared_init_mismatch_invalidates_both(self):
        records = []
        for seed in range(400, 410):
            left = _run(seed, "CAND", FAIL, PASS if seed == 400 else FAIL)
            right = _run(seed, "R-FIX-32", FAIL, FAIL if seed == 400 else FAIL)
            left["init"]["checkpoint_sha256"] = "h32-%d" % seed
            right["init"]["checkpoint_sha256"] = "h32-%d" % seed
            left["init"]["E1"] = {"components": {"prefix": 1.0, "total": 1.0, "xor": 2.0}}
            right["init"]["E1"] = {"components": {"prefix": 1.0, "total": 1.0, "xor": 2.0}}
            records.extend((left, right))
        reconcile_shared_inits(records)
        self.assertEqual(records[0]["init_status"], INVALID)
        self.assertEqual(records[1]["init_status"], INVALID)
        self.assertIn("shared_init_classification_mismatch", records[0]["init_invalid_reasons"])

    def test_report_renders_mandatory_lines(self):
        runs = []
        for arm in ("CAND", "R-FIX-32", "R-FIX-48"):
            for i in range(10):
                final = PASS if i < 8 else FAIL
                runs.append(_run(400 + i, arm, final, FAIL))
        from frozen_recurrent_compensation_labels import ledger_lines

        arms = {}
        for arm in ("CAND", "R-FIX-32", "R-FIX-48"):
            arm_runs = [run for run in runs if run["arm"] == arm]
            counts = arm_counts(arm_runs)
            sentences = statements_for_arm(arm, counts)
            arms[arm] = {
                "counts": counts,
                "statements": sentences,
                "best_median": best_and_median(arm_runs),
                "binding_final": binding_frequencies(arm_runs, "final"),
                "binding_init": binding_frequencies(arm_runs, "init"),
                "ledger": ledger_lines(arm, counts, sentences),
            }
        payload = {
            "reference": {"tau": 0.25, "PD_E1": PUBLISHED_PD, "PD_E2": PUBLISHED_PD, "thr_total": 0.02, "thr_xor": 0.002},
            "comparator": "R-FIX-vs-CAND comparison: UNRESOLVED (comparator not reproduced).",
            "arms": arms,
            "runs": runs,
            "paired": paired_differences(runs),
            "deviations_during_stages": "No further deviation was recorded during Stage 1 or Stage 2.",
        }
        # CAND reached 8/10, so this fake comparator line is not what stage 2 would choose.
        # The renderer must still print it verbatim when given it.
        text = render_report(payload)
        self.assertIn("final verified passes: 8/10", text)
        self.assertIn(WITNESS_SENTENCE, text)
        self.assertIn(REPRO_SENTENCE, text)
        self.assertIn(TAU_DISCLOSURE, text)
        self.assertIn("within-run prefix-loss improvement", text)
        self.assertIn("No consciousness claim.", text)
        self.assertNotIn("consciousness is", text.lower())


class ModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        configure_runtime()
        cls.world = World()

    def test_published_pd_and_thresholds(self):
        pd = pd_cd_components(self.world.q)["PD"]
        self.assertEqual(pd, PUBLISHED_PD)
        self.assertEqual(pd_q(self.world.q), pd)
        total = float(self.world.afit_threshold["TEST"]["total"])
        xor = float(self.world.afit_threshold["TEST"]["XOR"])
        self.assertEqual(format(total, ".7f"), "0.0203873")
        self.assertEqual(format(xor, ".8f"), "0.00228962")

    def test_parameter_counts(self):
        for arm, hidden in (("CAND", 32), ("R-FIX-32", 32), ("R-FIX-48", 48)):
            model = build_initialized(7, hidden)
            counts = trainable_count(model, arm)
            self.assertEqual(counts["trainable"], EXPECTED_COUNTS[arm]["trainable"])
            self.assertEqual(counts["stored"], EXPECTED_COUNTS[arm]["stored"])
            self.assertEqual(counts["frozen"], EXPECTED_COUNTS[arm]["frozen"])

    def test_pairing_all_ten_seeds(self):
        for seed in range(400, 410):
            flags = pairing_flags(seed)
            self.assertTrue(flags["full_equal_cand_rfix32"])
            self.assertTrue(flags["gru_equal_32_48"])
            self.assertTrue(flags["fc1_rows_0_31_equal"])
            self.assertTrue(flags["fc1_bias_differs"])
            self.assertTrue(flags["fc2_weight_shape_differs"])
            self.assertTrue(flags["fc2_bias_differs"])
            self.assertEqual(len(flags["w0_sha256"]), 64)

    def test_draw_is_stable_for_a_study_seed(self):
        first = draw_seed(400)
        second = draw_seed(400)
        for arm in first:
            self.assertEqual(checkpoint_sha256(first[arm]), checkpoint_sha256(second[arm]))
            self.assertEqual(tensor_sha256(first[arm]["rnn.weight_hh_l0"]), tensor_sha256(second["CAND"]["rnn.weight_hh_l0"]))

    def test_digest_is_deterministic_off_the_study_seeds(self):
        first = episode_stream_digest(11, steps=2, batch=256)
        second = episode_stream_digest(11, steps=2, batch=256)
        other = episode_stream_digest(12, steps=2, batch=256)
        self.assertEqual(first, second)
        self.assertNotEqual(first, other)

    def test_train_arm_sees_the_sample_batch_global(self):
        sentinel = object()
        original = rct_train.sample_batch
        rct_train.sample_batch = sentinel
        try:
            self.assertIs(train_arm.__globals__["sample_batch"], sentinel)
        finally:
            rct_train.sample_batch = original

    def test_e1_e2_agree_on_nonstudy_inits(self):
        from recurrent_core_transfer_spec import is_val_history

        val_mask = np.array([is_val_history(history) for history in range(256)], dtype=bool)
        thr_total = float(self.world.afit_threshold["TEST"]["total"])
        thr_xor = float(self.world.afit_threshold["TEST"]["XOR"])
        for hidden in (32, 48):
            state = snapshot_state(build_initialized(7, hidden))
            block = evaluate_state(state, hidden, self.world, thr_total, thr_xor, val_mask)
            self.assertTrue(block["components_agree"], msg=block["agreement_gaps"])
            self.assertLess(block["prediction_max_abs"], 1e-12)
            self.assertTrue(block["identity_ok"])
            self.assertTrue(block["outputs_valid_E1"])
            self.assertTrue(block["outputs_valid_E2"])
            self.assertIn(block["numeric_class"], (PASS, FAIL, BOUNDARY))
            self.assertTrue(values_agree(block["val_E1"]["total"], block["val_E2"]["total"]))
            self.assertTrue(values_agree(block["val_E1"]["XOR"], block["val_E2"]["XOR"]))

    def test_synthetic_fixture(self):
        from recurrent_core_transfer_spec import is_val_history

        result = run_synthetic_fixture(return_model=True)
        self.assertTrue(result["passed"])
        self.assertTrue(result["negative_case_caught"])
        self.assertEqual(result["seed"], 7)
        self.assertNotIn(result["seed"], range(400, 410))
        self.assertEqual(result["grad_none_steps_checked"], 4)
        model = result["model"]
        val_mask = np.array([is_val_history(history) for history in range(256)], dtype=bool)
        thr_total = float(self.world.afit_threshold["TEST"]["total"])
        thr_xor = float(self.world.afit_threshold["TEST"]["XOR"])
        block = evaluate_state(snapshot_state(model), 32, self.world, thr_total, thr_xor, val_mask)
        self.assertTrue(block["components_agree"], msg=block["agreement_gaps"])
        self.assertTrue(block["identity_ok"])
        self.assertLess(block["prediction_max_abs"], 1e-12)


class Stage0SealTests(unittest.TestCase):
    def test_stage0_manifest_matches_code_and_checkpoints(self):
        if not STAGE0_MANIFEST.exists():
            self.skipTest("stage 0 manifest is written by the freeze runner")
        manifest = json.loads(STAGE0_MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["protocol_sha256"], PROTOCOL_SHA256)
        self.assertEqual(manifest["code_tree_sha256"], code_tree_sha256())
        self.assertTrue(manifest["synthetic_fixture"]["passed"])
        self.assertFalse(manifest["scoring"])
        self.assertEqual(sorted(manifest["seeds"]), [str(seed) for seed in range(400, 410)])
        assert_no_scores(manifest)
        for seed in range(400, 410):
            row = manifest["seeds"][str(seed)]
            self.assertEqual(len(row["episode_digest"]), 64)
            self.assertTrue(row["pairing_ok"])
            cand = row["arms"]["CAND"]
            r32 = row["arms"]["R-FIX-32"]
            r48 = row["arms"]["R-FIX-48"]
            self.assertEqual(cand["init_checkpoint_sha256"], r32["init_checkpoint_sha256"])
            self.assertEqual(cand["w0_sha256"], r32["w0_sha256"])
            self.assertEqual(cand["w0_sha256"], r48["w0_sha256"])
            self.assertEqual(row["w0_sha256"], cand["w0_sha256"])
            for arm, spec in row["arms"].items():
                path = ROOT / spec["init_checkpoint_file"]
                state = load_checkpoint(path)
                self.assertEqual(checkpoint_sha256(state), spec["init_checkpoint_sha256"])
                self.assertEqual(tensor_sha256(state["rnn.weight_hh_l0"]), spec["w0_sha256"])


if __name__ == "__main__":
    unittest.main()
