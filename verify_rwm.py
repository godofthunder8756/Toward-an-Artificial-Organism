"""Run the RWM pre-scale verification gate (RWM-PSG v1) and write its outputs.

    python verify_rwm.py --out rwm_gate_v1

Exact enumeration on small discrete systems; no training, no learner, no
network access. Refuses to overwrite an existing results.json.
"""
import argparse
import hashlib
import json
import os
import platform
import sys
import time

import numpy as np

from rwm.gate import integration_profile, run_gate, structural_checks
from rwm.neural import RWMConfig, RWMNet, macro_skeleton, rollout

SOURCES = ["rwm/__init__.py", "rwm/primitives.py", "rwm/integration.py", "rwm/topology.py",
           "rwm/world.py", "rwm/gate.py", "rwm/neural.py", "verify_rwm.py"]


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def fmt(x, nd=4):
    return f"{x:.{nd}f}" if isinstance(x, float) else str(x)


def report(res):
    t = res["tests"]
    lines = ["# RWM pre-scale verification gate: results (ENGINEERING)", "",
             f"Protocol {res['protocol']}. Verdict: **{res['verdict']}**."
             + (f" Failed: {', '.join(res['failed'])}." if res["failed"] else ""), "",
             "A verdict here authorizes no training. See RWM_DESIGN_v1.md sections 8 to 10.", "",
             "## Gate tests on RWM-8", "", "| Test | Pass |", "| --- | --- |"]
    lines += [f"| {k} | {'yes' if v else 'NO'} |" for k, v in t.items()]
    lines += ["", "## Designs and matched rivals", "",
              "| Design | bits | T1 SCC | T2 bottleneck | T3 broadcast | T4 monitor | Phi_s>0 mass | core-complex mass | monitor-only complex mass | CD interv. (w) | CD closed loop (w) | mean lifetime |",
              "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for name, d in res["designs"].items():
        s, i = d["structure"], d["integration"]
        yn = lambda b: "yes" if b else "no"
        lines.append(
            f"| {name} | {len(d['description'])} | {yn(s['T1_single_scc'])} | {yn(s['T2_bottleneck'])} | "
            f"{yn(s['T3_broadcast'])} | {yn(s['T4_monitor_higher_order'])} | {fmt(i['mass_phi_positive'])} | "
            f"{fmt(i['mass_core_complex'])} | {fmt(i['mass_monitor_only_complex'])} | "
            f"{fmt(i['causal_density_interventional']['cd_weighted'])} | "
            f"{fmt(i['causal_density_closed_loop']['cd_weighted'])} | "
            f"{fmt(i['closed_loop']['mean_lifetime_steps'], 2)} |")
    main = res["designs"]["RWM-8"]["integration"]
    reasons = {}
    for r in main["states"]:
        key = f"{r['reason']} @ {r['mip'][0] if r.get('mip') else '-'}"
        reasons[key] = reasons.get(key, 0.0) + r["mass"]
    lines += ["", "## Why RWM-8 fails T6/T7", "",
              "Stationary mass by Phi_s outcome and the cut side A of the minimum-information partition:", "",
              "| Outcome | mass |", "| --- | --- |"]
    lines += [f"| {k} | {fmt(v)} |" for k, v in sorted(reasons.items(), key=lambda kv: -kv[1])]
    lines += ["", f"Workspace/first-order edges with zero closed-loop CMI: {', '.join(main['edges_inactive_in_closed_loop']) or 'none'}.",
              "", "## Instrument validation", ""]
    lines += [f"- {k}: {fmt(v)}" for k, v in res["instruments"].items()]
    o = res["objective"]
    lines += ["", "## Objective admission (exact rationals, all 2^10 memoryless policies)", "",
              "| Objective | optimal discounted cost | expected lifetime of every optimal policy |",
              "| --- | --- | --- |"]
    for k in ("extero_only", "extero_plus_intero", "intero_only"):
        lines.append(f"| {k} | {o[k]['optimal_value']} | {', '.join(o[k]['optimal_lifetimes'])} |")
    lines += ["", f"Dark-room lifetime {o['dark_room_lifetime']}; best lifetime over all policies {o['max_lifetime_any_policy']}.",
              "", "## Untrained neural reference (seed 0)", ""]
    n = res["neural_init"]
    lines += [f"- population edges equal discrete effective edges: {n['edges_match_discrete']}",
              f"- macro-skeleton structure: " + ", ".join(f"{k}={v}" for k, v in n["macro_structure"].items() if k.startswith("T")),
              f"- macro-skeleton Phi_s>0 stationary mass: {fmt(n['macro_mass_phi_positive'])}",
              f"- 5000-step rollout, no learning: " + ", ".join(f"{k}={fmt(v)}" for k, v in n["rollout"].items())]
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="rwm_gate_v1")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    path = os.path.join(args.out, "results.json")
    if os.path.exists(path):
        sys.exit(f"refusing to overwrite {path}")
    t0 = time.time()
    res = run_gate(with_complex=True)
    net = RWMNet(RWMConfig(seed=0))
    from rwm.topology import rwm8
    macro = macro_skeleton(net)
    mprof = integration_profile(macro, with_complex=False)
    res["neural_init"] = {
        "edges_match_discrete": sorted(net.population_edges()) == sorted(rwm8().effective_edges()),
        "macro_structure": structural_checks(macro),
        "macro_mass_phi_positive": mprof["mass_phi_positive"],
        "macro_lifetime": mprof["closed_loop"]["mean_lifetime_steps"],
        "rollout": rollout(net, 5000, np.random.default_rng(0)),
    }
    res["environment"] = {"python": platform.python_version(), "numpy": np.__version__,
                          "platform": platform.platform(), "seconds": round(time.time() - t0, 1)}
    res["source_sha256"] = {p: sha(p) for p in SOURCES}
    with open(path, "w") as fh:
        json.dump(res, fh, indent=1, default=float)
    with open(os.path.join(args.out, "REPORT.md"), "w") as fh:
        fh.write(report(res))
    print(f"verdict {res['verdict']}; failed {res['failed']}; wrote {args.out}")


if __name__ == "__main__":
    main()
