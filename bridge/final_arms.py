"""Rival arms 7-10 for the N11 final experiment (the "falsifying rivals").

Built ON TOP of the frozen harness (``bridge/agent.py``, ``bridge/modules.py``,
``bridge/substrate.py``, ``bridge/trainer.py``, ``bridge/arms.py``). This file
adds nothing to the frozen sources; it imports them and constructs the rival
mechanisms the v3 protocol §4 / N2 §5 / N4 §7 define:

  arm 9  sufficient-statistic rival -- the memoryless state machine of N6 §7.2,
         in its two forms:
           ``arm9_nod`` : duty cycle on (regime s, energy E) ONLY (no age read).
           ``arm9_d``   : duty cycle on (s, E, decay age d) -- which is exactly
                          the oracle (N6 §7.2's collapse, stated not hidden).
  arm 10 P_rb -- the raw-bookkeeping direct policy (N2 §5, N4 §7): recurrent,
         trained on the SAME homeostatic objective ``J_A``, reads the raw
         bookkeeping ``(E_t, d_t)`` + regime + history through its ordinary GRU
         state, and has NO explicit, discrete, paid-maintained V slot.
  arm 7  reward-only agent -- same recurrent capacity, single-consumer RL on
         the probe reward only (no homeostatic objective).
  arm 8  multi-objective RL -- two-head net on (probe reward, survival).

Everything is CPU-only and deterministic under ``seed_all``, matching the frozen
harness. Nothing here is a claim; these are the rivals the candidate must be
graded against, and per N6/N7 the direct same-information rivals (9/10) are the
strongest form of "no explicit V".

The documented, disclosed engineering choice: the rival allocator head reads a
normalized context ``[h_t, E_t/e0, d_t/lifetime, s_t]`` (h_t is the GRU state;
E_t, d_t are the raw substrate bookkeeping). Normalization is a conditioning
convenience, not added information -- E_t and d_t are the same raw bookkeeping
quantities the candidate's V reads, and the rival is denied nothing.
"""

from __future__ import annotations

from typing import Callable, Dict, List, Optional, Tuple

import torch
import torch.nn as nn

from bridge.config import BridgeConfig
from bridge.modules import Controller, Workspace, ProbeReadout, RefreshAction
from bridge.substrate import Substrate
from bridge.env import BridgeEnv, REGIME_STABLE
from bridge.trainer import integrity_label, _discounted_returns

__all__ = [
    "RivalBridge",
    "arm9_nod",
    "arm9_d",
    "train_rival",
    "evaluate_rival",
    "evaluate_episodes_uniform",
]

_EPS = 1e-8


# --------------------------------------------------------------------------- #
# Arm 9: the memoryless sufficient-statistic state machine (fixed rules)
# --------------------------------------------------------------------------- #

def arm9_nod(period: int = 16):
    """Sufficient-statistic rival WITHOUT the age read: (s, E) only.

    N6 §7.3: this arm cannot tell a fresh slot from one about to decay, so its
    only recourse is a fixed duty cycle gated on regime + energy. The period is
    the swept parameter (AC11/AC116: sweep the level family). Phase 0 is used so
    the rival is genuinely capable of holding the cue (a phase that lands
    pre-announcement would be a strawman by alignment, not by mechanism); the
    residual difference from the age-gated oracle is the honest no-age-read
    effect, whatever it measures to be.
    """
    def _rule(cfg, t, is_stable, energy, age, alive) -> torch.Tensor:
        on_clock = (t % period) == 0
        return (is_stable & (energy >= cfg.energy.e_crit) & on_clock).float()
    return _rule


def arm9_d(cfg: BridgeConfig, t: int, is_stable, energy, age, alive) -> torch.Tensor:
    """Sufficient-statistic rival WITH the age read: (s, E, d).

    This is the oracle's threshold rule (N6 §7.2): ``refresh iff s=stable and
    E>=E_crit and d>=L-1``. Identical to ``bridge.arms.action_oracle``; kept as
    a local definition so the arm-9 collapse is explicit in one place.
    """
    L = cfg.decay.lifetime
    return (is_stable & (energy >= cfg.energy.e_crit) & (age >= L - 1)).float()


