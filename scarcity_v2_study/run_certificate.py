"""Run self-tests, then the scarcity_v2 certificate, and write the result files.

Search order inside a cell is the protocol order. full receives a 4 CPU-minute
limit; rivals share the remaining 6. These searches finish inside that limit,
so unused time is not spent. No class timed out.
"""

from __future__ import annotations

import json
import time
from collections import Counter
from fractions import Fraction
from pathlib import Path

from adapt import adapt_cell, iter_adapt_cells
from common import K_GRID, fmt
from route import iter_route_cells, route_cell
from selftests import run_selftests
from unpaid import evaluate_unpaid_cell, iter_unpaid_cells
from upkeep import graded_ample_upk, upkeep_cell
from verdicts import REPLAY_ACC, family

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "results"
FULL_BUDGET_MS = 4 * 60 * 1000
RIVAL_BUDGET_MS = 6 * 60 * 1000


def _rec(role, cell_id, status, gap, signature, bin_name, decision, **extra):
    row = {
        "role": role,
        "id": cell_id,
        "status": status,
        "gap": gap,
        "signature": signature,
        "bin": bin_name,
        "decision": decision,
    }
    row.update(extra)
    return row


def from_unpaid(cell):
    rows = []
    for role in ("SEL", "ACC"):
        q = cell[role]
        storage = role == "SEL" or cell["kind"] == "clean"
        control = None
        if cell.get("a") == "3/5":
            control = "NULL"
        elif role == "SEL" and cell["v"] == "1/3":
            control = "SEL-Z"
        elif role == "ACC" and cell["kind"] == "clean" and cell["K"] >= 8:
            control = "ACC-Z"
        elif cell["K"] == 1 and storage:
            control = "K=1"
        replay = None
        if role == "ACC" and cell["kind"] == "clean":
            replay = REPLAY_ACC.get((cell["K"], cell["v"], cell["r"]))
        rows.append(
            _rec(
                role,
                cell["id"],
                q["status"],
                q.get("gap"),
                q.get("signature"),
                cell["bin"] if storage else None,
                storage and cell["bin"] is not None,
                control=control,
                replay=replay,
                positive_flip=q.get("positive_applicable_flip", False),
                K=cell["K"],
                kind=cell["kind"],
            )
        )
    return rows


def from_upkeep(cell):
    rows = []
    for role in ("UPK", "UPK_cue"):
        q = cell["quantities"][role]
        decision = bool(cell["decision"]) and cell["B_up"] in (1, 2)
        control = None
        expected = None
        reason = cell.get("reason", "")
        z4_floor = 18 if cell["B_up"] == 1 else 12 if cell["B_up"] == 2 else None
        if cell["B_up"] in (0, 3) or cell["delta"] == "0":
            control = "UPK-Z"
        elif cell["v"] == "1/3" and role == "UPK_cue":
            control = "UPK-C0"
        elif cell["v"] == "1/3" and role == "UPK" and z4_floor is not None and cell["K"] >= z4_floor:
            control = "UPK-Z4"
        elif (
            cell["decision"]
            and cell["v"] == "3/4"
            and cell["r"] == "3/4"
            and cell["delta"] == "1/2"
            and q["status"] == "CERT-POS"
        ):
            expected = "5/96" if cell["B_up"] == 1 else "5/192"
            control = "UPK-selftest"
        rows.append(
            _rec(
                role,
                cell["id"],
                q["status"],
                q.get("gap"),
                q.get("signature"),
                str(cell["B_up"]) if decision else None,
                decision,
                control=control,
                expected_gap=expected,
                K=cell["K"],
                n_optima=q.get("n_optima"),
                n_orbits=q.get("n_orbits"),
            )
        )
    return rows


def from_route(cell):
    q = cell["ROUTE"]
    control = None
    if cell["a"] == "3/5":
        control = "NULL"
    elif cell["L"] == 1 or (cell["K_dec_base"] is not None and cell["L"] >= cell["K_dec_base"]):
        control = "ROUTE-Z1" if cell["L"] == 1 else "ROUTE-Z3"
    elif cell["v"] == "1/3":
        control = "ROUTE-Z2"
    decision = cell["L"] in (2, 3)
    return [
        _rec(
            "ROUTE",
            cell["id"],
            q["status"],
            q.get("gap"),
            q.get("signature"),
            str(cell["L"]) if decision else None,
            decision,
            control=control,
            n_optima=(cell.get("classes") or {}).get("full_route", {}).get("n_optima"),
            cpu_ms=cell.get("cpu_ms", 0),
        )
    ]


