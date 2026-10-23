"""Freeze checks for recurrent-core transfer. No 4000-step training."""

from __future__ import annotations

import hashlib
import math
import unittest
from pathlib import Path

import numpy as np
import torch

from recurrent_core_transfer_e3 import pack_ratio
from recurrent_core_transfer_metrics import pdcd_ratio, variation_stats
from recurrent_core_transfer_models import (
    CoreGRU,
    MatrixOverride,
    build_initialized,
    checkpoint_sha256,
    eval_copy,
    load_checkpoint,
    parameter_counts,
    save_checkpoint,
    tune_recurrent,
)
from recurrent_core_transfer_p2 import ChartHarness, draw_matrices, observe_batch, transit_batch
from recurrent_core_transfer_spec import (
    CODE_FILES,
    EPS0,
    GATES,
    PROTOCOL_FILENAME,
    PROTOCOL_SHA256,
    READOUT_32,
    READOUT_70,
    RECURRENT_COUNT,
    SEEDS,
    TOTAL_843,
    VAL_LISTED,
    foreign_seed,
    is_grid_edge,
    is_val_history,
    select_configuration,
)
from recurrent_core_transfer_train import train_arm
from recurrent_core_transfer_verdicts import (
    assemble_claim,
    label_advantage,
    label_e1,
    label_specific,
    label_transfer,
    label_variation,
    specific_joint,
    transfer_pass,
    variation_joint,
)
from twostream_acquisition_e3_v2 import UNDEFINED, e3_v2_ratio
from twostream_acquisition_metrics import _observe_f, _transit_f, all_bits, rollout
from twostream_acquisition_oracle import World
from twostream_acquisition_spec import is_test_history

ROOT = Path(__file__).resolve().parent


class ProtocolHashTest(unittest.TestCase):
    def test_protocol_bytes(self):
        digest = hashlib.sha256((ROOT / PROTOCOL_FILENAME).read_bytes()).hexdigest()
        self.assertEqual(digest, PROTOCOL_SHA256)

    def test_freeze_manifest_matches_code_when_present(self):
        path = ROOT / "RECURRENT_CORE_TRANSFER_FREEZE_v1.json"
        if not path.exists():
            self.skipTest("manifest is written at the end of the freeze")
        import json

        manifest = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(manifest["protocol_sha256"], PROTOCOL_SHA256)
        self.assertEqual(manifest["status"][:6], "FREEZE")
        for name in CODE_FILES:
            digest = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
            self.assertEqual(manifest["code_sha256"][name], digest, name)


class AccountingTest(unittest.TestCase):
    def test_parameter_counts(self):
        small = CoreGRU(READOUT_32)
        large = CoreGRU(READOUT_70)
        small_counts = parameter_counts(small)
        large_counts = parameter_counts(large)
        self.assertEqual(small_counts["recurrent"], RECURRENT_COUNT)
        self.assertEqual(small_counts["readout"], 387)
        self.assertEqual(small_counts["total"], TOTAL_843)
        self.assertEqual(large_counts["recurrent"], RECURRENT_COUNT)
        self.assertEqual(large_counts["readout"], TOTAL_843)
        self.assertEqual(large_counts["total"], RECURRENT_COUNT + TOTAL_843)
        self.assertEqual(tuple(small.rnn.weight_hh_l0.shape), (24, 8))
        self.assertEqual(tuple(small.rnn.weight_ih_l0.shape), (24, 9))

    def test_checkpoint_roundtrip(self):
        model = build_initialized(100, READOUT_32)
        path = ROOT / "_tmp_checkpoint_roundtrip.ckpt"
        try:
            digest = save_checkpoint(path, model.state_dict())
            loaded = load_checkpoint(path)
            self.assertEqual(checkpoint_sha256(loaded), digest)
            for key, value in model.state_dict().items():
                self.assertTrue(torch.equal(value.cpu(), loaded[key]))
        finally:
            path.unlink(missing_ok=True)


