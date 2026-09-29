"""Pre-engineering source snapshot; never an authorization by itself."""

from __future__ import annotations

import hashlib
import importlib
import importlib.metadata
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

import numpy as np
import torch
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from phase3b import execution
from phase3b.resources import grid
from phase3b import PRIMARY


def _canonical(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode("utf-8")


def create_preflight_snapshot(path: Path) -> str:
    """Create one provisional snapshot with O_EXCL; no run or approval."""
    checks = execution.preflight()
    content: dict[str, Any] = {
        "schema": 1,
        "phase": "preflight_only",
        "source_sha256": checks["source_sha256"],
        "grids": checks["grids"],
        "h3": checks["h3"],
        "r9_clone_inputs": checks["r9_clone_inputs"],
        "python": sys.version,
        "torch": torch.__version__,
        "numpy": np.__version__,
        "h16_authorized": False,
        "approved": False,
    }
    raw = _canonical(content)
    with path.open("xb") as stream:
        stream.write(raw)
    return hashlib.sha256(raw).hexdigest()


def verify_preflight_snapshot(path: Path, expected_sha256: str) -> dict[str, Any]:
    """Reject source/config/runtime drift; neither this nor the digest is consent."""
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected_sha256:
        raise ValueError("preflight snapshot hash mismatch; STOP")
    document = json.loads(raw)
    if (raw != _canonical(document) or document.get("schema") != 1
            or document.get("phase") != "preflight_only"
            or document.get("approved") is not False
            or document.get("h16_authorized") is not False
            or document.get("source_sha256") != execution.source_hashes()
            or document.get("grids") != {family: [list(pair) for pair in grid(family)]
                                         for family in PRIMARY}
            or document.get("h3") != {"policy_triples": 27, "legal_words": 8}
            or document.get("r9_clone_inputs") != 8192
            or document.get("python") != sys.version
            or document.get("torch") != torch.__version__
            or document.get("numpy") != np.__version__):
        raise ValueError("preflight snapshot is stale or not the required design; STOP")
    return document


def dependency_hashes() -> dict[str, dict[str, str]]:
    """Pin both installed versions and their imported entry-point bytes."""
    result = {}
    for name in ("numpy", "torch", "psutil", "cryptography"):
        module = importlib.import_module(name)
        if module.__file__ is None:
            raise ValueError(f"{name}: missing dependency entry point; STOP")
        result[name] = {"version": importlib.metadata.version(name),
                        "sha256": hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest()}
    return result


def repository_head() -> str:
    root = Path(__file__).parent.parent
    return subprocess.run(("git", "rev-parse", "HEAD"), cwd=root, check=True,
                          capture_output=True, text=True).stdout.strip()


def execution_contract() -> dict[str, Any]:
    """H15/H16 v1 decisions, not inferred from results or approval."""
    return {
        "grids": {family: [list(pair) for pair in grid(family)] for family in PRIMARY},
        "engineering_seeds": list(range(4)),
        "final_seeds": list(range(1000, 1016)),
        "training": {"episodes": 8192, "batch": 32, "updates": 256,
                     "draw_seed": "100000 + seed * 256 + update",
                     "contexts": [0, 1, 2], "optimizer": "AdamW",
                     "weight_decay": 0, "gradient_clip": 1},
        "selection": {"draw_seed": "100000 + seed * 256 + update",
                      "contexts": [0, 1, 2], "tie_break": ["loss", "parameters", "learning_rate"]},
        "endpoint": {"context": 3, "evaluation_seed": "20000 + seed",
                     "episodes": 4096, "component_units": [50, 50, 50],
                     "abstain_units": 9, "joint_denominator": 150},
        "gate": {"strict_difference": "1/50", "minimum_wins": 14,
                 "maximum_two_sided_sign_p": "1/100"},
        "rival_envelope": list(PRIMARY[1:]),
        "resource_contract": {
            "hard_caps": {"whole_arm_trainable_parameters": 4096,
                          "declared_forward_linear_macs_per_12_tick_episode": 80000,
                          "training_episodes_per_fit": 8192, "optimizer_updates_per_fit": 256},
            "report": ["nonlinear_work", "backward_work", "optimizer_work",
                       "memory", "wall_time"],
            "not_hard_equality_gates": ["physical_memory_bus_traffic",
                                        "isolated_per_arm_os_peak"],
        },
        "r4": {"routes": 256, "training_contexts": [0, 1, 2],
               "heldout_route": "(route[2] + 1) % 4"},
    }


def create_execution_freeze(path: Path, snapshot_path: Path, snapshot_sha256: str,
                            proposer: str, reviewer_public_key: str) -> str:
    """Write an unapproved, immutable H15 design; approval is an external act."""
    if not proposer.strip():
        raise ValueError("proposer identity required")
    if (not isinstance(reviewer_public_key, str) or len(reviewer_public_key) != 64
            or reviewer_public_key != reviewer_public_key.lower()):
        raise ValueError("independent reviewer Ed25519 public key required; STOP")
    try:
        Ed25519PublicKey.from_public_bytes(bytes.fromhex(reviewer_public_key))
    except ValueError as exc:
        raise ValueError("invalid reviewer public key; STOP") from exc
    verify_preflight_snapshot(snapshot_path, snapshot_sha256)
    content = {"schema": 2, "phase": "execution", "approved": False,
               "proposer": proposer, "reviewer_public_key": reviewer_public_key,
               "head": repository_head(),
               "source_sha256": execution.source_hashes(),
               "dependencies": dependency_hashes(), "contract": execution_contract(),
               "preflight_snapshot_sha256": snapshot_sha256}
    raw = _canonical(content)
    with path.open("xb") as stream:
        stream.write(raw)
    return hashlib.sha256(raw).hexdigest()


def verify_execution_freeze(path: Path, digest: str) -> dict[str, Any]:
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != digest:
        raise ValueError("execution freeze hash mismatch; STOP")
    doc = json.loads(raw)
    if (not isinstance(doc, dict) or raw != _canonical(doc)
            or doc.get("schema") != 2 or doc.get("phase") != "execution"
            or doc.get("approved") is not False or not isinstance(doc.get("proposer"), str)
            or not doc["proposer"].strip() or doc.get("source_sha256") != execution.source_hashes()
            or doc.get("head") != repository_head()
            or not isinstance(doc.get("reviewer_public_key"), str)
            or len(doc["reviewer_public_key"]) != 64
            or doc.get("dependencies") != dependency_hashes()
            or doc.get("contract") != execution_contract()):
        raise ValueError("execution freeze drift or invalid contract; STOP")
    return doc


def verify_approval(authorization: Any, phase: str) -> dict[str, Any]:
    """Check externally recorded reviewer provenance against the exact freeze."""
    if phase not in ("engineering", "final") or not isinstance(authorization, dict):
        raise ValueError("phase-specific authorization required; STOP")
    keys = ("freeze_path", "freeze_sha256", "approval_path", "approval_sha256")
    if any(not isinstance(authorization.get(key), str) for key in keys):
        raise ValueError("missing freeze/approval provenance; STOP")
    frozen = verify_execution_freeze(Path(authorization["freeze_path"]),
                                     authorization["freeze_sha256"])
    raw = Path(authorization["approval_path"]).read_bytes()
    if hashlib.sha256(raw).hexdigest() != authorization["approval_sha256"]:
        raise ValueError("approval digest mismatch; STOP")
    approval = json.loads(raw)
    if (not isinstance(approval, dict) or raw != _canonical(approval)
            or approval.get("schema") != 1
            or approval.get("phase") != phase or approval.get("approved") is not True
            or approval.get("freeze_sha256") != authorization["freeze_sha256"]
            or not isinstance(approval.get("reviewer"), str)
            or not approval["reviewer"].strip() or approval["reviewer"] == frozen["proposer"]
            or approval.get("independent_review") is not True
            or approval.get("review_scope") != "H16"):
        raise ValueError("independent phase-specific freeze approval missing; STOP")
    if phase == "final" and (not isinstance(approval.get("selections_sha256"), dict)
                              or set(approval["selections_sha256"]) != set(PRIMARY)
                              or any(not isinstance(value, str) or len(value) != 64
                                     for value in approval["selections_sha256"].values())):
        raise ValueError("final approval must bind all engineering selections; STOP")
    signature = approval.get("signature")
    if not isinstance(signature, str) or len(signature) != 128:
        raise ValueError("missing independent approval signature; STOP")
    try:
        Ed25519PublicKey.from_public_bytes(bytes.fromhex(frozen["reviewer_public_key"])).verify(
            bytes.fromhex(signature),
            _canonical({key: value for key, value in approval.items() if key != "signature"}))
    except (ValueError, InvalidSignature) as exc:
        raise ValueError("invalid independent approval signature; STOP") from exc
    return {"freeze": frozen, "approval": approval}