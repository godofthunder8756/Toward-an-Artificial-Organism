"""H10 unscored wiring tests. Never authorize, fit or score a transfer head."""

from __future__ import annotations

from contextlib import ExitStack
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import torch
from torch.nn import functional as F

from phase3b import PRIMARY
from phase3b.execution import source_hashes
from phase3b.freeze import create_preflight_snapshot
from phase3b.models import Arm
from phase3b.transfer import (EVAL_EPISODES, HEAD_INPUTS, TRAIN_EPISODES, TransferHead,
                              _fresh_bit, _state_bytes, fit_transfer,
                              require_transfer_authorization, secondary_data)
from phase3b.world import Episode, generate


class TransferWiringTests(unittest.TestCase):
    def test_authorization_failure_precedes_data_and_training(self):
        arm = Arm("candidate", 8)
        original = _state_bytes(arm)
        with patch("phase3b.transfer.secondary_data", side_effect=AssertionError("generated")):
            for authorization in (None, {}, {"phase": "secondary_transfer", "approved": True,
                                               "source_sha256": {"wrong": "hash"}},
                                  {"phase": "secondary_transfer", "approved": True,
                                   "source_sha256": source_hashes(),
                                   "checkpoint_sha256": original}):
                with self.assertRaisesRegex(RuntimeError, "not authorized"):
                    fit_transfer(arm, 1000, authorization=authorization)
            with tempfile.TemporaryDirectory() as folder:
                path = Path(folder) / "preflight_snapshot.json"
                digest = create_preflight_snapshot(path)
                with self.assertRaisesRegex(RuntimeError, "provenance mismatch"):
                    fit_transfer(arm, 1000, authorization={
                        "phase": "secondary_transfer", "approved": True,
                        "source_sha256": source_hashes(), "final_audit_passed": True,
                        "checkpoint_sha256": "0" * 64,
                        "snapshot_path": str(path), "snapshot_sha256": digest})
        self.assertEqual(original, _state_bytes(arm))
        self.assertTrue(all(p.requires_grad for p in arm.parameters()))
        with self.assertRaisesRegex(RuntimeError, "not authorized"):
            require_transfer_authorization(None)

    def test_each_family_sees_only_its_intact_interface_and_equal_head(self):
        ep = generate(42, 5)  # unscored wiring histories, not transfer/final data
        bit = torch.tensor([0, 1, 0, 1, 1])
        for family in PRIMARY:
            with self.subTest(family=family):
                arm = Arm(family, 8)
                if family == "R4":
                    arm.route = (1, 2, 3, 0)
                specialist = 2 if family == "R3" else None
                head = TransferHead(arm, r3_specialist=specialist)
                before = _state_bytes(arm.heads)
                with torch.no_grad():
                    features = head.features(ep.common, bit)
                    states = arm.encode(ep.common)
                    if arm.word_arm:
                        word = arm.write(states, 1)[0][:, 0]
                        visible = F.one_hot(word, 8).float()
                        self.assertTrue(torch.all((word >= 0) & (word < 8)))
                        self.assertEqual(head.read_bits, 3)
                    elif family == "R3":
                        visible = states[:, 2]
                        self.assertEqual(head.read_bits, 8 * 32)
                    elif family == "R1":
                        visible = states.flatten(1)
                        self.assertEqual(head.read_bits, 4 * 8 * 32)
                    else:
                        visible = states
                        self.assertEqual(head.read_bits, 8 * 32)
                self.assertEqual(features.shape, (5, HEAD_INPUTS))
                self.assertTrue(torch.equal(features[:, :visible.shape[1]], visible))
                self.assertTrue(torch.equal(features[:, visible.shape[1]:visible.shape[1]+4],
                                            torch.tensor([[1., 0., 0., 0.]]).expand(5, -1)))
                self.assertTrue(torch.equal(features[:, visible.shape[1]+4], bit.float()))
                self.assertEqual(torch.count_nonzero(features[:, head.feature_count:]).item(), 0)
                self.assertEqual(sum(p.numel() for p in head.classifier.parameters()),
                                 2 * HEAD_INPUTS + 2)
                self.assertEqual(sum(p.numel() for p in head.parameters()), 2 * HEAD_INPUTS + 2)
                self.assertEqual(head(ep.common, bit).shape, (5, 2))
                with ExitStack() as stack:
                    for old in arm.heads:
                        stack.enter_context(patch.object(old, "forward", side_effect=AssertionError("old head called")))
                    self.assertEqual(head(ep.common, bit).shape, (5, 2))
                self.assertEqual(before, _state_bytes(arm.heads))

    def test_word_head_cannot_bypass_intact_word(self):
        ep = generate(47, 3)
        bit = torch.tensor([0, 1, 1])
        for family in ("candidate", "R4", "R9"):
            with self.subTest(family=family):
                arm = Arm(family, 8)
                if family == "R4":
                    arm.route = (2, 3, 0, 1)
                head = TransferHead(arm)
                intact = head.features(ep.common, bit)
                state = arm.encode(ep.common)
                fake = torch.randn_like(state)
                # Fix the legal on-wire token, severing every hidden state.
                word = arm.write(state, 1)[0]
                with patch.object(arm, "encode", return_value=fake), patch.object(
                        arm, "write", return_value=(word, None, None, None)):
                    self.assertTrue(torch.equal(intact, head.features(ep.common, bit)))

    def test_r3_requires_one_declared_specialist_not_concatenation(self):
        arm = Arm("R3", 8)
        for specialist in (None, -1, 3):
            with self.assertRaisesRegex(ValueError, "declare"):
                TransferHead(arm, r3_specialist=specialist)
        with self.assertRaisesRegex(ValueError, "only legal for R3"):
            TransferHead(Arm("R2", 8), r3_specialist=0)
        ep = generate(48, 2)
        head = TransferHead(arm, r3_specialist=1)
        states = arm.encode(ep.common)
        bit = torch.tensor([0, 1])
        original = head.features(ep.common, bit)
        changed = states.clone()
        changed[:, 0] += 42
        changed[:, 2] -= 33
        with patch.object(arm, "encode", return_value=changed):
            self.assertTrue(torch.equal(original, head.features(ep.common, bit)))
        changed[:, 1] += 1
        with patch.object(arm, "encode", return_value=changed):
            self.assertFalse(torch.equal(original, head.features(ep.common, bit)))

    def test_only_fresh_sensor_and_public_context_enter_readout(self):
        arm = Arm("candidate", 8)
        head = TransferHead(arm)
        ep = generate(49, 32)
        zeros = torch.zeros(32, dtype=torch.long)
        original = head.features(ep.common, zeros)
        changed = head.features(ep.common, 1 - zeros)
        private_column = head.feature_count - 1
        self.assertTrue(torch.equal(original[:, :private_column], changed[:, :private_column]))
        self.assertTrue(torch.equal(original[:, private_column+1:], changed[:, private_column+1:]))
        self.assertTrue(torch.equal(changed[:, private_column] -
                        original[:, private_column], torch.ones(32)))
        self.assertTrue(torch.equal(_fresh_bit(ep.truth, 1000), _fresh_bit(ep.truth, 1000)))
        self.assertFalse(torch.equal(_fresh_bit(ep.truth, 1000), _fresh_bit(ep.truth, 1001)))
        with self.assertRaisesRegex(ValueError, "public route"):
            TransferHead(Arm("R4", 8))
        with self.assertRaisesRegex(ValueError, "binary private bit"):
            head.features(ep.common, torch.full((32,), 2))

    def test_fixed_secondary_stream_and_allowance_without_generating_finals(self):
        count = TRAIN_EPISODES + EVAL_EPISODES
        common = torch.zeros(count, 8, dtype=torch.long)
        truth = torch.zeros(count, 4, dtype=torch.long)
        truth[TRAIN_EPISODES:, 3] = 1
        sentinel = Episode(common, torch.zeros(count, 4, 3, dtype=torch.long), truth)
        with patch("phase3b.transfer.generate", return_value=sentinel) as generator, patch(
                "phase3b.transfer._fresh_bit", return_value=truth[:, 3].clone()) as sensor:
            data = secondary_data(1000)
        generator.assert_called_once_with(31_000, count)
        sensor.assert_called_once()
        self.assertTrue(torch.equal(data.label[:TRAIN_EPISODES], torch.zeros(TRAIN_EPISODES, dtype=torch.long)))
        self.assertTrue(torch.equal(data.label[TRAIN_EPISODES:], torch.ones(EVAL_EPISODES, dtype=torch.long)))
        with patch("phase3b.transfer.generate", side_effect=AssertionError("generated")):
            with self.assertRaisesRegex(ValueError, "final seed"):
                secondary_data(0)


if __name__ == "__main__":
    unittest.main()