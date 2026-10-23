"""Family verdicts. Precedence is REJECT-ABSENT, then REJECT-SIG, then REJECT-NARROW.

ACC keeps the §7.3 replay record: REJECT-NARROW, including when every positive
cell is SIG-UNDEFINED. That specific record overrides the general signature rule.
"""

from __future__ import annotations

ZERO_OK = {"CERT-ZERO", "DEGENERATE"}
QUALIFYING = {"ROBUST", "PERMITTED"}
SIG_FAIL = {"NONE", "SIG-UNDEFINED"}

# Cited v1 replay access gaps. The protocol lists the two v=1/3 values in the
# same order as r ∈ {5/8, 3/4}. K=3 at v=3/4, r=5/8 is not cited.
REPLAY_ACC = {
    (1, "1/3", "5/8"): "0",
    (1, "1/3", "3/4"): "0",
    (1, "3/4", "5/8"): "0",
    (1, "3/4", "3/4"): "0",
    (2, "1/3", "5/8"): "0",
    (2, "1/3", "3/4"): "0",
    (2, "3/4", "5/8"): "0",
    (2, "3/4", "3/4"): "0",
    (3, "1/3", "5/8"): "1/48",
    (3, "1/3", "3/4"): "1/24",
    (3, "3/4", "3/4"): "1/192",
    (6, "1/3", "5/8"): "1/48",
    (6, "1/3", "3/4"): "1/24",
}


def _matches_zero(rec) -> bool:
    return rec["status"] in ZERO_OK and rec.get("gap") in ("0", "0/1")


def control_failures(role: str, records: list[dict]) -> list[str]:
    """§6 controls. A violation or an unresolved control blocks ADMIT."""
    bad = []
    for rec in records:
        if rec["role"] != role:
            continue
        if rec.get("expected_gap") is not None:
            if rec["status"] == "UNRESOLVED" or rec.get("gap") != rec["expected_gap"]:
                bad.append(
                    f"{rec['id']}: {rec.get('control')} expected gap {rec['expected_gap']}, "
                    f"got {rec.get('gap')} ({rec['status']})"
                )
            continue
        kind = rec.get("control")
        if not kind:
            continue
        if rec["status"] == "UNRESOLVED":
            bad.append(f"{rec['id']}: control {kind} is UNRESOLVED")
        elif not _matches_zero(rec):
            bad.append(f"{rec['id']}: control {kind} gap {rec.get('gap')} status {rec['status']}")
    if role == "ACC":
        for rec in records:
            if rec["role"] != "ACC" or not rec.get("replay"):
                continue
            expected = rec["replay"]
            if rec["status"] == "UNRESOLVED" or rec.get("gap") != expected:
                bad.append(f"{rec['id']}: replay expected {expected}, got {rec.get('gap')} ({rec['status']})")
            if rec.get("positive_flip"):
                bad.append(f"{rec['id']}: applicable O-ACC flip with positive ΔV")
    return bad


def _bin_rows(records, role, bins):
    out = {}
    for name in bins:
        members = [r for r in records if r["role"] == role and r.get("bin") == name and r.get("decision", True)]
        out[name] = {
            "members": members,
            "positive": [r for r in members if r["status"] == "CERT-POS"],
            "qualifying": [
                r for r in members
                if r["status"] == "CERT-POS" and r.get("signature") in QUALIFYING
            ],
            "unresolved": [r for r in members if r["status"] == "UNRESOLVED" or r.get("signature") == "UNRESOLVED"],
        }
    return out