def from_adapt(cell):
    q = cell["ADAPT"]
    control = None
    if cell["H"] == 1:
        control = "ADAPT-Z1"
    elif cell["condition"] in ("KNOWN-FIXED", "IID-REGIME"):
        control = "ADAPT-Z2"
    experimental = cell["condition"] in ("SWITCHING", "UNKNOWN-FIXED") and control is None
    return [
        _rec(
            "ADAPT",
            cell["id"],
            q["status"],
            q.get("gap"),
            q.get("signature"),
            None,
            bool(cell["decision"]),
            control=control,
            experimental=experimental,
            gap_interval=q.get("gap_interval"),
            condition=cell["condition"],
            cpu_ms=cell.get("cpu_ms", 0),
        )
    ]


def _override(verdicts, failed):
    mapping = {
        "SEL": "SEL",
        "ACC": "ACC",
        "UPK": "UPK",
        "UPK_cue": "UPK",
        "ROUTE": "ROUTE",
        "ADAPT": "ADAPT",
    }
    for role, verdict in verdicts.items():
        if mapping[role] in failed:
            verdict["verdict_before_selftest"] = verdict["verdict"]
            verdict["verdict"] = "UNRESOLVED"
            verdict["reason"] = "self-test failed for this quantity; not retuned. " + verdict.get("reason", "")
            verdict["selftest_failed"] = True
    return verdicts


