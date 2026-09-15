"""Driver for E3_OBSOLESCENCE_PROTOCOL_v1.md (E3-OB1).

    python -B e3_obsolescence_study.py select   # controls only; applies section 4
    python -B e3_obsolescence_study.py freeze   # records raw and LF-normalized hashes
    python -B e3_obsolescence_study.py final    # verifies the freeze, runs seeds 300-331, applies section 6

Every phase refuses to overwrite its outputs.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict, replace
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

import e3_obsolescence_world as ob

RESULTS = Path("e3_fep_seed_results/ob1")
AUDIT = RESULTS / "audit_ob1.json"
SELECTION = RESULTS / "selection_controls.json"
FINAL = RESULTS / "final_results.json"
FREEZE = Path("E3_OBSOLESCENCE_FREEZE_v1.json")

GRID = {"budget": (2, 3, 4), "corrupt_p": (0.015, 0.02, 0.025)}
ENGINEERING_SEEDS = tuple(range(8))
FINAL_SEEDS = tuple(range(300, 332))
MUA, SPEND_REDUCTION = 0.03, -0.10
BOOT_REPS, BOOT_SEED = 10000, 20260914
POPULATION_SEEDS, POPULATION_TICKS = (900, 901), 120000
FROZEN_FILES = ("E3_OBSOLESCENCE_PROTOCOL_v1.md", "e3_obsolescence_world.py", "audit_e3_obsolescence.py",
                "e3_obsolescence_study.py", AUDIT.as_posix(), SELECTION.as_posix())
SECONDARY = (("depth_flag", "depth_learned"), ("depth_learned", "depth_timeout_400"),
             ("depth_learned", "depth_timeout_2000"), ("learned_override_x0.25", "depth_learned"),
             ("learned_override_x4", "depth_learned"), ("depth_first", "uniform"), ("depth_first", "recency"))
DESCRIPTIVE = ("overall_accuracy", "post_return_accuracy", "last_third_accuracy", "obsolete_repair_share",
               "mistaken_abandonment_fraction", "lost_at_return_fraction", "long_return_lost_fraction",
               "correct_relinquishment_fraction", "false_abandonment_exposure", "binding_fraction",
               "repairs_per_tick", "learned_threshold_final", "realized_gap_q99")


def _json_default(o):
    return o.item() if hasattr(o, "item") else str(o)


def _write(path: Path, obj) -> None:
    if path.exists():
        sys.exit(f"refusing to overwrite {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=1, default=_json_default))


def _hashes(path: Path) -> dict:
    data = path.read_bytes()
    return {"bytes": len(data), "sha256_raw": hashlib.sha256(data).hexdigest(),
            "sha256_lf_normalized": hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()}


def _run_seed(args):
    w, seed, policies = args
    env = ob.generate_environment(seed, w)
    return [ob.run_one(p, seed, w, env=env) for p in policies]


def run_rows(w, seeds, policies, workers=7):
    with ProcessPoolExecutor(max_workers=workers) as pool:
        return [r for batch in pool.map(_run_seed, [(w, s, policies) for s in seeds]) for r in batch]


def _mean(rows, policy, key):
    vals = [r[key] for r in rows if r["policy"] == policy]
    return float(np.nanmean(vals)) if vals and not all(np.isnan(vals)) else float("nan")


def feasibility(rows, flag_gap_min, flag_min):
    m = {p: _mean(rows, p, "overall_accuracy") for p in ("none", "ample", "uniform", "depth_first", "depth_flag")}
    binding = _mean(rows, "depth_first", "binding_fraction")
    gap = m["depth_flag"] - m["depth_first"]
    checks = {"ample_feasible": m["ample"] >= 0.90, "maintenance_needed": m["none"] <= 0.65,
              "budget_binds": binding >= 0.50, "relinquishment_can_matter": gap >= flag_gap_min,
              "flag_viable": m["depth_flag"] >= flag_min}
    return {"overall_means": m, "depth_first_binding": binding, "flag_gap": gap, "checks": checks,
            "passes": all(checks.values())}


def select() -> None:
    if SELECTION.exists():
        sys.exit(f"refusing to overwrite {SELECTION}")
    evaluated = []
    for budget, p_flip in itertools.product(*GRID.values()):
        w = replace(ob.WorldParams(), budget=budget, corrupt_p=p_flip)
        f = feasibility(run_rows(w, ENGINEERING_SEEDS, ob.CONTROL_POLICIES), 0.05, 0.80)
        evaluated.append({"params": asdict(w), **f})
        print(f"budget {budget} p {p_flip}: passes={f['passes']} flag_gap={f['flag_gap']:+.3f} "
              f"means={ {k: round(v, 3) for k, v in f['overall_means'].items()} } binding={f['depth_first_binding']:.2f} "
              f"failed={[k for k, v in f['checks'].items() if not v]}", flush=True)
    passing = sorted((e for e in evaluated if e["passes"]),
                     key=lambda e: (-e["flag_gap"], -e["overall_means"]["depth_flag"]))
    selected = [e["params"] for e in passing[:2]]
    _write(SELECTION, {"rule": "E3_OBSOLESCENCE_PROTOCOL_v1.md section 4", "engineering_seeds": ENGINEERING_SEEDS,
                       "evaluated": evaluated, "selected": selected})
    print(f"selected: {[(s['budget'], s['corrupt_p']) for s in selected]}")


def freeze() -> None:
    if not json.loads(SELECTION.read_text())["selected"]:
        sys.exit("nothing selected; protocol stops before freeze")
    _write(FREEZE, {"kind": "local_exploratory_freeze", "external_preregistration": False,
                    "created_utc": datetime.now(timezone.utc).isoformat(), "protocol": FROZEN_FILES[0],
                    "verification_rule": "compare sha256 of file bytes with CRLF replaced by LF",
                    "final_seeds": FINAL_SEEDS, "files": {f: _hashes(Path(f)) for f in FROZEN_FILES}})
    print(f"wrote {FREEZE}")


def _paired(rows, a, b, metric, level):
    by = {(r["policy"], r["seed"]): r for r in rows}
    d = np.array([by[(a, s)][metric] - by[(b, s)][metric] for s in FINAL_SEEDS])
    d = d[~np.isnan(d)]
    means = d[np.random.default_rng(BOOT_SEED).integers(0, len(d), size=(BOOT_REPS, len(d)))].mean(axis=1)
    alpha = 1 - level
    lo, hi = np.quantile(means, [alpha / 2, 1 - alpha / 2])
    return {"mean": float(d.mean()), "interval": [float(lo), float(hi)], "level": level, "n": int(len(d)),
            "positive": int((d > 0).sum()), "negative": int((d < 0).sum()), "per_seed": d.tolist()}


def _population_gap_q99(w) -> float:
    gaps = []
    for seed in POPULATION_SEEDS:
        env = ob.generate_environment(seed, replace(w, ticks=POPULATION_TICKS, n_obsolete=0,
                                                   obsolete_start=1, obsolete_end=2))
        last = np.full(w.n_cues, -1)
        for t, q in enumerate(env.queries):
            if q >= 0:
                if last[q] >= 0:
                    gaps.append(t - last[q])
                last[q] = t
    return float(np.quantile(gaps, 0.99))


def final(workers: int) -> None:
    if FINAL.exists():
        sys.exit(f"refusing to overwrite {FINAL}")
    record = json.loads(FREEZE.read_text())
    bad = [f for f, h in record["files"].items() if _hashes(Path(f))["sha256_lf_normalized"] != h["sha256_lf_normalized"]]
    if bad:
        sys.exit(f"freeze verification failed: {bad}")
    selected = json.loads(SELECTION.read_text())["selected"]
    level = 1 - 0.05 / (2 * len(selected))
    reports = []
    for cfg in selected:
        w = ob.WorldParams(**cfg)
        rows = run_rows(w, FINAL_SEEDS, ob.POLICIES, workers)
        paired_env = all(len({r["env_digest"] for r in rows if r["seed"] == s}) == 1 for s in FINAL_SEEDS)
        f = feasibility(rows, 0.025, 0.75)
        valid = paired_env and f["passes"]
        a = _paired(rows, "depth_learned", "depth_first", "overall_accuracy", level)
        b = _paired(rows, "depth_learned", "depth_first", "obsolete_repair_share", level)
        if a["mean"] >= MUA and a["interval"][0] > 0 and b["mean"] <= SPEND_REDUCTION and b["interval"][1] < 0:
            decision = "demonstrated"
        elif a["interval"][1] < MUA or b["interval"][0] >= 0:
            decision = "not demonstrated"
        else:
            decision = "inconclusive"
        secondary = {}
        for x, y in SECONDARY:
            for metric in ("overall_accuracy", "obsolete_repair_share"):
                secondary[f"{x}-{y}:{metric}"] = _paired(rows, x, y, metric, 0.95)
        descriptive = {p: {k: _mean(rows, p, k) for k in DESCRIPTIVE} for p in ob.POLICIES}
        reports.append({"params": cfg, "environment_paired": paired_env, "feasibility": f, "valid": valid,
                        "primary": {"A_recall": a, "B_obsolete_repair_share": b, "decision": decision},
                        "secondary": secondary, "descriptive": descriptive,
                        "population_gap_q99_no_obsolescence": _population_gap_q99(w), "rows": rows})
    decisions = [r["primary"]["decision"] for r in reports if r["valid"]]
    status = ("uninterpretable" if not decisions else
              "supported in this world" if all(d == "demonstrated" for d in decisions) else
              "not supported in this world" if all(d == "not demonstrated" for d in decisions) else
              "mixed or inconclusive")
    _write(FINAL, {"protocol": FROZEN_FILES[0], "final_seeds": FINAL_SEEDS, "primary_level": level,
                   "freeze_sha256_lf_normalized": _hashes(FREEZE)["sha256_lf_normalized"],
                   "overall_status": status, "configs": reports})
    print(f"OVERALL STATUS: {status} (primary level {level:.4f})")
    for r in reports:
        p, pr = r["params"], r["primary"]
        print(f"\nbudget {p['budget']} p {p['corrupt_p']}: valid={r['valid']} "
              f"failed={[k for k, v in r['feasibility']['checks'].items() if not v]} decision={pr['decision']}")
        for key in ("A_recall", "B_obsolete_repair_share"):
            x = pr[key]
            print(f"  PRIMARY {key}: {x['mean']:+.4f} [{x['interval'][0]:+.4f}, {x['interval'][1]:+.4f}] "
                  f"+{x['positive']}/-{x['negative']}")
        for key, x in r["secondary"].items():
            print(f"  secondary {key}: {x['mean']:+.4f} [{x['interval'][0]:+.4f}, {x['interval'][1]:+.4f}]")
        print(f"  population q99 gap (no obsolescence): {r['population_gap_q99_no_obsolescence']:.0f}")
        for pol, d in r["descriptive"].items():
            print(f"  {pol:<23} recall {d['overall_accuracy']:.3f} last3 {d['last_third_accuracy']:.3f} "
                  f"obs_share {d['obsolete_repair_share']:.3f} mistaken {d['mistaken_abandonment_fraction']:.3f} "
                  f"lost@ret {d['lost_at_return_fraction']:.3f} long_lost {d['long_return_lost_fraction']:.3f} "
                  f"relinq {d['correct_relinquishment_fraction']:.3f} false_exp {d['false_abandonment_exposure']:.3f} "
                  f"thr {d['learned_threshold_final']:.0f} run_q99 {d['realized_gap_q99']:.0f}")
    print(f"\nwrote {FINAL}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("phase", choices=("select", "freeze", "final"))
    ap.add_argument("--workers", type=int, default=7)
    args = ap.parse_args()
    {"select": select, "freeze": freeze, "final": lambda: final(args.workers)}[args.phase]()


if __name__ == "__main__":
    main()
