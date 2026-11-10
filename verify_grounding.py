"""Grounding analysis G1: run the frozen protocol once and score its claims.

    python verify_grounding.py --config frozen --out grounding_v1
    python verify_grounding.py --config dev --out <scratch dir>     # code check only

Exact rational arithmetic; no learner, no sampling. Refuses to overwrite.
The grid, the claims and their classes (UNIVERSAL / REGION) are those of
GROUNDING_PROTOCOL_v1.md; coverage over the whole grid is the result.
"""
import argparse
import hashlib
import json
import os
import platform
import sys
import time
from dataclasses import replace
from fractions import Fraction as Fr
from itertools import product
from multiprocessing import Pool

from grounding.model import (Params, Solution, all_states, blind_optimum, never_forage,
                             objectives, scrambled, summarize)

SIZES = {"frozen": dict(E=4, d=4, N=4, eta_flat=Fr(1, 4)),
         "dev": dict(E=2, d=2, N=2, eta_flat=Fr(1, 4))}
GRIDS = {
    "frozen": dict(kappa=[Fr(1, 200), Fr(1, 50), Fr(1, 20), Fr(1, 8)],
                   p_food=[Fr(1, 4), Fr(1, 2), Fr(3, 4)],
                   p_decay=[Fr(1, 4), Fr(1, 2), Fr(3, 4)]),
    "dev": dict(kappa=[Fr(1, 200), Fr(1, 8)], p_food=[Fr(1, 2)], p_decay=[Fr(1, 2)]),
}
REFERENCE = dict(kappa=Fr(1, 50), p_food=Fr(1, 2), p_decay=Fr(1, 2))
VOI_TRIALS = 2
SHIFTS = [Fr(-1), Fr(0), Fr(1)]
TASKS = ["T1_gain", "T2_penalty", "T3_signed", "T4_anti", "T5_memfree", "T6_abstain"]
MEMORY_TASKS = ["T1_gain", "T2_penalty", "T3_signed", "T4_anti", "T6_abstain"]
AFFINE_TASKS = ["T1_gain", "T2_penalty", "T3_signed", "T4_anti"]
CELLS = {"F0D0": (False, False), "F1D0": (True, False), "F0D1": (False, True), "F1D1": (True, True)}
SOURCES = ["grounding/__init__.py", "grounding/model.py", "verify_grounding.py",
           "test_grounding.py", "GROUNDING_PROTOCOL_v1.md"]
UNIVERSAL = ["U1_no_stakes_no_regulation", "U2_shift_invariance_without_death",
             "U3_value_monotone_in_body", "U4_no_value_of_interoception_without_stakes",
             "U5_nonpositive_stream_no_maintenance", "U6_external_scramble_leaves_machinery",
             "U7_exact_equivalences"]
REGION = ["R1_derived_regulation", "R2_termination_positive_side", "R3_value_of_interoception",
          "R4_scrambling_costs_the_system", "R5_regulation_transfers", "R6_reliability_referent",
          "R7_external_scramble_costs_evaluator"]


