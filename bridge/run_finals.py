"""N11 final experiment runner — runs the untouched final experiment on the
frozen delta-decay scaffold.

Builds the FULL rival set (arms 7 reward-only, 8 multi-objective RL,
9 sufficient-statistic, 10 raw-bookkeeping direct policy P_rb) on top of the
frozen harness, runs every arm on the 12 final seeds (2000-2011), and applies
the frozen statistical plan (``TBRIDGE_STATISTICAL_PLAN_v1.md`` §4-§6):

  G-N1 (PRIMARY)   candidate vs no_maintenance on stable probe accuracy +
                   E1 slot survival (active paid persistence).
  G3b              candidate vs the swept fixed-level family (state-dependence).
  d_t-read         arm 9 (s,E) vs arm 9 (s,E,d) — the age-read necessity.
  ceiling          candidate vs oracle — one-sided equivalence, margin eps.

Plus the mechanistic controls (reward-removal, survival-decoupling, V and W
interventions, clock/generalization), the free-permanence control, and the
utility/resource tradeoff. All gates are FROZEN as constants before any result
is read; nothing is moved after results begin.

NOT claimed: any inferred-integrity result. The scaffold's integrity is OBSERVED
(I_t = f(d_t)); arms 9/10 collapse to the oracle by construction (N6/N7). The
N3c contrast is graded as "does the direct rival match the candidate", and if it
does the conclusion is "explicit maintained V was unnecessary in this task".

Usage:
    PYTHONPATH=. OPENBLAS_NUM_THREADS=1 .venv-bridge/bin/python -B \
        bridge/run_finals.py
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from dataclasses import replace

import torch

from bridge.config import BridgeConfig
from bridge import arms
from bridge import final_arms as fa
from bridge import exact_stats as st

# --------------------------------------------------------------------------- #
# FROZEN gate constants (declared before any result; do not edit after running)
# --------------------------------------------------------------------------- #
FINAL_SEEDS = [2000 + i for i in range(12)]   # N = 12
ALPHA = 0.01                                   # per-gate two-sided alpha (N7)
FAMILY_ALPHA = 0.05                            # family-wise over the 3 hypothesis gates
EQUIVALENCE_MARGIN = 0.05                      # ceiling attainment eps (op-score scale)
CHANCE = 0.5                                   # the free-permanence / arm-2-at-chance reference
FIXED_PERIODS = [1, 2, 4, 8, 16, 32, 64]       # swept fixed-level family (1=always, 64=~never)
REWARD_REMOVAL_SEEDS = [2000, 2001, 2002]      # controls run on a final-seed subset
CLOCK_CHECKS = [
    {"name": "announce_early", "decay": {"announce_m": 8}},
    {"name": "announce_late", "decay": {"announce_m": 24}},
    {"name": "delay_long", "decay": {"delay_d": 48}, "episode": {"horizon_t": 80}},
]

RESULTS_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "finals_v1"
)

SOURCE_PATHS = [
    "bridge/__init__.py",
    "bridge/config.py",
    "bridge/reproducibility.py",
    "bridge/episodes.py",
    "bridge/modules.py",
    "bridge/substrate.py",
    "bridge/agent.py",
    "bridge/env.py",
    "bridge/trainer.py",
    "bridge/arms.py",
    "bridge/final_arms.py",
    "bridge/exact_stats.py",
    "bridge/run_finals.py",
]

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def op_score(e: dict) -> float:
    """Operation score: hold in stable, release in volatile (v3 §8.3).

    ``0.5 * stable_slot_surv + 0.5 * (1 - volatile_slot_surv)`` — the fraction
    of episodes whose allocation matches the regime (correct allocation is
    regime-conditional). A state-blind fixed level scores ~0.5; the oracle 1.0.
    """
    return 0.5 * e["stable_slot_surv"] + 0.5 * (1.0 - e["volatile_slot_surv"])


# --------------------------------------------------------------------------- #
# Training the trained arms
# --------------------------------------------------------------------------- #

def train_all_arms(cfg: BridgeConfig, ckpt_dir: str) -> dict:
    """Train the four trained arms on every final seed; return a nested dict
    ``{seed: {arm_name: trainer}}``. Runs the frozen candidate trainer plus the
    three rival trainers (arm 7 reward, arm 8 multi, arm 10 homeo).

    Checkpoints each (seed, arm) trainer to ``ckpt_dir`` so a re-run that hits a
    later-phase bug reloads instead of re-training (idempotent: identical seeds
    reproduce identical weights)."""
    steps = cfg.training.training_episodes // cfg.training.batch_size
    batch_size = cfg.training.batch_size
    os.makedirs(ckpt_dir, exist_ok=True)
    out = {}
    for seed in FINAL_SEEDS:
        out[seed] = {}
        t0 = time.time()
        cand = _load_or_train_candidate(cfg, seed, steps, batch_size,
                                        os.path.join(ckpt_dir, f"cand_{seed}.pt"))
        t1 = time.time()
        out[seed]["candidate"] = cand
        for key, objective in [("arm10_P_rb", "homeo"),
                               ("arm7_reward", "reward"),
                               ("arm8_multi", "multi")]:
            out[seed][key] = _load_or_train_rival(
                cfg, seed, objective, steps, batch_size,
                os.path.join(ckpt_dir, f"{key}_{seed}.pt"))
        t4 = time.time()
        print(f"  seed {seed}: candidate {t1-t0:.0f}s  rivals {t4-t1:.0f}s",
              flush=True)
    return out


def _load_or_train_candidate(cfg, seed, steps, batch_size, ckpt_path):
    if os.path.exists(ckpt_path):
        from bridge.trainer import BridgeTrainer
        return BridgeTrainer.load_checkpoint(ckpt_path)
    trainer, _ = arms.train_candidate(cfg, seed, steps, batch_size)
    trainer.save_checkpoint(ckpt_path)
    return trainer


def _load_or_train_rival(cfg, seed, objective, steps, batch_size, ckpt_path):
    if os.path.exists(ckpt_path):
        trainer = fa.RivalTrainer(cfg, seed, objective)
        ckpt = torch.load(ckpt_path, map_location="cpu", weights_only=False)
        trainer.rival.load_state_dict(ckpt["rival"])
        return trainer
    trainer, _ = fa.train_rival(cfg, seed, objective, steps, batch_size)
    torch.save({"rival": trainer.rival.state_dict()}, ckpt_path)
    return trainer


def evaluate_all_arms(cfg: BridgeConfig, trainers: dict) -> list:
    """Evaluate every arm on every final seed; return a list of per-seed rows."""
    eval_episodes = cfg.training.eval_episodes
    rows = []

    for seed in FINAL_SEEDS:
        tr = trainers[seed]

        # trained arms
        cand = fa.evaluate_episodes_uniform(
            cfg, seed, eval_episodes,
            runner=lambda b, t=tr["candidate"]: fa.evaluate_candidate_full(t, b))
        p_rb = fa.evaluate_episodes_uniform(
            cfg, seed, eval_episodes,
            runner=lambda b, t=tr["arm10_P_rb"]: fa.evaluate_rival(t, b))
        r7 = fa.evaluate_episodes_uniform(
            cfg, seed, eval_episodes,
            runner=lambda b, t=tr["arm7_reward"]: fa.evaluate_rival(t, b))
        r8 = fa.evaluate_episodes_uniform(
            cfg, seed, eval_episodes,
            runner=lambda b, t=tr["arm8_multi"]: fa.evaluate_rival(t, b))

        # fixed arms
        no_maint = fa.evaluate_episodes_uniform(
            cfg, seed, eval_episodes,
            runner=lambda b: fa.run_fixed_with_probe(cfg, b, arms.action_never))
        free_mem = fa.evaluate_episodes_uniform(
            cfg, seed, eval_episodes,
            runner=lambda b: fa.run_fixed_with_probe(
                cfg, b, arms.action_never, write_cue=False))
        oracle = fa.evaluate_episodes_uniform(
            cfg, seed, eval_episodes,
            runner=lambda b: fa.run_fixed_with_probe(cfg, b, arms.action_oracle))
        arm9_d = fa.evaluate_episodes_uniform(
            cfg, seed, eval_episodes,
            runner=lambda b: fa.run_fixed_with_probe(cfg, b, fa.arm9_d))
        arm9_nod = fa.evaluate_episodes_uniform(
            cfg, seed, eval_episodes,
            runner=lambda b: fa.run_fixed_with_probe(cfg, b, fa.arm9_nod(16)))

        fixed_levels = {}
        for period in FIXED_PERIODS:
            fixed_levels[f"fixed_p{period}"] = fa.evaluate_episodes_uniform(
                cfg, seed, eval_episodes,
                runner=lambda b, p=period: fa.run_fixed_with_probe(
                    cfg, b, arms.action_fixed(p)))

        def row(arm_name, endpoints):
            return {"seed": seed, "arm": arm_name,
                    "op_score": op_score(endpoints), **endpoints}

        rows.append(row("candidate", cand))
        rows.append(row("no_maintenance", no_maint))
        rows.append(row("free_memory", free_mem))
        rows.append(row("oracle", oracle))
        rows.append(row("arm9_d", arm9_d))
        rows.append(row("arm9_nod", arm9_nod))
        rows.append(row("arm10_P_rb", p_rb))
        rows.append(row("arm7_reward", r7))
        rows.append(row("arm8_multi", r8))
        for name, e in fixed_levels.items():
            rows.append(row(name, e))

    return rows


# --------------------------------------------------------------------------- #
# Statistical plan
# --------------------------------------------------------------------------- #

def _by_arm(rows: list, arm: str) -> dict:
    return {r["seed"]: r for r in rows if r["arm"] == arm}


def _endpoint_series(by_seed: dict, key: str, seeds: list) -> list:
    return [by_seed[s][key] for s in seeds]


def compute_gates(rows: list) -> dict:
    """Apply the frozen statistical plan's hypothesis gates + controls."""
    seeds = sorted({r["seed"] for r in rows})
    g = {}

    cand = _by_arm(rows, "candidate")
    no_maint = _by_arm(rows, "no_maintenance")
    free_mem = _by_arm(rows, "free_memory")
    oracle = _by_arm(rows, "oracle")
    arm9_d = _by_arm(rows, "arm9_d")
    arm9_nod = _by_arm(rows, "arm9_nod")
    p_rb = _by_arm(rows, "arm10_P_rb")

    # ---- G-N1 (PRIMARY): candidate vs no_maintenance --------------------- #
    c_slot = _endpoint_series(cand, "stable_slot_surv", seeds)
    n_slot = _endpoint_series(no_maint, "stable_slot_surv", seeds)
    c_probe = _endpoint_series(cand, "stable_probe_correct", seeds)
    f_slot = _endpoint_series(free_mem, "stable_slot_surv", seeds)

    g["G_N1"] = {
        "endpoint": "stable probe accuracy + slot survival (active paid persistence)",
        "candidate_stable_slot_mean": sum(c_slot) / len(c_slot),
        "no_maintenance_stable_slot_mean": sum(n_slot) / len(n_slot),
        "candidate_stable_probe_mean": sum(c_probe) / len(c_probe),
        "free_memory_stable_slot_mean": sum(f_slot) / len(f_slot),
        "slot_effect": st.paired_effect(c_slot, n_slot),
        "slot_signflip": st.sign_flip_test([a - b for a, b in zip(c_slot, n_slot)]),
        "probe_effect": st.paired_effect(c_probe, n_slot),
    }

    # free-permanence: without paid W the cue is unrecoverable. The slot-survival
    # read is the deterministic E1 quantity (0 = cue lost). "Probe at chance" is
    # demonstrated causally by the W-intervention (force-drop -> candidate S_pol
    # at chance), not by inventing a probe for a fixed arm.
    g["G_N1"]["free_permanence"] = {
        "no_maintenance_stable_slot_mean": sum(n_slot) / len(n_slot),
        "free_memory_stable_slot_mean": sum(f_slot) / len(f_slot),
        "cue_unrecoverable_without_paid_W": (
            all(x == 0.0 for x in n_slot) and all(x == 0.0 for x in f_slot)
        ),
        "at_chance_readout": "W_intervention.force_drop (candidate S_pol on neutral slot)",
    }

    # ---- G3b: candidate vs swept fixed-level family ---------------------- #
    cand_op = [op_score(cand[s]) for s in seeds]
    g["G3b"] = {"family_periods": FIXED_PERIODS, "levels": {}, "dominance": None}
    best_level_op = -1.0
    best_level_name = None
    all_strictly_better = True
    for period in FIXED_PERIODS:
        name = f"fixed_p{period}"
        lvl = _by_arm(rows, name)
        lvl_op = [op_score(lvl[s]) for s in seeds]
        eff = st.paired_effect(cand_op, lvl_op)
        sf = st.sign_flip_test([a - b for a, b in zip(cand_op, lvl_op)])
        lvl_mean = sum(lvl_op) / len(lvl_op)
        g["G3b"]["levels"][name] = {
            "level_op_mean": lvl_mean,
            "candidate_op_mean": sum(cand_op) / len(cand_op),
            "effect": eff,
            "signflip": sf,
        }
        if lvl_mean > best_level_op:
            best_level_op = lvl_mean
            best_level_name = name
        if not all(a > b for a, b in zip(cand_op, lvl_op)):
            all_strictly_better = False
    g["G3b"]["best_level"] = {"name": best_level_name, "op_mean": best_level_op}
    g["G3b"]["dominance"] = {
        "candidate_strictly_better_than_every_level_in_every_seed": all_strictly_better,
        "candidate_op_mean": sum(cand_op) / len(cand_op),
    }

    # ---- d_t-read necessity: arm9_d vs arm9_nod -------------------------- #
    d_op = [op_score(arm9_d[s]) for s in seeds]
    nod_op = [op_score(arm9_nod[s]) for s in seeds]
    g["d_t_read"] = {
        "arm9_d_op_mean": sum(d_op) / len(d_op),
        "arm9_nod_op_mean": sum(nod_op) / len(nod_op),
        "effect": st.paired_effect(d_op, nod_op),
        "signflip": st.sign_flip_test([a - b for a, b in zip(d_op, nod_op)]),
    }

    # ---- ceiling attainment: candidate vs oracle (one-sided equivalence) - #
    o_op = [op_score(oracle[s]) for s in seeds]
    diffs_ceiling = [a - b for a, b in zip(cand_op, o_op)]
    g["ceiling"] = {
        "oracle_op_mean": sum(o_op) / len(o_op),
        "candidate_op_mean": sum(cand_op) / len(cand_op),
        "mean_candidate_minus_oracle": sum(diffs_ceiling) / len(diffs_ceiling),
        "min_candidate_minus_oracle": min(diffs_ceiling),
        "equivalence_margin": EQUIVALENCE_MARGIN,
        "within_margin_every_seed": all(d >= -EQUIVALENCE_MARGIN for d in diffs_ceiling),
        "effect": st.paired_effect(cand_op, o_op),
    }

    # ---- N3c: candidate vs P_rb (the direct raw-bookkeeping rival) ------- #
    p_op = [op_score(p_rb[s]) for s in seeds]
    p_slot = _endpoint_series(p_rb, "stable_slot_surv", seeds)
    g["N3c_same_information"] = {
        "endpoint": "candidate vs raw-bookkeeping direct policy (P_rb) on op score",
        "candidate_op_mean": sum(cand_op) / len(cand_op),
        "P_rb_op_mean": sum(p_op) / len(p_op),
        "candidate_stable_slot_mean": sum(c_slot) / len(c_slot),
        "P_rb_stable_slot_mean": sum(p_slot) / len(p_slot),
        "effect": st.paired_effect(cand_op, p_op),
        "signflip": st.sign_flip_test([a - b for a, b in zip(cand_op, p_op)]),
    }

    return g