class ValAndPairingTest(unittest.TestCase):
    def test_val_membership(self):
        found = {history for history in range(256) if is_val_history(history)}
        self.assertEqual(found, set(VAL_LISTED))
        self.assertEqual(len(found), 48)
        self.assertTrue(all(not is_test_history(history) for history in found))
        for prefix in range(16):
            self.assertEqual(sum(1 for history in found if history % 16 == prefix), 3)
        for continuation in range(16):
            self.assertEqual(sum(1 for history in found if history // 16 == continuation), 3)
        train = {history for history in range(256) if not is_test_history(history)}
        self.assertEqual(len(train - found), 144)

    def test_foreign_init_pairing(self):
        paired = [foreign_seed(seed) for seed in SEEDS]
        self.assertEqual(paired, [101, 102, 103, 104, 105, 106, 107, 108, 109, 100])
        self.assertEqual(len(set(paired)), 10)
        for seed in SEEDS:
            self.assertNotEqual(foreign_seed(seed), seed)
            self.assertIn(foreign_seed(seed), SEEDS)

    def test_tie_break_prefers_smaller_log_then_bias_then_scale(self):
        rows = []
        for g in (0.5, 1.0, 2.0):
            for b in (-2.0, 0.0, 2.0):
                rows.append({"g": g, "b": b, "criterion": 1.0})
        chosen, tied = select_configuration(rows)
        self.assertTrue(tied)
        self.assertEqual((chosen["g"], chosen["b"]), (1.0, 0.0))
        self.assertFalse(is_grid_edge(1.0, 0.0))
        self.assertTrue(is_grid_edge(2.0, 0.0))
        edged = []
        for g in (0.5, 1.0, 2.0):
            for b in (-2.0, 0.0, 2.0):
                criterion = 0.0 if (g, b) == (0.5, -2.0) else 1.0
                edged.append({"g": g, "b": b, "criterion": criterion})
        chosen, tied = select_configuration(edged)
        self.assertFalse(tied)
        self.assertEqual((chosen["g"], chosen["b"]), (0.5, -2.0))


class RatioTest(unittest.TestCase):
    def test_e3_v2_cases(self):
        self.assertEqual(e3_v2_ratio(1.0, 0.0), math.inf)
        self.assertIs(e3_v2_ratio(0.0, 0.0), UNDEFINED)
        self.assertIs(e3_v2_ratio(1e-12, 1e-12), UNDEFINED)
        self.assertEqual(e3_v2_ratio(1.0, 4.0), 0.25)
        self.assertEqual(pack_ratio(math.inf), "+inf")
        self.assertEqual(pack_ratio(UNDEFINED), "UNDEFINED")

    def test_pdcd_denominator_is_undefined_not_infinite(self):
        self.assertIs(pdcd_ratio(1.0, 0.0), UNDEFINED)
        self.assertIs(pdcd_ratio(0.0, 0.0), UNDEFINED)
        self.assertEqual(pdcd_ratio(1.0, 4.0), 0.25)


class ShamRestoreTest(unittest.TestCase):
    def test_sham_and_restore_identity(self):
        model = eval_copy(build_initialized(100, READOUT_32))
        intact, _states = rollout(model, all_bits())
        rows = (0, 8)
        trained = model.rnn.weight_hh_l0.detach()[0:8].clone()
        model.override = MatrixOverride((4, 5, 6, 7), rows, trained)
        sham, _states = rollout(model, all_bits())
        model.override = None
        self.assertLessEqual(float(np.max(np.abs(sham - intact))), EPS0)
        init_block = torch.randn(8, 8, dtype=torch.float64)
        model.override = MatrixOverride((4, 5, 6, 7), rows, init_block)
        _changed, _states = rollout(model, all_bits())
        model.override = None
        restored, _states = rollout(model, all_bits())
        self.assertLessEqual(float(np.max(np.abs(restored - intact))), 1e-9)
        self.assertTrue(torch.equal(model.rnn.weight_hh_l0[0:8], trained))


class VerdictRuleTest(unittest.TestCase):
    def test_transfer_counts(self):
        shown = [(True, True)] * 8 + [(True, False)] * 2
        self.assertEqual(label_transfer(shown), "TRANSFER SHOWN")
        self.assertEqual(label_transfer([(True, True)] * 7 + [(True, False)] * 3), "TRANSFER NOT SHOWN")
        unresolved = [(False, False)] * 3 + [(True, True)] * 7
        self.assertEqual(label_transfer(unresolved), "UNRESOLVED")
        self.assertTrue(transfer_pass(True, True, 0.1, 0.2))
        self.assertTrue(transfer_pass(True, True, 0.0, 0.0))
        self.assertFalse(transfer_pass(True, True, 0.2, 0.2))
        self.assertFalse(transfer_pass(False, True, 0.0, 1.0))

    def test_specific_joint_rules(self):
        random_deltas = [0.1] * 32
        self.assertTrue(specific_joint(True, 1.0, 0.3, random_deltas, 0.5))
        self.assertFalse(specific_joint(True, 1.0, 0.2, random_deltas, 0.5))
        self.assertFalse(specific_joint(True, 1e-12, 1.0, random_deltas, 0.5))
        self.assertFalse(specific_joint(True, 1.0, 0.3, random_deltas, 0.0))
        self.assertFalse(specific_joint(False, 1.0, 0.3, random_deltas, 0.5))
        almost = [0.1] * 31 + [0.3]
        self.assertFalse(specific_joint(True, 1.0, 0.3, almost, 0.5))

    def test_variation_and_advantage(self):
        flags = [(True, True)] * 8 + [(True, False)] * 2
        specific = label_specific(flags, "r")
        self.assertEqual(specific, "REPLICATED SPECIFIC(r)")
        self.assertEqual(label_variation(specific, flags, "r"), "PREFIX VARIATION REDUCED WITH CONTINUATION VARIATION RETAINED")
        self.assertEqual(
            label_variation("SPECIFIC(r) NOT DEMONSTRATED", flags, "r"),
            "selective variation reduction not demonstrated",
        )
        self.assertEqual(label_advantage(flags), "ADVANTAGE OVER TUNED FROZEN GRU-8 (843 TRAINABLE) OBSERVED")
        self.assertEqual(label_advantage([(True, False)] * 10), "not observed")
        self.assertIs(variation_joint(True, pdcd_ratio(1.0, 0.0), [1.0] * 32, 1.0), False)

    def test_claim_uses_the_preregistered_sentences(self):
        specific = {gate: "REPLICATED SPECIFIC(%s)" % gate if gate == "z" else "SPECIFIC(%s) NOT DEMONSTRATED" % gate for gate in GATES}
        variation = {gate: "selective variation reduction not demonstrated" for gate in GATES}
        claim = assemble_claim(
            "E1 REPLICATED",
            "TRANSFER SHOWN",
            specific,
            variation,
            "not observed",
            "not met",
            3,
        )
        self.assertIn(
            "reverting learned weights during continuation caused greater held-out prediction loss",
            claim,
        )
        self.assertIn("The specified matrix is W_hz.", claim)
        self.assertTrue(label_e1([True] * 8 + [False] * 2) == "E1 REPLICATED")
        self.assertEqual(label_e1([True] * 7 + [False] * 3), "UNRESOLVED (E1 not replicated)")


class DynamicsTest(unittest.TestCase):
    def test_vectorized_filter_matches_scalar(self):
        rng = np.random.default_rng(0)
        mx = rng.random(20)
        my = rng.random(20)
        c = (rng.random(20) - 0.5) * 0.05
        bit = rng.integers(0, 2, 20)
        for variable in ("X", "Y"):
            got = observe_batch(mx, my, c, variable, bit)
            for index in range(20):
                scalar = _observe_f(float(mx[index]), float(my[index]), float(c[index]), variable, int(bit[index]))
                for left, right in zip(got, scalar):
                    self.assertAlmostEqual(float(left[index]), float(right), places=12)
        got_t = transit_batch(mx, my, c)
        for index in range(20):
            scalar = _transit_f(float(mx[index]), float(my[index]), float(c[index]))
            for left, right in zip(got_t, scalar):
                self.assertAlmostEqual(float(left[index]), float(right), places=12)


class P2DeterminismTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.world = World()

    def test_draw_seeds_and_determinism(self):
        first = draw_matrices(0)
        second = draw_matrices(0)
        other = draw_matrices(1)
        self.assertTrue(np.array_equal(first["Q"], second["Q"]))
        self.assertTrue(np.array_equal(first["A"], second["A"]))
        self.assertTrue(np.array_equal(first["a"], second["a"]))
        self.assertTrue(np.array_equal(first["C"], second["C"]))
        self.assertFalse(np.array_equal(first["Q"], other["Q"]))
        self.assertTrue(np.all(first["diag_T"] > 0))
        self.assertLess(abs(first["spectral_radius"] - 0.9), 1e-8)
        self.assertLess(np.max(np.abs(first["Q"].T @ first["Q"] - np.eye(3))), 1e-10)
        self.assertLess(np.max(np.abs(first["Q"].T @ first["R"])), 1e-10)
        left = ChartHarness(first, 0.0, "plus")
        right = ChartHarness(second, 0.0, "plus")
        pred_left, _states = rollout(left, all_bits())
        pred_right, _states = rollout(right, all_bits())
        self.assertEqual(float(np.max(np.abs(pred_left - pred_right))), 0.0)
        gap = float(np.max(np.abs(pred_left - self.world.q)))
        self.assertLess(gap, 1e-8)

    def test_known_q_one_draw_is_localized_and_repeatable(self):
        from recurrent_core_transfer_p2 import run_draw_scale

        matrices = draw_matrices(0)
        left = run_draw_scale(matrices, 0.0, self.world, "plus")
        right = run_draw_scale(matrices, 0.0, self.world, "plus")
        self.assertEqual(left["known_q"]["localized"], right["known_q"]["localized"])
        self.assertEqual(left["known_q"]["ratios"], right["known_q"]["ratios"])
        self.assertTrue(left["known_q"]["localized"])
        complement = left["known_q"]["ratios"]["complement"]["vector"]["e3_v2"]
        self.assertTrue(complement == "+inf" or (isinstance(complement, float) and complement >= 0.75))
        minus = run_draw_scale(matrices, 0.0, self.world, "minus")
        self.assertTrue(minus["zero_effect_ok"])
        self.assertLessEqual(minus["zero_effect_gap"], EPS0)

    def test_uniform_variation_shape(self):
        stats = variation_stats(self.world.q, self.world)
        self.assertGreater(stats["uniform"]["PD"], 0.0)
        self.assertGreater(stats["uniform"]["CD"], 0.0)
        self.assertEqual(set(stats), {"uniform", "probability", "test"})


class SmokeTrainTest(unittest.TestCase):
    def test_two_steps_finish(self):
        torch.manual_seed(100)
        model = CoreGRU(READOUT_32)
        info = train_arm(model, 100, False, False, steps=2, batch=8)
        self.assertTrue(info["integrity_training"])
        tuned = tune_recurrent(model.state_dict(), 2.0, -2.0)
        self.assertFalse(torch.equal(tuned["rnn.weight_hh_l0"], model.rnn.weight_hh_l0.cpu()))


if __name__ == "__main__":
    unittest.main()
