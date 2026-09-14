"""Driver for E3_ALLOCATION_PROTOCOL_v2.md (exploratory side branch).

    python -B e3_allocation_study_v2.py select   # applies section 4 to existing phase-1 control data
    python -B e3_allocation_study_v2.py freeze   # records raw and LF-normalized hashes
    python -B e3_allocation_study_v2.py final    # verifies the freeze, runs seeds 200-231, applies section 7

Every phase refuses to overwrite its outputs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

import e3_fep_engineering_seed_v4 as v4

PHASE1 = Path("e3_fep_seed_results/v3/phase1_controls.json")
RESULTS = Path("e3_fep_seed_results/v4")
AUDIT = RESULTS / "audit_v4.json"
SELECTED = RESULTS / "selected_configs.json"
FINAL = RESULTS / "final_results.json"
FREEZE = Path("E3_ALLOCATION_FREEZE_v2.json")

FINAL_SEEDS = tuple(range(200, 232))
MUA = 0.03
BOOT_REPS, BOOT_SEED = 10000, 20260914
PRIMARY = ("depth_first", "recency")
SECONDARY = (("depth_first", "uniform"), ("depth_then_recency", "depth_first"), ("depth_first", "recov_supplied"),
             ("depth_first", "ample"), ("blind_oracle", "uniform"), ("recov_supplied", "recency"),
             ("recov_learned", "recov_supplied"), ("precision", "recency"))
FROZEN_FILES = ("E3_ALLOCATION_PROTOCOL_v2.md", "e3_fep_engineering_seed_v4.py", "e3_fep_engineering_seed_v3.py",
                "explore_e3_ceiling_search.py", "e3_allocation_study_v2.py", "audit_e3_allocation_v4.py",
                AUDIT.as_posix(), PHASE1.as_posix(), SELECTED.as_posix())


def _write(path: Path, obj) -> None:
    if path.exists():
        sys.exit(f"refusing to overwrite {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o)))


def _hashes(path: Path) -> dict:
    data = path.read_bytes()
    return {"bytes": len(data), "sha256_raw": hashlib.sha256(data).hexdigest(),
            "sha256_lf_normalized": hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()}


def _checks(m: dict, binding: float, first: float, last: float, uniform_band: tuple[float, float]) -> dict:
    return {
        "ample_feasible": m["ample"] >= 0.90,
        "maintenance_needed": m["none"] <= 0.65,
        "budget_binds": binding >= 0.50,
        "uniform_in_band": uniform_band[0] <= m["uniform"] <= uniform_band[1],
        "not_transient": last >= first - 0.05,
    }


def select() -> None:
    configs = json.loads(PHASE1.read_text())["configs"]
    evaluated = []
    for c in configs:
        checks = _checks(c["overall_means"], c["uniform_binding"], c["ample_first_third"],
                         c["ample_last_third"], (0.55, 0.90))
        evaluated.append({"params": c["params"], "uniform": c["overall_means"]["uniform"], "checks": checks,
                          "passes": all(checks.values())})
    passing = sorted((e for e in evaluated if e["passes"]), key=lambda e: abs(e["uniform"] - 0.725))
    selected = [e["params"] for e in passing[:3]]
    _write(SELECTED, {"rule": "E3_ALLOCATION_PROTOCOL_v2.md section 4",
                      "phase1_sha256_lf_normalized": _hashes(PHASE1)["sha256_lf_normalized"],
                      "evaluated": evaluated, "selected": selected})
    for e in evaluated:
        p = e["params"]
        print(f"width {p['trace_bits']} p {p['corrupt_p']} budget {p['budget']}: uniform {e['uniform']:.3f} "
              f"passes={e['passes']} failed={[k for k, v in e['checks'].items() if not v]}")
    print(f"selected: {[(s['trace_bits'], s['corrupt_p'], s['budget']) for s in selected]}")


def freeze() -> None:
    if not json.loads(SELECTED.read_text())["selected"]:
        sys.exit("nothing selected; protocol stops before freeze")
    _write(FREEZE, {"kind": "local_exploratory_freeze", "external_preregistration": False,
                    "created_utc": datetime.now(timezone.utc).isoformat(),
                    "protocol": "E3_ALLOCATION_PROTOCOL_v2.md",
                    "verification_rule": "compare sha256 of file bytes with CRLF replaced by LF",
                    "final_seeds": FINAL_SEEDS, "files": {f: _hashes(Path(f)) for f in FROZEN_FILES}})
    print(f"wrote {FREEZE}")


def _run_seed(args):
    params, seed = args
    env = v4.generate_environment(seed, params)
    return [v4.run_one(pol, seed, params, env=env) for pol in v4.POLICIES]


def _mean(rows, pol, key) -> float:
    return float(np.nanmean([r[key] for r in rows if r["policy"] == pol]))


def _paired(rows, a, b, metric, level) -> dict:
    by = {(r["policy"], r["seed"]): r for r in rows}
    d = np.array([by[(a, s)][metric] - by[(b, s)][metric] for s in FINAL_SEEDS])
    means = d[np.random.default_rng(BOOT_SEED).integers(0, len(d), size=(BOOT_REPS, len(d)))].mean(axis=1)
    alpha = 1 - level
    lo, hi = np.quantile(means, [alpha / 2, 1 - alpha / 2])
    return {"mean": float(d.mean()), "interval": [float(lo), float(hi)], "level": level, "n_seeds": len(d),
            "seeds_positive": int((d > 0).sum()), "seeds_negative": int((d < 0).sum()), "per_seed": d.tolist()}


def final(workers: int) -> None:
    if FINAL.exists():
        sys.exit(f"refusing to overwrite {FINAL}")
    record = json.loads(FREEZE.read_text())
    bad = [f for f, h in record["files"].items() if _hashes(Path(f))["sha256_lf_normalized"] != h["sha256_lf_normalized"]]
    if bad:
        sys.exit(f"freeze verification failed: {bad}")
    selected = json.loads(SELECTED.read_text())["selected"]
    level = 1 - 0.05 / len(selected)
    reports = []
    for cfg in selected:
        params = v4.Params(**cfg)
        with ProcessPoolExecutor(max_workers=workers) as pool:
            rows = [r for batch in pool.map(_run_seed, [(params, s) for s in FINAL_SEEDS]) for r in batch]
        paired_env = all(len({r["env_digest"] for r in rows if r["seed"] == s}) == 1 for s in FINAL_SEEDS)
        m = {pol: _mean(rows, pol, "overall_accuracy") for pol in ("none", "uniform", "ample")}
        checks = _checks(m, _mean(rows, "uniform", "binding_fraction"), _mean(rows, "ample", "accuracy_first_third"),
                         _mean(rows, "ample", "accuracy_last_third"), (0.50, 0.95))
        valid = paired_env and all(checks.values())
        primary = _paired(rows, *PRIMARY, "overall_accuracy", level)
        lo, hi = primary["interval"]
        primary["decision"] = ("useful advantage" if primary["mean"] >= MUA and lo > 0
                               else "no useful advantage" if hi < MUA else "inconclusive")
        secondary = {f"{PRIMARY[0]}-{PRIMARY[1]}:post_return_accuracy":
                     _paired(rows, *PRIMARY, "post_return_accuracy", 0.95)}
        for a, b in SECONDARY:
            secondary[f"{a}-{b}:overall_accuracy"] = _paired(rows, a, b, "overall_accuracy", 0.95)
        descriptive = {pol: {k: _mean(rows, pol, k) for k in (
            "overall_accuracy", "post_return_accuracy", "harmful_repair_fraction", "binding_fraction",
            "lost_at_return_fraction", "repairs_per_hot_cue_tick", "repairs_per_cold_cue_tick", "p_hat_final")}
            for pol in v4.POLICIES}
        reports.append({"params": cfg, "environment_paired": paired_env, "checks": checks, "valid": valid,
                        "primary": primary, "secondary": secondary, "descriptive": descriptive, "rows": rows})
    decisions = [r["primary"]["decision"] for r in reports if r["valid"]]
    status = ("uninterpretable" if not decisions else
              "supported in this toy" if all(d == "useful advantage" for d in decisions) else
              "not supported in this toy" if all(d == "no useful advantage" for d in decisions) else
              "mixed or inconclusive")
    _write(FINAL, {"protocol": "E3_ALLOCATION_PROTOCOL_v2.md", "final_seeds": FINAL_SEEDS,
                   "freeze_sha256_lf_normalized": _hashes(FREEZE)["sha256_lf_normalized"],
                   "primary_interval_level": level, "mua": MUA, "overall_status": status, "configs": reports})
    print(f"OVERALL STATUS: {status}  (primary interval level {level:.4f})")
    for r in reports:
        p = r["params"]
        pr = r["primary"]
        print(f"\nwidth {p['trace_bits']} p {p['corrupt_p']} budget {p['budget']}: valid={r['valid']} "
              f"failed={[k for k, v in r['checks'].items() if not v]} paired_env={r['environment_paired']}")
        print(f"  PRIMARY depth_first-recency: {pr['mean']:+.4f} [{pr['interval'][0]:+.4f}, {pr['interval'][1]:+.4f}] "
              f"+{pr['seeds_positive']}/-{pr['seeds_negative']} of {pr['n_seeds']} -> {pr['decision']}")
        for k, s in r["secondary"].items():
            print(f"  secondary {k}: {s['mean']:+.4f} [{s['interval'][0]:+.4f}, {s['interval'][1]:+.4f}] "
                  f"+{s['seeds_positive']}/-{s['seeds_negative']}")
        for pol, d in r["descriptive"].items():
            print(f"  {pol:<19} overall {d['overall_accuracy']:.3f} post {d['post_return_accuracy']:.3f} "
                  f"harmful {d['harmful_repair_fraction']:.3f} lost@ret {d['lost_at_return_fraction']:.3f} "
                  f"rep/hot {d['repairs_per_hot_cue_tick']:.3f} rep/cold {d['repairs_per_cold_cue_tick']:.3f}")
    print(f"\nwrote {FINAL}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("phase", choices=("select", "freeze", "final"))
    ap.add_argument("--workers", type=int, default=7)
    args = ap.parse_args()
    {"select": select, "freeze": freeze, "final": lambda: final(args.workers)}[args.phase]()


if __name__ == "__main__":
    main()
