# SPDX-License-Identifier: MPL-2.0
"""Verify the frozen normalized SITC evidence in a public package.

This verifier does not execute the reference construction and does not
reconstruct the historical six-run campaign.  It verifies exact frozen hashes,
checks the historical summary records for internal consistency, and re-scores
the published normalized scientific projection with the portable scientific
scorer.
"""
from __future__ import annotations

from pathlib import Path
import hashlib
import json

from sitc_plan import (
    PREREG_SHA256,
    canonical,
    freeze_receipt,
    preregistration,
    replication_plan,
    sha256,
)
from sitc_score import (
    FROZEN_DECISION_SHA256,
    expected_case_ids,
    frozen_decision_rules,
    score_raw_run,
    terminal_decision,
)


HERE = Path(__file__).resolve().parent
PACKAGE = HERE.parent
EVIDENCE = PACKAGE / "evidence"
RECEIPTS = PACKAGE / "receipts"

PROJECTION_SHA256 = "565cf5f59fdc0d13b2ea538bd3bc8830cd5fff0ad80a51e19328128efe72d7f0"
ANALYSIS_SHA256 = "264343255ef6d5ca2c7b2af03c8a81d7ee7ca674a7723bae1be7f8781cfd9027"
CANONICAL_CLAIM = (
    "In the registered finite construction, a relationally self-indexed "
    "temporal state causally influenced future-directed choice through the "
    "separately intervened prospective-evaluation path."
)


def require(condition: bool, code: str) -> None:
    if not condition:
        raise ValueError(code)


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def verify_projection() -> dict:
    path = EVIDENCE / "NORMALIZED_SCIENTIFIC_PROJECTION.json"
    payload = path.read_bytes()
    require(hashlib.sha256(payload).hexdigest() == PROJECTION_SHA256,
            "PROJECTION_HASH_MISMATCH")
    projection = json.loads(payload.decode("ascii"))
    require(canonical(projection) == payload, "PROJECTION_NOT_CANONICAL")
    require(projection.get("case_count") == 88, "PROJECTION_CASE_COUNT")
    cases = projection.get("cases")
    require(type(cases) is list and len(cases) == 88, "PROJECTION_CASES")

    ordered_ids = expected_case_ids()
    by_id = {
        case.get("case_id"): case
        for case in cases
        if type(case) is dict and type(case.get("case_id")) is str
    }
    require(len(by_id) == 88 and set(by_id) == set(ordered_ids),
            "PROJECTION_CASE_INVENTORY")
    raw = {
        "schema": "second-tier-sitc-raw-scientific-run/1",
        "preregistration_sha256": PREREG_SHA256,
        "registered_run_id": "PUBLIC-NORMALIZED",
        "ordering": "FORWARD",
        "token_bijection": {
            "controlled": "<CONTROLLED_TOKEN>",
            "other": "<OTHER_TOKEN>",
        },
        "case_count": 88,
        "case_order": ordered_ids,
        "cases": [by_id[case_id] for case_id in ordered_ids],
    }
    expected_run = {
        "registered_run_id": "PUBLIC-NORMALIZED",
        "ordering": "FORWARD",
        "controlled_token": "<CONTROLLED_TOKEN>",
        "other_token": "<OTHER_TOKEN>",
    }
    report = score_raw_run(raw, expected_run)
    require(report["status"] == "PASS" and report["scientific_failures"] == [],
            "NORMALIZED_PROJECTION_RESCORE_NOT_PASS")
    require(report["normalized_projection_sha256"] == PROJECTION_SHA256,
            "NORMALIZED_PROJECTION_RESCORE_HASH_MISMATCH")
    return report


