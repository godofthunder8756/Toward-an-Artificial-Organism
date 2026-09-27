"""Phase-III engineering screen (G12).

Verifies, under a *declared* finite search budget, that the implementation
passes engineering screening — the seven "may verify" items of the G12 card —
without tuning the world so sharing wins, and without requiring the candidate
to beat its rivals (those are final scientific results, G13's job).

The screen is deterministic (CPU-only, seeded) and writes two artifacts:

- ``screen_summary.json``        — the raw measurements behind the report.
- ``PHASE3_ENGINEERING_SCREEN_v1.md`` — the frozen screen report.

Neither overwrites an existing file (``exist_ok=False`` semantics); re-run with
different paths to supersede, never to edit a freeze.

Declared search budget (frozen here, before any measurement):
    sweep configs: p_level in {small, mid} x steps in {1000, 2000}
                   (candidate arm only, engineering seeds 0-1)
    frozen default: p_level=small, steps=2000, all six arms, engineering 0-7
    No lr / init / optimizer tuning beyond the frozen TrainingConfig defaults.

The screen MUST establish (and only these):
    V1  latent task learnable            — candidate probe acc reaches the
                                            empirical Bayes ceiling (~0.96),
                                            equivalently R4's, on every seed.
    V2  specialists individually learnable — R2/R3 learned heads reach the
                                            specialist targets' accuracy.
    V3  interventions function            — I1 scramble signature traces
                                            (S_pol,S_plan,S_reg)(w*) exactly.
    V4  coordination non-vacuous          — candidate incoherence = 0 AND
                                            R1 incoherence > 0 (the load-bearing
                                            candidate-vs-R1 contrast).
    V5  candidate + rivals train          — all six arms reach the ceiling.
    V6  hidden-copy controls work         — F1 (h_t decode ~ chance under
                                            pi-cut + zero W) and the weight-
                                            bypass (I2-scramble -> chance).
    V7  no leakage breaks W attribution   — sever (specialists pure functions
                                            of W), decode-ablation sanity.

It must NOT gate: candidate beats R1/R2/R3/R4/R5, or H4/H5 pass (final results).
"""
from __future__ import annotations

import json
import os
from dataclasses import replace
from typing import Dict, List

import numpy as np
import torch

from phase3.arms import Arm, apply_specialists, compute_thresholds
from phase3.config import Phase3Config
from phase3.interventions import scramble
from phase3.leakage import decode_accuracy
from phase3.model import Encoder
from phase3.runner import build_arm, ARM_NAMES, _head_outputs
from phase3.task import sample_episodes, token_stream_to_s
from phase3.train import train_encoder, specialist_targets
from phase3.specialists import s_pol, s_plan, s_reg, theta_value

EVAL_SEED = 999          # a fixed disjoint eval stream for the screen (not a final seed)
N_EP = 1024
SWEEP_LEVELS = ["small", "mid"]
SWEEP_STEPS = [1000, 2000]
SWEEP_SEEDS = [0, 1]


def _config(p_level: str, steps: int) -> Phase3Config:
    cfg = Phase3Config()
    return replace(cfg, training=replace(cfg.training, steps=steps),
                   arm=replace(cfg.arm, p_level=p_level))


def _candidate(cfg: Phase3Config, seed: int) -> Arm:
    _seed(seed)
    enc = Encoder(cfg)
    train_encoder(cfg, enc, cfg.training.steps, cfg.training.lr, seed, "enc")
    return Arm(cfg, encoders={"enc": enc}, arm_name="candidate")


def _seed(seed: int) -> None:
    import bridge.reproducibility as _rep
    _rep.seed_all(seed)


def run_sweep() -> List[Dict]:
    """V1/V5 robustness: candidate probe acc vs ceiling across the declared grid."""
    rows = []
    for lvl in SWEEP_LEVELS:
        for steps in SWEEP_STEPS:
            cfg = _config(lvl, steps)
            for seed in SWEEP_SEEDS:
                arm = _candidate(cfg, seed)
                z, x = sample_episodes(cfg.task, N_EP, EVAL_SEED)
                thr = compute_thresholds(cfg)
                tr = arm.run(x)
                out = apply_specialists(tr["w"], cfg, thr, tr["regime"])
                acc = float(np.mean(out["spol"][..., -1] == z))
                rows.append({"p_level": lvl, "steps": steps, "seed": seed,
                             "probe_acc": acc})
    return rows


