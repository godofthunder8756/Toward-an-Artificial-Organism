# SPDX-License-Identifier: MPL-2.0
"""Portable bindings for the public SITC reference construction.

This module deliberately binds only to files inside the extracted public
package. It has no external-repository, operating-system-specific,
current-working-directory, or historical campaign-layout dependency. The canonical preregistration lives at
``protocol/SITC_D2_PREREGISTRATION_v1.0.0.json`` relative to the package root.
"""
from __future__ import annotations

from pathlib import Path
import hashlib
import json


CODE_DIRECTORY = Path(__file__).resolve().parent
PACKAGE_ROOT = CODE_DIRECTORY.parent
PROTOCOL_DIRECTORY = PACKAGE_ROOT / "protocol"
PREREG = PROTOCOL_DIRECTORY / "SITC_D2_PREREGISTRATION_v1.0.0.json"
FREEZE_RECEIPT = PROTOCOL_DIRECTORY / "SITC_D2_FREEZE_RECEIPT.json"

PREREG_SHA256 = "fbecb854eca0e096a2e66e8d047baea2cf466f8872d23202eaa60b946c9d4019"
FREEZE_RECEIPT_SHA256 = "bd2b97fde0418d39ce5b80edfbe7f2f411dfe9c844046b4efd734644d4b04678"
CAMPAIGN_ID = "SITC_CAMPAIGN_001_SELF_INDEXED_TEMPORAL_CAUSALITY"


def canonical(value: object) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256(path: Path | str) -> str:
    result = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def read_json(path: Path | str) -> object:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def preregistration() -> dict:
    if not PREREG.is_file():
        raise ValueError("PUBLIC_PREREGISTRATION_MISSING")
    if sha256(PREREG) != PREREG_SHA256:
        raise ValueError("SITC_PREREGISTRATION_CHANGED")
    value = read_json(PREREG)
    if not isinstance(value, dict) or value.get("version") != "1.0.0":
        raise ValueError("SITC_PREREGISTRATION_SCHEMA")
    return value


def freeze_receipt() -> dict:
    """Load the exact public copy of the historical freeze receipt.

    This verifies the receipt bytes only.  It does not claim that the compact
    public package contains every artifact named by the historical receipt.
    In particular, any hash-bound withheld artifact is governed by the public
    scope/withholding record.
    """
    if not FREEZE_RECEIPT.is_file():
        raise ValueError("PUBLIC_FREEZE_RECEIPT_MISSING")
    if sha256(FREEZE_RECEIPT) != FREEZE_RECEIPT_SHA256:
        raise ValueError("SITC_FREEZE_RECEIPT_CHANGED")
    value = read_json(FREEZE_RECEIPT)
    if not isinstance(value, dict):
        raise ValueError("SITC_FREEZE_RECEIPT_SCHEMA")
    if value.get("status") != "SITC_D2_FROZEN_BEFORE_OUTCOME_EXECUTION":
        raise ValueError("SITC_FREEZE_STATUS")
    artifacts = value.get("artifacts")
    if not isinstance(artifacts, dict):
        raise ValueError("SITC_FREEZE_ARTIFACT_MAP")
    if artifacts.get(PREREG.name, {}).get("sha256") != PREREG_SHA256:
        raise ValueError("SITC_FREEZE_PREREG_BINDING")
    return value


def replication_plan() -> list[dict]:
    value = preregistration()["replication"]
    orders = value["order_sequence"]
    tokens = value["opaque_entity_token_bijections"]
    if len(orders) != 6 or len(tokens) != 6:
        raise ValueError("SITC_REPLICATION_PLAN_LENGTH")
    result = []
    for index, (order, mapping) in enumerate(zip(orders, tokens), 1):
        expected = f"SITC-R{index:03d}"
        if mapping["repetition"] != expected:
            raise ValueError("SITC_REPETITION_ID")
        if order not in ("FORWARD", "REVERSED"):
            raise ValueError("SITC_REPLICATION_ORDER")
        if mapping["controlled"] == mapping["other"]:
            raise ValueError("SITC_TOKEN_BIJECTION")
        result.append({
            "registered_run_id": expected,
            "ordering": order,
            "controlled_token": mapping["controlled"],
            "other_token": mapping["other"],
        })
    return result