def verify_historical_summary() -> tuple[dict, dict]:
    analysis_path = EVIDENCE / "ANALYSIS.json"
    require(sha256(analysis_path) == ANALYSIS_SHA256, "ANALYSIS_HASH_MISMATCH")
    analysis = load_json(analysis_path)
    require(type(analysis) is dict, "ANALYSIS_SCHEMA")
    require(analysis.get("preregistration_sha256") == PREREG_SHA256,
            "ANALYSIS_PREREGISTRATION")
    require(analysis.get("frozen_decision_sha256") == FROZEN_DECISION_SHA256,
            "ANALYSIS_DECISION")
    require(analysis.get("claim") == CANONICAL_CLAIM, "ANALYSIS_CLAIM")
    require(analysis.get("program_status") == "SITC_PASS", "ANALYSIS_STATUS")
    require(analysis.get("normalized_cross_run_equality") is True,
            "ANALYSIS_CROSS_RUN_EQUALITY")
    reports = analysis.get("reports")
    require(type(reports) is list and len(reports) == 6,
            "ANALYSIS_REPLICATION_COUNT")
    require(terminal_decision(reports) == "SITC_PASS", "ANALYSIS_TERMINAL_DECISION")

    receipt = load_json(RECEIPTS / "NORMALIZED_REPLICATION_RECEIPT.json")
    require(type(receipt) is dict, "REPLICATION_RECEIPT_SCHEMA")
    require(receipt.get("all_six_analyzer_pass") is True,
            "REPLICATION_RECEIPT_ANALYZER_STATUS")
    require(receipt.get("all_six_normalized_projections_byte_identical") is True,
            "REPLICATION_RECEIPT_CROSS_RUN_EQUALITY")
    require(receipt.get("normalized_projection_sha256") == PROJECTION_SHA256,
            "REPLICATION_RECEIPT_PROJECTION_HASH")
    receipt_runs = receipt.get("runs")
    require(type(receipt_runs) is list and len(receipt_runs) == 6,
            "REPLICATION_RECEIPT_RUN_COUNT")

    plan = replication_plan()
    for registered, report, item in zip(plan, reports, receipt_runs):
        expected = {
            "registered_run_id": registered["registered_run_id"],
            "ordering": registered["ordering"],
            "status": "PASS",
            "scientific_failures": [],
            "normalized_projection_sha256": PROJECTION_SHA256,
        }
        require(report == expected, "ANALYSIS_RUN_MAPPING:" + registered["registered_run_id"])
        require(item.get("registered_run_id") == registered["registered_run_id"]
                and item.get("ordering") == registered["ordering"],
                "REPLICATION_RECEIPT_RUN_MAPPING:" + registered["registered_run_id"])
        require(item.get("analyzer_status") == "PASS"
                and item.get("scientific_failures") == []
                and item.get("normalized_projection_sha256") == PROJECTION_SHA256,
                "REPLICATION_RECEIPT_RUN_STATUS:" + registered["registered_run_id"])
        require(type(item.get("raw_result_bytes")) is int
                and item["raw_result_bytes"] > 0,
                "REPLICATION_RECEIPT_RAW_BYTES:" + registered["registered_run_id"])
        raw_hash = item.get("raw_result_sha256")
        require(type(raw_hash) is str and len(raw_hash) == 64
                and all(ch in "0123456789abcdef" for ch in raw_hash),
                "REPLICATION_RECEIPT_RAW_HASH:" + registered["registered_run_id"])
    return analysis, receipt


def main() -> None:
    prereg = preregistration()
    freeze_receipt()
    require(prereg["claim_boundary"]["maximum_if_pass"] == CANONICAL_CLAIM,
            "PREREGISTERED_CLAIM_MISMATCH")
    frozen_decision_rules()
    report = verify_projection()
    analysis, receipt = verify_historical_summary()

    result = {
        "schema": "sitc-public-normalized-evidence-verification/2",
        "status": "PUBLIC_NORMALIZED_EVIDENCE_VERIFIED",
        "verification_mode": "FROZEN_NORMALIZED_EVIDENCE_VERIFICATION",
        "case_count": 88,
        "preregistration_sha256": PREREG_SHA256,
        "frozen_decision_sha256": FROZEN_DECISION_SHA256,
        "normalized_projection_sha256": PROJECTION_SHA256,
        "normalized_projection_hash_bound": True,
        "normalized_projection_rescore_status": report["status"],
        "historical_analysis_hash_verified": sha256(EVIDENCE / "ANALYSIS.json") == ANALYSIS_SHA256,
        "historical_summary_consistency_checked": True,
        "historical_summary_run_count": len(analysis["reports"]),
        "historical_raw_hashes_listed_in_receipt": len(receipt["runs"]),
        "reference_implementation_executed": False,
        "historical_raw_arrays_loaded": False,
        "historical_raw_campaign_reconstructed": False,
        "historical_process_provenance_replayed": False,
        "scientific_failures": report["scientific_failures"],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

