"""Training loop, losses, and gradient paths for the neural bridge (N9).

Wires the assembled :class:`~bridge.agent.NeuralBridge` to a CPU training loop
that realizes the exact objectives of the frozen v3 protocol §7 / N4:

- ``L_V`` — supervised cross-entropy of the integrity/energy estimator ``V``
  against the *measured* state (energy code ``quantize(E_t)``, integrity code
  ``1[d_t < lifetime]``). Teacher-forced and synchronous; the recurrence uses
  the detached prior slot content (no straight-through, no BPTT through the
  argmax).
- ``J_A`` — REINFORCE with a learned baseline (critic reads ``(v_t, s_t)``
  only) over the homeostatic cost ``c_homeo(t) = 1[I_t != I*(s_t, E_t)]``,
  with the trainer-supplied set point ``I* = intact iff stable and E_t >=
  E_crit``. The objective's argument is the *measured* ``I_t``, never V's
  estimate.
- Probe NLL — cross-entropy of ``S_pol``'s cue-answer logits against the cue,
  on stable-regime episodes only (the probe is cancelled in the volatile
  regime).

The three objectives are optimized **jointly** in one loop on one forward pass,
with **disjoint** weight sets enforced by the stop-gradients already in the
forward (detached W content, detached discrete ``v_t`` on the V->A edge,
argmax non-differentiable, substrate non-differentiable). ``J_A`` is applied
via the ``logp``/``value`` tensors the forward returns (REINFORCE, never
backprop through the dynamics). No loss references "continued operation" (E5);
no reward gradient reaches ``V`` or ``A``.

The optimizer is a single Adam with per-component learning-rate groups read
from :class:`~bridge.config.OptimizerConfig`. The GRU shares ``lr_v`` because
its only gradient is ``L_V``'s (content-blind, through the V read-in).

Everything is CPU-only; determinism is obtained via
:func:`bridge.reproducibility.seed_all` before any draw.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

import torch
import torch.nn.functional as F

from bridge.agent import NeuralBridge
from bridge.config import BridgeConfig
from bridge.env import BridgeEnv, REGIME_STABLE
from bridge.episodes import save_episodes, load_episodes
from bridge.reproducibility import seed_all

__all__ = ["BridgeTrainer", "compute_losses", "quantize_energy", "integrity_label"]


# --------------------------------------------------------------------------- #
# Label helpers (deterministic, content-blind)
# --------------------------------------------------------------------------- #

def quantize_energy(E: torch.Tensor, n_codes: int, e0: float) -> torch.Tensor:
    """Discretize measured energy into ``n_codes`` uniform bins over ``[0, e0]``.

    Deterministic and trainer-supplied (v3 §7.1: ``y_E(t) = quantize(E_t)``).
    Energy above ``e0`` saturates at the top bin.
    """
    width = e0 / n_codes
    code = (E.clamp(min=0.0, max=e0 - 1e-6) / width).floor().long()
    return code.clamp(max=n_codes - 1)


def integrity_label(age: torch.Tensor, lifetime: int) -> torch.Tensor:
    """Content-blind integrity label ``I_t = 1[age < lifetime]`` (N6: I_t=f(d_t))."""
    return (age < lifetime).long()


# --------------------------------------------------------------------------- #
# Losses
# --------------------------------------------------------------------------- #

def _discounted_returns(costs: torch.Tensor, gamma: float) -> torch.Tensor:
    """Return-to-go ``G_t = sum_{tau>=t} gamma^{tau-t} c(tau)``, (B, T)."""
    B, T = costs.shape
    rets = torch.zeros_like(costs)
    running = torch.zeros(B, device=costs.device, dtype=costs.dtype)
    for t in reversed(range(T)):
        running = costs[:, t] + gamma * running
        rets[:, t] = running
    return rets


def compute_losses(
    config: BridgeConfig,
    out: Dict[str, torch.Tensor],
    batch: Dict[str, torch.Tensor],
) -> Tuple[Dict[str, torch.Tensor], Dict[str, torch.Tensor]]:
    """Compute the three objectives and per-term metrics from one forward pass.

    Returns ``(losses, metrics)``. ``losses`` is keyed ``L_V``, ``J_A_policy``,
    ``J_A_critic``, ``probe``; ``metrics`` carries detached scalar diagnostics
    (per-episode means) used for logging. None of the loss terms is reduced
    across the batch in a way that would hide the per-tick structure: each is
    a scalar mean over (episode, tick), matching the protocol's (1/T) sum.
    """
    arch = config.arch
    n_energy = 2 ** arch.v_energy_bits
    n_integrity = 2 ** arch.v_integrity_bits

    v_logits = out["v_logits"]                    # (B, T, n_E + n_I)
    e_logits = v_logits[..., :n_energy]
    i_logits = v_logits[..., n_energy:]

    b = out["b"]                                   # (B, T, 2) = (E_t, d_t)
    E_t = b[..., 0]
    d_t = b[..., 1]

    # -- L_V: supervised estimator (energy code + integrity code) ---------- #
    y_E = quantize_energy(E_t, n_energy, config.energy.e0)          # (B, T)
    y_I = integrity_label(d_t, config.decay.lifetime)               # (B, T)
    l_v_energy = F.cross_entropy(
        e_logits.reshape(-1, n_energy), y_E.reshape(-1)
    )
    l_v_integrity = F.cross_entropy(
        i_logits.reshape(-1, n_integrity), y_I.reshape(-1)
    )
    L_V = (
        config.losses.v_energy_weight * l_v_energy
        + config.losses.v_integrity_weight * l_v_integrity
    )

    # -- J_A: homeostatic policy gradient over the measured state ---------- #
    is_stable = batch["regime"][..., REGIME_STABLE] > 0.5            # (B, T)
    I_star = (is_stable & (E_t >= config.energy.e_crit)).long()      # set point
    I_measured = integrity_label(d_t, config.decay.lifetime)         # measured
    c_homeo = (I_measured != I_star).float()                         # (B, T)

    gamma = config.losses.a_discount
    G = _discounted_returns(c_homeo, gamma)                          # return-to-go
    value = out["value"]                                             # (B, T)
    logp = out["logp"]                                               # (B, T)

    advantage = (G - value).detach()                                 # baseline
    J_A_policy = (logp * advantage).sum(dim=1).mean()
    J_A_critic = F.mse_loss(value, G.detach())

    # -- J_A entropy regularization (keeps the Bernoulli policy exploring) -- #
    # Minimizing -w·H maximizes the action entropy, preventing the premature
    # collapse of REINFORCE to a deterministic (and typically suboptimal)
    # policy. Off by default (w=0); tuned as a training hyperparameter.
    prob = out["refresh_prob"].clamp(1e-8, 1 - 1e-8)
    entropy = -(prob * prob.log() + (1.0 - prob) * (1.0 - prob).log())
    J_A_entropy = -config.losses.a_entropy_weight * entropy.mean()

    # -- probe: S_pol NLL on stable-regime episodes only ------------------- #
    stable = batch["regime_class"] == REGIME_STABLE                  # (B,)
    if stable.any():
        cue_target = (batch["cue"].squeeze(-1) < 0).long()           # +1->0, -1->1
        probe = F.cross_entropy(out["probe_logits"][stable], cue_target[stable])
    else:
        probe = torch.zeros((), device=v_logits.device)  # no stable episode

    losses = {
        "L_V": L_V,
        "J_A_policy": J_A_policy,
        "J_A_critic": J_A_critic,
        "J_A_entropy": J_A_entropy,
        "probe": probe,
    }

    metrics = {
        "L_V": L_V.detach(),
        "L_V_energy": l_v_energy.detach(),
        "L_V_integrity": l_v_integrity.detach(),
        "J_A_policy": J_A_policy.detach(),
        "J_A_critic": J_A_critic.detach(),
        "J_A_entropy": J_A_entropy.detach(),
        "entropy": entropy.mean().detach(),
        "probe": probe.detach(),
        "mean_cost": c_homeo.mean().detach(),
        "mean_energy": E_t.mean().detach(),
        "mean_age": d_t.mean().detach(),
        "alive_frac": out["alive"][:, -1].float().mean().detach(),
        "refresh_rate": out["refresh"].float().mean().detach(),
    }

    return losses, metrics


# --------------------------------------------------------------------------- #
# Trainer
# --------------------------------------------------------------------------- #

class BridgeTrainer:
    """CPU training loop for the neural bridge.

    Parameters
    ----------
    config : BridgeConfig
        The full reproducibility config (optimizer, LRs, horizon, losses,
        training schedule, seeds, energy, decay).
    seed : int
        Run seed; applied via ``seed_all`` on construction so every subsequent
        draw (environment, sampling) is deterministic.
    bridge : NeuralBridge, optional
        A pre-built bridge; built fresh from ``config`` when omitted.

    The optimizer groups are the explicit gradient paths, one LR group per
    distinct objective path:

    - ``lr_v`` -> ``f_V`` weights **and** the GRU (L_V's content-blind path),
    - ``lr_a_policy`` -> ``A``'s policy head (J_A policy gradient),
    - ``lr_a_critic`` -> ``A``'s critic head (J_A baseline),
    - ``lr_s_pol`` -> ``S_pol``'s readout (probe reward).
    """

    def __init__(
        self,
        config: BridgeConfig,
        seed: int,
        bridge: Optional[NeuralBridge] = None,
    ):
        self.config = config
        self.seed = seed
        # Seed BEFORE constructing the bridge so the parameter initialization
        # (xavier_uniform draws) is deterministic for a given seed — otherwise
        # two same-seed trainers get different initial weights depending on
        # the RNG state a previous trainer left behind.
        seed_all(seed)
        self.bridge = bridge if bridge is not None else NeuralBridge(config)
        self.env = BridgeEnv(config)
        self.optimizer = self._make_optimizer()
        self.history: List[Dict] = []

    def _make_optimizer(self) -> torch.optim.Optimizer:
        opt = self.config.optimizer
        groups = [
            {
                "params": list(self.bridge.v_estimator.parameters())
                + list(self.bridge.controller.parameters()),
                "lr": opt.lr_v,
            },
            {
                "params": self.bridge.allocator.policy.parameters(),
                "lr": opt.lr_a_policy,
            },
            {
                "params": self.bridge.allocator.critic.parameters(),
                "lr": opt.lr_a_critic,
            },
            {
                "params": self.bridge.probe.parameters(),
                "lr": opt.lr_s_pol,
            },
        ]
        return torch.optim.Adam(
            groups,
            lr=opt.lr_v,
            betas=tuple(opt.betas),
            weight_decay=opt.weight_decay,
        )

    # -- one training step -------------------------------------------------- #

    def step(self, batch: Dict[str, torch.Tensor]) -> Dict[str, torch.Tensor]:
        """Run one forward pass, compute losses, and take one optimizer step."""
        out = self.bridge(batch["x"], batch["cue"], batch["regime"], batch["correct"])
        losses, metrics = compute_losses(self.config, out, batch)

        total = (
            losses["L_V"]
            + losses["J_A_policy"]
            + losses["J_A_critic"]
            + losses["J_A_entropy"]
            + losses["probe"]
        )

        self.optimizer.zero_grad()
        total.backward()
        self.optimizer.step()

        metrics["total"] = total.detach()
        return metrics

    # -- the loop ----------------------------------------------------------- #

    def train(
        self,
        steps: int,
        batch_size: int = 32,
        *,
        log_every: int = 1,
    ) -> List[Dict]:
        """Run ``steps`` training episodes (batched) and return per-step metrics.

        One *step* here is one batch of ``batch_size`` episodes. The config's
        ``training_episodes`` is the episode budget; callers pass
        ``steps = training_episodes // batch_size`` (or the episode count
        directly for a small run with ``batch_size=1``).
        """
        self.history = []
        # Re-pin the RNG at the start of the run so the draw sequence depends
        # only on ``seed`` — not on whatever RNG state a previous trainer or
        # script left behind. This is what makes two same-seed trainers
        # bit-for-bit identical and a single trainer's run replayable.
        seed_all(self.seed)
        for step in range(steps):
            batch = self.env.sample(batch_size)
            metrics = self.step(batch)
            metrics = {k: float(v) for k, v in metrics.items()}
            metrics["step"] = step
            self.history.append(metrics)
        return self.history

    # -- evaluation / reuse of saved episodes ------------------------------- #

    def evaluate(
        self,
        batch: Dict[str, torch.Tensor],
    ) -> Dict[str, torch.Tensor]:
        """Run one eval batch under ``torch.no_grad`` and return loss metrics.

        No weight update; the economy is still simulated (forward pass runs the
        substrate), so energy/decay readouts are measured consequences, not
        training signals.
        """
        with torch.no_grad():
            out = self.bridge(
                batch["x"], batch["cue"], batch["regime"], batch["correct"]
            )
            _, metrics = compute_losses(self.config, out, batch)
        return {k: float(v) for k, v in metrics.items()}

    def save_eval_episodes(self, batch: Dict[str, torch.Tensor], path: str) -> int:
        """Serialize a batch for reuse by other arms (same environment, same
        episodes). Returns the number of episodes written."""
        return save_episodes(path, self.env.to_records(batch))

    @staticmethod
    def load_eval_episodes(path: str) -> Dict[str, torch.Tensor]:
        """Reconstruct a batch from a saved episode file."""
        return BridgeEnv.from_records(load_episodes(path))

    # -- checkpointing ------------------------------------------------------ #

    def state_dict(self) -> Dict:
        return {
            "config": self.config.to_dict(),
            "seed": self.seed,
            "bridge": self.bridge.state_dict(),
            "optimizer": self.optimizer.state_dict(),
        }

    def save_checkpoint(self, path: str) -> None:
        torch.save(self.state_dict(), path)

    @classmethod
    def load_checkpoint(cls, path: str, bridge: Optional[NeuralBridge] = None) -> "BridgeTrainer":
        ckpt = torch.load(path, map_location="cpu", weights_only=False)
        config = BridgeConfig.from_dict(ckpt["config"])
        seed = ckpt["seed"]
        trainer = cls(config, seed, bridge=bridge)
        trainer.bridge.load_state_dict(ckpt["bridge"])
        trainer.optimizer.load_state_dict(ckpt["optimizer"])
        return trainer