# --------------------------------------------------------------------------- #
# Controls
# --------------------------------------------------------------------------- #

def compute_controls(cfg: BridgeConfig, trainers: dict) -> dict:
    """Mechanistic controls + free-permanence + V-intervention (N3a) +
    utility/resource tradeoff. Run on the final sample (controls on a subset
    where a fresh forward is needed)."""
    ctrl = {}

    # V-intervention (N3a): does A's P(refresh) depend on the integrity code?
    integ_deps, energy_deps = [], []
    policy_tables = {}
    for seed in REWARD_REMOVAL_SEEDS:
        tr = trainers[seed]["candidate"]
        dep = fa.allocator_dependence(tr)
        integ_deps.append(dep["integrity_dep"])
        energy_deps.append(dep["energy_dep"])
        policy_tables[f"seed_{seed}"] = dep["policy_table"]
    ctrl["N3a_V_intervention"] = {
        "integrity_dep_mean": sum(integ_deps) / len(integ_deps),
        "integrity_dep_per_seed": integ_deps,
        "energy_dep_mean": sum(energy_deps) / len(energy_deps),
        "policy_tables": policy_tables,
    }

    # reward-removal (G3c) and survival-decoupling (G3d): re-run the frozen
    # unit checks directly on the final-seed-trained candidates.
    rm_rows, sd_rows = [], []
    for seed in REWARD_REMOVAL_SEEDS:
        tr = trainers[seed]["candidate"]
        rm_rows.append(_check_reward_invariant(tr, cfg))
        sd_rows.append(_check_survival_blind(tr, cfg))
    ctrl["G3c_reward_removal"] = {
        "per_seed": rm_rows,
        "pass": all(r["reward_adds_zero_A_policy_grad"] for r in rm_rows),
        "note": "zero/randomize the probe reward: A's policy head receives no "
                "reward gradient (reward reaches S_pol only), so E_pi is invariant.",
    }
    ctrl["G3d_survival_decoupling"] = {
        "per_seed": sd_rows,
        "pass": all(r["cost_survival_blind"] for r in sd_rows),
        "note": "remove the death threshold + zero reward: the homeostatic cost "
                "c_homeo is a function of (regime,E,age) only, never alive, so "
                "A keeps regulating I_t toward I*.",
    }

    # free-permanence: no auxiliary recurrent state solves the deferred-cue
    # task without paid W (free_memory = W read-in disabled -> probe at chance).
    ctrl["free_permanence"] = {
        "free_memory_W_readin_disabled": True,
        "note": "free_memory (W read-in disabled, recurrent state present) must "
                "be at chance in stable; measured in G_N1.free_memory_at_chance.",
    }

    # W-intervention: force-hold vs force-drop -> probe accuracy changes
    from bridge.env import BridgeEnv
    from bridge.reproducibility import seed_all
    w_ctrl = {}
    for seed in REWARD_REMOVAL_SEEDS:
        tr = trainers[seed]["candidate"]
        env = BridgeEnv(cfg)
        seed_all(seed)
        batch = env.sample(512)
        B, T = batch["x"].shape[:2]
        hold = fa.run_candidate_forced(
            tr, batch, forced_action=torch.ones(B, T))
        drop = fa.run_candidate_forced(
            tr, batch, forced_action=torch.zeros(B, T))
        stable = batch["regime_class"] == 0
        w_ctrl[f"seed_{seed}"] = {
            "force_hold_stable_probe": float(hold["probe_correct"][stable].mean()),
            "force_drop_stable_probe": float(drop["probe_correct"][stable].mean()),
            "force_hold_stable_slot": float(hold["slot_surv"][stable].mean()),
            "force_drop_stable_slot": float(drop["slot_surv"][stable].mean()),
        }
    ctrl["W_intervention"] = w_ctrl

    # clock/generalization: run the trained candidate forward under a shifted
    # announce/delay/horizon by loading its weights into a bridge built from the
    # alternate config (dims are unchanged, so the state dict transfers).
    from bridge.agent import NeuralBridge
    from bridge.env import BridgeEnv as BE
    from bridge.reproducibility import seed_all as sa
    clock = {}
    for chk in CLOCK_CHECKS:
        alt = cfg
        if "decay" in chk:
            alt = replace(alt, decay=replace(alt.decay, **chk["decay"]))
        if "episode" in chk:
            alt = replace(alt, episode=replace(alt.episode, **chk["episode"]))
        vals = []
        for seed in REWARD_REMOVAL_SEEDS:
            tr = trainers[seed]["candidate"]
            bridge_alt = NeuralBridge(alt)
            bridge_alt.load_state_dict(tr.bridge.state_dict())
            sa(seed)
            env = BE(alt)
            batch = env.sample(512)
            B = batch["x"].shape[0]
            T = batch["x"].shape[1]
            # run the alt bridge forward directly (no forced action)
            out = bridge_alt(batch["x"], batch["cue"], batch["regime"],
                             batch["correct"])
            probe_tick = min(alt.decay.delay_d, T - 1)
            stable = batch["regime_class"] == 0
            held = (out["slot"][:, probe_tick, 0] != 0.0).float()
            vals.append(float(held[stable].mean()))
        clock[chk["name"]] = {"stable_slot_surv_per_seed": vals,
                              "mean": sum(vals) / len(vals)}
    ctrl["clock_generalization"] = clock

    return ctrl


