"""Driver for E3_ALLOCATION_PROTOCOL_v1.md (exploratory side branch).

    python -B e3_allocation_study.py phase1   # controls only; applies the selection rule
    python -B e3_allocation_study.py freeze   # records raw and LF-normalized hashes
    python -B e3_allocation_study.py final    # verifies the freeze, runs final seeds, applies decisions

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

import e3_fep_engineering_seed_v3 as v3

RESULTS = Path("e3_fep_seed_results/v3")
AUDIT = RESULTS / "audit_v3.json"
PHASE1 = RESULTS / "phase1_controls.json"
SELECTED = RESULTS / "selected_configs.json"
FINAL = RESULTS / "final_results.json"
FREEZE = Path("E3_ALLOCATION_FREEZE_v1.json")

GRID = {"trace_bits": (5, 7, 9), "corrupt_p": (0.01, 0.02, 0.03), "budget": (2, 3, 4)}
ENGINEERING_SEEDS = tuple(range(8))
FINAL_SEEDS = tuple(range(100, 132))
SELECT_HEADROOM, FINAL_HEADROOM = 0.08, 0.04
MUA = 0.03
BOOT_REPS, BOOT_SEED = 10000, 20260914
PRIMARY = (("recov_supplied", "recency"), ("recov_learned", "recency"))
SECONDARY = (("recov_learned", "recov_supplied"), ("blind_oracle", "recov_supplied"),
             ("recov_supplied", "uniform"), ("precision", "recency"))
FROZEN_FILES = ("E3_ALLOCATION_PROTOCOL_v1.md", "e3_fep_engineering_seed_v3.py", "e3_allocation_study.py",
                "audit_e3_allocation.py", str(AUDIT.as_posix()), str(PHASE1.as_posix()), str(SELECTED.as_posix()))


def _run_seed(args):
    params, seed, policies = args
    env = v3.generate_environment(seed, params)
    return [v3.run_one(pol, seed, params, env=env) for pol in policies]


def run_rows(params: v3.Params, seeds, policies, workers: int) -> list[dict]:
    with ProcessPoolExecutor(max_workers=workers) as pool:
        batches = pool.map(_run_seed, [(params, s, policies) for s in seeds])
        return [row for batch in batches for row in batch]


def policy_mean(rows, policy, key) -> float:
    return float(np.nanmean([r[key] for r in rows if r["policy"] == policy]))


def feasibility(rows, headroom_min: float) -> dict:
    m = {pol: policy_mean(rows, pol, "overall_accuracy") for pol in ("none", "random", "uniform", "blind_oracle", "ample")}
    headroom = m["blind_oracle"] - max(m["uniform"], m["random"])
    first, last = policy_mean(rows, "ample", "accuracy_first_third"), policy_mean(rows, "ample", "accuracy_last_third")
    binding = policy_mean(rows, "uniform", "binding_fraction")
    checks = {
        "ample_feasible": m["ample"] >= 0.90,
        "maintenance_needed": m["none"] <= 0.65,
        "budget_binds": binding >= 0.50,
        "headroom": headroom >= headroom_min,
        "not_transient": last >= first - 0.05,
    }
    return {"overall_means": m, "headroom": headroom, "uniform_binding": binding,
            "ample_first_third": first, "ample_last_third": last, "checks": checks,
            "passes": all(checks.values())}


def _write(path: Path, obj) -> None:
    if path.exists():
        sys.exit(f"refusing to overwrite {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o)))


def phase1(workers: int) -> None:
    for path in (PHASE1, SELECTED):
        if path.exists():
            sys.exit(f"refusing to overwrite {path}")
    configs = []
    for bits, p_flip, budget in itertools.product(*GRID.values()):
        params = replace(v3.Params(), trace_bits=bits, corrupt_p=p_flip, budget=budget)
        rows = run_rows(params, ENGINEERING_SEEDS, v3.CONTROL_POLICIES, workers)
        f = feasibility(rows, SELECT_HEADROOM)
        configs.append({"params": asdict(params), **f})
        print(f"width {bits} p {p_flip} budget {budget}: passes={f['passes']} headroom={f['headroom']:+.3f} "
              f"ample={f['overall_means']['ample']:.3f} none={f['overall_means']['none']:.3f} "
              f"binding={f['uniform_binding']:.2f} {[k for k, v in f['checks'].items() if not v]}", flush=True)
    passing = sorted((c for c in configs if c["passes"]),
                     key=lambda c: (-c["headroom"], -c["overall_means"]["ample"]))
    selected = [c["params"] for c in passing[:2]]
    _write(PHASE1, {"engineering_seeds": ENGINEERING_SEEDS, "policies": v3.CONTROL_POLICIES, "configs": configs})
    _write(SELECTED, {"rule": "E3_ALLOCATION_PROTOCOL_v1.md section 4", "selected": selected})
    print(f"selected {len(selected)} configuration(s): {selected}" if selected
          else "no configuration passed; per protocol, no allocator comparison is run")


def _hashes(path: Path) -> dict:
    data = path.read_bytes()
    return {"bytes": len(data), "sha256_raw": hashlib.sha256(data).hexdigest(),
            "sha256_lf_normalized": hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()}


def freeze() -> None:
    selected = json.loads(SELECTED.read_text())["selected"]
    if not selected:
        sys.exit("nothing selected; protocol stops before freeze")
    _write(FREEZE, {
        "kind": "local_exploratory_freeze",
        "external_preregistration": False,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "protocol": "E3_ALLOCATION_PROTOCOL_v1.md",
        "verification_rule": "compare sha256 of file bytes with CRLF replaced by LF",
        "final_seeds": FINAL_SEEDS,
        "files": {name: _hashes(Path(name)) for name in FROZEN_FILES},
    })
    print(f"wrote {FREEZE}")


def verify_freeze() -> dict:
    record = json.loads(FREEZE.read_text())
    failures = [name for name, h in record["files"].items()
                if _hashes(Path(name))["sha256_lf_normalized"] != h["sha256_lf_normalized"]]
    if failures:
        sys.exit(f"freeze verification failed: {failures}")
    return {"freeze_sha256_lf_normalized": _hashes(FREEZE)["sha256_lf_normalized"], "files_verified": len(record["files"])}


def _bootstrap(d: np.ndarray, level: float) -> list[float]:
    rng = np.random.default_rng(BOOT_SEED)
    means = d[rng.integers(0, len(d), size=(BOOT_REPS, len(d)))].mean(axis=1)
    alpha = 1 - level
    return [float(np.quantile(means, alpha / 2)), float(np.quantile(means, 1 - alpha / 2))]


def paired(rows, a, b, metric, level) -> dict:
    by = {(r["policy"], r["seed"]): r for r in rows}
    seeds = sorted({r["seed"] for r in rows})
    d = np.array([by[(a, s)][metric] - by[(b, s)][metric] for s in seeds])
    lo, hi = _bootstrap(d, level)
    return {"mean": float(d.mean()), "interval": [lo, hi], "level": level, "n_seeds": len(d),
            "seeds_positive": int((d > 0).sum()), "seeds_negative": int((d < 0).sum()), "per_seed": d.tolist()}


def decide(result: dict) -> str:
    lo, hi = result["interval"]
    if result["mean"] >= MUA and lo > 0:
        return "useful advantage"
    if hi < MUA:
        return "no useful advantage"
    return "inconclusive"


def final(workers: int) -> None:
    if FINAL.exists():
        sys.exit(f"refusing to overwrite {FINAL}")
    freeze_check = verify_freeze()
    selected = json.loads(SELECTED.read_text())["selected"]
    level = 1 - 0.05 / (len(PRIMARY) * len(selected))
    reports = []
    for cfg in selected:
        params = v3.Params(**cfg)
        rows = run_rows(params, FINAL_SEEDS, v3.POLICIES, workers)
        paired_env = all(len({r["env_digest"] for r in rows if r["seed"] == s}) == 1 for s in FINAL_SEEDS)
        f = feasibility(rows, FINAL_HEADROOM)
        valid = paired_env and f["passes"]
        primary = {}
        for a, b in PRIMARY:
            res = paired(rows, a, b, "overall_accuracy", level)
            res["decision"] = decide(res)
            primary[f"{a}-{b}"] = res
        secondary = {}
        for a, b in PRIMARY:
            secondary[f"{a}-{b}:post_return_accuracy"] = paired(rows, a, b, "post_return_accuracy", 0.95)
        for a, b in SECONDARY:
            secondary[f"{a}-{b}:overall_accuracy"] = paired(rows, a, b, "overall_accuracy", 0.95)
        descriptive = {pol: {k: policy_mean(rows, pol, k) for k in (
            "overall_accuracy", "post_return_accuracy", "steady_accuracy", "harmful_repair_fraction",
            "binding_fraction", "lost_at_return_fraction", "repairs_per_hot_cue_tick",
            "repairs_per_cold_cue_tick", "p_hat_final")} for pol in v3.POLICIES}
        reports.append({"params": cfg, "environment_paired": paired_env, "feasibility": f, "valid": valid,
                        "primary": primary, "secondary": secondary, "descriptive": descriptive, "rows": rows})
    valid_reports = [r for r in reports if r["valid"]]
    decisions = [r["primary"]["recov_supplied-recency"]["decision"] for r in valid_reports]
    if not valid_reports:
        status = "uninterpretable"
    elif all(d == "useful advantage" for d in decisions):
        status = "supported in this toy"
    elif all(d == "no useful advantage" for d in decisions):
        status = "not supported in this toy"
    else:
        status = "mixed or inconclusive"
    _write(FINAL, {"protocol": "E3_ALLOCATION_PROTOCOL_v1.md", "freeze_check": freeze_check,
                   "final_seeds": FINAL_SEEDS, "primary_interval_level": level, "mua": MUA,
                   "overall_status": status, "configs": reports})
    print(f"overall status: {status}")
    for r in reports:
        print(f"\nconfig {r['params']['trace_bits']}/{r['params']['corrupt_p']}/{r['params']['budget']} "
              f"valid={r['valid']} failed_checks={[k for k, v in r['feasibility']['checks'].items() if not v]}")
        for key, res in r["primary"].items():
            lo, hi = res["interval"]
            print(f"  PRIMARY {key}: {res['mean']:+.4f} [{lo:+.4f}, {hi:+.4f}] ({res['level']:.4f}) "
                  f"+{res['seeds_positive']}/-{res['seeds_negative']} -> {res['decision']}")
        for key, res in r["secondary"].items():
            lo, hi = res["interval"]
            print(f"  secondary {key}: {res['mean']:+.4f} [{lo:+.4f}, {hi:+.4f}]")
        for pol, d in r["descriptive"].items():
            print(f"  {pol:<15} overall {d['overall_accuracy']:.3f} post {d['post_return_accuracy']:.3f} "
                  f"harmful {d['harmful_repair_fraction']:.3f} binding {d['binding_fraction']:.2f} "
                  f"lost@ret {d['lost_at_return_fraction']:.3f} rep/hot {d['repairs_per_hot_cue_tick']:.3f} "
                  f"rep/cold {d['repairs_per_cold_cue_tick']:.3f} p_hat {d['p_hat_final']:.4f}")
    print(f"\nwrote {FINAL}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("phase", choices=("phase1", "freeze", "final"))
    ap.add_argument("--workers", type=int, default=7)
    args = ap.parse_args()
    {"phase1": lambda: phase1(args.workers), "freeze": freeze, "final": lambda: final(args.workers)}[args.phase]()


if __name__ == "__main__":
    main()
