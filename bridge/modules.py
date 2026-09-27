"""Neural bridge modules (frozen v3 protocol, CPU-only torch).

Implements the six components of ``ACI_BRIDGE_PROTOCOL_v3.md`` §6 as the
smallest faithful neural modules:

- :class:`Controller`        — recurrent controller ``h_t`` (GRU), processes the
  c-independent distractor stream ``x_t``.
- :class:`Workspace`         — ``W``, the paid, non-recurrent 1-bit cue slot
  (storage; no trainable parameters).
- :class:`IntegrityEstimator`— ``V`` / ``f_V``, the discrete self-resource
  estimate with energy + integrity fields (a re-encoding of the observable
  ``(E_t, d_t)``, per N6).
- :class:`MaintenanceAllocator` — ``A``, the homeostatic refresh policy plus a
  learned critic, restricted to ``(v_t, s_t)`` inputs (N4 §6).
- :class:`ProbeReadout`      — ``S_pol``, the probe answer readout, restricted
  to ``(W, x_t)`` inputs (S4).
- :class:`RefreshAction`     — ``pi``, the paid refresh primitive (substrate
  action, no gradient).

The resource economy (energy budget ``B_t``, forward-pass cost ``E_proc``, paid
refresh cost ``E_pi``, set point ``E_crit``, decay-age deadline ``lifetime`` / age ``d_t``) is
carried as explicit arguments and return values throughout, so train/test code
can inspect it. The substrate law itself (energy/decay bookkeeping) lives in
:mod:`bridge.substrate`; this module is the differentiable part.

Nothing in this module references CUDA. All tensors are CPU.
"""

from __future__ import annotations

from typing import Optional, Tuple

import torch
import torch.nn as nn

from bridge.config import ArchConfig, EnergyConfig, InitConfig

__all__ = [
    "Controller",
    "Workspace",
    "IntegrityEstimator",
    "MaintenanceAllocator",
    "ProbeReadout",
    "RefreshAction",
    "count_parameters",
    "apply_init",
]

_EPS = 1e-8


def apply_init(module: nn.Module, init: InitConfig) -> nn.Module:
    """Apply the configured initializer (xavier_uniform/xavier_normal) to a module.

    Weights (dim >= 2) get the configured scheme/gain; biases are zeroed.
    Returns ``module`` for chaining.
    """
    scheme = getattr(init, "scheme", "xavier_uniform")
    gain = float(getattr(init, "gain", 1.0))
    for p in module.parameters():
        if p.dim() >= 2:
            if scheme == "xavier_normal":
                nn.init.xavier_normal_(p, gain=gain)
            else:  # xavier_uniform is the default
                nn.init.xavier_uniform_(p, gain=gain)
        else:
            nn.init.zeros_(p)
    return module


def count_parameters(module: nn.Module) -> int:
    """Number of trainable parameters in ``module``."""
    return sum(p.numel() for p in module.parameters() if p.requires_grad)


