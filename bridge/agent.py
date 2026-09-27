"""Assembled neural bridge (frozen v3 protocol): wires the six modules to the
substrate economy and runs a batch forward pass on CPU.

``NeuralBridge`` is the smallest faithful realization of ``ACI_BRIDGE_PROTOCOL
_v3.md`` §6: the controller (GRU ``h_t``), the paid maintained workspace ``W``,
the self-resource estimate ``V``, the maintenance allocator ``A``, the probe
readout ``S_pol``, and the paid refresh action ``pi`` — connected to the
substrate law (energy / decay bookkeeping) so every economy quantity is
inspectable per tick.

This is an implementation scaffold, not a claim: per v3 §13 the frozen
protocol records a STOP (the central contrast is unidentifiable, N6) and this
module must not be presented as a test of *inferred* integrity. It realizes
the architecture so downstream train/test code can inspect the economy and the
module APIs.
"""

from __future__ import annotations

from typing import Dict, Optional, Tuple

import torch
import torch.nn as nn

from bridge.config import BridgeConfig
from bridge.modules import (
    Controller,
    IntegrityEstimator,
    MaintenanceAllocator,
    ProbeReadout,
    RefreshAction,
    Workspace,
    count_parameters,
)
from bridge.substrate import Substrate

__all__ = ["NeuralBridge"]


class NeuralBridge(nn.Module):
    """The bridge agent: controller + W + V + A + S_pol + pi + substrate."""

    def __init__(self, config: BridgeConfig):
        super().__init__()
        self.config = config
        arch = config.arch
        self.controller = Controller(arch, config.init)
        self.workspace = Workspace(arch)
        self.v_estimator = IntegrityEstimator(arch, config.init)
        self.allocator = MaintenanceAllocator(arch, config.init)
        self.probe = ProbeReadout(arch, config.init)
        self.refresh = RefreshAction(config.energy)
        self.substrate = Substrate(config.energy, config.decay)

    # -- parameter accounting ---------------------------------------------- #

    def actual_parameter_counts(self) -> Dict[str, int]:
        """Actual trainable-parameter counts, keyed like ``BridgeConfig``."""
        counts = {
            "gru": count_parameters(self.controller.gru),
            "f_V": count_parameters(self.v_estimator.fc),
            "A_policy": count_parameters(self.allocator.policy),
            "A_critic": count_parameters(self.allocator.critic),
            "S_pol": count_parameters(self.probe.fc),
        }
        counts["total"] = sum(counts.values())
        return counts

    # -- forward ------------------------------------------------------------ #

    def forward(
        self,
        x: torch.Tensor,
        cue: torch.Tensor,
        regime: torch.Tensor,
        correct: Optional[torch.Tensor] = None,
    ) -> Dict[str, torch.Tensor]:
        """Run a batch of episodes through the bridge.

        Parameters
        ----------
        x : (B, T, distractor_dim) distractor stream (c-independent).
        cue : (B, w_bits) the cue identity presented at t=0.
        regime : (B, T, regime_dim) announced-regime one-hot per tick.
        correct : (B, T) bool, whether each distractor tick was processed
            correctly (the metabolic task that earns energy). Defaults to all
            correct.

        Returns a dict of per-tick tensors plus the probe readout, so train and
        test code can inspect the economy: ``h``, ``v`` (discrete code),
        ``v_logits`` (read-in logits, for the L_V supervision), ``b`` (the
        content-blind bookkeeping ``(E_t, d_t)`` V actually read each tick),
        ``refresh_logit``, ``refresh_prob``, ``refresh`` (action), ``logp``,
        ``value``, ``energy``, ``age``, ``alive``, ``spend``, ``slot``, and
        ``probe_logits`` (B, 2) at the probe tick.
        """
        B, T, _ = x.shape
        device = x.device
        dtype = x.dtype
        if correct is None:
            correct = torch.ones(B, T, dtype=torch.bool, device=device)

        self.workspace.reset(B, device)
        self.substrate.reset(B, device)

        # Controller over the full sequence; h_seq[:, t] is h_t (after x_t).
        h_seq, _ = self.controller(x)  # (B, T, H)

        v_prev = torch.zeros(B, self.v_estimator.code_dim, device=device, dtype=dtype)
        h_prev = torch.zeros(B, self.controller.hidden_size, device=device, dtype=dtype)

        self.workspace.write(cue)

        # Accumulators.
        v_seq, v_logits_seq, b_seq, refresh_logits, refresh_probs, refresh_acts = (
            [], [], [], [], [], []
        )
        logps, values = [], []
        energy_seq, age_seq, alive_seq, spend_seq = [], [], [], []
        slot_seq = []

        for t in range(T):
            # Content-blind bookkeeping b_t = (E_t, d_t).
            b_t = torch.stack(
                [self.substrate.energy, self.substrate.age.float()], dim=-1
            )

            v_logits = self.v_estimator(v_prev, h_prev, b_t)
            e_code, i_code = self.v_estimator.decode(v_logits)
            v_t = self.v_estimator.encode(e_code, i_code)  # detached discrete code

            s_t = regime[:, t]
            refresh_logit, value = self.allocator(v_t, s_t)
            action, prob, logp = self.allocator.sample(refresh_logit)

            # Substrate economy for this tick.
            self.substrate.earn(correct[:, t])
            spend = self.substrate.spend(action)
            self.substrate.apply_refresh(action)
            slot_readout = self.substrate.decay_slot(self.workspace.slot, action)
            self.substrate.tick_age()

            v_seq.append(v_t)
            v_logits_seq.append(v_logits)
            b_seq.append(b_t)
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

            v_prev = v_t
            h_prev = h_seq[:, t]

        # Probe readout at the probe tick (t = delay_d), over (W, x_t) only.
        # W is the slot state *at* the probe tick (after that tick's decay),
        # not the end-of-episode slot.
        probe_tick = min(self.config.decay.delay_d, T - 1)
        probe_logits = self.probe(slot_seq[probe_tick], x[:, probe_tick])

        return {
            "h": h_seq,
            "v": torch.stack(v_seq, dim=1),               # (B, T, code_dim)
            "v_logits": torch.stack(v_logits_seq, dim=1),  # (B, T, n_E + n_I)
            "b": torch.stack(b_seq, dim=1),                # (B, T, 2) = (E_t, d_t)
            "refresh_logit": torch.stack(refresh_logits, dim=1),
            "refresh_prob": torch.stack(refresh_probs, dim=1),
            "refresh": torch.stack(refresh_acts, dim=1),
            "logp": torch.stack(logps, dim=1),
            "value": torch.stack(values, dim=1),
            "energy": torch.stack(energy_seq, dim=1),      # (B, T)
            "age": torch.stack(age_seq, dim=1),
            "alive": torch.stack(alive_seq, dim=1),
            "spend": torch.stack(spend_seq, dim=1),
            "slot": torch.stack(slot_seq, dim=1),          # (B, T, w_bits)
            "probe_logits": probe_logits,                  # (B, 2)
        }