def _check_reward_invariant(trainer, cfg) -> dict:
    """G3c structural check: reward/probe/L_V/critic losses add zero gradient
    to A's policy head (mirrors the frozen test_allocator_invariant_to_reward)."""
    from bridge.trainer import compute_losses
    batch = trainer.env.sample(16)
    out = trainer.bridge(batch["x"], batch["cue"], batch["regime"], batch["correct"])
    losses, _ = compute_losses(cfg, out, batch)

    def a_grad(loss):
        trainer.bridge.zero_grad(set_to_none=True)
        loss.backward(retain_graph=True)
        total = 0.0
        for n, p in trainer.bridge.named_parameters():
            if n.startswith("allocator.policy") and p.grad is not None:
                total += float(p.grad.abs().sum().item())
        return total

    joint = losses["J_A_policy"] + losses["probe"] + losses["L_V"] + losses["J_A_critic"]
    g_joint = a_grad(joint)
    g_alone = a_grad(losses["J_A_policy"])
    return {
        "reward_adds_zero_A_policy_grad": abs(g_joint - g_alone) < 1e-5,
        "g_joint": g_joint, "g_alone": g_alone,
    }


def _check_survival_blind(trainer, cfg) -> dict:
    """G3d structural check: c_homeo is invariant to the alive mask (mirrors
    the frozen test_homeostatic_cost_is_survival_blind)."""
    from bridge.trainer import compute_losses
    batch = trainer.env.sample(16)
    out = trainer.bridge(batch["x"], batch["cue"], batch["regime"], batch["correct"])
    _, m1 = compute_losses(cfg, out, batch)
    out_dead = {**out, "alive": torch.zeros_like(out["alive"])}
    _, m_dead = compute_losses(cfg, out_dead, batch)
    return {
        "cost_survival_blind": bool(
            torch.equal(m_dead["mean_cost"], m1["mean_cost"])
            and torch.equal(m_dead["J_A_policy"], m1["J_A_policy"])
        ),
        "mean_cost_live": float(m1["mean_cost"]),
        "mean_cost_dead": float(m_dead["mean_cost"]),
    }