class Controller(nn.Module):
    """Recurrent controller ``h_t`` (GRU).

    Input is the c-independent distractor stream ``x_t`` (width
    ``arch.distractor_dim``); the hidden state ``h_t`` is read by ``V`` only.
    No cue content, reward, or regime ever enters this module (S1).
    """

    def __init__(self, arch: ArchConfig, init: InitConfig):
        super().__init__()
        self.input_size = arch.distractor_dim
        self.hidden_size = arch.gru_hidden
        self.gru = nn.GRU(
            input_size=self.input_size,
            hidden_size=self.hidden_size,
            batch_first=True,
        )
        apply_init(self.gru, init)

    def forward(
        self,
        x: torch.Tensor,
        h: Optional[torch.Tensor] = None,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """Run the controller over a sequence.

        ``x``: (B, T, input_size) or (B, input_size). Returns
        ``(h_seq, h_final)`` where ``h_seq`` is (B, T, hidden_size) and
        ``h_final`` is (1, B, hidden_size).
        """
        if x.dim() == 2:
            x = x.unsqueeze(1)
        out, h_final = self.gru(x, h)
        return out, h_final


class Workspace(nn.Module):
    """``W`` — the paid, non-recurrent 1-bit cue slot (v3 §6, §6.2).

    Storage, not parameters: it holds the cue identity written at t=0 by the
    supplied acquisition write (S1). The write/read are hard and
    stop-gradiented (S2) so no reward gradient carrying the cue reaches the
    controller. Persistence against the per-tick decay (age toward ``lifetime``) is the job of
    the paid refresh ``pi``, not of any self-dynamics here.
    """

    def __init__(self, arch: ArchConfig):
        super().__init__()
        self.w_bits = arch.w_bits
        # Sized lazily by reset(); empty until the first episode is allocated.
        self.register_buffer("slot", torch.empty(0), persistent=False)

    def reset(self, batch_size: int, device: Optional[torch.device] = None) -> None:
        self.slot = torch.zeros(batch_size, self.w_bits, device=device)

    def write(self, cue: torch.Tensor) -> torch.Tensor:
        """Hard acquisition write (S2): stores ``cue`` detached. Returns slot."""
        self.slot = cue.detach().to(self.slot.dtype)
        return self.slot

    def read(self) -> torch.Tensor:
        """Read the slot, detached (no gradient through W's content)."""
        return self.slot.detach()


class IntegrityEstimator(nn.Module):
    """``V`` — discrete self-resource estimate with energy + integrity fields.

    ``f_V`` maps ``(v_{t-1}, h_{t-1}, b_t)`` to softmax logits over the
    discrete energy codes (``2**v_energy_bits``) and integrity codes
    (``2**v_integrity_bits``); the stored code ``v_t`` is the detached argmax
    of each head, encoded as a ``v_energy_bits + v_integrity_bits`` binary
    vector. ``b_t = (E_t, d_t)`` is the content-blind bookkeeping (S3).

    Supervised by ``L_V`` (trainer-only, severed at eval); no gradient flows
    from A back through V (stop-gradient on the V→A edge, N4 §6).
    """

    def __init__(self, arch: ArchConfig, init: InitConfig):
        super().__init__()
        self.v_energy_bits = arch.v_energy_bits
        self.v_integrity_bits = arch.v_integrity_bits
        self.n_energy_codes = 2 ** arch.v_energy_bits
        self.n_integrity_codes = 2 ** arch.v_integrity_bits
        self.code_dim = arch.v_energy_bits + arch.v_integrity_bits
        self.b_dim = 2  # b_t = (E_t, d_t), two scalars
        v_in = self.code_dim + arch.gru_hidden + self.b_dim
        v_out = self.n_energy_codes + self.n_integrity_codes
        self.fc = nn.Linear(v_in, v_out)
        apply_init(self.fc, init)

    def forward(
        self,
        v_prev: torch.Tensor,
        h_prev: torch.Tensor,
        b: torch.Tensor,
    ) -> torch.Tensor:
        """Return the read-in logits (B, n_energy_codes + n_integrity_codes)."""
        x = torch.cat([v_prev, h_prev, b], dim=-1)
        return self.fc(x)

    def decode(self, logits: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """Detached argmax over each field -> (energy_code, integrity_code)."""
        e_logits = logits[:, : self.n_energy_codes]
        i_logits = logits[:, self.n_energy_codes:]
        e_code = torch.argmax(e_logits.detach(), dim=-1)  # (B,) in [0, 2^ve)
        i_code = torch.argmax(i_logits.detach(), dim=-1)  # (B,) in [0, 2^vi)
        return e_code, i_code

    def encode(self, e_code: torch.Tensor, i_code: torch.Tensor) -> torch.Tensor:
        """Binary-encode the discrete code -> (B, code_dim) float vector."""
        bits = []
        for k in range(self.v_energy_bits):
            bits.append(((e_code >> k) & 1).float())
        for k in range(self.v_integrity_bits):
            bits.append(((i_code >> k) & 1).float())
        return torch.stack(bits, dim=-1)


class MaintenanceAllocator(nn.Module):
    """``A`` — the homeostatic maintenance allocator (policy + critic).

    Reads ``(v_t, s_t)`` only (N4 §6): the discrete self-resource code and the
    announced regime one-hot. The policy emits a scalar refresh logit
    (Bernoulli over ``refresh``); the critic is the learned baseline for the
    REINFORCE estimate of ``J_A``. Objective is over the *measured* state, never
    V's estimate; "continued operation" (E5) appears in no loss.
    """

    def __init__(self, arch: ArchConfig, init: InitConfig):
        super().__init__()
        in_dim = (arch.v_energy_bits + arch.v_integrity_bits) + arch.regime_dim
        self.policy = nn.Linear(in_dim, 1)  # scalar refresh logit
        self.critic = nn.Linear(in_dim, 1)  # learned baseline b(v_t, s_t)
        apply_init(self.policy, init)
        apply_init(self.critic, init)

    def forward(
        self,
        v: torch.Tensor,
        s: torch.Tensor,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """Return ``(refresh_logit, value)``, each (B,)."""
        x = torch.cat([v, s], dim=-1)
        refresh_logit = self.policy(x).squeeze(-1)
        value = self.critic(x).squeeze(-1)
        return refresh_logit, value

    @staticmethod
    def sample(
        refresh_logit: torch.Tensor,
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """Sample the refresh action.

        Returns ``(action, prob, logp)``: ``action`` in {0,1} (1 = refresh),
        ``prob = sigmoid(logit)``, and the log-probability of the sampled action.
        """
        prob = torch.sigmoid(refresh_logit)
        action = torch.bernoulli(prob)
        logp = torch.where(
            action > 0.5,
            torch.log(prob + _EPS),
            torch.log(1.0 - prob + _EPS),
        )
        return action, prob, logp


class ProbeReadout(nn.Module):
    """``S_pol`` — probe answer readout, restricted to ``(W, x_t)`` (S4).

    Trained on the probe reward (NLL over the cue answer). Reads only the
    maintained slot and the current distractor vector; never ``h_t``, ``V``,
    ``A``, or any auxiliary activation.
    """

    def __init__(self, arch: ArchConfig, init: InitConfig):
        super().__init__()
        in_dim = arch.w_bits + arch.distractor_dim
        self.fc = nn.Linear(in_dim, 2)  # cue answer logits {A, B}
        apply_init(self.fc, init)

    def forward(self, w: torch.Tensor, x_t: torch.Tensor) -> torch.Tensor:
        """Return cue-answer logits (B, 2)."""
        return self.fc(torch.cat([w, x_t], dim=-1))


class RefreshAction:
    """``pi`` — the paid refresh primitive (substrate action, no gradient).

    Not a :class:`torch.nn.Module`: it has no parameters and no gradient path
    (N4 §7.3). It makes the maintenance price and set point explicit so
    train/test code can inspect the economy. The substrate applies its effect
    (pay ``E_pi``, reset decay age ``d_t``) — see :mod:`bridge.substrate`.
    """

    def __init__(self, energy: EnergyConfig):
        self.e_pi = energy.e_pi       # maintenance price per refresh
        self.e_crit = energy.e_crit   # A's set-point threshold (v3 §7.2)

    def cost(self, action: torch.Tensor) -> torch.Tensor:
        """Energy spent on refresh: ``action.float() * E_pi``, shape (B,)."""
        return action.float() * self.e_pi

    @staticmethod
    def reset_age(action: torch.Tensor, age: torch.Tensor) -> torch.Tensor:
        """Decay age after applying the action: 0 where refreshed, else kept."""
        return torch.where(action > 0.5, torch.zeros_like(age), age)
