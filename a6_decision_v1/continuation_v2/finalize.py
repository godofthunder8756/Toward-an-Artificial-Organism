"""Publish the decision with qualified, corrected resource accounting."""

from __future__ import annotations

import json

from a6_decision_v1.independent_replay import check_evidence
from a6_decision_v1.preservation import digest, write_once
from a6_decision_v1.runner import HERE, JOBS
from a6_decision_v1.continuation_v2.runner import LOCAL, normalize_counts


def finalize():
    evidence = check_evidence()
    result = {
        "schema": 2, "outcome": evidence["outcome"], "bounded_effort_closed": True,
        "mathematical_question_closed": evidence["outcome"] != "UNRESOLVED",
        "training_authorized": False, "training_executed": False,
        "phase3b_verdict": "B unchanged",
        "unconditional_shared4_bracket_exact": evidence["unconditional_shared4_bracket_exact"],
        "conditional_relaxation_bounds_exact": evidence["conditional_bounds_exact"],
        "orientation_bounds_exact": evidence["orientation_bounds_exact"],
        "analytic_corollaries": evidence["analytic_corollaries"],
        "preservation": evidence["preservation"], "candidates": evidence["candidates"],
        "jobs": evidence["jobs"],
        "boundary": "Gate reduction is proved; legal shared R9 existence is not decided without a certified witness or full-family impossibility.",
    }
    accounting = []
    for name in JOBS:
        closure = json.loads((HERE / (name + "_result.json")).read_text())
        worker = HERE / (name + "_worker.json")
        report = normalize_counts(json.loads(worker.read_text())) if worker.exists() else {}
        diagnostic = report.get("milp_NOT_CERTIFICATE", {})
        nodes = (report.get("aggregate_nodes") if name.startswith("f3") else
                 diagnostic.get("aggregate_nodes"))
        accounting.append({
            "job": name, "state": closure["state"], "aggregate_nodes": nodes,
            "node_usage_known": nodes is not None,
            "elapsed_seconds": closure.get("elapsed_seconds"),
            "peak_committed_bytes": closure.get("peak_job_committed_bytes"),
            "absolute_deadline_used": closure.get("absolute_deadline_used", False),
            "exclusive_supervisor": closure.get("exclusive_supervisor", False),
            "prefix_enforcement_qualified": name in JOBS[:2],
        })
    result["resource_accounting"] = accounting
    result["resource_erratum"] = {
        "path": "continuation_v2/RESOURCE_ERRATA.md",
        "sha256": digest(LOCAL / "RESOURCE_ERRATA.md"),
        "prefix_source_and_raw_outputs_preserved": True,
        "prefix_negative_interrupted_and_not_retried": True,
        "no_extra_search_jobs": True,
        "unknown_node_use_is_not_zero": True,
        "resource_audit_qualified_for_prefix": True,
    }
    write_once(HERE / "decision.json", result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    finalize()