# --------------------------------------------------------------------------- #
# Utility / resource tradeoff
# --------------------------------------------------------------------------- #

def compute_tradeoff(rows: list) -> dict:
    """Per-arm, per-regime utility + resource tradeoff (probe performance,
    maintenance expenditure (refresh rate), processing expenditure (fixed
    e_proc), energy trajectories (E_final), operation rate (survival), and
    continued operation)."""
    arms_of_interest = ["candidate", "no_maintenance", "oracle", "arm9_d",
                        "arm10_P_rb", "arm7_reward", "arm8_multi"]
    out = {}
    for arm in arms_of_interest:
        sub = [r for r in rows if r["arm"] == arm]
        def mean(key):
            return sum(r[key] for r in sub) / len(sub)
        out[arm] = {
            "stable_probe_correct": mean("stable_probe_correct"),
            "volatile_probe_correct": mean("volatile_probe_correct"),
            "stable_slot_surv": mean("stable_slot_surv"),
            "volatile_slot_surv": mean("volatile_slot_surv"),
            "stable_refresh": mean("stable_refresh"),
            "volatile_refresh": mean("volatile_refresh"),
            "stable_survival": mean("stable_survival"),
            "volatile_survival": mean("volatile_survival"),
            "stable_E_final": mean("stable_E_final"),
            "volatile_E_final": mean("volatile_E_final"),
            "op_score": mean("op_score"),
        }
    return out


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #

