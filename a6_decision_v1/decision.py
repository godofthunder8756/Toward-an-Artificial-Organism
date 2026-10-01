"""Solver-free disposition of the bounded effort; no optimizer attribution."""

from __future__ import annotations

import argparse
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

from a6_decision_v1.exact import GATE
from a6_decision_v1.preservation import digest, verify, write_once
from a6_decision_v1.runner import HERE, JOBS, contract
from a6_decision_v1.verify import certify_candidate, verify_lemmas


def verify_cut(proof, policies):
    selection = proof["selection"]
    if len(selection) != 32 or any(type(k) is not int or not 0 <= k < 27 for k in selection):
        raise ValueError("invalid infeasible-head selection")
    rows, rhs = [], []
    consumer = proof["consumer"]
    if consumer not in (0, 2) or type(proof["positive"]) is not bool:
        raise ValueError("invalid head-cut scope")
    for c, m in product(range(4), range(8)):
        for bit in (0, 1):
            action = policies[selection[c * 8 + m]][consumer][bit]
            row = [0] * 13
            sign = 1 if action == 0 else -1
            row[m], row[8 + c], row[12] = sign, sign, sign * bit
            rows.append(row)
            rhs.append(-action)
    rows.append([0] * 12 + ([-1] if proof["positive"] else [1]))
    rhs.append(-1 if consumer == 0 else 0)
    multipliers = [F(v) for v in proof["multipliers"]]
    if len(multipliers) != len(rows) or any(v < 0 for v in multipliers):
        raise ValueError("invalid Farkas multipliers")
    if any(sum(v * row[j] for v, row in zip(multipliers, rows)) != 0 for j in range(13)):
        raise ValueError("Farkas column cancellation failed")
    contradiction = sum(v * r for v, r in zip(multipliers, rhs))
    if contradiction >= 0 or str(contradiction) != proof["contradiction"]:
        raise ValueError("Farkas contradiction failed")
    return True


def decide():
    from a6_decision_v1.search import relaxation
    from shared4_v1.coupled_lower import replay_dual
    contract()
    preservation = verify(json.loads((HERE / "baseline_hashes.json").read_text()))
    lemmas = verify_lemmas()
    rows, conditional, candidates = [], {}, []
    for name in JOBS:
        result_path = HERE / (name + "_result.json")
        start = HERE / (name + "_start.json")
        if not start.exists():
            rows.append({"job": name, "state": "unused"})
            continue
        if not result_path.exists():
            raise ValueError(f"started job lacks supervisor disposition: {name}")
        result = json.loads(result_path.read_text())
        row = {"supervisor": result}
        root = HERE / (name + "_root.json")
        if root.exists():
            document = json.loads(root.read_text())
            model, offset, _, _, policies = relaxation(name.endswith("positive"),
                                                       name.startswith("f2"))
            bounds = []
            for key in ("lifted_prior_dual", "discovered_exact_dual"):
                proof = document.get(key)
                if proof is not None:
                    bounds.append(replay_dual(model, offset, proof))
            row["conditional_exact_lower"] = str(max(bounds))
            conditional[name] = max(bounds)
            worker = HERE / (name + "_worker.json")
            if worker.exists():
                details = json.loads(worker.read_text())
                for cut in details.get("cuts", []):
                    verify_cut(cut, policies)
                row["certified_head_cuts"] = len(details.get("cuts", []))
                row["numerical_diagnostics"] = details.get("milp_NOT_CERTIFICATE")
        candidate = HERE / (name + "_candidate.json")
        if candidate.exists():
            checked = certify_candidate(json.loads(candidate.read_text()))
            candidates.append({"path": candidate.name, "sha256": digest(candidate),
                               "independent_replay": checked})
        rows.append(row)
    passed = [c for c in candidates if c["independent_replay"]["certified_gate_PASS"]]
    failed = all(conditional.get(name, F(0)) > GATE
                 for name in ("f1_positive", "f1_negative"))
    if passed and failed:
        raise AssertionError("constructive and impossibility certificates conflict")
    outcome = "PASS" if passed else "FAIL" if failed else "UNRESOLVED"
    if outcome == "UNRESOLVED" and any(
            not (HERE / (name + "_result.json")).exists() for name in JOBS):
        raise ValueError("bounded effort is incomplete; do not close it as UNRESOLVED")
    bracket = [F(5159249, 29296875), F(1031759, 4687500)]
    for candidate in candidates:
        checked = candidate["independent_replay"]
        if checked["positive_margins"]:
            bracket[1] = min(bracket[1], F(checked["population"]["shared_joint_exact"]))
    return {
        "schema": 1, "outcome": outcome, "bounded_effort_closed": True,
        "mathematical_question_closed": outcome != "UNRESOLVED",
        "training_authorized": False, "training_executed": False,
        "phase3b_verdict": "B unchanged",
        "unconditional_shared4_bracket_exact": [str(v) for v in bracket],
        "joint_gate_exact": str(GATE),
        "conditional_relaxation_bounds_exact": {k: str(v) for k, v in conditional.items()},
        "conditional_bounds_are_not_unconstrained_global_optima": True,
        "independent_lemmas": lemmas, "preservation": preservation,
        "jobs": rows, "candidates": candidates,
        "boundary": ("No certified legal full-gate witness or full-family conjunction "
                     "impossibility obtained within the approved finite analytic effort."
                     if outcome == "UNRESOLVED" else
                     "Certificate applies only to the unchanged frozen conjunction/family."),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = decide()
    if args.output:
        write_once(args.output, result)
    print(json.dumps(result, indent=2))
