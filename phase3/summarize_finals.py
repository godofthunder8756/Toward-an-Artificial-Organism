"""G13 final summary — apply the frozen statistical plan to the endpoints.

Reads the frozen rows (``phase3_results_finals_v1/rows.jsonl`` + ``results.json``)
and the analysis endpoints (``phase3_finals_analysis_v1/endpoints.json``),
applies the frozen statistical plan (exact sign-flip, effect sizes with exact
binomial CIs), and writes ``summary.json`` + ``PHASE3_FINALS_SUMMARY_v1.md``.

Equivalence and byte-identity gates are reported per-seed; they are never run
as hypothesis tests and never turned into a "p > 0.05 therefore equal" claim.
"""

from __future__ import annotations

import argparse
import json
import os
import sys

import numpy as np

from bridge import exact_stats as st

ARM_NAMES = ["candidate", "r1", "r4", "r5", "r2", "r3"]
ALPHA = 0.01
FLOOR = 2.0 / (2 ** 12)          # 0.00049 at n=12
CHANCE = 0.5
EPS = 0.02                       # finite-sample resolution for categorical gates


def _series(rows, arm, key):
    return [r[key] for r in rows if r["arm"] == arm and r[key] is not None]


def _mean(v):
    v = [x for x in v if x is not None]
    return float(sum(v) / len(v)) if v else None


def _f(x, nd=4):
    return "" if x is None else f"{float(x):.{nd}f}"


