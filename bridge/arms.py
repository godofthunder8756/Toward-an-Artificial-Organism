"""Bridge arm set for engineering validation (N10) — the mechanical arms.

The v3 §4 arm set reduced to the arms the N10 engineering screen needs:

  candidate      -- the learned maintenance allocator (a trained
                    :class:`~bridge.agent.NeuralBridge`).
  no_maintenance -- pi forced off every tick (v3 arm 2; the N1 null).
  fixed          -- state-blind periodic duty cycle, period family swept
                    (v3 arm 3).
  oracle         -- threshold rule ``refresh iff s=stable and E>=E_crit and
                    d>=L-1`` (v3 arm 6; the N6 same-information state machine).
  free_memory    -- W read-in disabled (v3 arm 2's GRU-only variant): the cue
                    must not reach the probe through the recurrent state.

Fixed-policy arms drive the substrate law directly (no learned modules); the
candidate trains the learned allocator. All arms share the environment and the
same episode stream. This is the reusable machinery N11 builds the final rival
set (arms 7-10) on top of; it is not itself the final experiment.

Every arm returns the same endpoint schema so the arms are comparable:

  stable_slot_surv     P(slot readout intact at the probe | stable regime)
  volatile_slot_surv   P(slot readout intact at the probe | volatile regime)
  stable_refresh       mean refresh rate over ticks in the stable regime
  volatile_refresh     mean refresh rate over ticks in the volatile regime
  stable_survival      fraction of stable episodes alive at the horizon
  volatile_survival    fraction of volatile episodes alive at the horizon
  stable_E_final       mean final energy, stable episodes
  volatile_E_final     mean final energy, volatile episodes

CPU-only; deterministic under :func:`bridge.reproducibility.seed_all`.
"""

from __future__ import annotations

from typing import Callable, Dict, List, Tuple

import torch

from bridge.config import BridgeConfig
from bridge.env import BridgeEnv, REGIME_STABLE
from bridge.substrate import Substrate
from bridge.trainer import BridgeTrainer

__all__ = [
    "action_never",
    "action_always",
    "action_oracle",
    "action_fixed",
    "run_fixed_policy",
    "train_candidate",
    "evaluate_candidate",
    "evaluate_episodes",
    "arm_summary",
]

# An action rule maps the current tick's substrate state to a refresh action.
ActionRule = Callable[..., torch.Tensor]


# --------------------------------------------------------------------------- #
# Action rules (fixed-policy arms)
# --------------------------------------------------------------------------- #

def action_never(cfg, t, is_stable, energy, age, alive) -> torch.Tensor:
    """Never refresh (v3 arm 2: pi cut)."""
    return torch.zeros(energy.shape[0], device=energy.device)


def action_always(cfg, t, is_stable, energy, age, alive) -> torch.Tensor:
    """Refresh every tick (a degenerate bound; unaffordable by design)."""
    return torch.ones(energy.shape[0], device=energy.device)


def action_oracle(cfg, t, is_stable, energy, age, alive) -> torch.Tensor:
    """The N6 §3.2 threshold rule: refresh iff stable and E>=E_crit and d>=L-1."""
    L = cfg.decay.lifetime
    return (is_stable & (energy >= cfg.energy.e_crit) & (age >= L - 1)).float()


def action_fixed(period: int) -> ActionRule:
    """Return a state-blind periodic duty cycle: refresh every ``period`` ticks.

    A deterministic schedule, independent of regime/energy/age (v3 arm 3). The
    period is the swept level parameter.
    """
    def _rule(cfg, t, is_stable, energy, age, alive) -> torch.Tensor:
        refresh_this_tick = (t % period) == 0
        return torch.full((energy.shape[0],), float(refresh_this_tick),
                          device=energy.device)
    return _rule


# --------------------------------------------------------------------------- #
# Fixed-policy runner
# --------------------------------------------------------------------------- #