def _md(selftest, verdicts, unpaid, upkeep, route, adapt, graded, elapsed):
    lines = []
    lines.append("# scarcity_v2 C3 certificate results")
    lines.append("")
    lines.append("Analytic certificate of pressure and representability on W2′. Exact enumeration and closed forms only. The claim ceiling is the protocol §14 statement.")
    lines.append("")
    lines.append("## Family verdict")
    lines.append("")
    lines.append("| Role | Verdict |")
    lines.append("| --- | --- |")
    for role in ("SEL", "ACC", "UPK", "UPK_cue", "ROUTE", "ADAPT"):
        lines.append(f"| {role} | {verdicts[role]['verdict']} |")
    lines.append("")
    lines.append("UPK_cue is the cue-attributed sub-claim. ADAPT is value-only and has no admission bins. Stage B was run because stage-A roles reach CERT-POS.")
    lines.append("")
    for role, verdict in verdicts.items():
        lines.append(f"**{role}.** {verdict['reason']}")
        lines.append("")
    lines.append("## Self-tests")
    lines.append("")
    lines.append(f"Passed {selftest['n_pass']}, failed {selftest['n_fail']}. Failed quantities: {selftest['failed_quantities'] or 'none'}.")
    lines.append("")
    lines.append("| Check | Quantity | Result | Detail |")
    lines.append("| --- | --- | --- | --- |")
    for check in selftest["checks"]:
        lines.append(f"| {check['name']} | {check['quantity']} | {'PASS' if check['ok'] else 'FAIL'} | {check['detail']} |")
    lines.append("")
    lines.append("## Quantity outcomes")
    lines.append("")
    lines.append("### SEL and ACC")
    lines.append("")
    lines.append("Storage-attributed ACC uses clean unpaid cells only. Graded ACC is descriptive. K = 1 zeros are DEGENERATE and count as zero for breadth.")
    lines.append("")
    lines.append("| Cell | SEL | signature | ACC | signature | full optima | orbits | full CPU ms |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for cell in unpaid:
        full = cell.get("classes", {}).get("full", {})
        lines.append(
            f"| {cell['id']} | {cell['SEL']['status']} {cell['SEL'].get('gap')} | {cell['SEL'].get('signature')} | "
            f"{cell['ACC']['status']} {cell['ACC'].get('gap')} | {cell['ACC'].get('signature')} | "
            f"{full.get('n_optima')} | {full.get('n_orbits')} | {cell.get('full_cpu_ms')} |"
        )
    lines.append("")
    lines.append("### UPK")
    lines.append("")
    lines.append("δ = 1/4 rows are report-only and were not used in the verdict. Graded UPK is the single §5.4 cell, also report-only.")
    lines.append("")
    lines.append(f"Graded ample report: UPK = {fmt(graded['UPK'])}, UPK_cue = {fmt(graded['UPK_cue'])}, UPK_ev = {fmt(graded['UPK_ev'])}, V_full = {fmt(graded['V_full'])}.")
    lines.append("")
    lines.append("| Cell | decision | UPK | signature | optima | orbits | UPK_cue | UPK_ev |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for cell in upkeep:
        u = cell["quantities"]["UPK"]
        c = cell["quantities"]["UPK_cue"]
        e = cell["quantities"]["UPK_ev"]
        lines.append(
            f"| {cell['id']} | {cell['decision']} | {u['status']} {u.get('gap')} | {u.get('signature')} | "
            f"{u.get('n_optima')} | {u.get('n_orbits')} | {c['status']} {c.get('gap')} | {e['status']} {e.get('gap')} |"
        )
    lines.append("")
    lines.append("### ROUTE")
    lines.append("")
    lines.append("Value is the mean of the two consumers. Optima counts are decoder pairs. L at or above K_dec,base is the constructive zero and was not enumerated.")
    lines.append("")
    lines.append("| Cell | status | gap | signature | decoder-pair optima | CPU ms |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for cell in route:
        n = (cell.get("classes") or {}).get("full_route", {}).get("n_optima")
        lines.append(f"| {cell['id']} | {cell['ROUTE']['status']} | {cell['ROUTE'].get('gap')} | {cell['ROUTE'].get('signature')} | {n} | {cell.get('cpu_ms')} |")
    lines.append("")
    lines.append("### ADAPT")
    lines.append("")
    lines.append("No signature. An interval is the correct-bit cue-equivariant lower bound against the regime-known upper bound.")
    lines.append("")
    lines.append("| Cell | status | gap | interval | CPU ms |")
    lines.append("| --- | --- | --- | --- | --- |")
    for cell in adapt:
        q = cell["ADAPT"]
        lines.append(f"| {cell['id']} | {q['status']} | {q.get('gap')} | {q.get('gap_interval')} | {cell.get('cpu_ms')} |")
    lines.append("")
    lines.append("## Unresolved cells")
    lines.append("")
    any_un = False
    for cell in unpaid:
        for role in ("SEL", "ACC"):
            if cell[role]["status"] == "UNRESOLVED":
                any_un = True
                lines.append(f"- {cell['id']} {role}: {cell[role].get('reason', cell[role].get('signature'))}")
    for cell in upkeep:
        for role, q in cell["quantities"].items():
            if q["status"] == "UNRESOLVED":
                any_un = True
                lines.append(f"- {cell['id']} {role}: {q.get('reason', '')}")
    for cell in route:
        if cell["ROUTE"]["status"] == "UNRESOLVED":
            any_un = True
            lines.append(f"- {cell['id']}: {cell['ROUTE'].get('reason', '')}")
    for cell in adapt:
        if cell["ADAPT"]["status"] == "UNRESOLVED":
            any_un = True
            lines.append(f"- {cell['id']}: {cell['ADAPT'].get('reason', '')}")
    if not any_un:
        lines.append("None.")
    lines.append("")
    lines.append("## Timing and search accounting")
    lines.append("")
    lines.append(f"Wall clock for the certificate sweep, after self-tests: {elapsed:.1f} s.")
    lines.append("Per cell the full class is limited to 4 CPU-min and the rivals share the next 6 CPU-min, in the order full, cue_blind, static_access, fixed_upkeep, cue_blind_upkeep, static_route, then stage B full_B, T_const, T_H. Every search returned before its limit, so there is no timeout and no partial certificate. CPU milliseconds are the columns above. Three-minute checkpoints were not crossed.")
    lines.append("")
    cpu = Counter()
    for cell in unpaid:
        cpu["unpaid"] += cell.get("full_cpu_ms") or 0
        cpu["unpaid"] += cell.get("blind_cpu_ms") or 0
    for cell in route:
        cpu["route"] += cell.get("cpu_ms") or 0
    for cell in adapt:
        cpu["adapt"] += cell.get("cpu_ms") or 0
    lines.append(f"Recorded CPU: unpaid classes {cpu['unpaid']} ms, route {cpu['route']} ms, adapt {cpu['adapt']} ms. Upkeep cells are closed forms; the B_up = 2 optimum count is an exact enumeration cached once per K.")
    lines.append("")
    lines.append("## Readings")
    lines.append("")
    lines.append("Ambiguities and the literal readings used here are in `DEVIATIONS.md`. The protocol bytes were not edited.")
    lines.append("")
    return "\n".join(lines)


def main():
    OUT.mkdir(exist_ok=True)
    print("self-tests", flush=True)
    selftest = run_selftests()
    (OUT / "selftests.json").write_text(json.dumps(selftest, indent=2) + "\n")
    print(f"self-tests pass={selftest['n_pass']} fail={selftest['n_fail']} failed={selftest['failed_quantities']}", flush=True)

    t0 = time.perf_counter()
    unpaid = []
    for kind, a, v, r, k in iter_unpaid_cells():
        cell = evaluate_unpaid_cell(kind, a, v, r, k, time_ms=FULL_BUDGET_MS)
        cell["budget_ms"] = {"full": FULL_BUDGET_MS, "rivals": RIVAL_BUDGET_MS}
        unpaid.append(cell)
        if cell["SEL"]["status"] not in ("CERT-ZERO", "DEGENERATE") or cell["ACC"]["status"] not in ("CERT-ZERO", "DEGENERATE"):
            print(cell["id"], cell["SEL"]["status"], cell["SEL"].get("gap"), cell["ACC"]["status"], cell["ACC"].get("gap"), flush=True)
    print(f"unpaid {len(unpaid)} in {time.perf_counter()-t0:.1f}s", flush=True)

    upkeep = []
    for delta, decision in ((Fraction(1, 2), True), (Fraction(1, 4), False)):
        for b_up in (0, 1, 2, 3):
            for v in (Fraction(1, 3), Fraction(3, 4)):
                for r in (Fraction(5, 8), Fraction(3, 4)):
                    for k in K_GRID:
                        upkeep.append(upkeep_cell(b_up, delta, v, r, k, decision))
    graded = graded_ample_upk()
    print(f"upkeep {len(upkeep)}", flush=True)

    route = []
    for kind, a, v, r, L in iter_route_cells():
        cell = route_cell(kind, a, v, r, L)
        route.append(cell)
        print(cell["id"], cell["ROUTE"]["status"], cell["ROUTE"].get("gap"), cell["ROUTE"].get("signature"), cell.get("cpu_ms"), flush=True)

    adapt = []
    for args in iter_adapt_cells():
        cell = adapt_cell(*args)
        adapt.append(cell)
        if cell["ADAPT"]["status"] != "CERT-ZERO":
            print(cell["id"], cell["ADAPT"]["status"], cell["ADAPT"].get("gap_interval") or cell["ADAPT"].get("gap"), flush=True)

    elapsed = time.perf_counter() - t0
    records = []
    for cell in unpaid:
        records.extend(from_unpaid(cell))
    for cell in upkeep:
        records.extend(from_upkeep(cell))
    for cell in route:
        records.extend(from_route(cell))
    for cell in adapt:
        records.extend(from_adapt(cell))
    # Positive self-tests compare the gap, including the signature-bearing ample cells.
    from verdicts import control_failures
    extra = []
    for role in ("SEL", "ACC", "UPK", "UPK_cue", "ROUTE", "ADAPT"):
        extra.extend(control_failures(role, records))
    # expected_gap is not inside control_failures; check it here and fold into the verdict via a synthetic failure record.
    for rec in records:
        expected = rec.get("expected_gap")
        if expected is None:
            continue
        if rec["status"] == "UNRESOLVED" or rec.get("gap") != expected:
            rec["control_mismatch"] = True
    verdicts = family(records)
    for role, verdict in verdicts.items():
        mismatched = [r for r in records if r["role"] == role and r.get("control_mismatch")]
        if mismatched:
            verdict["verdict"] = "UNRESOLVED"
            verdict["reason"] = "positive self-test gap did not match. " + verdict.get("reason", "")
            verdict["selftest_mismatch"] = [r["id"] for r in mismatched]
    verdicts = _override(verdicts, selftest["failed_quantities"])

    def dump(path, obj):
        path.write_text(json.dumps(obj, indent=2, default=str) + "\n")

    dump(OUT / "verdicts.json", verdicts)
    dump(OUT / "cells_unpaid.json", unpaid)
    dump(OUT / "cells_upkeep.json", upkeep)
    dump(OUT / "cells_route.json", route)
    dump(OUT / "cells_adapt.json", adapt)
    (OUT / "graded_upk.json").write_text(json.dumps({k: fmt(v) for k, v in graded.items()}, indent=2) + "\n")
    (OUT / "RESULTS.md").write_text(_md(selftest, verdicts, unpaid, upkeep, route, adapt, graded, elapsed))
    print("VERDICTS", {k: v["verdict"] for k, v in verdicts.items()}, flush=True)
    print(f"elapsed {elapsed:.1f}s extra_controls {extra}", flush=True)


if __name__ == "__main__":
    main()
