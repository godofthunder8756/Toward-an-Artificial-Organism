"""Phase-III arms (G4): the candidate (SLW) and the five reduction rivals.

Each arm is a uniform interface over the same token stream:

- ``run(x, *, cut_pi, zero_w)`` unrolls a batch of episodes and returns the
  arm's *content* trajectory plus the economy ledger. For the scalar-W arms
  (candidate, R1, R4, R5) the content is the quantized W (one slot for the
  candidate/R4, three private slots for R1/R5); for R2 the content is the
  monolithic hidden state; for R3 it is the raw history.

- The specialist outputs are derived *separately* by ``apply_specialists``
  (the fixed function forms of G3), which is what makes the interventions
  (I1-I5) a pure wiring check: overwrite the content, re-apply the fixed
  functions, and assert the signature traces the injected value exactly.

Every arm runs the identical token stream (observation equality), never
receives z in its forward graph, and holds no pristine copy of its content.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

from phase3.config import Phase3Config
from phase3.model import Encoder, Maintenance
from phase3.specialists import (
    s_bias, s_conf, s_plan, s_pol, s_reg, sprt_boundaries, theta_value,
)
from phase3.task import Quantizer, token_stream_to_s

__all__ = [
    "Arm",
    "compute_thresholds",
    "apply_specialists",
    "quantize_w",
    "trajectory",
]

REGIME_ACCUMULATE, REGIME_PROBE = 0, 1


def compute_thresholds(cfg: Phase3Config) -> Dict[str, float]:
    """Derive (a, b, theta_bias) before training (G2 §2 / G3 §2.2 / G7 §2.2)."""
    a, b = sprt_boundaries(
        cfg.specialist, cfg.w.bits, cfg.w.lo, cfg.w.hi, cfg.task.informative_steps
    )
    theta_bias = float(np.log(cfg.specialist.c_ba / cfg.specialist.c_ab))
    return {"a": a, "b": b, "theta_bias": theta_bias}


def quantize_w(cfg: Phase3Config, w_raw: np.ndarray) -> np.ndarray:
    """Quantize a raw scalar (or trajectory) to the b-bit level value."""
    q = Quantizer(cfg.w)
    return q.round_trip(np.asarray(w_raw, dtype=np.float64))


def _one_hot(x: torch.Tensor, n_tokens: int) -> torch.Tensor:
    return F.one_hot(x.long(), num_classes=n_tokens).float()


class Arm:
    """A named arm binding its learned modules to its topology.

    ``run`` returns a dict of per-batch trajectories. Scalar-W arms expose
    ``w`` (quantized content) plus the economy ledger; R2 exposes ``h``; R3
    exposes the history. ``n_copies`` is 1 (shared) or 3 (private), and
    ``has_w`` marks whether a latent W exists to scramble/cut (R2/R3 do not).
    """

    arm_name: str = "candidate"

    def __init__(self, cfg: Phase3Config, encoders: Optional[Dict[str, nn.Module]] = None,
                 arm_name: Optional[str] = None):
        self.cfg = cfg
        self.q = Quantizer(cfg.w)
        self.maint = Maintenance(cfg)
        self.thr = compute_thresholds(cfg)
        self.encoders = encoders or {}
        if arm_name is not None:
            self.arm_name = arm_name

    # -- topology facts (auditable wiring) ---------------------------------- #

    @property
    def has_w(self) -> bool:
        return self.arm_name in {"candidate", "r1", "r4", "r5"}

    @property
    def n_copies(self) -> int:
        return 3 if self.arm_name in {"r1", "r5"} else 1

    @property
    def has_maintenance(self) -> bool:
        return self.arm_name in {"candidate", "r1"}

    # -- unroll ------------------------------------------------------------- #

    def run(self, x: np.ndarray, *, cut_pi: bool = False, zero_w: bool = False) -> Dict[str, np.ndarray]:
        """Unroll a batch of episodes x (B, H) token indices."""
        x = np.asarray(x, dtype=np.int64)
        if self.arm_name == "candidate":
            return self._run_scalar_w(x, cut_pi=cut_pi, zero_w=zero_w,
                                      n_copies=1, use_encoder=True, use_maint=True)
        if self.arm_name == "r1":
            return self._run_scalar_w(x, cut_pi=cut_pi, zero_w=False,
                                      n_copies=3, use_encoder=True, use_maint=True)
        if self.arm_name == "r4":
            return self._run_scalar_w(x, cut_pi=False, zero_w=False,
                                      n_copies=1, use_encoder=False, use_maint=False)
        if self.arm_name == "r5":
            return self._run_scalar_w(x, cut_pi=False, zero_w=False,
                                      n_copies=3, use_encoder=False, use_maint=False)
        if self.arm_name == "r2":
            return self._run_r2(x)
        if self.arm_name == "r3":
            return self._run_r3(x)
        raise ValueError(f"unknown arm {self.arm_name!r}")

    # -- scalar-W arms (candidate, R1, R4, R5) ------------------------------ #

    def _run_scalar_w(self, x: np.ndarray, *, cut_pi: bool, zero_w: bool,
                      n_copies: int, use_encoder: bool, use_maint: bool) -> Dict[str, np.ndarray]:
        cfg = self.cfg
        B, H = x.shape
        K = cfg.task.probe_window

        if not use_encoder:
            # R4/R5: fixed analytic accumulator S_t = sum lambda(x_i), free register.
            s = token_stream_to_s(cfg.task, x)                     # (B, H)
            w_raw = s
            w = quantize_w(cfg, w_raw)
            if n_copies == 1:
                w_out = w
            else:
                w_out = np.stack([w, w, w], axis=-1)               # (B, H, 3) identical copies
            return {
                "w": w_out, "w_raw": w_raw,
                "refresh": np.zeros((B, H)), "energy": np.zeros((B, H)),
                "age": np.zeros((B, H)), "regime": _regime_traj(H, K),
            }

        # candidate / R1: learned encoder(s) + paid maintenance.
        n_tok = cfg.task.n_tokens
        device = next(iter(self.encoders.values())).parameters().__next__().device \
            if self.encoders else torch.device("cpu")
        keys = ["enc"] if n_copies == 1 else [f"enc{i}" for i in range(n_copies)]
        encoders = [self.encoders[k] for k in keys]

        x_t = torch.from_numpy(x).long()
        x_oh = _one_hot(x_t, n_tok)                                 # (B, H, n_tok)

        w_raw_copies = []
        w_stored_copies = []
        refresh_copies = []
        h_copies = []
        for enc in encoders:
            w_raw_list, w_stored_list, refresh_list, h_list = [], [], [], []
            h = None
            w_stored = torch.zeros(B, device=device)
            e = torch.full((B,), self.maint.p.e0, device=device)
            d = torch.zeros(B, device=device)
            for t in range(H):
                s = REGIME_PROBE if t >= H - K else REGIME_ACCUMULATE
                s_t = torch.full((B,), s, device=device, dtype=torch.long)
                if cut_pi or not use_maint:
                    refresh = torch.zeros(B, device=device)
                else:
                    refresh = self.maint.decide_refresh(s_t, e, d)
                w_prev = torch.zeros(B, device=device) if zero_w else w_stored
                h, w_raw = enc.step(x_oh[:, t, :], w_prev, h)
                # workspace leak: h_t relaxes toward neutral unless pi re-energizes it
                leak = torch.where(refresh > 0.5, 1.0, 1.0 - self.maint.p.delta)
                h = h * leak.view(1, -1, 1)
                e = e - self.maint.p.e_proc - self.maint.refresh_cost(refresh)
                e = torch.clamp(e, min=0.0)
                w_stored = self.maint.persist(w_raw, refresh)
                d = torch.where(refresh > 0.5, torch.zeros_like(d), d + 1)
                w_raw_list.append(w_raw.detach().cpu().numpy())
                w_stored_list.append(w_stored.detach().cpu().numpy())
                refresh_list.append(refresh.detach().cpu().numpy())
                h_list.append(h.detach().squeeze(0).cpu().numpy())   # (B, d_h)
            w_raw_copies.append(np.stack(w_raw_list, axis=1))       # (B, H)
            w_stored_copies.append(np.stack(w_stored_list, axis=1))
            refresh_copies.append(np.stack(refresh_list, axis=1))
            h_copies.append(np.stack(h_list, axis=1))               # (B, H, d_h)

        w_raw = w_raw_copies[0] if n_copies == 1 else np.stack(w_raw_copies, axis=-1)
        w_stored = w_stored_copies[0] if n_copies == 1 else np.stack(w_stored_copies, axis=-1)
        refresh = refresh_copies[0] if n_copies == 1 else np.stack(refresh_copies, axis=-1)
        w = quantize_w(cfg, w_raw)

        # Energy ledger (single shared budget for the candidate; R1 carries three
        # independent budgets, reported as the 3x maintenance economy).
        energy = np.zeros((B, H))
        e = np.full((B,), cfg.persistence.e0)
        age = np.zeros((B, H))
        d = np.zeros(B)
        for t in range(H):
            s = REGIME_PROBE if t >= H - K else REGIME_ACCUMULATE
            r = refresh[:, t] if n_copies == 1 else refresh[:, t, 0]
            e = e - cfg.persistence.e_proc - r * cfg.persistence.cost
            e = np.clip(e, 0.0, None)
            energy[:, t] = e
            d = np.where(r > 0.5, 0.0, d + 1)
            age[:, t] = d

        return {
            "w": w, "w_raw": w_raw, "w_stored": w_stored,
            "h": h_copies[0] if n_copies == 1 else np.stack(h_copies, axis=-2),
            "refresh": refresh, "energy": energy, "age": age,
            "regime": _regime_traj(H, K),
        }

    # -- R2: monolithic recurrent policy (no W, no pi) ---------------------- #

    def _run_r2(self, x: np.ndarray) -> Dict[str, np.ndarray]:
        cfg = self.cfg
        B, H = x.shape
        device = next(iter(self.encoders.values())).parameters().__next__().device
        rnn = self.encoders["rnn"]
        x_t = torch.from_numpy(x).long()
        x_oh = _one_hot(x_t, cfg.task.n_tokens)                      # (B, H, n_tok)
        out, _ = rnn(x_oh.transpose(0, 1))                            # (H, B, d_h)
        h = out.transpose(0, 1)                                       # (B, H, d_h)
        return {
            "h": h.detach().cpu().numpy(),
            "regime": _regime_traj(H, cfg.task.probe_window),
        }

    # -- R3: direct history-access readers (no W, no pi) -------------------- #

    def _run_r3(self, x: np.ndarray) -> Dict[str, np.ndarray]:
        cfg = self.cfg
        B, H = x.shape
        device = next(iter(self.encoders.values())).parameters().__next__().device
        x_t = torch.from_numpy(x).long()
        x_oh = _one_hot(x_t, cfg.task.n_tokens)                      # (B, H, n_tok)
        feats = []
        for i in range(cfg.arm.n_specialists):
            reader = self.encoders[f"reader{i}"]
            out, _ = reader(x_oh.transpose(0, 1))
            feats.append(out.transpose(0, 1).detach().cpu().numpy())  # (B, H, d_h)
        return {
            "features": np.stack(feats, axis=-2),                     # (B, H, 3, d_h)
            "history": x_oh.detach().cpu().numpy(),
            "regime": _regime_traj(H, cfg.task.probe_window),
        }


def _regime_traj(H: int, K: int) -> np.ndarray:
    r = np.zeros(H, dtype=np.int64)
    r[H - K:] = REGIME_PROBE
    return r


def apply_specialists(w: np.ndarray, cfg: Phase3Config, thr: Dict[str, float],
                      regime: Optional[np.ndarray] = None) -> Dict[str, np.ndarray]:
    """Apply the three fixed specialist functions to a W trajectory.

    ``w`` is (..., H) for the shared arms (candidate/R4) — all three
    specialists read the *same* slot — or (..., H, 3) for the private arms
    (R1/R5), where specialist i reads copy i (S_pol -> copy 0, S_plan -> copy 1,
    S_reg -> copy 2). Returns spol/splan/sreg with the leading (..., H) shape in
    both cases. ``regime`` (H,) supplies the probe/accumulate flag for S_reg's
    reactive theta; energy is taken at the affluent reference value.
    """
    w = np.asarray(w, dtype=np.float64)
    a = thr["a"]
    b = thr["b"]
    e_crit = cfg.persistence.e_crit
    if regime is None:
        regime = np.zeros(w.shape[-1], dtype=np.int64)
        regime[w.shape[-1] - cfg.task.probe_window:] = REGIME_PROBE

    def _theta_for(w_sub: np.ndarray) -> np.ndarray:
        # broadcast the (H,) regime over w_sub's trailing dims
        lead = w_sub.shape[:-1]
        reg = np.broadcast_to(regime.reshape((1,) * len(lead) + (-1,)), w_sub.shape)
        e = np.full(w_sub.shape, cfg.persistence.e0)
        return theta_value(cfg.specialist, e, reg, a, e_crit)

    if w.ndim >= 3 and w.shape[-1] == 3:
        # private copies: specialist i reads copy i
        return {
            "spol": s_pol(w[..., 0]),
            "splan": s_plan(w[..., 1], a, b),
            "sreg": s_reg(w[..., 2], _theta_for(w[..., 2])),
        }
    return {
        "spol": s_pol(w),
        "splan": s_plan(w, a, b),
        "sreg": s_reg(w, _theta_for(w)),
    }