# --------------------------------------------------------------------------- #
# The rival recurrent agent (arms 7, 8, 10 share this body; they differ only in
# the objective the trainer feeds them)
# --------------------------------------------------------------------------- #

class RivalBridge(nn.Module):
    """A recurrent maintenance agent with no explicit V slot.

    Components (reusing the frozen modules): the GRU controller (reads the
    c-independent distractor ``x_t``), the workspace ``W`` (the paid cue slot),
    the probe readout ``S_pol`` (reads ``(W, x_t)``), and the paid refresh
    primitive ``pi``. In place of the candidate's ``V -> A`` path, a single
    allocator head reads the raw bookkeeping context
    ``[h_t, E_t/e0, d_t/lifetime, s_t]`` and emits a scalar refresh logit, with
    a matching critic for the REINFORCE baseline.

    This is exactly N2 §5.1/N4 §7's P_rb: raw bookkeeping + regime + history,
    no discrete maintained self-state, no separate E_pi line item on a
    self-state. Arms 7 and 8 use the same body but are trained on the probe
    reward (arm 7) or reward + survival (arm 8) instead of the homeostatic cost.
    """

    def __init__(self, config: BridgeConfig):
        super().__init__()
        self.config = config
        arch = config.arch
        self.controller = Controller(arch, config.init)
        self.workspace = Workspace(arch)
        self.probe = ProbeReadout(arch, config.init)
        self.refresh = RefreshAction(config.energy)
        self.substrate = Substrate(config.energy, config.decay)

        # Allocator head: reads (h_t, E_norm, d_norm, s_t).
        ctx_dim = arch.gru_hidden + 2 + arch.regime_dim
        self.allocator_policy = nn.Linear(ctx_dim, 1)
        self.allocator_critic = nn.Linear(ctx_dim, 1)
        # Same init scheme as the frozen modules (xavier_uniform, gain 1).
        for p in self.allocator_policy.parameters():
            if p.dim() >= 2:
                nn.init.xavier_uniform_(p, gain=1.0)
            else:
                nn.init.zeros_(p)
        for p in self.allocator_critic.parameters():
            if p.dim() >= 2:
                nn.init.xavier_uniform_(p, gain=1.0)
            else:
                nn.init.zeros_(p)

    # -- parameter accounting ---------------------------------------------- #

    def actual_parameter_counts(self) -> Dict[str, int]:
        def n(mod):
            return sum(p.numel() for p in mod.parameters() if p.requires_grad)
        return {
            "gru": n(self.controller.gru),
            "allocator_policy": n(self.allocator_policy),
            "allocator_critic": n(self.allocator_critic),
            "S_pol": n(self.probe.fc),
        }

    # -- forward ------------------------------------------------------------ #

    def forward(
        self,
        x: torch.Tensor,
        cue: torch.Tensor,
        regime: torch.Tensor,
        correct: Optional[torch.Tensor] = None,
        *,
        forced_action: Optional[torch.Tensor] = None,
    ) -> Dict[str, torch.Tensor]:
        """Run a batch of episodes through the rival (mirrors the candidate's
        substrate loop exactly: earn -> spend -> apply_refresh -> decay_slot ->
        tick_age). Returns the candidate's output schema plus the per-tick
        context so trainers can compute any objective."""
        B, T, _ = x.shape
        device = x.device
        dtype = x.dtype
        if correct is None:
            correct = torch.ones(B, T, dtype=torch.bool, device=device)

        self.workspace.reset(B, device)
        self.substrate.reset(B, device)

        h_seq, _ = self.controller(x)  # (B, T, H)

        e0 = self.config.energy.e0
        L = float(self.config.decay.lifetime)
        self.workspace.write(cue)

        ctx_seq, refresh_logits, refresh_probs, refresh_acts = [], [], [], []
        logps, values = [], []
        energy_seq, age_seq, alive_seq, spend_seq = [], [], [], []
        slot_seq = []
        b_seq = []

        for t in range(T):
            h_t = h_seq[:, t]
            E_t = self.substrate.energy
            d_t = self.substrate.age.float()

            b_seq.append(torch.stack([E_t, d_t], dim=-1))
            ctx = torch.cat(
                [h_t, E_t.unsqueeze(-1) / e0, d_t.unsqueeze(-1) / L, regime[:, t]],
                dim=-1,
            )
            refresh_logit = self.allocator_policy(ctx).squeeze(-1)
            value = self.allocator_critic(ctx).squeeze(-1)

            if forced_action is not None:
                action = forced_action[:, t].float()
                prob = torch.sigmoid(refresh_logit)
                logp = torch.where(
                    action > 0.5,
                    torch.log(prob + _EPS),
                    torch.log(1.0 - prob + _EPS),
                )
            else:
                prob = torch.sigmoid(refresh_logit)
                action = torch.bernoulli(prob)
                logp = torch.where(
                    action > 0.5,
                    torch.log(prob + _EPS),
                    torch.log(1.0 - prob + _EPS),
                )

            self.substrate.earn(correct[:, t])
            spend = self.substrate.spend(action)
            self.substrate.apply_refresh(action)
            slot_readout = self.substrate.decay_slot(self.workspace.slot, action)
            self.substrate.tick_age()

            ctx_seq.append(ctx)
            refresh_logits.append(refresh_logit)
            refresh_probs.append(prob)
            refresh_acts.append(action)
            logps.append(logp)
            values.append(value)
            energy_seq.append(self.substrate.energy.clone())
            age_seq.append(self.substrate.age.clone())
            alive_seq.append(self.substrate.alive.clone())
            spend_seq.append(spend)
            slot_seq.append(slot_readout)

        probe_tick = min(self.config.decay.delay_d, T - 1)
        probe_logits = self.probe(slot_seq[probe_tick], x[:, probe_tick])

        return {
            "h": h_seq,
            "ctx": torch.stack(ctx_seq, dim=1),
            "b": torch.stack(b_seq, dim=1),
            "refresh_logit": torch.stack(refresh_logits, dim=1),
            "refresh_prob": torch.stack(refresh_probs, dim=1),
            "refresh": torch.stack(refresh_acts, dim=1),
            "logp": torch.stack(logps, dim=1),
            "value": torch.stack(values, dim=1),
            "energy": torch.stack(energy_seq, dim=1),
            "age": torch.stack(age_seq, dim=1),
            "alive": torch.stack(alive_seq, dim=1),
            "spend": torch.stack(spend_seq, dim=1),
            "slot": torch.stack(slot_seq, dim=1),
            "probe_logits": probe_logits,
        }