def _standard(role, records, bins):
    failures = control_failures(role, records)
    if failures:
        return {
            "verdict": "UNRESOLVED",
            "reason": "a §6 control failed or is unresolved",
            "controls": failures,
        }
    info = _bin_rows(records, role, bins)
    positives = [r for r in records if r["role"] == role and r.get("decision", True) and r["status"] == "CERT-POS"]
    decision = [r for r in records if r["role"] == role and r.get("decision", True)]
    unresolved_values = [r for r in decision if r["status"] == "UNRESOLVED"]
    if all(info[b]["qualifying"] for b in bins):
        return {
            "verdict": f"ADMIT({role})",
            "reason": "controls pass and each bin has a CERT-POS cell with a ROBUST or PERMITTED optimum",
            "controls": [],
            "bins": {b: _brief(info[b]) for b in bins},
        }
    # A bin with no qualifier can still be saved by an unresolved cell.
    open_bins = [b for b in bins if not info[b]["qualifying"] and info[b]["unresolved"]]
    if open_bins:
        return {
            "verdict": "UNRESOLVED",
            "reason": "unresolved cells could still qualify bins " + ", ".join(open_bins),
            "controls": [],
            "bins": {b: _brief(info[b]) for b in bins},
        }
    if not positives:
        return {
            "verdict": f"REJECT-ABSENT({role})",
            "reason": "no decision cell is CERT-POS",
            "controls": [],
            "bins": {b: _brief(info[b]) for b in bins},
        }
    sig_open = [r for r in positives if r.get("signature") == "UNRESOLVED"]
    resolved_fail = [r for r in positives if r.get("signature") in SIG_FAIL]
    if unresolved_values or sig_open:
        return {
            "verdict": "UNRESOLVED",
            "reason": "positive or in-bin cells are not fully certified",
            "controls": [],
            "bins": {b: _brief(info[b]) for b in bins},
        }
    if positives and len(resolved_fail) == len(positives):
        return {
            "verdict": f"REJECT-SIG({role})",
            "reason": "every CERT-POS cell is NONE or SIG-UNDEFINED and every decision value is resolved",
            "controls": [],
            "bins": {b: _brief(info[b]) for b in bins},
        }
    # Some bin qualifies, every failing bin is resolved and does not.
    return {
        "verdict": f"REJECT-NARROW({role})",
        "reason": "CERT-POS is present but at least one declared bin has no qualifying cell",
        "controls": [],
        "bins": {b: _brief(info[b]) for b in bins},
    }


def _brief(info):
    return {
        "n": len(info["members"]),
        "n_pos": len(info["positive"]),
        "n_qualifying": len(info["qualifying"]),
        "n_unresolved": len(info["unresolved"]),
    }


def verdict_acc(records):
    """§7.3 preservation. Replay REJECT-NARROW stands once the cited gaps match."""
    base = _standard("ACC", records, ["(0,1/4]", "(1/4,1/2]", "(1/2,1)"])
    failures = control_failures("ACC", records)
    if failures:
        base["preserved_7_3"] = False
        return base
    info = _bin_rows(records, "ACC", ["(0,1/4]", "(1/4,1/2]", "(1/2,1)"])
    first_clear = not info["(0,1/4]"]["positive"] and not info["(0,1/4]"]["unresolved"]
    later_positive = bool(info["(1/4,1/2]"]["positive"] or info["(1/2,1)"]["positive"])
    if first_clear and later_positive:
        return {
            "verdict": "REJECT-NARROW(ACC)",
            "reason": (
                "§7.3 replay record: the first storage bin is only K=1 and K=2, both zero, "
                "while a later bin is CERT-POS. Preserved even where the positive cells are "
                "SIG-UNDEFINED, which the general signature rule would call REJECT-SIG."
            ),
            "controls": [],
            "bins": {b: _brief(info[b]) for b in info},
            "preserved_7_3": True,
            "standard_rule_would_say": base["verdict"],
        }
    base["preserved_7_3"] = False
    return base


def verdict_adapt(records):
    rows = [r for r in records if r["role"] == "ADAPT" and r.get("decision", True)]
    failures = control_failures("ADAPT", rows)
    experimental = [r for r in rows if r.get("experimental")]
    if failures:
        verdict = "UNRESOLVED"
        reason = "a §6 ADAPT control failed or is unresolved"
    else:
        verdict = "VALUE-ONLY"
        reason = (
            "ADAPT has no response property and no admission bins. "
            "Controls are CERT-ZERO. Experimental cells are reported individually."
        )
    return {
        "verdict": verdict,
        "reason": reason,
        "controls": failures,
        "experimental": [
            {"id": r["id"], "status": r["status"], "gap": r.get("gap"), "interval": r.get("gap_interval")}
            for r in experimental
        ],
    }


def family(records):
    bins_k = ["(0,1/4]", "(1/4,1/2]", "(1/2,1)"]
    return {
        "SEL": _standard("SEL", records, bins_k),
        "ACC": verdict_acc(records),
        "UPK": _standard("UPK", records, ["1", "2"]),
        "UPK_cue": _standard("UPK_cue", records, ["1", "2"]),
        "ROUTE": _standard("ROUTE", records, ["2", "3"]),
        "ADAPT": verdict_adapt(records),
    }