def compute(rows, endpoints):
    seeds = sorted({r["seed"] for r in rows})
    by_seed = {e["seed"]: e for e in endpoints}

    g = {"n_seeds": len(seeds), "seeds": seeds, "alpha": ALPHA, "floor": FLOOR}
    cand_probe = _series(rows, "candidate", "probe_acc")
    r4_probe = _series(rows, "r4", "probe_acc")
    cand_cut = _series(rows, "candidate", "pi_cut_probe_acc")
    cand_by_seed = {r["seed"]: r["probe_acc"] for r in rows if r["arm"] == "candidate"}
    cut_by_seed = {r["seed"]: r["pi_cut_probe_acc"] for r in rows if r["arm"] == "candidate"}
    s_shared = sorted(set(cand_by_seed) & set(cut_by_seed))
    drop = [cand_by_seed[s] - cut_by_seed[s] for s in s_shared]
    r1_inc = _series(rows, "r1", "incoherence_rate")
    cand_inc = _series(rows, "candidate", "incoherence_rate")
    f1 = [by_seed[s]["f1_decode"] for s in seeds if s in by_seed]
    s_conf = _series(rows, "candidate", "s_conf_log_loss")
    s_conf_ceil = _series(rows, "candidate", "s_conf_ceiling")
    r4_conf = _series(rows, "r4", "s_conf_log_loss")
    r4_bias = _series(rows, "r4", "s_bias_accuracy")
    cand_bias = _series(rows, "candidate", "s_bias_accuracy")

    g["H1_1"] = {
        "candidate_probe_mean": _mean(cand_probe),
        "candidate_probe_min": min(cand_probe),
        "all_above_chance_plus_eps": all(a > CHANCE + EPS for a in cand_probe),
    }
    diffs = [a - b for a, b in zip(cand_probe, r4_probe)]
    g["H1_2"] = {
        "r4_probe_mean": _mean(r4_probe),
        "candidate_minus_r4_per_seed": diffs,
        "max_abs_diff": max(abs(d) for d in diffs),
    }
    g["H1_3"] = {
        "probe_mean": _mean(cand_probe), "pi_cut_mean": _mean(cand_cut),
        "drop_per_seed": drop,
        "signflip": st.sign_flip_test(drop),
        "effect": st.paired_effect([cand_by_seed[s] for s in s_shared],
                                   [cut_by_seed[s] for s in s_shared]),
    }
    g["H1_4"] = {
        "f1_decode_per_seed": f1, "f1_decode_mean": _mean(f1),
        "f1_decode_max": max(f1) if f1 else None,
        "all_at_chance": all(x <= CHANCE + EPS for x in f1) if f1 else None,
    }
    g["H4_1"] = {
        "candidate_incoherence": cand_inc, "r1_incoherence": r1_inc,
        "candidate_all_zero": all(x == 0.0 for x in cand_inc),
        "r1_any_positive": any(x > 0.0 for x in r1_inc),
        "r1_incoherence_mean": _mean(r1_inc),
        "signflip": st.sign_flip_test([a - b for a, b in zip(r1_inc, cand_inc)]),
        "effect": st.paired_effect(r1_inc, cand_inc),
    }
    g["H5_1"] = {
        "s_conf_log_loss_mean": _mean(s_conf), "ceiling_mean": _mean(s_conf_ceil),
        "gap_per_seed": [a - b for a, b in zip(s_conf, s_conf_ceil)],
        "max_gap": max(abs(a - b) for a, b in zip(s_conf, s_conf_ceil)),
    }
    g["H5_2"] = {
        "s_conf_diff_per_seed": [a - b for a, b in zip(s_conf, r4_conf)],
        "s_bias_diff_per_seed": [a - b for a, b in zip(cand_bias, r4_bias)],
    }
    g["interventions"] = {
        "I1_all_seeds_match": all(all(v["match"] for v in by_seed[s]["i1"].values())
                                  for s in seeds),
        "I2_all_seeds_ok": all(all(v["no_w_baseline_ok"] and v["survivors_byte_identical"]
                                   for v in by_seed[s]["i2"].values()) for s in seeds),
        "I5_all_seeds_coherent": all(by_seed[s]["i5"]["wrong_sign"]["coherent"]
                                     and by_seed[s]["i5"]["stale"]["coherent"]
                                     for s in seeds),
        "I4_divergence_mean": {nm: _mean([by_seed[s]["i4"][nm] for s in seeds])
                               for nm in ("spol", "splan", "sreg")},
        "single_write_reach": {
            "candidate": by_seed[seeds[0]]["single_write_reach"]["candidate"],
            "r1": by_seed[seeds[0]]["single_write_reach"]["r1"],
            "r5": by_seed[seeds[0]]["single_write_reach"]["r5"],
        },
    }
    extras_by_arm = {}
    for arm in ARM_NAMES:
        extras_by_arm[arm] = {
            key: _mean([by_seed[s]["extras"][arm][key] for s in seeds])
            for key in ("spol_probe_acc", "splan_commit_rate", "splan_commit_acc",
                        "sreg_preserve_rate", "n_refresh_targets",
                        "total_refresh_events", "mean_refresh_per_ep",
                        "final_energy_mean")
        }
    g["per_specialist_and_resource"] = extras_by_arm
    from phase3.config import Phase3Config, parameter_counts
    g["parameter_counts"] = parameter_counts(Phase3Config())
    return g