def fr(x):
    return {"exact": str(x), "float": float(x)}


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def run_point(args):
    config, kappa, p_food, p_decay = args
    base = Params(kappa=kappa, p_food=p_food, p_decay=p_decay, **SIZES[config])
    O = objectives()
    res = {"point": {"kappa": str(kappa), "p_food": str(p_food), "p_decay": str(p_decay)}}

    # A. regulation table ------------------------------------------------
    table = {}
    sols = {}
    for cell, (fate, death) in CELLS.items():
        for name, obj in O.items():
            for b in SHIFTS:
                sol = Solution(replace(base, fate=fate, death=death, shift=b), obj)
                sols[(cell, name, b)] = sol
                st = summarize(sol)
                table[f"{cell}|{name}|b={b}"] = {k: fr(v) for k, v in st.items()}
    res["regulation"] = table

    def forages(cell, name, b=Fr(0)):
        return summarize(sols[(cell, name, b)])["expected_forages"]

    # shift invariance of the optimal action table when death is off
    shift_inv = {}
    for cell in ("F0D0", "F1D0"):
        for name in O:
            ref = sols[(cell, name, Fr(0))]
            states = all_states(ref)
            shift_inv[f"{cell}|{name}"] = all(
                sols[(cell, name, b)].action(s) == ref.action(s) for b in SHIFTS for s in states)
    res["shift_invariance"] = shift_inv

    # B. monotonicity in the body variable (theorem check) -----------------
    mono = {}
    for cell in ("F0D0", "F1D0"):
        for name in TASKS:
            sol = sols[(cell, name, Fr(0))]
            keys = {(n, k, f) for (n, k, e, f) in all_states(sol)}
            nondecreasing, constant = True, True
            for (n, k, f) in keys:
                vals = [sol.value((n, k, e, f)) for e in range(base.E + 1)]
                nondecreasing &= all(a <= b for a, b in zip(vals, vals[1:]))
                constant &= len(set(vals)) == 1
            mono[f"{cell}|{name}"] = {"nondecreasing_in_e": nondecreasing, "constant_in_e": constant}
    res["monotonicity"] = mono

    # C. value of interoception ------------------------------------------
    voi = {}
    for cell in ("F0D0", "F1D0"):
        fate, death = CELLS[cell]
        for name in TASKS + ["H_homeo"]:
            p = replace(base, fate=fate, death=death, N=VOI_TRIALS)
            v_obs = Solution(p, O[name]).optimum()
            v_blind, seq = blind_optimum(p, O[name])
            voi[f"{cell}|{name}"] = {"observed": fr(v_obs), "blind": fr(v_blind),
                                     "voi": fr(v_obs - v_blind), "blind_plan": list(seq)}
    res["value_of_interoception"] = voi

    # D. scrambling (viability-relative semantic information) --------------
    scr = {}
    for cell, name in [("F1D0", "T1_gain"), ("F1D0", "T3_signed"), ("F1D0", "T6_abstain"),
                       ("F1D0", "H_homeo"), ("F0D0", "H_homeo"), ("F0D0", "T1_gain")]:
        sol = sols[(cell, name, Fr(0))]
        intact, sc = summarize(sol), scrambled(sol)
        scr[f"{cell}|{name}"] = {
            "intact_value": fr(intact["value"]), "scrambled_value": fr(sc["value"]),
            "intact_fidelity": fr(intact["mean_report_fidelity"]),
            "scrambled_fidelity": fr(sc["mean_report_fidelity"]),
            "intact_energy": fr(intact["mean_energy"]), "scrambled_energy": fr(sc["mean_energy"]),
            "value_loss": fr(intact["value"] - sc["value"]),
            "fidelity_loss": fr(intact["mean_report_fidelity"] - sc["mean_report_fidelity"]),
        }
    res["scrambling"] = scr

    # E. transfer of the regulation policy across objectives (F1D0) --------
    transfer = {}
    for src in MEMORY_TASKS + ["H_homeo"]:
        s_src = sols[("F1D0", src, Fr(0))]
        for dst in MEMORY_TASKS:
            s_dst = sols[("F1D0", dst, Fr(0))]
            v_star = s_dst.optimum()
            v_never = summarize(s_dst, policy=never_forage)["value"]
            v_tr = summarize(s_src, eval_obj=O[dst])["value"]
            gap = v_star - v_never
            transfer[f"{src}->{dst}"] = {
                "optimal": fr(v_star), "never_forage": fr(v_never), "transferred": fr(v_tr),
                "regret_ratio": fr((v_star - v_tr) / gap) if gap else None}
    res["transfer"] = transfer

    # F. report options under the abstain objective -------------------------
    opts = {}
    for cell in ("F0D0", "F1D0"):
        sol = sols[(cell, "T6_abstain", Fr(0))]
        per_trial = {}
        dist = {sol.start}
        frontier = [sol.start]
        while frontier:
            s = frontier.pop()
            n, k, e, f = s
            for pr, nxt, _ in sol.successors(n, k, e, f, sol.action(s)):
                if k + 1 == base.d:
                    f2 = f * (1 - sol.p.eta(e))
                    per_trial.setdefault(n, set()).add(sol.obj.report((1 + f2) / 2)[1])
                if nxt is not None and nxt not in dist:
                    dist.add(nxt)
                    frontier.append(nxt)
        opts[cell] = {str(n): sorted(v) for n, v in sorted(per_trial.items())}
    res["abstain_options"] = opts

    # claims ---------------------------------------------------------------
    def rr(src, dst):
        r = transfer[f"{src}->{dst}"]["regret_ratio"]
        return None if r is None else Fr(r["exact"])

    C = {}
    C["U1_no_stakes_no_regulation"] = all(forages("F0D0", t, b) == 0 for t in TASKS for b in SHIFTS)
    C["U2_shift_invariance_without_death"] = all(shift_inv.values())
    C["U3_value_monotone_in_body"] = (
        all(mono[f"F1D0|{t}"]["nondecreasing_in_e"] for t in TASKS) and
        all(mono[f"F0D0|{t}"]["constant_in_e"] for t in TASKS))
    C["U4_no_value_of_interoception_without_stakes"] = all(
        Fr(voi[f"F0D0|{t}"]["voi"]["exact"]) == 0 for t in TASKS)
    C["U5_nonpositive_stream_no_maintenance"] = (
        forages("F0D1", "T2_penalty", Fr(0)) == 0 and forages("F0D1", "T1_gain", Fr(-1)) == 0)
    C["U6_external_scramble_leaves_machinery"] = Fr(scr["F0D0|H_homeo"]["fidelity_loss"]["exact"]) == 0
    C["U7_exact_equivalences"] = (
        rr("T1_gain", "T2_penalty") in (None, Fr(0)) and rr("T3_signed", "T4_anti") in (None, Fr(0)) and
        forages("F1D0", "T5_memfree") == 0)
    C["R1_derived_regulation"] = all(forages("F1D0", t) > 0 for t in MEMORY_TASKS)
    C["R2_termination_positive_side"] = (
        forages("F0D1", "T1_gain", Fr(0)) > 0 and forages("F0D1", "T5_memfree", Fr(1)) > 0)
    C["R3_value_of_interoception"] = all(Fr(voi[f"F1D0|{t}"]["voi"]["exact"]) > 0 for t in AFFINE_TASKS)
    a = scr["F1D0|T1_gain"]
    C["R4_scrambling_costs_the_system"] = (
        Fr(a["value_loss"]["exact"]) > 0 and Fr(a["fidelity_loss"]["exact"]) > 0)
    pairs = [rr(x, y) for x in AFFINE_TASKS for y in AFFINE_TASKS]
    C["R5_regulation_transfers"] = all(r is not None and r <= Fr(1, 4) for r in pairs)
    C["R6_reliability_referent"] = (
        any(len(v) == 2 for v in opts["F1D0"].values()) and
        len({o for v in opts["F0D0"].values() for o in v}) == 1)
    C["R7_external_scramble_costs_evaluator"] = Fr(scr["F0D0|H_homeo"]["value_loss"]["exact"]) > 0
    res["claims"] = C
    res["derived"] = {
        "forages_F1D0_T1": fr(forages("F1D0", "T1_gain")),
        "forages_F0D0_H": fr(forages("F0D0", "H_homeo")),
        "voi_F1D0_T6": voi["F1D0|T6_abstain"]["voi"],
    }
    return res


