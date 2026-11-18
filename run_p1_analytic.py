"""P1 analytic stage: exact optimum of the abstain task with evidence over G1's 36-point grid.

    python run_p1_analytic.py      # writes p1_selfeval_analytic/results.json and REPORT.md

Design computation for the P1 card (ACI_METHODOLOGY_REVIEW_v1.md §5); see P1_SELFEVAL_DESIGN_v1.md.
Simulated variables only; no operator-stop variable exists.
"""
import json
import os
from fractions import Fraction as Fr
from itertools import product
from statistics import median

from grounding.model import Params
from grounding.selfeval import ARMS, DRAIN, F_HI, F_LO, analyse

GRID = dict(kappa=[Fr(1, 200), Fr(1, 50), Fr(1, 20), Fr(1, 8)], p_food=[Fr(1, 4), Fr(1, 2), Fr(3, 4)],
            p_decay=[Fr(1, 4), Fr(1, 2), Fr(3, 4)])
REFERENCE = dict(kappa=Fr(1, 50), p_food=Fr(1, 2), p_decay=Fr(1, 2))
CLAIMS = {
    "U1": "HOST and PAID: the drain intervention never changes abstention, and the body is worth 0 to the report",
    "U2": "FATE: the drain intervention never lowers abstention",
    "R1": "FATE: the drain intervention raises abstention, and every added abstention is a mistake (the register was fine)",
    "R2": "FATE: the body history is worth something to the report decision beyond the evidence",
    "R3a": "FATE: unclear evidence raises abstention (the evidence route exists alongside the body route)",
    "R3b": "HOST and PAID: unclear evidence raises abstention (only possible where their constant reliability lies between 0.6 and 0.6/F_LO)",
}


def check(r):
    F, H, P = r["FATE"], r["HOST"], r["PAID"]
    return {"U1": all(x["drain_effect"] == 0 and x["value_of_body_for_report"] == 0 for x in (H, P)),
            "U2": F["drain_effect"] >= 0,
            "R1": F["drain_effect"] > 0 and F["wrong_abstain_drain"] == F["drain_effect"],
            "R2": F["value_of_body_for_report"] > 0,
            "R3a": F["evidence_effect"] > 0,
            "R3b": H["evidence_effect"] > 0 and P["evidence_effect"] > 0,
            "value_check": all(r[a]["optimum"] == r[a]["value_check"] for a in ARMS)}


def main():
    pts = []
    for k, f, d in product(GRID["kappa"], GRID["p_food"], GRID["p_decay"]):
        r = analyse(Params(kappa=k, p_food=f, p_decay=d))
        pts.append({"point": {"kappa": str(k), "p_food": str(f), "p_decay": str(d)}, "checks": check(r),
                    "result": {a: {kk: str(v) for kk, v in r[a].items()} for a in ARMS} | {"eta_matched": str(r["eta_matched"])},
                    "float": {a: {kk: float(v) for kk, v in r[a].items()} for a in ARMS}})
    cov = {c: sum(p["checks"][c] for p in pts) for c in [*CLAIMS, "value_check"]}
    ref = next(p for p in pts if p["point"] == {k: str(v) for k, v in REFERENCE.items()})
    rel = lambda p: p["float"]["FATE"]["value_of_body_for_report"] / p["float"]["FATE"]["optimum"]
    summary = {"coverage": cov, "n_points": len(pts),
               "FATE_drain_effect_median": median(p["float"]["FATE"]["drain_effect"] for p in pts),
               "FATE_drain_effect_range": [min(p["float"]["FATE"]["drain_effect"] for p in pts),
                                           max(p["float"]["FATE"]["drain_effect"] for p in pts)],
               "FATE_value_of_body_share_median": median(rel(p) for p in pts if p["float"]["FATE"]["optimum"] > 0),
               "FATE_abstain_median": median(p["float"]["FATE"]["abstain"] for p in pts),
               "FATE_forage_rate_median": median(p["float"]["FATE"]["forage_rate"] for p in pts)}
    os.makedirs("p1_selfeval_analytic", exist_ok=True)
    with open("p1_selfeval_analytic/results.json", "w") as fh:
        json.dump({"grid": {k: [str(x) for x in v] for k, v in GRID.items()}, "constants": {"F_HI": str(F_HI), "F_LO": str(F_LO), "DRAIN": DRAIN},
                   "claims": CLAIMS, "summary": summary, "reference": ref, "points": pts}, fh, indent=1)
    L = ["# P1 analytic stage: body as the referent of self-evaluation (exact)", "",
         f"{len(pts)} grid points (G1's grid). Evidence F_HI = {F_HI}, F_LO = {F_LO}; drain = {DRAIN} body levels.", "",
         "| Claim | Holds at |", "| --- | --- |"]
    L += [f"| {c}: {t} | {cov[c]}/{len(pts)} |" for c, t in CLAIMS.items()]
    L += [f"| exact value check (forward pass equals the optimum) | {cov['value_check']}/{len(pts)} |", "",
          "Reference point (kappa 1/50, p_food 1/2, p_decay 1/2):", "",
          "| Arm | Optimum | Abstain | Drain effect | Mistaken abstentions under drain | Evidence effect | Body worth to report | Mean reliability | Forage rate |",
          "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for a in ARMS:
        x = ref["float"][a]
        L.append(f"| {a} | {x['optimum']:.3f} | {x['abstain']:.3f} | {x['drain_effect']:.3f} | {x['wrong_abstain_drain']:.3f} | "
                 f"{x['evidence_effect']:.3f} | {x['value_of_body_for_report']:.3f} | {x['reliability']:.3f} | {x['forage_rate']:.3f} |")
    L += ["", f"FATE over the grid: drain effect median {summary['FATE_drain_effect_median']:.3f} (range "
          f"{summary['FATE_drain_effect_range'][0]:.3f} to {summary['FATE_drain_effect_range'][1]:.3f}); body worth to the report "
          f"as a share of the optimum, median {summary['FATE_value_of_body_share_median']:.3f}; abstention median "
          f"{summary['FATE_abstain_median']:.3f}; forage rate median {summary['FATE_forage_rate_median']:.3f}.", ""]
    with open("p1_selfeval_analytic/REPORT.md", "w") as fh:
        fh.write("\n".join(L))
    print("\n".join(L))


if __name__ == "__main__":
    main()
