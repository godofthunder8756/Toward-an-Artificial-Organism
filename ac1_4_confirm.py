"""AC1-AC4 foundational-claims confirmation (confirmatory v1).

Re-runs the decisive arm contrasts of AC1 (vulnerable controller paying for its
own repair), AC2 (produced W repair catalysts), AC3 (produced C converters) and
AC4 (produced B boundary; long-horizon controller-repair dependence) on fresh
seeds disjoint from all engineering seeds, reusing the frozen physics
unmodified. Prespecified gates are declared in
AC1_4_CONFIRMATION_PROTOCOL_v1.md and computed by the analyze_* functions here;
the audit re-derives them from the saved table without simulating.

Frozen source of truth (hashed into pre_run_snapshot.json): the protocol, this
runner, and every frozen dependency. Verification tools are hashed separately
in results.json, never into the frozen snapshot (AC16/AC17 lesson).
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import time

import numpy as np

import ac1
import ac1_followup
import ac2
import ac3
import ac4
import ac4_transport  # noqa: F401  frozen dependency of ac4

PROTOCOL = "AC1_4_CONFIRMATION_PROTOCOL_v1.md"
FROZEN_SOURCES = (
    "ac1.py", "ac1_followup.py", "ac2.py", "ac3.py", "ac4.py", "ac4_transport.py",
)

SEEDS = {
    "ac1": list(range(5100, 5108)),
    "ac2": list(range(5200, 5216)),
    "ac3": list(range(5300, 5308)),
    "ac4_short": list(range(5400, 5408)),
    "ac4_long": list(range(5500, 5508)),
}

AC1_RATES = (0.0005, 0.001)
AC2_RATES = (0.00025, 0.0005)
AC3_RATES = (0.0001, 0.0002, 0.0004)
AC4_RATES = (0.00005, 0.0001)


def contrast(a, b) -> dict:
    """Paired per-individual contrast; descriptive 95% bootstrap interval."""
    return ac1.contrast(list(a), list(b))


def _mean(rows, arm, key):
    vals = [r[key] for r in rows if r["arm"] == arm]
    return float(np.mean(vals)) if vals else float("nan")


def _completed(rows, arm):
    return sum(1 for r in rows if r["arm"] == arm and r["completed"])


def gate(name, passes, **detail):
    return {"gate": name, "pass": bool(passes), "detail": detail}


# --- pure gate analyses (the audit re-derives these from the saved rows) ---

def analyze_ac1(rows):
    arms = ("self", "no_policy_write", "free_policy_ablation", "protected")
    means = {a: dict(active_fraction=_mean(rows, a, "active_fraction"),
                     completed=_completed(rows, a),
                     policy_accuracy=_mean(rows, a, "policy_accuracy")) for a in arms}
    c_paid = contrast([r["active_fraction"] for r in rows if r["arm"] == "self"],
                      [r["active_fraction"] for r in rows if r["arm"] == "no_policy_write"])
    c_free = contrast([r["active_fraction"] for r in rows if r["arm"] == "self"],
                      [r["active_fraction"] for r in rows if r["arm"] == "free_policy_ablation"])
    gates = [
        gate("G1", means["self"]["completed"] == 8 and means["self"]["active_fraction"] >= 0.90,
             self_completed=means["self"]["completed"], self_activity=means["self"]["active_fraction"]),
        gate("G2", c_paid["mean"] >= 0.20 and c_paid["interval"][0] > 0, contrast=c_paid),
        gate("G3", c_free["mean"] >= 0.20 and c_free["interval"][0] > 0, contrast=c_free),
        gate("G4", means["protected"]["completed"] == 8 and means["protected"]["active_fraction"] >= 0.90,
             protected_completed=means["protected"]["completed"],
             protected_activity=means["protected"]["active_fraction"]),
        gate("G5", all(all(w > 0 for w in r["bank_writes"]) for r in rows if r["arm"] == "self"),
             bank_writes=[r["bank_writes"] for r in rows if r["arm"] == "self"]),
    ]
    return means, dict(paid=c_paid, free=c_free), gates


def analyze_ac2(rows):
    arms = ("self", "no_synthesis", "no_synthesis_rescue", "protected",
            "self_clamp", "no_synthesis_clamp")
    means = {a: dict(activity=_mean(rows, a, "active_fraction"),
                     completed=_completed(rows, a),
                     policy_accuracy=_mean(rows, a, "policy_accuracy")) for a in arms}
    c_synth = contrast([r["active_fraction"] for r in rows if r["arm"] == "self"],
                       [r["active_fraction"] for r in rows if r["arm"] == "no_synthesis"])
    c_info = contrast([r["policy_accuracy"] for r in rows if r["arm"] == "self_clamp"],
                      [r["policy_accuracy"] for r in rows if r["arm"] == "no_synthesis_clamp"])
    gates = [
        gate("G1", means["self"]["completed"] == 16 and means["self"]["activity"] >= 0.90,
             self_completed=means["self"]["completed"], self_activity=means["self"]["activity"]),
        gate("G2", c_synth["mean"] >= 0.20 and c_synth["interval"][0] > 0, contrast=c_synth),
        gate("G3", means["no_synthesis_rescue"]["activity"] >= 0.90
             and means["no_synthesis_rescue"]["completed"] >= 14,
             rescue_activity=means["no_synthesis_rescue"]["activity"],
             rescue_completed=means["no_synthesis_rescue"]["completed"]),
        gate("G4", c_info["mean"] >= 0.20 and c_info["interval"][0] > 0, contrast=c_info),
        gate("G5", all(r["ledger"]["births"] > 120 and all(w > 0 for w in r["bank_writes"])
                       for r in rows if r["arm"] == "self"),
             births=[r["ledger"]["births"] for r in rows if r["arm"] == "self"],
             bank_writes=[r["bank_writes"] for r in rows if r["arm"] == "self"]),
        gate("G6", means["protected"]["activity"] >= 0.90,
             protected_activity=means["protected"]["activity"]),
    ]
    return means, dict(synthesis=c_synth, clamp_info=c_info), gates


def analyze_ac3(rows):
    arms = ("self", "no_C", "no_C_rescue", "no_C_energy", "protected",
            "self_energy", "no_W_energy")
    means = {a: dict(activity=_mean(rows, a, "active_fraction"),
                     completed=_completed(rows, a),
                     policy_accuracy=_mean(rows, a, "policy_accuracy")) for a in arms}
    c_C = contrast([r["active_fraction"] for r in rows if r["arm"] == "self"],
                   [r["active_fraction"] for r in rows if r["arm"] == "no_C"])
    c_W = contrast([r["policy_accuracy"] for r in rows if r["arm"] == "self_energy"],
                   [r["policy_accuracy"] for r in rows if r["arm"] == "no_W_energy"])
    gates = [
        gate("G1", means["self"]["completed"] == 8 and means["self"]["activity"] >= 0.90,
             self_completed=means["self"]["completed"], self_activity=means["self"]["activity"]),
        gate("G2", c_C["mean"] >= 0.20 and c_C["interval"][0] > 0, contrast=c_C),
        gate("G3", means["no_C_rescue"]["completed"] == 8 and means["no_C_rescue"]["activity"] >= 0.90,
             rescue_completed=means["no_C_rescue"]["completed"],
             rescue_activity=means["no_C_rescue"]["activity"]),
        gate("G4", c_W["mean"] >= 0.20 and c_W["interval"][0] > 0, contrast=c_W),
        gate("G5", means["no_C_energy"]["activity"] >= 0.90,
             energy_rescue_activity=means["no_C_energy"]["activity"]),
        gate("G6", all(r["ledger"]["births"] > 120 and r["ledger"]["C_births"] > 30
                       and r["ledger"]["converted"] > 0 and all(w > 0 for w in r["bank_writes"])
                       for r in rows if r["arm"] == "self"),
             births=[r["ledger"]["births"] for r in rows if r["arm"] == "self"],
             C_births=[r["ledger"]["C_births"] for r in rows if r["arm"] == "self"]),
    ]
    return means, dict(C_dependence=c_C, W_clamp_info=c_W), gates


def analyze_ac4_short(rows):
    arms = ("self", "no_B", "no_B_rescue", "no_B_retention", "protected")
    means = {a: dict(activity=_mean(rows, a, "activity"), completed=_completed(rows, a)) for a in arms}
    c_B = contrast([r["activity"] for r in rows if r["arm"] == "self"],
                   [r["activity"] for r in rows if r["arm"] == "no_B"])
    exports = [r["ledger"]["particle_export"] for r in rows if r["arm"] == "no_B"]
    gates = [
        gate("GA1", means["self"]["completed"] == 8 and means["self"]["activity"] >= 0.90,
             self_completed=means["self"]["completed"], self_activity=means["self"]["activity"]),
        gate("GA2", c_B["mean"] >= 0.20 and c_B["interval"][0] > 0 and all(x > 0 for x in exports),
             contrast=c_B, no_B_exports=exports),
        gate("GA3", means["no_B_rescue"]["activity"] >= 0.90 and means["no_B_retention"]["activity"] >= 0.90,
             rescue_activity=means["no_B_rescue"]["activity"],
             retention_activity=means["no_B_retention"]["activity"]),
        gate("GA4", all(r["ledger"]["B_birth"] > 40 for r in rows if r["arm"] == "self"),
             B_births=[r["ledger"]["B_birth"] for r in rows if r["arm"] == "self"]),
    ]
    return means, dict(B_dependence=c_B), gates


def analyze_ac4_long(rows):
    arms = ("self", "no_policy_write", "protected", "no_B_retention")
    means = {a: dict(activity=_mean(rows, a, "activity"), completed=_completed(rows, a),
                     policy_accuracy=_mean(rows, a, "policy_accuracy")) for a in arms}
    c = contrast([r["activity"] for r in rows if r["arm"] == "self"],
                 [r["activity"] for r in rows if r["arm"] == "no_policy_write"])
    npw_completed = _completed(rows, "no_policy_write")
    gates = [
        gate("GB1", means["self"]["completed"] == 8 and means["self"]["activity"] >= 0.90
             and means["self"]["policy_accuracy"] >= 0.99,
             self_completed=means["self"]["completed"], self_activity=means["self"]["activity"],
             self_policy_accuracy=means["self"]["policy_accuracy"]),
        gate("GB2", c["mean"] >= 0.20 and c["interval"][0] > 0 and npw_completed <= 2,
             contrast=c, no_policy_write_completed=npw_completed),
        gate("GB3", means["protected"]["completed"] == 8 and means["protected"]["activity"] >= 0.90,
             protected_completed=means["protected"]["completed"],
             protected_activity=means["protected"]["activity"]),
    ]
    return means, dict(repair_dependence=c), gates


# --- row generation (final runs) ---

def run_ac1(rows_file):
    configs = []
    for p in AC1_RATES:
        c = ac1.Config(flip_p=p, pulse=False)
        rows = []
        for seed in SEEDS["ac1"]:
            inputs = ac1.world(seed, c)
            for arm in ("self", "no_policy_write", "free_policy_ablation", "protected"):
                rows.append(ac1_followup.run_free(seed, c, inputs) if arm == "free_policy_ablation"
                            else ac1.run_one(seed, c, arm, inputs))
                rows_file.write(json.dumps(rows[-1]) + "\n")
                rows_file.flush()
        means, contrasts, gates = analyze_ac1(rows)
        configs.append(dict(config=ac1.Config(flip_p=p, pulse=False).__dict__, means=means,
                            contrasts=contrasts, gates=gates, rows=rows))
        print(json.dumps(dict(study="ac1", p=p, gates={g["gate"]: g["pass"] for g in gates})), flush=True)
    return configs


def run_ac2(rows_file):
    configs = []
    arms = ("self", "no_synthesis", "no_synthesis_rescue", "protected",
            "self_clamp", "no_synthesis_clamp")
    for p in AC2_RATES:
        c = ac2.Config(flip_p=p)
        rows = []
        for seed in SEEDS["ac2"]:
            inputs = ac2.world(seed, c)
            for arm in arms:
                rows.append(ac2.run_one(seed, c, arm, inputs))
                rows_file.write(json.dumps(rows[-1]) + "\n")
                rows_file.flush()
        means, contrasts, gates = analyze_ac2(rows)
        configs.append(dict(config=ac2.Config(flip_p=p).__dict__, means=means,
                            contrasts=contrasts, gates=gates, rows=rows))
        print(json.dumps(dict(study="ac2", p=p, gates={g["gate"]: g["pass"] for g in gates})), flush=True)
    return configs


def run_ac3(rows_file):
    configs = []
    arms = ("self", "no_C", "no_C_rescue", "no_C_energy", "protected",
            "self_energy", "no_W_energy")
    for p in AC3_RATES:
        c = ac3.Config(flip_p=p)
        rows = []
        for seed in SEEDS["ac3"]:
            inputs = ac3.world(seed, c)
            for arm in arms:
                rows.append(ac3.run_one(seed, c, arm, inputs))
                rows_file.write(json.dumps(rows[-1]) + "\n")
                rows_file.flush()
        means, contrasts, gates = analyze_ac3(rows)
        configs.append(dict(config=ac3.Config(flip_p=p).__dict__, means=means,
                            contrasts=contrasts, gates=gates, rows=rows))
        print(json.dumps(dict(study="ac3", p=p, gates={g["gate"]: g["pass"] for g in gates})), flush=True)
    return configs


def run_ac4_short(rows_file):
    configs = []
    arms = ("self", "no_B", "no_B_rescue", "no_B_retention", "protected")
    for p in AC4_RATES:
        rows = []
        for seed in SEEDS["ac4_short"]:
            for arm in arms:
                rows.append(ac4.run(seed, p, arm, 2048))
                rows_file.write(json.dumps(rows[-1]) + "\n")
                rows_file.flush()
        means, contrasts, gates = analyze_ac4_short(rows)
        configs.append(dict(config=dict(p=p, ticks=2048), means=means,
                            contrasts=contrasts, gates=gates, rows=rows))
        print(json.dumps(dict(study="ac4_short", p=p, gates={g["gate"]: g["pass"] for g in gates})), flush=True)
    return configs


def run_ac4_long(rows_file):
    configs = []
    arms = ("self", "no_policy_write", "protected", "no_B_retention")
    for p in AC4_RATES:
        rows = []
        for seed in SEEDS["ac4_long"]:
            for arm in arms:
                rows.append(ac4.run(seed, p, arm, 8192))
                rows_file.write(json.dumps(rows[-1]) + "\n")
                rows_file.flush()
        means, contrasts, gates = analyze_ac4_long(rows)
        configs.append(dict(config=dict(p=p, ticks=8192), means=means,
                            contrasts=contrasts, gates=gates, rows=rows))
        print(json.dumps(dict(study="ac4_long", p=p, gates={g["gate"]: g["pass"] for g in gates})), flush=True)
    return configs


def study(out: Path):
    out.mkdir(exist_ok=False)
    result: dict = dict(kind="confirmatory_v1", protocol=PROTOCOL, seeds=SEEDS,
                        python=platform.python_version(), numpy=np.__version__,
                        source_hashes={p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
                                       for p in (PROTOCOL,) + FROZEN_SOURCES + ("ac1_4_confirm.py",)})
    (out / "pre_run_snapshot.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    started = time.monotonic()
    studies = {}
    with (out / "rows.jsonl").open("x", encoding="utf-8") as rows_file:
        studies["ac1"] = run_ac1(rows_file)
        studies["ac2"] = run_ac2(rows_file)
        studies["ac3"] = run_ac3(rows_file)
        studies["ac4_short"] = run_ac4_short(rows_file)
        studies["ac4_long"] = run_ac4_long(rows_file)
    result["studies"] = studies
    result["wall_seconds"] = time.monotonic() - started
    (out / "results.json").write_text(json.dumps(result, indent=2, allow_nan=False), encoding="utf-8")
    summary = {s: {g["gate"]: g["pass"] for cfg in studies[s] for g in cfg["gates"]}
               for s in studies}
    print(json.dumps(summary), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    study(parser.parse_args().out)
