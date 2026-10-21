"""Protocol self-tests. A failure marks that quantity UNRESOLVED. Nothing is retuned."""

from __future__ import annotations

from fractions import Fraction

from adapt import zero_adapt_report
from common import fmt
from route import route_cell
from unpaid import evaluate_unpaid_cell
from upkeep import (
    graded_ample_upk,
    phase_counts_bup1,
    phase_counts_displayed_bup2,
    phase_counts_fixed,
    upkeep_cell,
    withdrawal_cued,
    withdrawal_fixed_field,
)

# K=3 v=1/3 gaps follow the protocol's list order, which is r = 5/8 then r = 3/4.
REPLAY = [
    (1, Fraction(1, 3), Fraction(5, 8), "0"),
    (1, Fraction(1, 3), Fraction(3, 4), "0"),
    (1, Fraction(3, 4), Fraction(5, 8), "0"),
    (1, Fraction(3, 4), Fraction(3, 4), "0"),
    (2, Fraction(1, 3), Fraction(5, 8), "0"),
    (2, Fraction(1, 3), Fraction(3, 4), "0"),
    (2, Fraction(3, 4), Fraction(5, 8), "0"),
    (2, Fraction(3, 4), Fraction(3, 4), "0"),
    (3, Fraction(1, 3), Fraction(5, 8), "1/48"),
    (3, Fraction(1, 3), Fraction(3, 4), "1/24"),
    (3, Fraction(3, 4), Fraction(3, 4), "1/192"),
    (6, Fraction(1, 3), Fraction(5, 8), "1/48"),
    (6, Fraction(1, 3), Fraction(3, 4), "1/24"),
]

ACC_SUFF = [
    ("clean", None, Fraction(3, 4), Fraction(3, 4), 8, "0"),
    ("graded", Fraction(3, 4), Fraction(3, 4), Fraction(3, 4), 27, "3/32"),
    ("graded", Fraction(3, 4), Fraction(5, 8), Fraction(3, 4), 27, "3/64"),
    ("graded", Fraction(5, 6), Fraction(3, 4), Fraction(3, 4), 27, "5/72"),
    ("graded", Fraction(5, 6), Fraction(5, 8), Fraction(3, 4), 27, "5/144"),
    ("graded", Fraction(3, 5), Fraction(3, 4), Fraction(3, 4), 1, "0"),
]


def _explicit_withdrawals():
    """Sum the §8 event over the 24 (item, cue) states, equal weight 1/24."""
    delta, v, r = Fraction(1, 2), Fraction(3, 4), Fraction(3, 4)
    cued = Fraction(0)
    fixed = Fraction(0)
    for _x in range(8):
        for c in range(3):
            # Cued field is durable and correct. Queried with probability v.
            cued += Fraction(1, 24) * (-delta * v * (1 - r))
            if c == 0:
                fixed += Fraction(1, 24) * (-delta * v * (1 - r))
    return cued, fixed


