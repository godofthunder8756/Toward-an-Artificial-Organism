"""Pretraining H3, eight-word, leak, clone, resource and exact-gate tests."""

from __future__ import annotations

import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

import numpy as np
import torch

from phase3b import PRIMARY
from phase3b.audit import save_raw_fresh
from phase3b.execution import clone_check, fit, leak_check, preflight
from phase3b.external import oracle_actions, oracle_selector
from phase3b.interventions import ExpandedWord, NoMessage, UnlimitedRead, first_divergence, intervene
from phase3b.models import Arm
from phase3b.proof import bayes_action, verify_h3
from phase3b.resources import count, require_fit
from phase3b.statistics import final_gate, sign_p
from phase3b.world import generate, loss_units, targets


class PretrainingTests(unittest.TestCase):
    def test_world_replay_schedule_and_loss(self):
        ep = generate(42, 128)
        again = generate(42, 128)
        self.assertTrue(torch.equal(ep.common, again.common))
        self.assertTrue(torch.equal(ep.local, again.local))
        self.assertEqual(ep.common.shape, (128, 8))
        target = targets(ep.truth, 4)
        self.assertEqual(loss_units(target, ep.truth).sum().item(), 0)
        wrong = (1 - target[0], torch.full_like(target[1], 2), 1 - target[2])
        self.assertTrue(torch.all(loss_units(wrong, ep.truth) == torch.tensor([50, 9, 50])))

    def test_h3_exact_policies_and_implemented_losses(self):
        self.assertEqual(verify_h3()["policy_triples"], 27)
        # Enumerate positive-probability factors and both local bits. Check
        # the action loss expectation against the independently implemented
        # integer-unit evaluator ledger for each conditional target law.
        for n in [(a, b, c, 2) for a in range(3) for b in range(3) for c in range(3)]:
            for bit in (0, 1):
                for i in range(3):
                    self.assertIn(bayes_action(i, n, bit), range(3 if i == 1 else 2))
        self.assertEqual(len({tuple(tuple(bayes_action(i, (a, b, c, 2), v) for v in (0, 1))
                                    for i in range(3)) for a in range(3) for b in range(3)
                              for c in range(3)}), 27)

    def test_all_compulsory_arms_and_resource_caps(self):
        ep = generate(12, 3)
        for family in PRIMARY:
            model = Arm(family, 8)
            if family == "R4":
                model.route = (0, 1, 2, 3)
            cost = require_fit(model)
            self.assertLessEqual(cost["trainable_parameters"], 4096)
            self.assertLessEqual(cost["forward_macs_per_episode"], 80000)
            out = model(ep.common, ep.local)
            self.assertEqual(len(out.actions), 3)
            if model.word_arm:
                self.assertTrue(torch.all((out.word >= 0) & (out.word <= 7)))
            else:
                self.assertIsNone(out.word)

    def test_leak_clone_and_all_seven_hooks(self):
        torch.manual_seed(15)
        model = Arm("candidate", 8)
        leak_check(model)
        self.assertEqual(clone_check(model), 8192)
        ep = generate(6, 3)
        intact = model(ep.common, ep.local)
        diagnostic = NoMessage()
        for kind in ("I1", "I3"):
            changed = intervene(model, ep.common, ep.local, kind, address=1)
            self.assertEqual(changed.word.shape, intact.word.shape)
            if kind == "I1":
                self.assertTrue(torch.equal(changed.word % 2, intact.word % 2))
            else:
                forced = torch.ones_like(intact.address)
                self.assertTrue(torch.equal(changed.word,
                                            model.write(intact.states, 4, forced=forced)[0]))
        for kind in ("I2", "I6"):
            changed = intervene(model, ep.common, ep.local, kind, consumer=1,
                                diagnostic=diagnostic)
            self.assertEqual(changed.actions[0].shape, intact.actions[0].shape)
            if kind == "I6":
                for i in (0, 2):
                    self.assertTrue(torch.equal(changed.logits[i], intact.logits[i]))
        for bits in (4, 8, 16):
            out = intervene(model, ep.common, ep.local, "I4", expanded=ExpandedWord(8, bits))
            self.assertTrue(torch.all(out.word < 2 ** bits))
        self.assertEqual(intervene(model, ep.common, ep.local, "I5",
                                   unlimited=UnlimitedRead(8)).actions[0].shape, (3, 4))
        paired = generate(7, 3).common
        for port in range(4):
            corrupt = intervene(model, ep.common, ep.local, "I7", paired_common=paired, port=port)
            self.assertEqual(corrupt.word.shape, (3, 4))
            for other in range(4):
                if port != other:
                    self.assertTrue(torch.equal(intact.states[:, other], corrupt.states[:, other]))
            # If the word remains identical, changed hidden states cannot
            # affect any head through an uncharged bypass.
            same = corrupt.word == intact.word
            for before, after in zip(intact.logits, corrupt.logits):
                self.assertTrue(torch.equal(before[same], after[same]))
        self.assertTrue(torch.equal(first_divergence(intact, intervene(model, ep.common, ep.local, "noop")),
                                    torch.full((3,), -1)))

    def test_external_controls_and_hard_training_gate(self):
        ep = generate(45, 5)
        self.assertTrue(all(torch.equal(x, y) for x, y in zip(oracle_actions(ep, "R5"),
                                                                oracle_actions(ep, "R7"))))
        r6 = oracle_selector(Arm("candidate", 8), ep)
        self.assertEqual(r6.word.shape, (5, 4))
        with self.assertRaisesRegex(RuntimeError, "pretraining STOP"):
            fit(Arm("candidate", 8), 0, 0.001)

    def test_sign_test_and_integer_threshold(self):
        self.assertEqual(sign_p(14, 2), Fraction(137, 32768))
        self.assertEqual(sign_p(0, 0), Fraction(1))
        example = {seed: {arm: np.full(4096, 100 if arm == "candidate" else
                                        (104 if seed < 1014 else 102), dtype=np.int64)
                          for arm in PRIMARY} for seed in range(1000, 1016)}
        gate = final_gate(example)
        self.assertEqual((gate["wins"], gate["losses"], gate["ties"]), (14, 2, 0))
        self.assertTrue(gate["pass"])
        example[1000]["R9"] = np.full(4096, 101, dtype=np.int64)
        self.assertFalse(final_gate(example)["pass"])
        with self.assertRaisesRegex(ValueError, "16 declared"):
            final_gate({})

    def test_raw_exclusive_and_unscored_full_preflight(self):
        report = preflight()  # proof, dry-run counts, structural checks only
        self.assertEqual(len(report["grids"]), 7)
        self.assertEqual(report["r9_clone_inputs"], 8192)
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "unit.npz"
            raw = {"components": np.zeros((2, 4, 3), dtype=np.uint8),
                   "actions": np.zeros((2, 4, 3), dtype=np.uint8),
                   "words": np.zeros((2, 4), dtype=np.uint8)}
            self.assertEqual(len(save_raw_fresh(path, raw)), 64)
            with self.assertRaises(FileExistsError):
                save_raw_fresh(path, raw)


if __name__ == "__main__":
    unittest.main()