def _md(g, rows, frozen_dir, cross_fail):
    lines = []
    add = lines.append
    add("# Phase-III finals summary v1 — G13")
    add("")
    add("The frozen final runs on seeds 100–111 (N = 12 model seeds), all six arms, "
        "plus the five interventions (I1–I5), the π-cut, F1, the coordination and "
        "novel-consumer endpoints. Frozen statistical plan (§10): exact sign-flip on "
        "paired per-seed differences, α = 0.01, floor 2/2^12 = 0.00049. Equivalence "
        "and byte-identity gates are reported per-seed, never inferred from "
        "nonsignificance.")
    add("")
    add(f"- Frozen artifact: `{frozen_dir}/` ({len(rows)} rows, "
        f"state_hash from results.json)")
    add(f"- Cross-check (analysis re-train vs frozen rows): "
        f"{'0 mismatches — byte-reproducible' if not cross_fail else str(cross_fail) + ' MISMATCHES'}")
    add(f"- Seeds: {g['seeds']}")
    add("")

    # per-arm table
    pm = {}
    for arm in ARM_NAMES:
        ar = [r for r in rows if r["arm"] == arm]
        pm[arm] = {
            "probe": _mean([r["probe_acc"] for r in ar]),
            "clean": _mean([r["clean_acc"] for r in ar]),
            "inc": _mean([r["incoherence_rate"] for r in ar]),
            "pi_cut": _mean([r["pi_cut_probe_acc"] for r in ar]),
            "conf_ll": _mean([r["s_conf_log_loss"] for r in ar]),
            "bias": _mean([r["s_bias_accuracy"] for r in ar]),
            "ceil": _mean([r["s_conf_ceiling"] for r in ar]),
        }
    add("## 1. The six arms at a glance (per-arm mean over 12 final seeds)")
    add("")
    add("| arm | probe_acc | clean_acc | incoherence | π-cut probe | S_conf ll | S_bias acc | S_conf ceiling |")
    add("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for arm in ARM_NAMES:
        d = pm[arm]
        add(f"| {arm} | {_f(d['probe'])} | {_f(d['clean'])} | {_f(d['inc'],6)} | "
            f"{_f(d['pi_cut'])} | {_f(d['conf_ll'])} | {_f(d['bias'])} | {_f(d['ceil'])} |")
    add("")
    add("Rivals: R1 private-state, R4 sufficient-statistic broadcast (ceiling), "
        "R5 independent-copy, R2 monolithic RNN, R3 raw-history.")
    add("")

    add("## 2. Gates (frozen statistical plan)")
    add("")
    h = g["H1_1"]
    add("### H1 — maintained hidden-state content (latent-state inference + W information)")
    add(f"- H1.1 probe above memoryless bound 0.500: candidate mean "
        f"{_f(h['candidate_probe_mean'])}, min {_f(h['candidate_probe_min'])} "
        f"(every seed above chance+ε: {h['all_above_chance_plus_eps']}).")
    h = g["H1_2"]
    add(f"- H1.2 ceiling equivalence with R4 (empirical ceiling "
        f"{_f(h['r4_probe_mean'])}): candidate−R4 per seed "
        f"[{', '.join(_f(x) for x in h['candidate_minus_r4_per_seed'])}], "
        f"max |diff| {_f(h['max_abs_diff'])}. Equivalence, reported not tested.")
    h = g["H1_3"]
    sf = h["signflip"]
    add(f"- H1.3 paid persistence (π-cut): probe {_f(h['probe_mean'])} → π-cut "
        f"{_f(h['pi_cut_mean'])}; sign-flip p = {sf['p']:.5f} (N_eff {sf['N_eff']}, "
        f"floor {FLOOR}).")
    h = g["H1_4"]
    add(f"- H1.4 free recurrence (F1): h_t decode of z under π-cut+zero-W "
        f"mean {_f(h['f1_decode_mean'])}, max {_f(h['f1_decode_max'])} "
        f"(chance 0.500; all ≤ chance+ε: {h['all_at_chance']}).")
    add("")

    h = g["H4_1"]
    sf = h["signflip"]
    add("### H4 — coordination (the load-bearing candidate-vs-R1 contrast)")
    add(f"- H4.1 incoherence: candidate all-zero {h['candidate_all_zero']}; R1 mean "
        f"{_f(h['r1_incoherence_mean'],6)} (any>0: {h['r1_any_positive']}); "
        f"sign-flip p = {sf['p']:.5f} (N_eff {sf['N_eff']}).")
    add("")

    add("### H5 — novel-consumer reuse (treated separately)")
    h = g["H5_1"]
    add(f"- H5.1 S_conf log loss {_f(h['s_conf_log_loss_mean'])} vs posterior-entropy "
        f"ceiling {_f(h['ceiling_mean'])} (max gap {_f(h['max_gap'])}). Equivalence, "
        f"reported not tested.")
    h = g["H5_2"]
    add(f"- H5.2 candidate−R4 S_conf ll per seed "
        f"[{', '.join(_f(x) for x in h['s_conf_diff_per_seed'])}]; S_bias acc "
        f"[{', '.join(_f(x) for x in h['s_bias_diff_per_seed'])}]. Equivalence, "
        f"reported not tested.")
    add("")

    iv = g["interventions"]
    add("## 3. Interventions (each specialist's response to a W intervention)")
    add(f"- I1 differential-scramble (w★ ↦ triple traces the sign/two-sided/even "
        f"functions): matches on all seeds — {iv['I1_all_seeds_match']}.")
    add(f"- I2 per-consumer W-cut (cut consumer → exact no-W baseline, survivors "
        f"byte-identical): all seeds — {iv['I2_all_seeds_ok']}.")
    add(f"- I5 coherent error (wrong-sign and stale → mutually consistent triple): "
        f"all seeds — {iv['I5_all_seeds_coherent']}.")
    add(f"- I4 private-copy divergence (identity vs value): mean divergence "
        f"spol {_f(iv['I4_divergence_mean']['spol'])}, splan "
        f"{_f(iv['I4_divergence_mean']['splan'])}, sreg "
        f"{_f(iv['I4_divergence_mean']['sreg'])}.")
    add(f"- Single-write reach (SHARED): candidate {iv['single_write_reach']['candidate']} "
        f"(one write → 3 consumers); R1 {iv['single_write_reach']['r1']}; R5 "
        f"{iv['single_write_reach']['r5']} (one write → 1 consumer).")
    add("")

    ex = g["per_specialist_and_resource"]
    add("## 4. Per-specialist task performance + resource cost")
    add("")
    add("| arm | S_pol probe | S_plan commit rate | S_plan commit acc | S_reg preserve | refresh targets | total refresh | mean refresh/ep | final E |")
    add("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for arm in ARM_NAMES:
        e = ex[arm]
        add(f"| {arm} | {_f(e['spol_probe_acc'])} | {_f(e['splan_commit_rate'])} | "
            f"{_f(e['splan_commit_acc'])} | {_f(e['sreg_preserve_rate'])} | "
            f"{e['n_refresh_targets']} | {_f(e['total_refresh_events'],1)} | "
            f"{_f(e['mean_refresh_per_ep'],1)} | {_f(e['final_energy_mean'])} |")
    add("")
    pc = g["parameter_counts"]
    add(f"- Trainable parameters: candidate encoder {pc['candidate_encoder']}, R1 "
        f"three× {pc['r1_per_copy']} (total {pc['r1_three_encoders']}), R2 "
        f"{pc['r2_total']}, R3 {pc['r3_total']}, R4/R5 0.")
    add("")
    add("## 5. Not claimed")
    add("No equivalence is inferred from nonsignificance; ceiling/byte-identity gates "
        "are per-seed facts. This is a level-(b)/(c) representational result — no "
        "autopoiesis, workspace-seat, metacognition, or consciousness claim.")
    return "\n".join(lines)


def main(argv):
    p = argparse.ArgumentParser()
    p.add_argument("--frozen", required=True)
    p.add_argument("--analysis", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args(argv)

    with open(os.path.join(args.frozen, "rows.jsonl")) as fh:
        rows = [json.loads(l) for l in fh if l.strip()]
    with open(os.path.join(args.analysis, "endpoints.json")) as fh:
        endpoints = json.load(fh)
    cross_fail = sum(1 for e in endpoints if not e["crosscheck"]["ok"])

    g = compute(rows, endpoints)
    os.makedirs(args.out, exist_ok=True)
    with open(os.path.join(args.out, "summary.json"), "w") as fh:
        json.dump(g, fh, indent=2, default=_default)
    md = _md(g, rows, args.frozen, cross_fail)
    with open(os.path.join(args.out, "PHASE3_FINALS_SUMMARY_v1.md"), "w") as fh:
        fh.write(md + "\n")
    print(md)


def _default(o):
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, np.generic):
        return o.item()
    raise TypeError(type(o))


if __name__ == "__main__":
    main(sys.argv[1:])