# --------------------------------------------------------------------------- #
# Rival objectives and training
# --------------------------------------------------------------------------- #

def _homeostatic_cost(cfg: BridgeConfig, out: Dict, batch: Dict) -> torch.Tensor:
    """c_homeo(t) = 1[I_t != I*(s_t, E_t)] over the measured state (N4 §4.3)."""
    is_stable = batch["regime"][..., REGIME_STABLE] > 0.5
    E_t = out["b"][..., 0]
    d_t = out["b"][..., 1]
    I_star = (is_stable & (E_t >= cfg.energy.e_crit)).long()
    I_measured = integrity_label(d_t, cfg.decay.lifetime)
    return (I_measured != I_star).float()


def _probe_reward(cfg: BridgeConfig, out: Dict, batch: Dict) -> torch.Tensor:
    """Per-episode scalar reward: 1[probe answer correct in the stable regime].

    Returns (B, T) where the reward is placed at the probe tick (return-to-go
    from earlier ticks then credits the refresh actions that held the cue).
    """
    B, T = out["refresh"].shape
    stable = batch["regime_class"] == REGIME_STABLE
    cue_target = (batch["cue"].squeeze(-1) < 0).long()
    pred = out["probe_logits"].argmax(dim=-1)
    correct_ans = (pred == cue_target).float()  # (B,)
    r = torch.zeros(B, T, device=out["refresh"].device)
    probe_tick = min(cfg.decay.delay_d, T - 1)
    r[:, probe_tick] = correct_ans * stable.float()
    return r


def _survival_reward(cfg: BridgeConfig, out: Dict, batch: Dict) -> torch.Tensor:
    """Per-episode scalar reward: 1[alive at the horizon] (continued operation)."""
    B, T = out["refresh"].shape
    r = torch.zeros(B, T, device=out["refresh"].device)
    r[:, T - 1] = out["alive"][:, -1].float()
    return r


