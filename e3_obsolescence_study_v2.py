"""Driver for E3_OBSOLESCENCE_PROTOCOL_v2.md (E3-OB2).

    python -B e3_obsolescence_study_v2.py tune     # timeout T* on engineering seeds 0-7 (timeouts only)
    python -B e3_obsolescence_study_v2.py freeze   # raw and LF-normalized hashes
    python -B e3_obsolescence_study_v2.py final    # verifies the freeze, runs seeds 400-431, applies section 6

Every phase refuses to overwrite its outputs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

import e3_obsolescence_world as ob
import e3_obsolescence_world_v2 as ob2

RESULTS = Path("e3_fep_seed_results/ob2")
AUDIT, TABLE = RESULTS / "audit_ob2.json", RESULTS / "return_table.json"
TUNING, FINAL = RESULTS / "timeout_tuning.json", RESULTS / "final_results.json"
FREEZE = Path("E3_OBSOLESCENCE_FREEZE_v2.json")
CONFIGS = ({"budget": 3, "corrupt_p": 0.02}, {"budget": 4, "corrupt_p": 0.025})
TIMEOUT_GRID = (300, 500, 750, 1000, 1500, 2000, 3000, 4000)
ENGINEERING_SEEDS, FINAL_SEEDS = tuple(range(8)), tuple(range(400, 432))
BOOT_REPS, BOOT_SEED = 10000, 20260914
LEVEL = 1 - 0.05 / 6
FROZEN_FILES = ("E3_OBSOLESCENCE_PROTOCOL_v2.md", "e3_obsolescence_world.py", "e3_obsolescence_world_v2.py",
                "audit_e3_obsolescence_v2.py", "e3_obsolescence_study_v2.py",
                AUDIT.as_posix(), TABLE.as_posix(), TUNING.as_posix())
SECONDARY = (("return_supplied", "timeout_2000"), ("return_learned", "return_supplied"),
             ("return_learned", "timeout_tuned"), ("depth_flag", "return_learned"),
             ("timeout_tuned", "timeout_2000"), ("return_learned_c0.05", "return_learned"),
             ("return_learned_c0.2", "return_learned"), ("return_supplied_c0.05", "return_supplied"),
             ("return_supplied_c0.2", "return_supplied"), ("return_learned_frozen1500", "return_learned"))
METRICS = ("overall_accuracy", "obsolete_repair_share", "lost_at_return_fraction")
DESCRIPTIVE = ("overall_accuracy", "last_third_accuracy", "obsolete_repair_share", "lost_at_return_fraction",
               "long_return_lost_fraction", "mistaken_abandonment_fraction", "relinquished_obsolete_fraction",
               "ineligible_dormant_fraction", "unspent_per_tick", "repairs_per_tick", "binding_fraction")


def _default(o):
    return o.item() if hasattr(o, "item") else str(o)


def _write(path, obj):
    if path.exists():
        sys.exit(f"refusing to overwrite {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=1, default=_default))


def _hashes(path):
    data = Path(path).read_bytes()
    return {"bytes": len(data), "sha256_raw": hashlib.sha256(data).hexdigest(),
            "sha256_lf_normalized": hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()}


def _table():
    return np.array(json.loads(TABLE.read_text())["prob"])


def _run_seed(args):
    cfg, seed, policies, tuned, timeout_override = args
    w = ob.WorldParams(budget=cfg["budget"], corrupt_p=cfg["corrupt_p"])
    env = ob.generate_environment(seed, w)
    table = _table()
    rows = []
    for p in policies:
        if timeout_override is not None:
            row = ob2.run_one("timeout_tuned", seed, w, table, tuned_timeout=timeout_override, env=env)
            row["policy"] = f"timeout_{timeout_override}"
        else:
            row = ob2.run_one(p, seed, w, table, tuned_timeout=tuned, env=env)
        row.pop("calibration") if timeout_override is not None else None
        rows.append(row)
    return rows


def tune():
    if TUNING.exists():
        sys.exit(f"refusing to overwrite {TUNING}")
    out = {}
    with ProcessPoolExecutor(max_workers=7) as pool:
        for cfg in CONFIGS:
            jobs = [(cfg, s, ("timeout",), None, T) for T in TIMEOUT_GRID for s in ENGINEERING_SEEDS]
            rows = [r for batch in pool.map(_run_seed, jobs) for r in batch]
            means = {T: float(np.mean([r["overall_accuracy"] for r in rows if r["policy"] == f"timeout_{T}"]))
                     for T in TIMEOUT_GRID}
            best = max(TIMEOUT_GRID, key=lambda T: (means[T], T))
            out[f"budget{cfg['budget']}_p{cfg['corrupt_p']}"] = {"mean_recall_by_timeout": means, "tuned_timeout": best}
            print(f"{cfg}: {means} -> T* = {best}", flush=True)
    _write(TUNING, {"rule": "E3_OBSOLESCENCE_PROTOCOL_v2.md section 3", "engineering_seeds": ENGINEERING_SEEDS,
                    "configs": out})


def freeze():
    _write(FREEZE, {"kind": "local_exploratory_freeze", "external_preregistration": False,
                    "created_utc": datetime.now(timezone.utc).isoformat(), "protocol": FROZEN_FILES[0],
                    "verification_rule": "compare sha256 of file bytes with CRLF replaced by LF",
                    "final_seeds": FINAL_SEEDS, "files": {f: _hashes(f) for f in FROZEN_FILES}})
    print(f"wrote {FREEZE}")


def _paired(rows, a, b, metric, level):
    by = {(r["policy"], r["seed"]): r for r in rows}
    d = np.array([by[(a, s)][metric] - by[(b, s)][metric] for s in FINAL_SEEDS])
    d = d[~np.isnan(d)]
    means = d[np.random.default_rng(BOOT_SEED).integers(0, len(d), size=(BOOT_REPS, len(d)))].mean(axis=1)
    lo, hi = np.quantile(means, [(1 - level) / 2, 1 - (1 - level) / 2])
    return {"mean": float(d.mean()), "interval": [float(lo), float(hi)], "level": level, "n": int(len(d)),
            "positive": int((d > 0).sum()), "negative": int((d < 0).sum())}


def _calibration(rows, policy):
    cal = {k: sum(np.array(r["calibration"][k]) for r in rows if r["policy"] == policy)
           for k in ("n", "sum_p", "sum_y", "sum_sq")}
    by_class = []
    for i in range(cal["n"].shape[0]):
        n = cal["n"][i]
        total = n.sum()
        if total == 0:
            by_class.append({"n": 0})
            continue
        with np.errstate(invalid="ignore", divide="ignore"):
            gap = np.where(n > 0, np.abs(cal["sum_p"][i] / n - cal["sum_y"][i] / n), 0)
        by_class.append({"n": int(total), "ece": float((n * gap).sum() / total),
                         "brier": float(cal["sum_sq"][i].sum() / total),
                         "mean_pred": float(cal["sum_p"][i].sum() / total), "mean_real": float(cal["sum_y"][i].sum() / total)})
    long_n = cal["n"][2:].sum(axis=0)
    with np.errstate(invalid="ignore", divide="ignore"):
        long_gap = np.where(long_n > 0, np.abs(cal["sum_p"][2:].sum(axis=0) / long_n - cal["sum_y"][2:].sum(axis=0) / long_n), 0)
    long_ece = float((long_n * long_gap).sum() / long_n.sum()) if long_n.sum() else float("nan")
    return {"edges": list(ob2.CALIBRATION_SILENCE_EDGES), "by_silence_class": by_class, "long_silence_ece": long_ece}


def final():
    if FINAL.exists():
        sys.exit(f"refusing to overwrite {FINAL}")
    record = json.loads(FREEZE.read_text())
    bad = [f for f, h in record["files"].items() if _hashes(f)["sha256_lf_normalized"] != h["sha256_lf_normalized"]]
    if bad:
        sys.exit(f"freeze verification failed: {bad}")
    tuning = json.loads(TUNING.read_text())["configs"]
    reports = []
    with ProcessPoolExecutor(max_workers=7) as pool:
        for cfg in CONFIGS:
            key = f"budget{cfg['budget']}_p{cfg['corrupt_p']}"
            tuned = tuning[key]["tuned_timeout"]
            rows = [r for batch in pool.map(_run_seed, [(cfg, s, ob2.POLICIES, tuned, None) for s in FINAL_SEEDS])
                    for r in batch]
            mean = {p: float(np.nanmean([r["overall_accuracy"] for r in rows if r["policy"] == p])) for p in ob2.POLICIES}
            checks = {
                "environment_paired": all(len({r["env_digest"] for r in rows if r["seed"] == s}) == 1 for s in FINAL_SEEDS),
                "ample_feasible": mean["ample"] >= 0.90, "maintenance_needed": mean["none"] <= 0.65,
                "budget_binds": float(np.mean([r["binding_fraction"] for r in rows if r["policy"] == "depth_first"])) >= 0.50,
                "relinquishment_can_matter": mean["depth_flag"] - mean["depth_first"] >= 0.025,
                "no_repairs_to_ineligible": sum(r["repairs_to_ineligible"] for r in rows if r["policy"] != "ample") == 0,
            }
            valid = all(checks.values())
            A = _paired(rows, "return_learned", "timeout_2000", "overall_accuracy", LEVEL)
            B = _paired(rows, "return_learned", "depth_first", "obsolete_repair_share", LEVEL)
            C = _paired(rows, "return_learned", "depth_first", "lost_at_return_fraction", LEVEL)
            cal_learned, cal_supplied = _calibration(rows, "return_learned"), _calibration(rows, "return_supplied")
            D = cal_learned["long_silence_ece"]
            if (A["mean"] >= 0.03 and A["interval"][0] > 0 and B["mean"] <= -0.10 and B["interval"][1] < 0
                    and C["mean"] <= 0.05 and C["interval"][1] < 0.10 and D <= 0.10):
                decision = "demonstrated"
            elif A["interval"][1] < 0.03 or B["interval"][0] >= 0 or C["interval"][0] >= 0.10 or D > 0.10:
                decision = "not demonstrated"
            else:
                decision = "inconclusive"
            secondary = {f"{a}-{b}:{m}": _paired(rows, a, b, m, 0.95) for a, b in SECONDARY for m in METRICS}
            descriptive = {p: {k: float(np.nanmean([r[k] for r in rows if r["policy"] == p])) for k in DESCRIPTIVE}
                           for p in ob2.POLICIES}
            state = {p: next(r["state_size"] for r in rows if r["policy"] == p) for p in ob2.POLICIES}
            for r in rows:
                r.pop("calibration")
            reports.append({"config": cfg, "tuned_timeout": tuned, "checks": checks, "valid": valid,
                            "primary": {"A": A, "B": B, "C": C, "D_long_silence_ece": D, "decision": decision},
                            "calibration": {"return_learned": cal_learned, "return_supplied": cal_supplied},
                            "secondary": secondary, "descriptive": descriptive, "state_size": state, "rows": rows})
    decisions = [r["primary"]["decision"] for r in reports if r["valid"]]
    status = ("uninterpretable" if not decisions else
              "supported in this world" if all(d == "demonstrated" for d in decisions) else
              "not supported in this world" if all(d == "not demonstrated" for d in decisions) else
              "mixed or inconclusive")
    _write(FINAL, {"protocol": FROZEN_FILES[0], "final_seeds": FINAL_SEEDS, "level": LEVEL,
                   "freeze_sha256_lf_normalized": _hashes(FREEZE)["sha256_lf_normalized"],
                   "overall_status": status, "configs": reports})
    print(f"OVERALL STATUS: {status}")
    for r in reports:
        pr = r["primary"]
        print(f"\n{r['config']} T*={r['tuned_timeout']} valid={r['valid']} "
              f"failed={[k for k, v in r['checks'].items() if not v]} decision={pr['decision']}")
        for k in ("A", "B", "C"):
            x = pr[k]
            print(f"  PRIMARY {k}: {x['mean']:+.4f} [{x['interval'][0]:+.4f}, {x['interval'][1]:+.4f}] +{x['positive']}/-{x['negative']}")
        print(f"  PRIMARY D long-silence ECE (learned): {pr['D_long_silence_ece']:.4f}; supplied: "
              f"{r['calibration']['return_supplied']['long_silence_ece']:.4f}")
        for name in ("return_learned", "return_supplied"):
            cls = r["calibration"][name]["by_silence_class"]
            print(f"  calibration {name}: " + "; ".join(
                f"[{r['calibration'][name]['edges'][i]},..) pred {c['mean_pred']:.3f} real {c['mean_real']:.3f} ece {c['ece']:.3f}"
                for i, c in enumerate(cls) if c.get("n")))
        for k, x in r["secondary"].items():
            print(f"  secondary {k}: {x['mean']:+.4f} [{x['interval'][0]:+.4f}, {x['interval'][1]:+.4f}]")
        for p, d in r["descriptive"].items():
            print(f"  {p:<26} recall {d['overall_accuracy']:.3f} last3 {d['last_third_accuracy']:.3f} "
                  f"obs {d['obsolete_repair_share']:.3f} lost@ret {d['lost_at_return_fraction']:.3f} "
                  f"long_lost {d['long_return_lost_fraction']:.3f} mistaken {d['mistaken_abandonment_fraction']:.3f} "
                  f"relinq {d['relinquished_obsolete_fraction']:.3f} inel_dorm {d['ineligible_dormant_fraction']:.3f} "
                  f"unspent {d['unspent_per_tick']:.2f} state {r['state_size'][p]}")
    print(f"\nwrote {FINAL}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("phase", choices=("tune", "freeze", "final"))
    {"tune": tune, "freeze": freeze, "final": final}[ap.parse_args().phase]()


if __name__ == "__main__":
    main()