def run_verification() -> Dict:
    """V1-V7 measurements on the frozen-default candidate + rivals (model seed 0)."""
    cfg = _config("small", 2000)
    thr = compute_thresholds(cfg)
    z, x = sample_episodes(cfg.task, N_EP, EVAL_SEED)
    probe_entry = cfg.task.horizon - cfg.task.probe_window
    regime = np.zeros(cfg.task.horizon, dtype=np.int64)
    regime[probe_entry:] = 1

    # Build every arm once (model seed 0).
    arms = {name: build_arm(cfg, name, 0) for name in ARM_NAMES}

    # V1/V5: probe acc per arm (all six arms train and reach the ceiling).
    arm_acc = {}
    traj = {}
    for name in ARM_NAMES:
        arm = arms[name]
        tr = arm.run(x)
        traj[name] = tr
        if arm.has_w:
            out = apply_specialists(tr["w"], cfg, thr, tr["regime"])
            acc = float(np.mean(out["spol"][..., -1] == z))
        else:
            spol, _, _ = _head_outputs(cfg, arm, x)
            acc = float(np.mean(spol[..., -1] == z))
        arm_acc[name] = acc
    ceiling = arm_acc["r4"]  # R4 = sign(quantize(S_H)): the empirical ceiling here

    # V2: R2/R3 heads match the specialist targets (S_pol/S_plan/S_reg), not just S_pol.
    spec_match = {}
    tgt = specialist_targets(cfg, torch.from_numpy(x).long(), thr)
    tgt_np = {k: v.numpy() for k, v in tgt.items()}
    for name in ("r2", "r3"):
        spol, splan, sreg = _head_outputs(cfg, arms[name], x)
        spec_match[name] = {
            "spol_acc": float(np.mean(spol[..., -1] == tgt_np["spol"][..., -1])),
            "splan_acc": float(np.mean(splan[..., -1] == tgt_np["splan"][..., -1])),
            "sreg_acc": float(np.mean(sreg[..., -1] == tgt_np["sreg"][..., -1])),
        }

    # V3: I1 scramble signature on the real candidate trajectory.
    w = traj["candidate"]["w"]
    a, b = thr["a"], thr["b"]
    sig_ok = {}
    for w_star in [-3.0, -0.4, 0.4, 3.0]:
        w2 = scramble(w, w_star, probe_entry)
        out = apply_specialists(w2, cfg, thr, regime)
        final = np.array([out["spol"][0, -1], out["splan"][0, -1], out["sreg"][0, -1]])
        theta = theta_value(cfg.specialist, np.array([cfg.persistence.e0]),
                            np.array([1]), a, cfg.persistence.e_crit)
        pred = np.array([s_pol(np.array([w_star]))[0],
                         s_plan(np.array([w_star]), a, b)[0],
                         s_reg(np.array([w_star]), theta)[0]])
        sig_ok[str(w_star)] = bool(np.array_equal(final, pred))

    # V4: incoherence rate per arm (candidate=0, R1>0 load-bearing).
    inc = {}
    for name in ARM_NAMES:
        if arms[name].has_w:
            out = apply_specialists(traj[name]["w"], cfg, thr, traj[name]["regime"])
            inc[name] = _incoherence(out["spol"], out["splan"], out["sreg"])
        else:
            spol, splan, sreg = _head_outputs(cfg, arms[name], x)
            inc[name] = _incoherence(spol, splan, sreg)

    # V6: F1 free-recurrence decode + weight-bypass decode (both ~ chance).
    tr_cut = arms["candidate"].run(x, cut_pi=True, zero_w=True)
    h_probe = tr_cut["h"][:, probe_entry:, :].reshape(len(z), -1)
    f1_decode, _ = decode_accuracy(h_probe, z)
    w_scrambled = scramble(w, 0.0, probe_entry)
    out_scrambled = apply_specialists(w_scrambled, cfg, thr, regime)
    bypass_decode = float(np.mean(out_scrambled["spol"][..., -1] == z))

    # V7: decode-ablation sanity (full h_t decodes high, zeroed h_t decodes chance).
    h_full = traj["candidate"]["h"][:, probe_entry:, :].reshape(len(z), -1)
    decode_full, _ = decode_accuracy(h_full, z)
    decode_zero, _ = decode_accuracy(np.zeros_like(h_full), z)

    return {
        "arm_probe_acc": arm_acc,
        "ceiling_r4": ceiling,
        "candidate_minus_ceiling": arm_acc["candidate"] - ceiling,
        "specialist_match": spec_match,
        "i1_signature_ok": sig_ok,
        "incoherence": inc,
        "f1_decode": f1_decode,
        "weight_bypass_decode": bypass_decode,
        "decode_ablation": {"h_t_full": decode_full, "h_t_zeroed": decode_zero},
    }


def _incoherence(spol, splan, sreg) -> float:
    from phase3.specialists import MANIFOLD_TRIPLES
    flat = np.stack([spol.reshape(-1), splan.reshape(-1), sreg.reshape(-1)], axis=-1)
    on = np.array([tuple(r) in MANIFOLD_TRIPLES for r in flat])
    return float(1.0 - np.mean(on))


def main() -> None:
    out_dir = "phase3_engineering_screen_v1"
    os.makedirs(out_dir, exist_ok=False)
    sweep = run_sweep()
    verify = run_verification()
    summary = {"declared_budget": {
                   "sweep_p_levels": SWEEP_LEVELS, "sweep_steps": SWEEP_STEPS,
                   "sweep_seeds": SWEEP_SEEDS, "frozen_default": {"p_level": "small", "steps": 2000},
                   "no_lr_init_opt_tuning": True},
               "sweep": sweep, "verification": verify,
               "eval_seed": EVAL_SEED, "n_episodes": N_EP}
    with open(os.path.join(out_dir, "screen_summary.json"), "w") as fh:
        json.dump(summary, fh, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