def _rival_losses(
    cfg: BridgeConfig,
    out: Dict[str, torch.Tensor],
    batch: Dict[str, torch.Tensor],
    objective: str,
) -> Tuple[Dict[str, torch.Tensor], Dict[str, torch.Tensor]]:
    """Compute the rival's policy-gradient loss + metrics for ``objective``.

    ``objective`` is one of:

      "homeo"   -- minimize homeostatic cost c_homeo (arm 10 / P_rb).
      "reward"  -- maximize probe reward (arm 7).
      "multi"   -- maximize probe reward + survival (arm 8).

    All use REINFORCE with a learned baseline; the probe NLL (supervised) is
    added for the reward/multi objectives so S_pol can actually answer the
    probe. The homeo objective reuses the candidate's myopic set point exactly.
    """
    gamma = cfg.losses.a_discount
    value = out["value"]
    logp = out["logp"]

    if objective == "homeo":
        signal = _homeostatic_cost(cfg, out, batch)      # cost to MINIMIZE
        G = _discounted_returns(signal, gamma)
        advantage = (G - value).detach()
        j_policy = (logp * advantage).sum(dim=1).mean()
        j_critic = torch.nn.functional.mse_loss(value, G.detach())
        probe_loss = torch.zeros((), device=logp.device)
    elif objective in ("reward", "multi"):
        reward = _probe_reward(cfg, out, batch)
        if objective == "multi":
            reward = reward + _survival_reward(cfg, out, batch)
        G = _discounted_returns(reward, gamma)           # reward to MAXIMIZE
        advantage = (G - value).detach()
        j_policy = -(logp * advantage).sum(dim=1).mean()
        j_critic = torch.nn.functional.mse_loss(value, G.detach())
        # Supervised probe readout (stable episodes only), as in the candidate.
        stable = batch["regime_class"] == REGIME_STABLE
        if stable.any():
            cue_target = (batch["cue"].squeeze(-1) < 0).long()
            probe_loss = torch.nn.functional.cross_entropy(
                out["probe_logits"][stable], cue_target[stable]
            )
        else:
            probe_loss = torch.zeros((), device=logp.device)
    else:
        raise ValueError(f"unknown rival objective: {objective}")

    prob = out["refresh_prob"].clamp(1e-8, 1 - 1e-8)
    entropy = -(prob * prob.log() + (1.0 - prob) * (1.0 - prob).log())
    j_entropy = -cfg.losses.a_entropy_weight * entropy.mean()

    losses = {
        "J_policy": j_policy,
        "J_critic": j_critic,
        "J_entropy": j_entropy,
        "probe": probe_loss,
    }
    metrics = {
        "J_policy": j_policy.detach(),
        "J_critic": j_critic.detach(),
        "entropy": entropy.mean().detach(),
        "probe": probe_loss.detach(),
        "mean_energy": out["energy"].mean().detach(),
        "alive_frac": out["alive"][:, -1].float().mean().detach(),
        "refresh_rate": out["refresh"].float().mean().detach(),
    }
    return losses, metrics