def run_fixed_policy(
    cfg: BridgeConfig,
    batch: Dict[str, torch.Tensor],
    action_rule: ActionRule,
    *,
    write_cue: bool = True,
) -> Dict[str, torch.Tensor]:
    """Drive the substrate law for one batch with a fixed action rule.

    ``write_cue`` is False for the free-memory arm (W read-in disabled): the
    slot is never written, so only the recurrent state could carry the cue.
    Returns per-episode tensors keyed as the shared endpoint schema.
    """
    sub = Substrate(cfg.energy, cfg.decay)
    x, cue, regime, regime_class, correct = (
        batch["x"], batch["cue"], batch["regime"],
        batch["regime_class"], batch["correct"],
    )
    B = x.shape[0]
    T = cfg.episode.horizon_t
    probe_tick = min(cfg.decay.delay_d, T - 1)

    sub.reset(B)
    slot = cue.clone() if write_cue else torch.zeros_like(cue)
    slot_at_probe = None
    refreshes: List[torch.Tensor] = []

    for t in range(T):
        E_t = sub.energy
        d_t = sub.age
        is_stable = regime[:, t, REGIME_STABLE] > 0.5
        action = action_rule(cfg, t, is_stable, E_t, d_t, sub.alive)
        refreshes.append(action)
        sub.earn(correct[:, t])
        sub.spend(action)
        sub.apply_refresh(action)
        slot = sub.decay_slot(slot, action)
        sub.tick_age()
        if t == probe_tick:
            slot_at_probe = slot.clone()

    stable = regime_class == REGIME_STABLE
    refresh = torch.stack(refreshes, dim=1)  # (B, T)
    held = (slot_at_probe != 0.0).squeeze(-1)
    return {
        "slot_surv": held.float(),
        "refresh": refresh.float().mean(dim=1),
        "survival": sub.alive.float(),
        "E_final": sub.energy,
        "stable": stable,
    }


# --------------------------------------------------------------------------- #
# Candidate arm
# --------------------------------------------------------------------------- #

def train_candidate(
    cfg: BridgeConfig,
    seed: int,
    steps: int,
    batch_size: int,
) -> Tuple[BridgeTrainer, List[Dict]]:
    """Train the learned allocator; return (trainer, per-step history)."""
    trainer = BridgeTrainer(cfg, seed)
    history = trainer.train(steps, batch_size=batch_size)
    return trainer, history


def evaluate_candidate(
    trainer: BridgeTrainer,
    batch: Dict[str, torch.Tensor],
) -> Dict[str, torch.Tensor]:
    """Run the trained bridge forward; return the shared endpoint schema."""
    cfg = trainer.config
    out = trainer.bridge(batch["x"], batch["cue"], batch["regime"], batch["correct"])
    probe_tick = min(cfg.decay.delay_d, cfg.episode.horizon_t - 1)
    stable = batch["regime_class"] == REGIME_STABLE
    held = (out["slot"][:, probe_tick, 0] != 0.0).float()
    return {
        "slot_surv": held,
        "refresh": out["refresh"].float().mean(dim=1),
        "survival": out["alive"][:, -1].float(),
        "E_final": out["energy"][:, -1],
        "stable": stable,
    }


# --------------------------------------------------------------------------- #
# Aggregation
# --------------------------------------------------------------------------- #

def evaluate_episodes(
    cfg: BridgeConfig,
    seed: int,
    n_episodes: int,
    runner: Callable[[Dict[str, torch.Tensor]], Dict[str, torch.Tensor]],
) -> Dict[str, float]:
    """Run ``runner`` over batches of eval episodes and aggregate per regime.

    ``runner(batch)`` returns the shared per-episode tensor schema; this
    function draws episodes with a fixed seed and aggregates the stable /
    volatile splits into means. The seed is applied once, and the runner's own
    draws (the candidate's Bernoulli sampling) follow deterministically, so the
    whole sweep is reproducible given ``seed``.
    """
    from bridge.reproducibility import seed_all

    seed_all(seed)
    env = BridgeEnv(cfg)
    acc: Dict[str, List[float]] = {
        "stable_slot_surv": [], "volatile_slot_surv": [],
        "stable_refresh": [], "volatile_refresh": [],
        "stable_survival": [], "volatile_survival": [],
        "stable_E_final": [], "volatile_E_final": [],
    }
    remaining = n_episodes
    batch_size = 256
    while remaining > 0:
        b = min(batch_size, remaining)
        batch = env.sample(b)
        res = runner(batch)
        st = res["stable"]
        for key in ("slot_surv", "refresh", "survival", "E_final"):
            vals = res[key]
            acc[f"stable_{key}"].append(float(vals[st].mean()))
            acc[f"volatile_{key}"].append(float(vals[~st].mean()))
        remaining -= b

    import statistics
    return {k: statistics.mean(v) for k, v in acc.items()}


def arm_summary(name: str, endpoints: Dict[str, float]) -> Dict[str, object]:
    """Wrap an arm's aggregated endpoints with its name for the results file."""
    return {"arm": name, **endpoints}