def main() -> None:
    cfg = BridgeConfig()

    os.makedirs(RESULTS_DIR, exist_ok=False)

    snapshot = {
        "study": "bridge final experiment v1 (N11)",
        "sources": {rel: sha256_file(os.path.join(REPO_ROOT, rel))
                    for rel in SOURCE_PATHS},
        "config": cfg.to_dict(),
        "final_seeds": FINAL_SEEDS,
        "gate_constants": {
            "alpha": ALPHA, "family_alpha": FAMILY_ALPHA,
            "equivalence_margin": EQUIVALENCE_MARGIN,
            "chance": CHANCE, "fixed_periods": FIXED_PERIODS,
            "reward_removal_seeds": REWARD_REMOVAL_SEEDS,
        },
        "protocol_refs": [
            "ACI_BRIDGE_PROTOCOL_v3.md",
            "TBRIDGE_IDENTIFIABILITY_v1.md",
            "TBRIDGE_STATISTICAL_PLAN_v1.md",
        ],
        "stop_note": (
            "delta-decay scaffold: integrity I_t = f(d_t) is OBSERVED, not inferred. "
            "Arms 9/10 collapse to the oracle (N6/N7); N3c graded as 'does the direct "
            "rival match the candidate' -> if yes, explicit maintained V is unnecessary."
        ),
    }
    with open(os.path.join(RESULTS_DIR, "pre_run_snapshot.json"), "w") as fh:
        json.dump(snapshot, fh, indent=2)

    print("=== training all arms on final seeds ===", flush=True)
    t0 = time.time()
    trainers = train_all_arms(cfg, os.path.join(RESULTS_DIR, "checkpoints"))
    print(f"training complete: {time.time()-t0:.0f}s", flush=True)

    print("=== evaluating all arms ===", flush=True)
    rows = evaluate_all_arms(cfg, trainers)

    with open(os.path.join(RESULTS_DIR, "rows.jsonl"), "w") as fh:
        for r in rows:
            fh.write(json.dumps(r))
            fh.write("\n")

    print("=== computing gates ===", flush=True)
    gates = compute_gates(rows)
    print("=== computing controls ===", flush=True)
    controls = compute_controls(cfg, trainers)
    tradeoff = compute_tradeoff(rows)

    results = {"gates": gates, "controls": controls, "tradeoff": tradeoff}
    with open(os.path.join(RESULTS_DIR, "results.json"), "w") as fh:
        json.dump(results, fh, indent=2)

    print("\n===== RESULTS =====")
    print(json.dumps(gates, indent=2))
    print("\ncontrols:")
    print(json.dumps({k: v for k, v in controls.items()
                      if k != "N3a_V_intervention"}, indent=2))

    print(f"\nresults saved to {RESULTS_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
