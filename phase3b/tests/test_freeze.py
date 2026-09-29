"""Unscored preflight snapshot and seed-family stop tests."""

from __future__ import annotations

import tempfile
import unittest
from unittest.mock import patch
import hashlib
from pathlib import Path
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from phase3b.execution import (engineering_selection, fit, require_authorization,
                               source_hashes, validate_training_seed)
from phase3b.freeze import (create_preflight_snapshot, verify_preflight_snapshot,
                            create_execution_freeze, verify_execution_freeze,
                            verify_approval, _canonical)
from phase3b.models import Arm


class FreezeTests(unittest.TestCase):
    def test_snapshot_hash_inventory_includes_protocol_and_replay_tests(self):
        inventory = source_hashes()
        for name in ("ACI_PHASE3B_PROTOCOL_v1.md",
                     "PHASE3B_RESOURCE_CONTRACT_v1.md",
                     "PHASE3B_COMPETITION_SIGNATURE_v1.md",
                     "phase3b/models.py", "phase3b/transfer.py",
                     "phase3b/tests/test_freeze.py"):
            self.assertIn(name, inventory)
        contract = Path(__file__).parents[2] / "PHASE3B_RESOURCE_CONTRACT_v1.md"
        self.assertEqual(inventory[contract.name], hashlib.sha256(contract.read_bytes()).hexdigest())

    def test_preflight_snapshot_is_exclusive_replayable_and_not_approval(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "preflight_snapshot.json"
            digest = create_preflight_snapshot(path)
            snapshot = verify_preflight_snapshot(path, digest)
            self.assertFalse(snapshot["approved"])
            self.assertFalse(snapshot["h16_authorized"])
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
        for seed in range(1000, 1016):
            validate_training_seed(seed, "final")
        for seed in (0, 999, 1016, True):
            with self.assertRaisesRegex(ValueError, "undeclared"):
                validate_training_seed(seed, "final")
        with self.assertRaisesRegex(RuntimeError, "STOP"):
            fit(Arm("candidate", 4), 0, 0.001,
                authorization={"phase": "engineering", "approved": True})

    def test_execution_freeze_requires_independent_phase_specific_approval(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            snapshot = root / "preflight.json"
            snapshot_hash = create_preflight_snapshot(snapshot)
            frozen = root / "freeze.json"
            reviewer_key = Ed25519PrivateKey.generate()
            public_hex = reviewer_key.public_key().public_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PublicFormat.Raw).hex()
            freeze_hash = create_execution_freeze(frozen, snapshot, snapshot_hash,
                                                  "proposer", public_hex)
            document = verify_execution_freeze(frozen, freeze_hash)
            self.assertFalse(document["approved"])
            self.assertEqual(document["contract"]["engineering_seeds"], list(range(4)))
            self.assertEqual(document["contract"]["final_seeds"], list(range(1000, 1016)))
            contract = document["contract"]["resource_contract"]
            self.assertEqual(contract["hard_caps"]["whole_arm_trainable_parameters"], 4096)
            self.assertEqual(contract["hard_caps"]["declared_forward_linear_macs_per_12_tick_episode"], 80000)
            self.assertIn("physical_memory_bus_traffic", contract["not_hard_equality_gates"])
            with self.assertRaises(FileExistsError):
                create_execution_freeze(frozen, snapshot, snapshot_hash, "proposer", public_hex)
            approval = root / "approval.json"
            value = {"schema": 1, "phase": "engineering", "approved": True,
                     "freeze_sha256": freeze_hash, "reviewer": "independent",
                     "independent_review": True, "review_scope": "H16"}
            signed = dict(value, signature=reviewer_key.sign(_canonical(value)).hex())
            raw = _canonical(signed)
            approval.write_bytes(raw)
            auth = {"freeze_path": str(frozen), "freeze_sha256": freeze_hash,
                    "approval_path": str(approval),
                    "approval_sha256": hashlib.sha256(raw).hexdigest()}
            self.assertEqual(verify_approval(auth, "engineering")["approval"], signed)
            self.assertEqual(require_authorization(dict(auth, snapshot_path=str(snapshot)))["freeze"],
                             document)
            with self.assertRaisesRegex(ValueError, "STOP"):
                verify_approval(auth, "final")
            with self.assertRaisesRegex(RuntimeError, "STOP"):
                require_authorization(None)
            fake = dict(value, signature="0" * 128)
            approval.write_bytes(_canonical(fake))
            auth["approval_sha256"] = hashlib.sha256(approval.read_bytes()).hexdigest()
            with self.assertRaisesRegex(ValueError, "signature"):
                verify_approval(auth, "engineering")
            for altered in (dict(value, reviewer="proposer"),
                            dict(value, freeze_sha256="0" * 64),
                            dict(value, review_scope="H15"),
                            dict(value, independent_review=False)):
                altered["signature"] = reviewer_key.sign(_canonical(altered)).hex()
                approval.write_bytes(_canonical(altered))
                auth["approval_sha256"] = hashlib.sha256(approval.read_bytes()).hexdigest()
                with self.assertRaisesRegex(ValueError, "STOP"):
                    verify_approval(auth, "engineering")

    def test_selection_path_reserved_before_fit(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "R1.json"
            output.write_text("existing", encoding="utf-8")
            checked = {"freeze": {"contract": {"grids": {"R1": [[4, 0.0003]]}}}}
            with patch("phase3b.execution.require_authorization", return_value=checked):
                with patch("phase3b.execution.fit", side_effect=AssertionError("fit called")):
                    with self.assertRaises(FileExistsError):
                        engineering_selection("R1", {"freeze_sha256": "a",
                                                     "approval_sha256": "b"}, output=output)
            self.assertEqual(output.read_text(encoding="utf-8"), "existing")

    def test_fit_rejects_off_grid_before_optimizer_or_training(self):
        frozen = {"freeze": {"contract": {"grids": {"candidate": [[4, 0.0003]]}}}}
        with patch("phase3b.execution.require_authorization", return_value=frozen):
            with self.assertRaisesRegex(ValueError, "nonprotocol"):
                fit(Arm("candidate", 4), 0, 0.001, authorization={})
            with self.assertRaisesRegex(ValueError, "nonprotocol"):
                fit(Arm("candidate", 5), 1000, 0.0003,
                    authorization={}, phase="final")


if __name__ == "__main__":
    unittest.main()