def run_selftests():
    checks = []

    def add(name, quantity, ok, detail):
        checks.append({"name": name, "quantity": quantity, "ok": bool(ok), "detail": detail})

    i2, q2 = phase_counts_displayed_bup2()
    i1, q1 = phase_counts_bup1()
    add("K_suff=16 counts", "UPK", (i2, q2) == (16, 16), f"I,Q={i2, q2}")
    add("K_suff=26 counts", "UPK", (i1, q1) == (24, 26), f"I,Q={i1, q1}")
    fixed_q = phase_counts_fixed(1)[1]
    add("fixed B_up=1 Q", "UPK", fixed_q == 18, f"Q={fixed_q}")

    cell = upkeep_cell(1, Fraction(1, 2), Fraction(3, 4), Fraction(3, 4), 26, True)
    add(
        "UPK B_up=1 ample",
        "UPK",
        cell["quantities"]["UPK"]["gap"] == "5/96"
        and cell["V_full"] == "31/32"
        and cell["quantities"]["UPK_cue"]["gap"] == "5/96"
        and cell["quantities"]["UPK"]["signature"] == "ROBUST",
        cell["quantities"]["UPK"]["gap"],
    )
    cell = upkeep_cell(2, Fraction(1, 2), Fraction(3, 4), Fraction(3, 4), 16, True)
    add(
        "UPK B_up=2 ample",
        "UPK",
        cell["quantities"]["UPK"]["gap"] == "5/192"
        and cell["quantities"]["UPK_cue"]["gap"] == "5/192"
        and cell["quantities"]["UPK"]["signature"] == "ROBUST",
        f"gap={cell['quantities']['UPK']['gap']} n={cell['quantities']['UPK'].get('n_optima')}",
    )
    cued_f = withdrawal_cued(Fraction(1, 2), Fraction(3, 4), Fraction(3, 4))
    fixed_f = withdrawal_fixed_field(Fraction(1, 2), Fraction(3, 4), Fraction(3, 4))
    cued_s, fixed_s = _explicit_withdrawals()
    add("withdrawal -3/32", "UPK", cued_f == cued_s == Fraction(-3, 32), fmt(cued_s))
    add("withdrawal -1/32", "UPK", fixed_f == fixed_s == Fraction(-1, 32), fmt(fixed_s))

    graded = graded_ample_upk()
    add(
        "graded UPK 33/4096",
        "UPK",
        graded["UPK"] == Fraction(33, 4096) and graded["UPK_cue"] == 0 and graded["UPK_ev"] == Fraction(33, 4096),
        fmt(graded["UPK"]),
    )
    z4 = upkeep_cell(1, Fraction(1, 2), Fraction(1, 3), Fraction(3, 4), 18, True)
    add("UPK-Z4", "UPK", z4["quantities"]["UPK"]["gap"] == "0" and z4["quantities"]["UPK_cue"]["gap"] == "0", z4["quantities"]["UPK"]["status"])
    c0 = upkeep_cell(1, Fraction(1, 2), Fraction(1, 3), Fraction(3, 4), 2, True)
    add("UPK-C0 below K_suff", "UPK", c0["quantities"]["UPK_cue"]["status"] == "CERT-ZERO" and c0["quantities"]["UPK_cue"]["gap"] == "0", c0["quantities"]["UPK"]["status"])

    report = zero_adapt_report()
    b1 = report["B1"]
    add(
        "zero-ADAPT values",
        "ADAPT",
        b1["values_match"] and b1["known_slice"] == Fraction(31, 32) and b1["iid_slice"] == Fraction(119, 128),
        f"known={b1['known_slice']} iid={b1['iid_slice']} hist={b1['iid_history']}",
    )
    add(
        "zero-ADAPT capacity",
        "ADAPT",
        b1["capacity_nonincrease"] and b1["collapsed_counts"] == (1, 24, 26),
        str(b1["collapsed_counts"]),
    )
    add("B_up=2 matches omni", "ADAPT", report["B2"]["equal"] and report["B2"]["omni"] == Fraction(63, 64), fmt(report["B2"]["omni"]))

    for k, v, r, expected in REPLAY:
        rec = evaluate_unpaid_cell("clean", None, v, r, k, time_ms=240000)
        gap = rec["ACC"]["gap"]
        flip = rec["ACC"].get("positive_applicable_flip")
        add(f"replay ACC K={k} v={v} r={r}", "ACC", gap == expected and not flip, f"gap={gap} sig={rec['ACC'].get('signature')}")
        if v == Fraction(1, 3):
            add(f"SEL-Z K={k} r={r}", "SEL", rec["SEL"]["gap"] == "0", rec["SEL"]["gap"])

    for kind, a, r, v, k, expected in ACC_SUFF:
        rec = evaluate_unpaid_cell(kind, a, v, r, k, time_ms=240000)
        add(f"ACC_suff {kind} a={a} r={r}", "ACC", rec["ACC"]["gap"] == expected, rec["ACC"]["gap"])

    k1 = evaluate_unpaid_cell("clean", None, Fraction(3, 4), Fraction(3, 4), 1)
    add("K=1 degenerate", "SEL", k1["SEL"]["status"] == "DEGENERATE" and k1["ACC"]["status"] == "DEGENERATE", k1["SEL"]["status"])

    null = evaluate_unpaid_cell("graded", Fraction(3, 5), Fraction(3, 4), Fraction(3, 4), 4)
    add("NULL", "SEL", null["SEL"]["gap"] == "0" and null["ACC"]["gap"] == "0", f"SEL={null['SEL']['gap']} ACC={null['ACC']['gap']}")

    for L, v, expected_gap in ((1, Fraction(3, 4), "0"), (2, Fraction(1, 3), "0"), (8, Fraction(3, 4), "0")):
        cell = route_cell("clean", None, v, Fraction(3, 4), L)
        add(f"ROUTE control L={L} v={v}", "ROUTE", cell["ROUTE"]["gap"] == expected_gap, cell["ROUTE"]["gap"])
    # The §5.6 construction is a lower bound of 7/8, not a claimed gap.
    posed = route_cell("clean", None, Fraction(3, 4), Fraction(3, 4), 2)
    full = posed["classes"]["full_route"]["value"]
    add("ROUTE L=2 lower bound", "ROUTE", Fraction(full) >= Fraction(7, 8), full)

    failed = sorted({c["quantity"] for c in checks if not c["ok"]})
    return {"checks": checks, "failed_quantities": failed, "n_pass": sum(1 for c in checks if c["ok"]), "n_fail": sum(1 for c in checks if not c["ok"])}
