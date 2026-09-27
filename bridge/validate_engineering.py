"""N10 engineering validation driver for the neural bridge scaffold.

Runs the six engineering checks on engineering seeds [0, 1, 2] and freezes the
result: a versioned results dir with a ``pre_run_snapshot.json`` (sha256 of
every frozen source) and a ``results.json`` (the measured endpoints).

The six checks (N10 card, engineering seeds only):

  1. learning converges            -- candidate losses decrease.
  2. economy non-vacuous           -- the oracle holds the cue at the probe while
                                      no-maintenance loses it (maintenance pays).
  3. maintenance/dropping locally  -- stable: refresh + hold; volatile: drop
      rational                        (the oracle does this by construction; the
                                      candidate learns it).
  4. candidate/rivals/interventions -- the arms run and produce distinct,
      function                        correct endpoints; forced refresh/hold
                                      interventions are causal (unit-tested).
  5. free-memory control           -- W read-in disabled -> readout neutral
                                      (probe at chance; the cue has no path to
                                      the probe except W).
  6. information paths match       -- gradient-path and cue-leakage checks
      the protocol                   re-run programmatically.

The frozen config is ``BridgeConfig()`` — the dataclass defaults now carry the
tuned training hyperparameters (a_entropy_weight=0.1, lr_a_policy=1e-2,
training_episodes=64000, eval_episodes=2048, batch_size=64), chosen under the
declared finite search budget recorded in BRIDGE_ENGINEERING_v1.md. Engineering
seeds 0-2 are excluded from the final sample (disjoint families, AC39); N11's
finals are 2000-2011.

NOT frozen, NOT claimed: the bridge's central question. Per N6/N6b and the
v3/v4 protocol STOPs, the delta-decay scaffold's integrity is OBSERVED
(I_t = f(d_t)), not inferred; the central contrast is unidentifiable by
construction and no statistical plan exists (N7b). This run validates the
scaffold's mechanics only and must not be read as an inferred-integrity
experiment.

Usage:
    PYTHONPATH=. .venv-bridge/bin/python -B bridge/validate_engineering.py
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import replace

import torch

from bridge.config import BridgeConfig
from bridge import arms

ENGINEERING_SEEDS = [0, 1, 2]
FINAL_SEEDS = [2000 + i for i in range(12)]  # N11's finals (N=12)

RESULTS_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "engineering_v1"
)

# Frozen sources hashed into the snapshot (simulation code + machinery). The
# verification tools (bridge/tests/*) are intentionally NOT hashed: they are
# not part of the frozen source of truth (see the research skill).
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
    "bridge/run.py",
    "bridge/arms.py",
    "bridge/validate_engineering.py",
    "bridge/configs/default.yaml",
]

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def build_snapshot(cfg: BridgeConfig) -> dict:
    sources = {}
    for rel in SOURCE_PATHS:
        p = os.path.join(REPO_ROOT, rel)
        sources[rel] = sha256_file(p)
    return {
        "study": "bridge engineering validation v1 (N10)",
        "sources": sources,
        "config": cfg.to_dict(),
        "engineering_seeds": ENGINEERING_SEEDS,
        "final_seeds": FINAL_SEEDS,
        "protocol_refs": [
            "ACI_BRIDGE_PROTOCOL_v3.md",
            "ACI_BRIDGE_PROTOCOL_v4.md",
            "TBRIDGE_IDENTIFIABILITY_v1.md",
            "TBRIDGE_IDENTIFIABILITY_v2.md",
            "TBRIDGE_STATISTICAL_PLAN_v1.md",
            "TBRIDGE_STATISTICAL_PLAN_v2.md",
        ],
        "stop_note": (
            "The bridge's central contrast is unidentifiable (N6/N6b; v3/v4 STOP). "
            "This scaffold realizes the delta-decay design whose integrity "
            "I_t = f(d_t) is OBSERVED, not inferred. No inferred-integrity claim "
            "is frozen or presented here."
        ),
    }


# --------------------------------------------------------------------------- #
# Info-path checks (inlined from the unit suite so results.json carries them)
# --------------------------------------------------------------------------- #

def _grad_components(bridge, loss):
    bridge.zero_grad()
    loss.backward()
    comps = set()
    for name, p in bridge.named_parameters():
        if p.grad is not None and p.grad.abs().sum() > 0:
            if name.startswith("controller."):
                comps.add("gru")
            elif name.startswith("v_estimator."):
                comps.add("f_V")
            elif name.startswith("allocator.policy"):
                comps.add("A_policy")
            elif name.startswith("allocator.critic"):
                comps.add("A_critic")
            elif name.startswith("probe."):
                comps.add("S_pol")
            else:
                comps.add(name)
    return comps


def check_info_paths(cfg: BridgeConfig) -> dict:
    from bridge.trainer import BridgeTrainer, compute_losses
    from bridge.agent import NeuralBridge
    from bridge.env import BridgeEnv
    from bridge.reproducibility import seed_all

    trainer = BridgeTrainer(cfg, seed=2)
    batch = trainer.env.sample(16)
    out = trainer.bridge(batch["x"], batch["cue"], batch["regime"], batch["correct"])
    losses, _ = compute_losses(cfg, out, batch)

    gradient_paths = {
        "L_V": sorted(_grad_components(trainer.bridge, losses["L_V"])),
        "J_A_policy": sorted(_grad_components(trainer.bridge, losses["J_A_policy"])),
        "J_A_critic": sorted(_grad_components(trainer.bridge, losses["J_A_critic"])),
        "probe": sorted(_grad_components(trainer.bridge, losses["probe"])),
    }

    # Cue leakage: with lifetime > horizon the cue survives, so the flip is
    # visible; it must show only in the slot and the probe readout.
    leak_cfg = replace(cfg, decay=replace(cfg.decay, lifetime=100))
    env = BridgeEnv(leak_cfg)
    bridge = NeuralBridge(leak_cfg)
    seed_all(11)
    batch_a = env.sample(16)
    batch_b = {**batch_a, "cue": -batch_a["cue"]}
    seed_all(11)
    out_a = bridge(batch_a["x"], batch_a["cue"], batch_a["regime"], batch_a["correct"])
    seed_all(11)
    out_b = bridge(batch_b["x"], batch_b["cue"], batch_b["regime"], batch_b["correct"])
    non_slot_keys = [
        "h", "v", "v_logits", "b", "refresh_logit", "refresh_prob", "refresh",
        "logp", "value", "energy", "age", "alive", "spend",
    ]
    cue_leakage = {
        "non_slot_channels_identical": all(
            torch.equal(out_a[k], out_b[k]) for k in non_slot_keys
        ),
        "slot_differs": not torch.equal(out_a["slot"], out_b["slot"]),
        "probe_differs": not torch.equal(out_a["probe_logits"], out_b["probe_logits"]),
    }

    return {"gradient_paths": gradient_paths, "cue_leakage": cue_leakage}


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #

def main() -> None:
    cfg = BridgeConfig()  # frozen defaults (tuned training hyperparameters)
    steps = cfg.training.training_episodes // cfg.training.batch_size
    batch_size = cfg.training.batch_size
    eval_episodes = cfg.training.eval_episodes

    os.makedirs(RESULTS_DIR, exist_ok=False)

    snapshot = build_snapshot(cfg)
    with open(os.path.join(RESULTS_DIR, "pre_run_snapshot.json"), "w") as fh:
        json.dump(snapshot, fh, indent=2)

    results: dict = {"arms": [], "convergence": {}, "checks": {}}

    # -- 1. learning converges + candidate behavior (seeds 0,1,2) ----------- #
    convergence = {}
    candidate_endpoints = []
    metrics_lines = []
    for seed in ENGINEERING_SEEDS:
        trainer, history = arms.train_candidate(cfg, seed, steps, batch_size)
        first, last = history[0], history[-1]
        convergence[f"seed_{seed}"] = {
            "L_V_first": first["L_V"], "L_V_last": last["L_V"],
            "J_A_critic_first": first["J_A_critic"], "J_A_critic_last": last["J_A_critic"],
            "probe_first": first["probe"], "probe_last": last["probe"],
            "entropy_first": first.get("entropy", None),
            "entropy_last": last.get("entropy", None),
        }
        endp = arms.evaluate_episodes(
            cfg, seed=seed, n_episodes=eval_episodes,
            runner=lambda b: arms.evaluate_candidate(trainer, b),
        )
        candidate_endpoints.append(endp)
        for i, row in enumerate(history):
            row = dict(row)
            row["seed"] = seed
            metrics_lines.append(row)

    with open(os.path.join(RESULTS_DIR, "metrics.jsonl"), "w") as fh:
        for row in metrics_lines:
            fh.write(json.dumps(row))
            fh.write("\n")

    cand_avg = {
        k: sum(e[k] for e in candidate_endpoints) / len(candidate_endpoints)
        for k in candidate_endpoints[0]
    }
    results["arms"].append(arms.arm_summary("candidate", cand_avg))

    # -- 2/3/4/5. fixed-policy arms + free-memory --------------------------- #
    fixed_rules = [
        ("no_maintenance", arms.action_never),
        ("oracle", arms.action_oracle),
        ("always", arms.action_always),
        ("fixed_p16", arms.action_fixed(16)),
        ("fixed_p4", arms.action_fixed(4)),
    ]
    for name, rule in fixed_rules:
        eps = [
            arms.evaluate_episodes(
                cfg, seed=seed, n_episodes=eval_episodes,
                runner=lambda b, r=rule: arms.run_fixed_policy(cfg, b, r),
            )
            for seed in ENGINEERING_SEEDS
        ]
        avg = {k: sum(e[k] for e in eps) / len(eps) for k in eps[0]}
        results["arms"].append(arms.arm_summary(name, avg))

    free_mem = arms.evaluate_episodes(
        cfg, seed=0, n_episodes=eval_episodes,
        runner=lambda b: arms.run_fixed_policy(cfg, b, arms.action_never, write_cue=False),
    )
    results["arms"].append(arms.arm_summary("free_memory", free_mem))

    # -- checks (from the measured endpoints) ------------------------------- #
    oracle = next(a for a in results["arms"] if a["arm"] == "oracle")
    never = next(a for a in results["arms"] if a["arm"] == "no_maintenance")
    results["checks"]["economy_non_vacuous"] = {
        "oracle_stable_slot_surv": oracle["stable_slot_surv"],
        "no_maintenance_stable_slot_surv": never["stable_slot_surv"],
        "pass": oracle["stable_slot_surv"] > 0.9 and never["stable_slot_surv"] < 0.1,
    }
    results["checks"]["locally_rational"] = {
        "oracle_stable_refresh": oracle["stable_refresh"],
        "oracle_volatile_refresh": oracle["volatile_refresh"],
        "candidate_stable_refresh": cand_avg["stable_refresh"],
        "candidate_volatile_refresh": cand_avg["volatile_refresh"],
        "candidate_stable_slot_surv": cand_avg["stable_slot_surv"],
        "candidate_volatile_slot_surv": cand_avg["volatile_slot_surv"],
        "pass": (
            oracle["stable_refresh"] > oracle["volatile_refresh"]
            and cand_avg["stable_refresh"] > cand_avg["volatile_refresh"]
            and cand_avg["stable_slot_surv"] > cand_avg["volatile_slot_surv"]
        ),
    }
    results["checks"]["free_memory"] = {
        "slot_surv_stable": free_mem["stable_slot_surv"],
        "slot_surv_volatile": free_mem["volatile_slot_surv"],
        "pass": free_mem["stable_slot_surv"] < 0.1,
    }
    results["checks"]["info_paths"] = check_info_paths(cfg)
    results["convergence"] = convergence

    with open(os.path.join(RESULTS_DIR, "results.json"), "w") as fh:
        json.dump(results, fh, indent=2)

    print("engineering validation complete:", RESULTS_DIR)
    for arm in results["arms"]:
        print(
            f"  {arm['arm']:14s} stable_slot={arm['stable_slot_surv']:.3f} "
            f"vol_slot={arm['volatile_slot_surv']:.3f} "
            f"stable_refr={arm['stable_refresh']:.3f} vol_refr={arm['volatile_refresh']:.3f} "
            f"stable_surv={arm['stable_survival']:.3f}"
        )
    for name, c in results["checks"].items():
        if isinstance(c, dict) and "pass" in c:
            print(f"  CHECK {name}: {'PASS' if c['pass'] else 'FAIL'}")


if __name__ == "__main__":
    main()