class RivalTrainer:
    """Minimal REINFORCE trainer for the rival bridge.

    Mirrors ``bridge.trainer.BridgeTrainer``'s determinism contract: seeds the
    RNG on construction (before building the rival, so parameter init is
    deterministic) and again at ``train`` start.
    """

    def __init__(self, cfg: BridgeConfig, seed: int, objective: str,
                 rival: Optional[RivalBridge] = None):
        from bridge.reproducibility import seed_all
        self.cfg = cfg
        self.seed = seed
        self.objective = objective
        seed_all(seed)
        self.rival = rival if rival is not None else RivalBridge(cfg)
        self.env = BridgeEnv(cfg)

        opt = cfg.optimizer
        groups = [
            {"params": list(self.rival.controller.parameters()), "lr": opt.lr_v},
            {"params": self.rival.allocator_policy.parameters(), "lr": opt.lr_a_policy},
            {"params": self.rival.allocator_critic.parameters(), "lr": opt.lr_a_critic},
            {"params": self.rival.probe.parameters(), "lr": opt.lr_s_pol},
        ]
        self.optimizer = torch.optim.Adam(
            groups, lr=opt.lr_v, betas=tuple(opt.betas),
            weight_decay=opt.weight_decay,
        )
        self.history: List[Dict] = []

    def step(self, batch: Dict[str, torch.Tensor]) -> Dict[str, torch.Tensor]:
        out = self.rival(batch["x"], batch["cue"], batch["regime"], batch["correct"])
        losses, metrics = _rival_losses(self.cfg, out, batch, self.objective)
        total = (
            losses["J_policy"] + losses["J_critic"]
            + losses["J_entropy"] + losses["probe"]
        )
        self.optimizer.zero_grad()
        total.backward()
        self.optimizer.step()
        metrics["total"] = total.detach()
        return metrics

    def train(self, steps: int, batch_size: int = 64) -> List[Dict]:
        from bridge.reproducibility import seed_all
        self.history = []
        seed_all(self.seed)
        for step in range(steps):
            batch = self.env.sample(batch_size)
            metrics = self.step(batch)
            metrics = {k: float(v) for k, v in metrics.items()}
            metrics["step"] = step
            self.history.append(metrics)
        return self.history


def train_rival(
    cfg: BridgeConfig, seed: int, objective: str, steps: int, batch_size: int
) -> Tuple[RivalTrainer, List[Dict]]:
    """Train a rival arm; return (trainer, history)."""
    trainer = RivalTrainer(cfg, seed, objective)
    history = trainer.train(steps, batch_size=batch_size)
    return trainer, history


# --------------------------------------------------------------------------- #
# Uniform evaluation (same endpoint schema for every arm)
# --------------------------------------------------------------------------- #

def evaluate_rival(
    trainer: RivalTrainer,
    batch: Dict[str, torch.Tensor],
) -> Dict[str, torch.Tensor]:
    """Run a trained rival forward and return the shared per-episode schema."""
    cfg = trainer.cfg
    out = trainer.rival(batch["x"], batch["cue"], batch["regime"], batch["correct"])
    probe_tick = min(cfg.decay.delay_d, cfg.episode.horizon_t - 1)
    stable = batch["regime_class"] == REGIME_STABLE
    held = (out["slot"][:, probe_tick, 0] != 0.0).float()
    cue_target = (batch["cue"].squeeze(-1) < 0).long()
    probe_correct = (out["probe_logits"].argmax(-1) == cue_target).float()
    return {
        "slot_surv": held,
        "refresh": out["refresh"].float().mean(dim=1),
        "survival": out["alive"][:, -1].float(),
        "E_final": out["energy"][:, -1],
        "stable": stable,
        "probe_correct": probe_correct,
    }


