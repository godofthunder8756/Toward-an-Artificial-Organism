"""Recompute scarcity_v2 v1 labels from the frozen outputs plus erratum E2.

Reads scarcity_v2_study/results and the frozen protocol. Writes only under
results_v1_errata/. Does not search, and does not rewrite a frozen file.

E2 certificate. At K=1 an S-DIRECT policy maps each (evidence, cue) pair to an
I-phase configuration, and the reachable-configuration budget is 1. The image
is therefore a single configuration, fixed independently of evidence and cue.
Every admissible full policy is a constant policy, so it also belongs to
fixed_upkeep and to cue_blind_upkeep. Those two classes are subclasses of
full, and at K=1 full is contained in each of them. The three optimal values
coincide, and

    UPK = UPK_cue = UPK_ev = 0

with status DEGENERATE. The certificate is the class inclusion. It is not an
enumeration.
"""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

STUDY = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(STUDY))

from run_certificate import from_adapt, from_route, from_unpaid, from_upkeep  # noqa: E402
from verdicts import _bin_rows, _brief, _standard, control_failures, family  # noqa: E402

ROOT = STUDY.parent
OUT = Path(__file__).resolve().parent
RESULTS = STUDY / "results"
PROTOCOL_SHA = "ea47d1375c9e3c2fc4abdc538d714f65c66ed44243ca6ddd5e319684bd0fd4a6"
STAGE_A = (1, 2, 3, 4, 6, 8, 12, 16, 18, 24, 26, 27, 32, 48, 64, 96, 125)
ADAPT_K_RUN = {1, 16, 26, 48, 64, 125}
ACC_BINS = ["(0,1/4]", "(1/4,1/2]", "(1/2,1)"]
ZERO_GAP = {"0", "0/1"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def load(name: str):
    return json.loads((RESULTS / name).read_text())


def stage_b_grid(H: int) -> list[int]:
    cap = 125 * 2 * H
    return sorted({k * m for k in STAGE_A for m in (1, H, 2 * H) if k * m <= cap})


def k1_certificate() -> dict:
    """Structural zero at K=1. See the module docstring."""
    reachable_I = 1
    depends_on_evidence_or_cue = reachable_I > 1
    if depends_on_evidence_or_cue:
        raise RuntimeError("E2 certificate does not apply when more than one I-configuration is reachable")
    # fixed_upkeep ⊆ full and cue_blind_upkeep ⊆ full always.
    # At K=1, full ⊆ fixed_upkeep and full ⊆ cue_blind_upkeep, because every
    # full policy is constant. The three feasible sets are equal.
    return {"UPK": "0", "UPK_cue": "0", "UPK_ev": "0", "status": "DEGENERATE", "reachable_I": reachable_I}


def _tag_k1(records: list[dict], decision_only: bool) -> list[dict]:
    """Literal §5.5 reading: every applicable K=1 upkeep row is a K=1 control."""
    out = []
    for rec in records:
        rec = copy.deepcopy(rec)
        if rec["role"] in ("UPK", "UPK_cue") and rec.get("K") == 1:
            if decision_only and not rec.get("decision"):
                out.append(rec)
                continue
            rec["control"] = "K=1"
            rec["expected_gap"] = None
        out.append(rec)
    return out


def _apply_e2(records: list[dict]) -> tuple[list[dict], list[dict]]:
    cert = k1_certificate()
    out = []
    changes = []
    for rec in records:
        rec = copy.deepcopy(rec)
        if rec["role"] in ("UPK", "UPK_cue") and rec.get("K") == 1:
            before = {"status": rec["status"], "gap": rec.get("gap")}
            if before["gap"] not in (None, "0", "0/1"):
                raise RuntimeError(f"E2 disagrees with a certified nonzero K=1 gap: {rec['id']} {rec['role']} {before}")
            rec["status"] = cert["status"]
            rec["gap"] = cert[rec["role"]]
            rec["signature"] = "not-required"
            rec["control"] = "K=1"
            rec["expected_gap"] = None
            rec["correction"] = "E2"
            changes.append(
                {
                    "id": rec["id"],
                    "role": rec["role"],
                    "decision": rec.get("decision"),
                    "v1_status": before["status"],
                    "v1_gap": before["gap"],
                    "result": rec["status"],
                    "gap": rec["gap"],
                    "execution": "PROVED",
                }
            )
        out.append(rec)
    return out, changes


def _narrow(records: list[dict]) -> dict:
    info = _bin_rows(records, "ACC", ACC_BINS)
    first = info["(0,1/4]"]
    later = info["(1/4,1/2]"]["positive"] or info["(1/2,1)"]["positive"]
    established = (not first["positive"]) and (not first["unresolved"]) and bool(later)
    return {
        "established": established,
        "bins": {b: _brief(info[b]) for b in info},
        "statement": (
            "The first storage bin contains no positive cell."
            if established
            else "REJECT-NARROW is not established on these records."
        ),
    }


def _positive_signatures(records: list[dict], role: str) -> dict:
    rows = [r for r in records if r["role"] == role and r.get("decision") and r["status"] == "CERT-POS"]
    return {
        "n": len(rows),
        "signatures": dict(Counter(r.get("signature") for r in rows)),
        "ids": [r["id"] for r in rows],
    }


def _verdict_view(block: dict) -> dict:
    keep = ("verdict", "reason", "controls", "bins", "preserved_7_3", "standard_rule_would_say")
    out = {k: block[k] for k in keep if k in block}
    if "experimental" in block:
        out["n_experimental"] = len(block["experimental"])
        out["experimental"] = block["experimental"]
    return out


def _exec_unpaid(cell, quantity: str) -> dict:
    q = cell[quantity]
    return {
        "family": "unpaid",
        "quantity": quantity,
        "id": cell["id"],
        "result": q["status"],
        "execution": "RUN",
        "gap": q.get("gap"),
        "signature": q.get("signature"),
        "v1_result": q["status"],
        "v1_gap": q.get("gap"),
        "correction": None,
        "decision": quantity == "SEL" or cell["kind"] == "clean",
        "K": cell["K"],
        "cpu_ms": cell.get("full_cpu_ms", 0),
        "truncated": (cell.get("classes") or {}).get("full", {}).get("truncated", False),
    }


def _exec_upkeep(cell, quantity: str, cert: dict) -> dict:
    q = cell["quantities"][quantity]
    v1_status = q["status"]
    v1_gap = q.get("gap")
    correction = None
    result = v1_status
    gap = v1_gap
    execution = "PROVED" if v1_status != "UNRESOLVED" else "NOT-RUN"
    note = None
    if cell["K"] == 1:
        if v1_gap not in (None, "0", "0/1"):
            raise RuntimeError(f"E2 disagrees with certified K=1 gap on {cell['id']} {quantity}: {v1_gap}")
        result = cert["status"]
        gap = cert[quantity]
        execution = "PROVED"
        correction = "E2"
        note = "constant-policy certificate; classes coincide"
    elif v1_status == "UNRESOLVED":
        note = (
            "Not searched. No residual I-configuration search was run, and no timeout is asserted. "
            "The v1 reason text said the search was not exhausted inside the cell budget; that wording is withdrawn."
        )
    return {
        "family": "upkeep",
        "quantity": quantity,
        "id": cell["id"],
        "result": result,
        "execution": execution,
        "gap": gap,
        "signature": "not-required" if correction == "E2" else q.get("signature"),
        "v1_result": v1_status,
        "v1_gap": v1_gap,
        "correction": correction,
        "decision": bool(cell["decision"]) and cell["B_up"] in (1, 2),
        "K": cell["K"],
        "B_up": cell["B_up"],
        "delta": cell["delta"],
        "v": cell["v"],
        "r": cell["r"],
        "cpu_ms": cell.get("cpu_ms", 0),
        "bin": str(cell["B_up"]) if cell["B_up"] in (1, 2) else None,
        "note": note,
        "v1_reason": q.get("reason") or cell.get("reason"),
    }


def _exec_route(cell) -> dict:
    q = cell["ROUTE"]
    reason = cell.get("reason") or q.get("reason") or ""
    execution = "PROVED" if reason.startswith("ROUTE-Z3") else "RUN"
    return {
        "family": "route",
        "quantity": "ROUTE",
        "id": cell["id"],
        "result": q["status"],
        "execution": execution,
        "gap": q.get("gap"),
        "signature": q.get("signature"),
        "v1_result": q["status"],
        "v1_gap": q.get("gap"),
        "correction": None,
        "decision": cell["L"] in (2, 3),
        "L": cell["L"],
        "kind": cell["kind"],
        "a": cell.get("a"),
        "v": cell["v"],
        "r": cell["r"],
        "cpu_ms": cell.get("cpu_ms", 0),
        "proved_reason": reason if execution == "PROVED" else None,
    }


def _exec_adapt(cell) -> dict:
    q = cell["ADAPT"]
    interval = q.get("gap_interval")
    if interval:
        execution = "RUN"
        note = None
    elif q["status"] in ("CERT-ZERO", "DEGENERATE"):
        execution = "PROVED"
        note = None
    elif q["status"] == "UNRESOLVED":
        execution = "NOT-RUN"
        note = (
            "No policy-class search was run to completion, and no timeout is asserted. "
            "A v1 reason that says the residual search was not exhausted does not mean a budget was spent."
        )
    else:
        execution = "UNSPECIFIED"
        note = "execution classifier did not recognise this status"
    return {
        "family": "adapt",
        "quantity": "ADAPT",
        "id": cell["id"],
        "result": q["status"],
        "execution": execution,
        "gap": q.get("gap"),
        "gap_interval": interval,
        "signature": q.get("signature"),
        "v1_result": q["status"],
        "v1_gap": q.get("gap"),
        "correction": None,
        "decision": bool(cell["decision"]),
        "condition": cell["condition"],
        "H": cell["H"],
        "B_up": cell["B_up"],
        "K": cell["K"],
        "cpu_ms": cell.get("cpu_ms", 0),
        "note": note,
        "v1_reason": q.get("reason"),
        "V_T_const": q.get("V_T_const"),
        "V_T_H": q.get("V_T_H"),
    }


def _route_sel(route_cells, unpaid_cells) -> dict:
    sel = {}
    for cell in unpaid_cells:
        sel[(cell["kind"], cell.get("a"), cell["r"], cell["v"], cell["K"])] = cell["SEL"].get("gap")
    compared = []
    mismatches = []
    missing = []
    for cell in route_cells:
        key = (cell["kind"], cell.get("a"), cell["r"], cell["v"], cell["L"])
        gap = cell["ROUTE"].get("gap")
        if key not in sel:
            missing.append({"id": cell["id"], "route_gap": gap})
            continue
        row = {"id": cell["id"], "L": cell["L"], "route_gap": gap, "sel_gap": sel[key]}
        compared.append(row)
        if gap != sel[key]:
            mismatches.append(row)
    return {"n_compared": len(compared), "n_match": len(compared) - len(mismatches), "mismatches": mismatches, "no_sel_counterpart": missing}


def _upk_ev_summary(rows: list[dict]) -> dict:
    ev = [r for r in rows if r["quantity"] == "UPK_ev" and r["family"] == "upkeep"]
    def bucket(pred):
        sub = [r for r in ev if pred(r)]
        return {"n": len(sub), "results": dict(Counter(r["result"] for r in sub)), "gaps": dict(Counter(str(r["gap"]) for r in sub))}
    ample = bucket(lambda r: r["result"] != "placeholder" and r["B_up"] in (1, 2) and r["delta"] == "1/2" and r["v"] == "3/4" and (
        (r["B_up"] == 1 and r["K"] >= 26) or (r["B_up"] == 2 and r["K"] >= 16)
    ))
    return {
        "all": bucket(lambda r: True),
        "ample_clean_v_3/4_primary": ample,
        "k1": bucket(lambda r: r["K"] == 1),
    }


def _counts(rows: list[dict]) -> dict:
    out = {}
    for row in rows:
        key = f"{row['family']}:{row['quantity']}"
        slot = out.setdefault(key, {"n": 0, "result": Counter(), "execution": Counter()})
        slot["n"] += 1
        slot["result"][row["result"]] += 1
        slot["execution"][row["execution"]] += 1
    return {k: {"n": v["n"], "result": dict(v["result"]), "execution": dict(v["execution"])} for k, v in out.items()}


def main() -> None:
    protocol = STUDY / "SCARCITY_V2_PROTOCOL_FINAL.md"
    digest = sha256(protocol)
    if digest != PROTOCOL_SHA:
        raise SystemExit(f"protocol hash changed: {digest}")

    unpaid = load("cells_unpaid.json")
    upkeep = load("cells_upkeep.json")
    route = load("cells_route.json")
    adapt = load("cells_adapt.json")
    graded = load("graded_upk.json")
    selftests = load("selftests.json")
    verdicts_v1 = load("verdicts.json")

    base_records = []
    for cell in unpaid:
        base_records.extend(from_unpaid(cell))
    for cell in upkeep:
        base_records.extend(from_upkeep(cell))
    for cell in route:
        base_records.extend(from_route(cell))
    for cell in adapt:
        base_records.extend(from_adapt(cell))

    before_decision = _tag_k1(base_records, decision_only=True)
    before_all = _tag_k1(base_records, decision_only=False)
    after, k1_role_changes = _apply_e2(base_records)

    def pack(records):
        fam = family(records)
        # family() still routes ACC through the v1 override. The corrected
        # primary label is the §7.2 standard rule on the same records.
        standard_acc = _standard("ACC", records, ACC_BINS)
        return {
            "family_code_path": {role: _verdict_view(fam[role]) for role in fam},
            "ACC_standard_rule": _verdict_view(standard_acc),
            "ACC_narrow": _narrow(records),
            "ACC_positive": _positive_signatures(records, "ACC"),
            "control_failures": {
                role: control_failures(role, records)
                for role in ("SEL", "ACC", "UPK", "UPK_cue", "ROUTE", "ADAPT")
            },
        }

    before_d = pack(before_decision)
    before_a = pack(before_all)
    after_p = pack(after)

    cert = k1_certificate()
    rows = []
    for cell in unpaid:
        for quantity in ("SEL", "ACC"):
            rows.append(_exec_unpaid(cell, quantity))
    for cell in upkeep:
        for quantity in ("UPK", "UPK_cue", "UPK_ev"):
            rows.append(_exec_upkeep(cell, quantity, cert))
    for cell in route:
        rows.append(_exec_route(cell))
    for cell in adapt:
        rows.append(_exec_adapt(cell))
    for quantity, gap in (("UPK", graded["UPK"]), ("UPK_cue", graded["UPK_cue"]), ("UPK_ev", graded["UPK_ev"])):
        rows.append(
            {
                "family": "graded_upkeep_report",
                "quantity": quantity,
                "id": "graded/ample/a=3/4/B=1/d=1/2/v=3/4/r=3/4",
                "result": "CERT-POS" if gap not in ZERO_GAP else "CERT-ZERO",
                "execution": "PROVED",
                "gap": gap,
                "v1_result": "report",
                "v1_gap": gap,
                "correction": None,
                "decision": False,
                "descriptive": True,
                "note": "§5.4 report-only closed form. Not an admission cell.",
            }
        )

    unspecified = [r["id"] + " " + r["quantity"] for r in rows if r["execution"] == "UNSPECIFIED"]
    if unspecified:
        raise RuntimeError("unclassified records: " + ", ".join(unspecified))

    k1_rows = [r for r in rows if r.get("K") == 1 and r["family"] == "upkeep"]
    disagree_nonzero = [
        {"id": r["id"], "quantity": r["quantity"], "v1_gap": r["v1_gap"], "v1_result": r["v1_result"]}
        for r in k1_rows
        if r["v1_gap"] not in (None, "0", "0/1")
    ]

    route_sel = _route_sel(route, unpaid)
    cpus = []
    for cell in unpaid:
        for key in ("full_cpu_ms", "blind_cpu_ms"):
            if cell.get(key) is not None:
                cpus.append(("unpaid", cell["id"], key, cell[key]))
    for cell in route:
        cpus.append(("route", cell["id"], "cpu_ms", cell.get("cpu_ms", 0)))
    for cell in adapt:
        cpus.append(("adapt", cell["id"], "cpu_ms", cell.get("cpu_ms", 0)))
    for cell in upkeep:
        cpus.append(("upkeep", cell["id"], "cpu_ms", cell.get("cpu_ms", 0)))
    max_cpu = max(cpus, key=lambda item: item[3])

    frozen = [
        STUDY / "SCARCITY_V2_PROTOCOL_FINAL.md",
        STUDY / "SCARCITY_V2_FREEZE_NOTE.md",
        STUDY / "SCARCITY_V2_FREEZE_v1.json",
        STUDY / "DEVIATIONS.md",
        RESULTS / "RESULTS.md",
        RESULTS / "verdicts.json",
        RESULTS / "cells_unpaid.json",
        RESULTS / "cells_upkeep.json",
        RESULTS / "cells_route.json",
        RESULTS / "cells_adapt.json",
        RESULTS / "graded_upk.json",
        RESULTS / "selftests.json",
    ]
    hashes = {str(path.relative_to(ROOT)): sha256(path) for path in frozen}

    adapt_intervals = [
        {
            "id": r["id"],
            "result": r["result"],
            "execution": r["execution"],
            "gap_interval": r["gap_interval"],
            "cpu_ms": r["cpu_ms"],
            "V_T_const": r["V_T_const"],
            "V_T_H": r["V_T_H"],
        }
        for r in rows
        if r["family"] == "adapt" and r.get("gap_interval")
    ]
    adapt_notrun_with_cpu = [
        {"id": r["id"], "cpu_ms": r["cpu_ms"], "v1_reason": r.get("v1_reason")}
        for r in rows
        if r["family"] == "adapt" and r["execution"] == "NOT-RUN" and r.get("cpu_ms", 0) > 0
    ]

    h2 = stage_b_grid(2)
    h3 = stage_b_grid(3)
    h1 = stage_b_grid(1)
    ran_k = sorted({cell["K"] for cell in adapt})
    facts = {
        "protocol_sha256": digest,
        "frozen_sha256": hashes,
        "certificate_E2": cert,
        "n_base_verdict_records": len(base_records),
        "n_result_records": len(rows),
        "record_counts": _counts(rows),
        "k1_upkeep_records": {
            "n": len(k1_rows),
            "by_quantity": dict(Counter(r["quantity"] for r in k1_rows)),
            "v1_result": {
                f"{quantity}|{status}|decision={decision}": n
                for (quantity, status, decision), n in Counter(
                    (r["quantity"], r["v1_result"], r["decision"]) for r in k1_rows
                ).items()
            },
            "v2_all_degenerate_zero": all(r["result"] == "DEGENERATE" and r["gap"] == "0" and r["execution"] == "PROVED" for r in k1_rows),
            "nonzero_v1_gaps": disagree_nonzero,
        },
        "k1_role_changes_n": len(k1_role_changes),
        "before_decision_bearing_controls": {
            "UPK": before_d["family_code_path"]["UPK"]["verdict"],
            "UPK_cue": before_d["family_code_path"]["UPK_cue"]["verdict"],
            "UPK_failures": before_d["control_failures"]["UPK"],
            "UPK_cue_failures": before_d["control_failures"]["UPK_cue"],
            "n_UPK_failures": len(before_d["control_failures"]["UPK"]),
            "n_UPK_cue_failures": len(before_d["control_failures"]["UPK_cue"]),
        },
        "before_all_k1_tagged": {
            "UPK": before_a["family_code_path"]["UPK"]["verdict"],
            "UPK_cue": before_a["family_code_path"]["UPK_cue"]["verdict"],
            "n_UPK_failures": len(before_a["control_failures"]["UPK"]),
            "n_UPK_cue_failures": len(before_a["control_failures"]["UPK_cue"]),
            "UPK_failures": before_a["control_failures"]["UPK"],
            "UPK_cue_failures": before_a["control_failures"]["UPK_cue"],
        },
        "after_E2": {
            "code_path": {role: after_p["family_code_path"][role]["verdict"] for role in after_p["family_code_path"]},
            "reasons": {role: after_p["family_code_path"][role]["reason"] for role in after_p["family_code_path"]},
            "bins": {role: after_p["family_code_path"][role].get("bins") for role in ("SEL", "ACC", "UPK", "UPK_cue", "ROUTE")},
            "ACC_standard_rule": after_p["ACC_standard_rule"]["verdict"],
            "ACC_standard_reason": after_p["ACC_standard_rule"]["reason"],
            "ACC_standard_bins": after_p["ACC_standard_rule"].get("bins"),
            "ACC_narrow": after_p["ACC_narrow"],
            "ACC_positive": {k: after_p["ACC_positive"][k] for k in ("n", "signatures")},
            "control_failures": {role: after_p["control_failures"][role] for role in after_p["control_failures"]},
            "UPK_bins": after_p["family_code_path"]["UPK"].get("bins"),
            "UPK_cue_bins": after_p["family_code_path"]["UPK_cue"].get("bins"),
        },
        "v1_recorded": {role: verdicts_v1[role]["verdict"] for role in verdicts_v1},
        "route_vs_sel": route_sel,
        "upk_ev": _upk_ev_summary(rows),
        "graded_upk": graded,
        "max_cpu_ms": {"family": max_cpu[0], "id": max_cpu[1], "field": max_cpu[2], "cpu_ms": max_cpu[3]},
        "adapt_k_run": ran_k,
        "stage_b": {
            "H2_grid": h2,
            "H2_run": sorted(ADAPT_K_RUN),
            "H2_not_run": [k for k in h2 if k not in ADAPT_K_RUN],
            "H3_grid_not_run": h3,
            "H1_grid": h1,
            "H1_executed": sorted({cell["K"] for cell in adapt if cell["H"] == 1}),
        },
        "adapt_intervals": adapt_intervals,
        "adapt_notrun_with_cpu": adapt_notrun_with_cpu,
        "selftests": {
            "n_pass": selftests.get("n_pass"),
            "n_fail": selftests.get("n_fail"),
            "names": [c["name"] for c in selftests["checks"]],
            "k1_upkeep_control_among_them": any("K=1" in c["name"] and "UPK" in c["name"].upper() for c in selftests["checks"]),
        },
        "labels": None,
    }

    acc_primary = after_p["ACC_standard_rule"]["verdict"]
    acc_narrow_ok = after_p["ACC_narrow"]["established"]
    acc_sigs = after_p["ACC_positive"]["signatures"]
    upk_after = after_p["family_code_path"]["UPK"]["verdict"]
    cue_after = after_p["family_code_path"]["UPK_cue"]["verdict"]
    failures_after = {role: after_p["control_failures"][role] for role in after_p["control_failures"]}
    agrees = {
        "ACC_primary_REJECT_SIG": acc_primary == "REJECT-SIG(ACC)",
        "ACC_narrow_retained": acc_narrow_ok,
        "ACC_positive_all_SIG_UNDEFINED": acc_sigs == {"SIG-UNDEFINED": acc_sigs.get("SIG-UNDEFINED", 0)} and acc_sigs.get("SIG-UNDEFINED", 0) == after_p["ACC_positive"]["n"] and after_p["ACC_positive"]["n"] > 0,
        "UPK_ADMIT_restored": upk_after == "ADMIT(UPK)" and not failures_after["UPK"],
        "UPK_cue_ADMIT_restored": cue_after == "ADMIT(UPK_cue)" and not failures_after["UPK_cue"],
        "SEL_ADMIT": after_p["family_code_path"]["SEL"]["verdict"] == "ADMIT(SEL)",
        "ROUTE_ADMIT": after_p["family_code_path"]["ROUTE"]["verdict"] == "ADMIT(ROUTE)",
        "ADAPT_VALUE_ONLY": after_p["family_code_path"]["ADAPT"]["verdict"] == "VALUE-ONLY",
        "route_sel_gaps_equal_where_both_exist": not route_sel["mismatches"],
        "k1_all_degenerate": facts["k1_upkeep_records"]["v2_all_degenerate_zero"],
        "no_timeout_near_budget": max_cpu[3] < 4 * 60 * 1000,
        "before_decision_controls_block": before_d["family_code_path"]["UPK"]["verdict"] != "ADMIT(UPK)" and before_d["family_code_path"]["UPK_cue"]["verdict"] != "ADMIT(UPK_cue)",
    }
    facts["agrees_with_errata"] = agrees
    facts["disagreements"] = [name for name, ok in agrees.items() if not ok]
    facts["labels"] = {
        "SEL": "ADMIT(SEL)",
        "ACC_primary": acc_primary,
        "ACC_retained": "REJECT-NARROW(ACC)" if acc_narrow_ok else "NOT-ESTABLISHED",
        "UPK": upk_after,
        "UPK_cue": cue_after,
        "UPK_ev": "descriptive",
        "ROUTE": after_p["family_code_path"]["ROUTE"]["verdict"],
        "ADAPT": after_p["family_code_path"]["ADAPT"]["verdict"],
        "v1_code_path_ACC_still": after_p["family_code_path"]["ACC"]["verdict"],
    }

    # v1 code path on the corrected records still forces REJECT-NARROW. That is
    # the implementation being corrected, not the recomputed label.
    verdicts_out = {
        "source": "recomputed from results/*.json plus the E2 certificate; original verdicts.json is unchanged",
        "before_E2_decision_bearing_K1_controls_tagged": {
            "note": "v1 did not tag unresolved K=1 upkeep cells as controls. This block tags the decision-bearing ones and reruns rule 4.",
            "UPK": before_d["family_code_path"]["UPK"],
            "UPK_cue": before_d["family_code_path"]["UPK_cue"],
        },
        "after_E2_code_path": after_p["family_code_path"],
        "after_E2_corrected_labels": facts["labels"],
        "after_E2_ACC_standard_rule": after_p["ACC_standard_rule"],
        "after_E2_ACC_narrow_record": after_p["ACC_narrow"],
        "control_failures_after_E2": failures_after,
    }

    (OUT / "verdicts_v2.json").write_text(json.dumps(verdicts_out, indent=2) + "\n")
    (OUT / "k1_corrections.json").write_text(json.dumps(k1_rows, indent=2) + "\n")
    (OUT / "records_v2.json").write_text(json.dumps(rows, indent=2) + "\n")
    (OUT / "recompute_facts.json").write_text(json.dumps(facts, indent=2) + "\n")
    print(json.dumps({
        "labels": facts["labels"],
        "disagreements": facts["disagreements"],
        "agrees": agrees,
        "before_decision": {
            "UPK": facts["before_decision_bearing_controls"]["UPK"],
            "UPK_cue": facts["before_decision_bearing_controls"]["UPK_cue"],
            "n_UPK": facts["before_decision_bearing_controls"]["n_UPK_failures"],
            "n_UPK_cue": facts["before_decision_bearing_controls"]["n_UPK_cue_failures"],
        },
        "before_all": {
            "UPK": facts["before_all_k1_tagged"]["UPK"],
            "n_UPK": facts["before_all_k1_tagged"]["n_UPK_failures"],
            "n_UPK_cue": facts["before_all_k1_tagged"]["n_UPK_cue_failures"],
        },
        "k1_n": len(k1_rows),
        "k1_v1": facts["k1_upkeep_records"]["v1_result"],
        "route_sel": {"n": route_sel["n_compared"], "match": route_sel["n_match"], "mismatch": len(route_sel["mismatches"]), "missing": len(route_sel["no_sel_counterpart"])},
        "stage_b_H2_not_run": facts["stage_b"]["H2_not_run"],
        "max_cpu": facts["max_cpu_ms"],
        "counts": facts["record_counts"],
        "upk_ev": facts["upk_ev"],
        "adapt_intervals": adapt_intervals,
        "adapt_notrun_cpu": adapt_notrun_with_cpu,
        "selftest_names_n": len(facts["selftests"]["names"]),
        "acc_pos": facts["after_E2"]["ACC_positive"],
        "acc_bins": facts["after_E2"]["ACC_standard_bins"],
        "upk_bins": facts["after_E2"]["UPK_bins"],
    }, indent=2))


if __name__ == "__main__":
    main()
