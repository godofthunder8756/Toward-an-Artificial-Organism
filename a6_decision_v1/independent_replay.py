"""Read-only evidence replay; execution HEAD restrictions remain in runner."""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import importlib.metadata
import json
from pathlib import Path
import platform

from a6_decision_v1.decision import verify_cut
from a6_decision_v1.exact import GATE
from a6_decision_v1.preservation import digest, verify, write_once
from a6_decision_v1.runner import HERE, JOBS, LIMITS
from a6_decision_v1.verify import certify_candidate, verify_lemmas


def check_evidence():
    import torch
    from a6_decision_v1.search import relaxation
    from shared4_v1.coupled_lower import replay_dual
    torch.set_num_threads(1)
    frozen = json.loads((HERE / "contract.json").read_text())
    if frozen["limits"] != LIMITS or frozen["jobs"] != list(JOBS) or frozen["training"]:
        raise ValueError("prospective analytic contract mismatch")
    for name, sha in frozen["source_sha256"].items():
        if digest(HERE / name) != sha:
            raise ValueError(f"frozen source mismatch: {name}")
    if digest(HERE / "baseline_hashes.json") != frozen["baseline_sha256"]:
        raise ValueError("preservation inventory mismatch")
    continuation_path = HERE / "continuation_v2" / "contract.json"
    successor = json.loads(continuation_path.read_text())
    if successor["limits"] != LIMITS or successor["remaining_jobs"] != list(JOBS[2:]):
        raise ValueError("continuation budget differs")
    if successor["original_contract_sha256"] != digest(HERE / "contract.json"):
        raise ValueError("continuation provenance mismatch")
    for name, sha in successor["source_sha256"].items():
        if digest(continuation_path.parent / name) != sha:
            raise ValueError(f"continuation source mismatch: {name}")
    for name, sha in successor["additional_checker_sha256"].items():
        if digest(HERE / name) != sha:
            raise ValueError(f"continuation checker mismatch: {name}")
    from a6_decision_v1.preservation import ROOT
    if digest(ROOT / "A6_GATE_REDUCTION_v1.md") != successor["reduction_sha256"]:
        raise ValueError("gate-reduction proof changed")
    from a6_decision_v1.analytic_corollaries import verify as verify_corollaries
    corollaries = verify_corollaries()
    preservation = verify(json.loads((HERE / "baseline_hashes.json").read_text()))
    lemmas = verify_lemmas()
    bounds, candidates, counts, resource_exceptions = {}, [], [], []
    jobs = []
    for name in JOBS:
        start = HERE / (name + "_start.json")
        result = HERE / (name + "_result.json")
        if not start.exists():
            continue
        entry = json.loads(start.read_text())
        if entry["contract_sha256"] != digest(HERE / "contract.json") or entry["limits"] != LIMITS:
            raise ValueError("job did not start under frozen contract")
        if not result.exists():
            raise ValueError("started job missing supervisor closure")
        closure = json.loads(result.read_text())
        jobs.append(closure)
        if name in JOBS[2:]:
            if entry.get("continuation_contract_sha256") != digest(continuation_path):
                raise ValueError("continuation job contract differs")
            if not closure.get("exclusive_supervisor") or not closure.get("absolute_deadline_used"):
                raise ValueError("missing successor enforcement")
        if not closure["memory_limit_enforced"]:
            raise ValueError("missing resource enforcement")
        if not closure["watchdog_enforced"]:
            if name != "f1_negative" or closure["state"] != "audit_interrupted":
                raise ValueError("unexplained watchdog-enforcement gap")
            resource_exceptions.append({
                "job": name, "scope": "owned audit interruption; exact elapsed/peak not captured",
                "strict_prefix_watchdog_certified": False,
            })
        root = HERE / (name + "_root.json")
        if root.exists():
            record = json.loads(root.read_text())
            if record.get("formulation") == "compact_scalar_v2":
                from a6_decision_v1.continuation_v2.compact import relaxation as compact
                model, offset, _, policies = compact(name.endswith("positive"))
            else:
                model, offset, _, _, policies = relaxation(name.endswith("positive"),
                                                           name.startswith("f2"))
            verified = [replay_dual(model, offset, record[key])
                        for key in ("lifted_prior_dual", "discovered_exact_dual")
                        if record.get(key) is not None]
            bounds[name] = max(verified)
            worker = HERE / (name + "_worker.json")
            if worker.exists():
                details = json.loads(worker.read_text())
                for proof in details.get("cuts", []):
                    verify_cut(proof, policies)
                diagnostic = details.get("milp_NOT_CERTIFICATE", {})
                nodes = (None if diagnostic.get("nodes_reported") is None else
                         diagnostic.get("aggregate_nodes"))
                if nodes is not None and nodes > LIMITS["node_limit"]:
                    raise ValueError("aggregate integer node cap exceeded")
                counts.append({"job": name, "nodes": nodes,
                               "verified_cuts": len(details.get("cuts", []))})
            else:
                counts.append({"job": name, "nodes": None, "verified_cuts": 0})
        if name.startswith("f3"):
            worker = HERE / (name + "_worker.json")
            details = json.loads(worker.read_text()) if worker.exists() else {}
            nodes = details.get("nodes_reported")
            if nodes is not None and nodes > LIMITS["node_limit"]:
                raise ValueError("constructive node cap exceeded")
            counts.append({"job": name, "nodes": nodes, "verified_cuts": 0})
        candidate = HERE / (name + "_candidate.json")
        if candidate.exists():
            checked = certify_candidate(json.loads(candidate.read_text()))
            candidates.append({"path": candidate.name, "sha256": digest(candidate),
                               "literal_graph_replay": checked})
    passed = any(c["literal_graph_replay"]["certified_gate_PASS"] for c in candidates)
    orientation_bounds = {
        orientation: max((v for name, v in bounds.items() if name.endswith(orientation)),
                         default=F(0))
        for orientation in ("positive", "negative")
    }
    failed = all(value > GATE for value in orientation_bounds.values())
    if passed and failed:
        raise AssertionError("contradictory certificates")
    outcome = "PASS" if passed else "FAIL" if failed else "UNRESOLVED"
    if outcome == "UNRESOLVED" and not all((HERE / (name + "_result.json")).exists() for name in JOBS):
        raise ValueError("effort not closed")
    bracket = [F(5159249, 29296875), F(1031759, 4687500)]
    for candidate in candidates:
        checked = candidate["literal_graph_replay"]
        if checked["positive_margins"]:
            bracket[1] = min(bracket[1], F(checked["population"]["shared_joint_exact"]))
    return {
        "outcome": outcome,
        "scope": "exact lemmas/duals/cuts, candidate graph replay, preservation and bounded disposition",
        "not_a_global_optimum_or_learning_certificate": True,
        "checker_sha256": digest(Path(__file__)),
        "preservation": preservation, "lemmas": lemmas,
        "conditional_bounds_exact": {k: str(v) for k, v in bounds.items()},
        "orientation_bounds_exact": {k: str(v) for k, v in orientation_bounds.items()},
        "unconditional_shared4_bracket_exact": [str(v) for v in bracket],
        "node_counts_and_cuts": counts, "candidates": candidates,
        "jobs": jobs, "analytic_corollaries": corollaries,
        "resource_exceptions": resource_exceptions,
        "prefix_resource_audit_qualified": True,
        "replay_python": platform.python_version(),
        "replay_dependencies": {n: importlib.metadata.version(n) for n in ("numpy", "scipy", "torch")},
        "replay_only": True, "execution_authorized": False,
        "execution_head_still_locked": frozen["head"],
    }


def replay():
    result = check_evidence()
    disposition = json.loads((HERE / "decision.json").read_text())
    if disposition["outcome"] != result["outcome"] or disposition["training_authorized"]:
        raise ValueError("published outcome/authorization differs from replay")
    if disposition["conditional_relaxation_bounds_exact"] != result["conditional_bounds_exact"]:
        raise ValueError("published conditional bounds differ")
    if disposition["unconditional_shared4_bracket_exact"] != result["unconditional_shared4_bracket_exact"]:
        raise ValueError("published unconditional bracket differs")
    result["decision_sha256"] = digest(HERE / "decision.json")
    result["independent_replay_passed"] = True
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = replay()
    if args.output:
        write_once(args.output, result)
    print(json.dumps(result, indent=2))