def run_fixed_with_probe(
    cfg: BridgeConfig,
    batch: Dict[str, torch.Tensor],
    action_rule: Callable,
    *,
    write_cue: bool = True,
) -> Dict[str, torch.Tensor]:
    """Drive a fixed action rule over a batch (mirrors ``arms.run_fixed_policy``)
    and return the shared per-episode schema including a probe-correct read.

    For a fixed arm the cue is recoverable iff the slot readout is intact at the
    probe (the slot holds the true cue); when neutral, a readout is at chance.
    ``probe_correct`` here is therefore ``held`` (the deterministic E1 read),
    matching how the plan grades arm 2 at chance vs arm 1 above chance.
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
    refresh = torch.stack(refreshes, dim=1)
    held = (slot_at_probe != 0.0).squeeze(-1).float()
    return {
        "slot_surv": held,
        "refresh": refresh.float().mean(dim=1),
        "survival": sub.alive.float(),
        "E_final": sub.energy,
        "stable": stable,
        "probe_correct": held,  # deterministic E1 read (see docstring)
    }


def evaluate_episodes_uniform(
    cfg: BridgeConfig,
    seed: int,
    n_episodes: int,
    runner: Callable[[Dict[str, torch.Tensor]], Dict[str, torch.Tensor]],
) -> Dict[str, float]:
    """Run ``runner`` over seeded eval episodes and aggregate per regime.

    Same aggregation contract as ``bridge.arms.evaluate_episodes``, extended
    with ``probe_correct``. The seed is applied once; the runner's own draws
    follow deterministically.
    """
    from bridge.reproducibility import seed_all
    seed_all(seed)
    env = BridgeEnv(cfg)
    acc: Dict[str, List[float]] = {
        "stable_slot_surv": [], "volatile_slot_surv": [],
        "stable_refresh": [], "volatile_refresh": [],
        "stable_survival": [], "volatile_survival": [],
        "stable_E_final": [], "volatile_E_final": [],
        "stable_probe_correct": [], "volatile_probe_correct": [],
    }
    remaining = n_episodes
    batch_size = 256
    while remaining > 0:
        b = min(batch_size, remaining)
        batch = env.sample(b)
        res = runner(batch)
        st = res["stable"]
        for key in ("slot_surv", "refresh", "survival", "E_final", "probe_correct"):
            vals = res[key]
            acc[f"stable_{key}"].append(float(vals[st].mean()))
            acc[f"volatile_{key}"].append(float(vals[~st].mean()))
        remaining -= b

    import statistics
    return {k: statistics.mean(v) for k, v in acc.items()}


# --------------------------------------------------------------------------- #
# Candidate-level probes used by the final runner (read-only on the frozen
# candidate; these do not modify any frozen source)
# --------------------------------------------------------------------------- #

def evaluate_candidate_full(
    trainer,
    batch: Dict[str, torch.Tensor],
) -> Dict[str, torch.Tensor]:
    """Run the frozen candidate forward and return per-episode readouts:
    slot survival, refresh rate, survival, final energy, stable mask, AND
    probe correctness (S_pol argmax vs cue) + held/lost masks for E2."""
    cfg = trainer.config
    out = trainer.bridge(batch["x"], batch["cue"], batch["regime"], batch["correct"])
    probe_tick = min(cfg.decay.delay_d, cfg.episode.horizon_t - 1)
    stable = batch["regime_class"] == REGIME_STABLE
    held = (out["slot"][:, probe_tick, 0] != 0.0).float()
    cue_target = (batch["cue"].squeeze(-1) < 0).long()
    probe_correct = (out["probe_logits"].argmax(-1) == cue_target).float()
    return {
        "slot_surv": held,
        "refresh": out["refresh"].float().mean(dim=1),
        "survival": out["alive"][:, -1].float(),
        "E_final": out["energy"][:, -1],
        "stable": stable,
        "probe_correct": probe_correct,
        "held": held,
    }


def run_candidate_forced(
    trainer,
    batch: Dict[str, torch.Tensor],
    forced_action: Optional[torch.Tensor] = None,
) -> Dict[str, torch.Tensor]:
    """Run the frozen candidate's own modules with an optional forced refresh.

    Mirrors ``NeuralBridge.forward``'s substrate loop exactly (earn -> spend ->
    apply_refresh -> decay_slot -> tick_age) using the SAME trained weights, so
    with ``forced_action=None`` it reproduces the frozen candidate bit-for-bit.
    A forced action is the do-intervention used by the W-intervention control:
    force-hold (action=1) and force-drop (action=0) over the whole episode.
    """
    cfg = trainer.config
    bridge = trainer.bridge
    x, cue, regime, correct = (
        batch["x"], batch["cue"], batch["regime"], batch["correct"],
    )
    B, T, _ = x.shape
    device = x.device
    dtype = x.dtype
    if correct is None:
        correct = torch.ones(B, T, dtype=torch.bool, device=device)

    bridge.workspace.reset(B, device)
    bridge.substrate.reset(B, device)
    h_seq, _ = bridge.controller(x)

    v_prev = torch.zeros(B, bridge.v_estimator.code_dim, device=device, dtype=dtype)
    h_prev = torch.zeros(B, bridge.controller.hidden_size, device=device, dtype=dtype)
    bridge.workspace.write(cue)

    refresh_acts, logps, values, energy_seq, age_seq, alive_seq, slot_seq = (
        [], [], [], [], [], [], []
    )

    for t in range(T):
        b_t = torch.stack(
            [bridge.substrate.energy, bridge.substrate.age.float()], dim=-1
        )
        v_logits = bridge.v_estimator(v_prev, h_prev, b_t)
        e_code, i_code = bridge.v_estimator.decode(v_logits)
        v_t = bridge.v_estimator.encode(e_code, i_code)
        s_t = regime[:, t]
        refresh_logit, value = bridge.allocator(v_t, s_t)
        if forced_action is not None:
            action = forced_action[:, t].float()
        else:
            action, _, logp = bridge.allocator.sample(refresh_logit)
            logps.append(logp)
        values.append(value)

        bridge.substrate.earn(correct[:, t])
        bridge.substrate.spend(action)
        bridge.substrate.apply_refresh(action)
        slot_readout = bridge.substrate.decay_slot(bridge.workspace.slot, action)
        bridge.substrate.tick_age()

        refresh_acts.append(action)
        energy_seq.append(bridge.substrate.energy.clone())
        age_seq.append(bridge.substrate.age.clone())
        alive_seq.append(bridge.substrate.alive.clone())
        slot_seq.append(slot_readout)

        v_prev = v_t
        h_prev = h_seq[:, t]

    probe_tick = min(cfg.decay.delay_d, T - 1)
    probe_logits = bridge.probe(slot_seq[probe_tick], x[:, probe_tick])
    stable = batch["regime_class"] == REGIME_STABLE
    held = (slot_seq[probe_tick] != 0.0).squeeze(-1).float()
    cue_target = (cue.squeeze(-1) < 0).long()
    probe_correct = (probe_logits.argmax(-1) == cue_target).float()

    return {
        "slot_surv": held,
        "refresh": torch.stack(refresh_acts, dim=1).float().mean(dim=1),
        "survival": bridge.substrate.alive.float(),
        "E_final": bridge.substrate.energy,
        "stable": stable,
        "probe_correct": probe_correct,
        "held": held,
    }


def allocator_dependence(trainer) -> Dict[str, object]:
    """Measure the candidate A's dependence on the discrete V code fields.

    Reads the trained allocator policy head directly: for each of the
    ``2^(v_energy_bits + v_integrity_bits)`` discrete codes and each regime,
    compute P(refresh). Then:

      integrity_dep = mean over (energy_code, regime) of
                        |P(refresh | integrity=1) - P(refresh | integrity=0)|
      energy_dep    = mean over (integrity_code, regime) of
                        |P(refresh | energy=max) - P(refresh | energy=min)|

    This is the exact, forward-loop-free form of N3a/G3a's question: does the
    allocation causally depend on the maintained integrity/resource estimate?
    It measures the trained mapping A(v, s) -> P(refresh), nothing more.
    """
    cfg = trainer.config
    arch = cfg.arch
    bridge = trainer.bridge
    ve, vi = arch.v_energy_bits, arch.v_integrity_bits
    n_energy = 2 ** ve
    n_integrity = 2 ** vi

    def p_refresh(e_code, i_code, stable_bit):
        v = bridge.v_estimator.encode(
            torch.tensor([e_code]), torch.tensor([i_code])
        )
        s = torch.zeros(1, arch.regime_dim)
        s[0, 0 if stable_bit else 1] = 1.0
        logit, _ = bridge.allocator(v, s)
        return torch.sigmoid(logit).item()

    with torch.no_grad():
        # integrity dependence
        integ_diffs = []
        for e in range(n_energy):
            for sb in (0, 1):
                integ_diffs.append(abs(p_refresh(e, 1, sb) - p_refresh(e, 0, sb)))
        integrity_dep = float(sum(integ_diffs) / len(integ_diffs))

        # energy dependence (min vs max energy code)
        energy_diffs = []
        for i in range(n_integrity):
            for sb in (0, 1):
                energy_diffs.append(abs(p_refresh(n_energy - 1, i, sb) - p_refresh(0, i, sb)))
        energy_dep = float(sum(energy_diffs) / len(energy_diffs))

        # the full policy table, for the record
        table = {}
        for e in range(n_energy):
            for i in range(n_integrity):
                for sb in (0, 1):
                    table[f"e{e}_i{i}_{'stable' if sb == 0 else 'volatile'}"] = p_refresh(e, i, sb)

    return {
        "integrity_dep": integrity_dep,
        "energy_dep": energy_dep,
        "policy_table": table,
    }

