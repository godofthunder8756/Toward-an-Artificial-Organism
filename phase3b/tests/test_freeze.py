"""Unscored preflight snapshot and seed-family stop tests."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from phase3b.execution import fit, source_hashes, validate_training_seed
from phase3b.freeze import create_preflight_snapshot, verify_preflight_snapshot
from phase3b.models import Arm


class FreezeTests(unittest.TestCase):
    def test_snapshot_hash_inventory_includes_protocol_and_replay_tests(self):
        inventory = source_hashes()
        for name in ("ACI_PHASE3B_PROTOCOL_v1.md",
                     "PHASE3B_COMPETITION_SIGNATURE_v1.md",
                     "phase3b/models.py", "phase3b/transfer.py",
                     "phase3b/tests/test_freeze.py"):
            self.assertIn(name, inventory)

    def test_preflight_snapshot_is_exclusive_replayable_and_not_approval(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "preflight_snapshot.json"
            digest = create_preflight_snapshot(path)
            snapshot = verify_preflight_snapshot(path, digest)
            self.assertFalse(snapshot["approved"])
            self.assertFalse(snapshot["meter_complete"])
            with self.assertRaises(FileExistsError):
                create_preflight_snapshot(path)
            with self.assertRaisesRegex(ValueError, "hash mismatch"):
                verify_preflight_snapshot(path, "0" * 64)
            with path.open("ab") as stream:
                stream.write(b" ")
            with self.assertRaisesRegex(ValueError, "hash mismatch"):
                verify_preflight_snapshot(path, digest)

    def test_seed_family_and_training_authorization_stay_locked(self):
        for seed in range(4):
            validate_training_seed(seed, "engineering")
        for seed in (True, -1, 4, 1000):
            with self.assertRaisesRegex(ValueError, "undeclared"):
                validate_training_seed(seed, "engineering")
        with self.assertRaisesRegex(ValueError, "undeclared"):
            validate_training_seed(1000, "final")
        with self.assertRaisesRegex(RuntimeError, "STOP"):
            fit(Arm("candidate", 4), 0, 0.001,
                authorization={"phase": "engineering", "approved": True})


if __name__ == "__main__":
    unittest.main()