def run(config):
    grid = GRIDS[config]
    points = [(config, k, f, d) for k, f, d in product(grid["kappa"], grid["p_food"], grid["p_decay"])]
    with Pool(min(len(points), os.cpu_count() or 1)) as pool:
        results = pool.map(run_point, points)
    cov = {c: {"holds": sum(r["claims"][c] for r in results), "of": len(results),
               "fails_at": [r["point"] for r in results if not r["claims"][c]]}
           for c in UNIVERSAL + REGION}
    ref = next((r for r in results if all(
        r["point"][k] == str(v) for k, v in REFERENCE.items())), results[0])
    return {"config": config, "sizes": {k: str(v) for k, v in SIZES[config].items()},
            "grid": {k: [str(x) for x in v] for k, v in grid.items()},
            "voi_trials": VOI_TRIALS, "shifts": [str(b) for b in SHIFTS],
            "coverage": cov,
            "all_universal_hold": all(cov[c]["holds"] == cov[c]["of"] for c in UNIVERSAL),
            "reference_point": ref["point"], "reference": ref, "points": results}


def report(res):
    cov = res["coverage"]
    L = ["# Grounding analysis G1: results", "",
         f"Config `{res['config']}`, {cov[UNIVERSAL[0]]['of']} grid points. "
         f"All UNIVERSAL claims hold at every point: **{res['all_universal_hold']}**.", "",
         "## Coverage", "", "| Claim | class | holds at |", "| --- | --- | --- |"]
    L += [f"| {c} | UNIVERSAL | {cov[c]['holds']} / {cov[c]['of']} |" for c in UNIVERSAL]
    L += [f"| {c} | REGION | {cov[c]['holds']} / {cov[c]['of']} |" for c in REGION]
    L += ["", "## REGION claims by grid point", "",
          "| kappa | p_food | p_decay | " + " | ".join(c.split("_")[0] for c in REGION) +
          " | forages F1D0,T1 | forages F0D0,H |",
          "| --- | --- | --- | " + " | ".join("---" for _ in REGION) + " | --- | --- |"]
    for r in res["points"]:
        pt = r["point"]
        L.append(f"| {pt['kappa']} | {pt['p_food']} | {pt['p_decay']} | " +
                 " | ".join("y" if r["claims"][c] else "." for c in REGION) +
                 f" | {r['derived']['forages_F1D0_T1']['float']:.2f} | {r['derived']['forages_F0D0_H']['float']:.2f} |")
    ref = res["reference"]
    reg = ref["regulation"]
    L += ["", f"## Reference point {ref['point']}", "",
          "### Expected forage actions under the optimal policy", ""]
    names = sorted({k.split("|")[1] for k in reg})
    for b in ("0", "-1", "1"):
        L += [f"Shift b = {b}:", "", "| Objective | F0D0 | F1D0 | F0D1 | F1D1 |", "| --- | --- | --- | --- | --- |"]
        for n in names:
            L.append(f"| {n} | " + " | ".join(
                f"{reg[f'{c}|{n}|b={b}']['expected_forages']['float']:.3f}" for c in CELLS) + " |")
        L.append("")
    L += ["### Fidelity, energy, survival and value under the optimum (b = 0)", "",
          "| Objective | cell | fidelity | energy | survival | value |", "| --- | --- | --- | --- | --- | --- |"]
    for n in names:
        for c in CELLS:
            r = reg[f"{c}|{n}|b=0"]
            L.append(f"| {n} | {c} | {r['mean_report_fidelity']['float']:.4f} | {r['mean_energy']['float']:.3f} | "
                     f"{r['survival']['float']:.4f} | {r['value']['float']:.4f} |")
    L += ["", "### Value of interoception (hidden body vs observed body)", "",
          "| Cell, objective | observed | blind | VoI |", "| --- | --- | --- | --- |"]
    for k, v in ref["value_of_interoception"].items():
        L.append(f"| {k} | {v['observed']['float']:.5f} | {v['blind']['float']:.5f} | {v['voi']['float']:.5f} |")
    L += ["", "### Scrambling the body input of the optimal policy", "",
          "| Agent | value loss | fidelity loss | energy intact -> scrambled |", "| --- | --- | --- | --- |"]
    for k, v in ref["scrambling"].items():
        L.append(f"| {k} | {v['value_loss']['float']:.5f} | {v['fidelity_loss']['float']:.5f} | "
                 f"{v['intact_energy']['float']:.3f} -> {v['scrambled_energy']['float']:.3f} |")
    L += ["", "### Transfer of the regulation policy (F1D0): regret ratio", "",
          "| Source -> destination | regret ratio |", "| --- | --- |"]
    for k, v in ref["transfer"].items():
        rr = v["regret_ratio"]
        L.append(f"| {k} | {rr['float']:.4f} |" if rr else f"| {k} | n/a |")
    L += ["", "### Report options reached under T6_abstain", ""]
    L += [f"- {c}: {v}" for c, v in ref["abstain_options"].items()]
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", choices=sorted(SIZES), required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    path = os.path.join(args.out, "results.json")
    if os.path.exists(path):
        sys.exit(f"refusing to overwrite {path}")
    t0 = time.time()
    res = run(args.config)
    res["environment"] = {"python": platform.python_version(), "seconds": round(time.time() - t0, 1)}
    res["source_sha256"] = {p: sha(p) for p in SOURCES if os.path.exists(p)}
    with open(path, "w") as fh:
        json.dump(res, fh, indent=1)
    with open(os.path.join(args.out, "REPORT.md"), "w") as fh:
        fh.write(report(res))
    for c, v in res["coverage"].items():
        print(f"{c}: {v['holds']}/{v['of']}")
    print("all universal hold:", res["all_universal_hold"], "| seconds:", res["environment"]["seconds"])


if __name__ == "__main__":
    main()
