from __future__ import annotations

import copy
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import validate_manifest as vm

SCHEMA = vm.load_structured(ROOT / "configs/schema/experiment_manifest.schema.json")
BASE_PATH = ROOT / "configs/confirmatory/STAGE_A_DUMMY_001.yaml"


def base_manifest():
    return vm.load_structured(BASE_PATH)


def issues_for(m):
    issues = vm.schema_validate(m, SCHEMA)
    if not issues:
        issues.extend(vm.semantic_validate(m, BASE_PATH, ROOT, ROOT / "configs/experiment_registry.yaml"))
    return issues


def codes(issues):
    return {x.code for x in issues}


def test_valid_manifest_passes():
    assert issues_for(base_manifest()) == []


def test_missing_required_field_fails():
    m = base_manifest()
    del m["hypothesis"]
    assert "SCHEMA" in codes(issues_for(m))


def test_duplicate_seed_rejected():
    m = base_manifest()
    m["seeds"]["values"].append(m["seeds"]["values"][0])
    assert "V014" in codes(issues_for(m))


def test_floating_version_rejected():
    m = base_manifest()
    m["environment"]["version"] = "latest"
    assert issues_for(m)


def test_necessity_requires_bypass():
    m = base_manifest()
    m["hypothesis"]["claim_type"] = "necessity"
    assert "V009" in codes(issues_for(m))


def test_causal_claim_requires_intervention():
    m = base_manifest()
    m["hypothesis"]["claim_type"] = "causal_contribution"
    m["interventions"] = []
    m["rescues"] = []
    assert "V010" in codes(issues_for(m))


def test_rescue_target_must_exist():
    m = base_manifest()
    m["rescues"][0]["target_intervention_id"] = "INT_DOES_NOT_EXIST"
    assert "V011" in codes(issues_for(m))


def test_training_false_requires_zero_budget():
    m = base_manifest()
    m["training"]["budget"]["value"] = 1
    assert "V016" in codes(issues_for(m))


def test_decision_rule_must_reference_hypothesis():
    m = base_manifest()
    m["decision"]["rules"][0]["hypothesis_id"] = "H_UNKNOWN"
    assert "V023" in codes(issues_for(m))


def test_freeze_and_verify_then_detect_edit(tmp_path):
    manifest_path = tmp_path / "manifest.yaml"
    manifest_path.write_text(BASE_PATH.read_text(), encoding="utf-8")
    # Referenced files are resolved from ROOT, so this copy can be frozen safely.
    lock = tmp_path / "manifest.lock.json"
    issues = vm.freeze_manifest(
        manifest_path,
        lock,
        ROOT / "configs/schema/experiment_manifest.schema.json",
        ROOT,
        ROOT / "configs/experiment_registry.yaml",
        "TEST_COMMIT_001",
    )
    assert issues == []
    assert vm.verify_frozen(manifest_path, lock, ROOT) == []
    manifest_path.write_text(manifest_path.read_text() + "\n# changed after freeze\n", encoding="utf-8")
    assert "V019" in codes(vm.verify_frozen(manifest_path, lock, ROOT))


def test_valid_negative_is_scientific_evidence():
    m = base_manifest()
    d = {
        "experiment_id": m["experiment"]["id"],
        "hypothesis_id": m["hypothesis"]["id"],
        "manifest_version": m["experiment"]["version"],
        "validity": "VALID_NEGATIVE",
        "decision": "REJECT"
    }
    assert vm.validate_decision_record(m, d) == []


def test_invalid_run_cannot_carry_scientific_decision():
    m = base_manifest()
    d = {
        "experiment_id": m["experiment"]["id"],
        "hypothesis_id": m["hypothesis"]["id"],
        "manifest_version": m["experiment"]["version"],
        "validity": "INVALID_RUN",
        "decision": "REJECT",
        "invalid_reason": "software crash"
    }
    assert "V021" in codes(vm.validate_decision_record(m, d))


def test_development_cannot_be_relabelled_confirmatory():
    m = base_manifest()
    m["experiment"]["mode"] = "development"
    provenance = {
        "experiment_id": m["experiment"]["id"],
        "experiment_version": m["experiment"]["version"],
        "execution_mode": "confirmatory",
        "manifest_sha256": "0" * 64,
        "software_version": "0.1.0",
        "source_commit": "TEST",
        "environment_id": m["environment"]["id"],
        "environment_version": m["environment"]["version"],
        "environment_sha256": "1" * 64,
        "architecture_hashes": {m["architectures"][0]["id"]: "2" * 64},
        "seed": m["seeds"]["values"][0],
        "timestamp_utc": "2026-09-21T12:00:00Z",
        "runtime_seconds": 0.1,
    }
    assert "V022" in codes(vm.validate_provenance_record(m, provenance))
