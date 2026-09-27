"""Phase-III training (G10's training objective, G2 §1.1 / G3 §2).

The learned component of every arm is trained here. The encoder (candidate,
R1) is supervised toward the running sufficient statistic via BCE over
sigma(W_raw_t) with z as the training-only label. R2's RNN + heads and R3's
readers + heads are trained to match the fixed specialist *targets* computed
from the true S_t (training-only scaffold): S_pol targets sign(S_H), S_plan
targets the SPRT decision, S_reg targets the even threshold. No arm ever
receives z (or the specialist targets) in its forward graph at eval.

All training is deterministic given the model seed (``seed_all``) and uses a
fresh episode stream per step (no arm sees a different task).
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

import bridge.reproducibility as _rep

from phase3.config import Phase3Config
from phase3.model import Encoder, Maintenance
from phase3.specialists import COMMIT_A, COMMIT_B, POSTPONE
from phase3.task import sample_episodes, token_stream_to_s

__all__ = ["train_encoder", "train_r2", "train_r3", "r2_heads", "r3_heads",
           "encoder_forward", "specialist_targets"]


def encoder_forward(encoder: Encoder, x_oh: torch.Tensor,
                    maint: Optional[Maintenance] = None) -> torch.Tensor:
    """Unroll the encoder over a batch x_oh (B, H, n_tok); returns w_raw (B, H).

    The maintenance substrate is the *intact* (always-affordable) schedule here:
    training the encoder toward the clean running LLR. The decay is applied by
    the persistence transition so the trained encoder learns to compensate for
    the read-back it will see at eval.
    """
    B, H, _ = x_oh.shape
    device = x_oh.device
    h = None
    w_stored = torch.zeros(B, device=device)
    e = torch.full((B,), maint.p.e0, device=device) if maint is not None else None
    d = torch.zeros(B, device=device) if maint is not None else None
    w_raw_list = []
    for t in range(H):
        w_prev = w_stored
        h, w_raw = encoder.step(x_oh[:, t, :], w_prev, h)
        if maint is not None:
            probe_entry = H - maint.cfg.task.probe_window
            s = torch.full((B,), 1 if t >= probe_entry else 0,
                           device=device, dtype=torch.long)
            refresh = maint.decide_refresh(s, e, d)
            leak = torch.where(refresh > 0.5, 1.0, 1.0 - maint.p.delta)
            h = h * leak.view(1, -1, 1)
            e = e - maint.p.e_proc - maint.refresh_cost(refresh)
            e = torch.clamp(e, min=0.0)
            w_stored = maint.persist(w_raw, refresh)
            d = torch.where(refresh > 0.5, torch.zeros_like(d), d + 1)
        else:
            w_stored = w_raw
        w_raw_list.append(w_raw)
    return torch.stack(w_raw_list, dim=1)  # (B, H)


def specialist_targets(cfg: Phase3Config, x: torch.Tensor, thr: Dict[str, float]) -> Dict[str, torch.Tensor]:
    """Fixed specialist targets from the true running LLR S_t (training-only).

    Returns spol (B, H) int, splan (B, H) int, sreg (B, H) int computed from
    S_t = cumsum(lambda(x)) — the analytic optima G3 keeps as co-equal rivals.
    """
    lam = torch.tensor(cfg.task.token_lambda, dtype=torch.float64)
    s = torch.cumsum(lam[x.long()], dim=-1)  # (B, H) float64
    a, b = thr["a"], thr["b"]
    e_crit = cfg.persistence.e_crit
    e0 = cfg.persistence.e0
    H = cfg.task.horizon
    K = cfg.task.probe_window
    # theta per step (reactive); for the target we use the affluent regime.
    regime = torch.zeros(H, dtype=torch.int64)
    regime[H - K:] = 1
    theta = torch.clamp(
        cfg.specialist.theta_base
        - cfg.specialist.theta_probe * (regime == 1).float()
        + cfg.specialist.theta_energy * torch.clamp(e0 - torch.tensor(e_crit), min=0.0),
        cfg.specialist.theta_lo, a,
    )
    spol = (s <= 0).long()                              # B=1 when S<=0, A=0 when S>0
    splan = torch.full(s.shape, POSTPONE, dtype=torch.long)  # postpone (encoding = specialists.s_plan)
    splan[s >= a] = COMMIT_A                            # commit-A
    splan[s <= -b] = COMMIT_B                           # commit-B
    sreg = (s.abs() < theta).long()                    # release=1 when |S|<theta
    return {"spol": spol, "splan": splan, "sreg": sreg}


def train_encoder(cfg: Phase3Config, encoder: Encoder, steps: int,
                  lr: float, seed: int, name: str = "encoder") -> List[float]:
    """Train one encoder (candidate or one R1 private encoder) by BCE."""
    maint = Maintenance(cfg)
    opt = torch.optim.Adam(encoder.parameters(), lr=lr, weight_decay=cfg.training.weight_decay)
    losses: List[float] = []
    for step_i in range(steps):
        _rep.seed_all(seed + step_i)
        z, x = sample_episodes(cfg.task, cfg.training.batch_size, seed + step_i)
        x_t = torch.from_numpy(x).long()
        x_oh = F.one_hot(x_t, num_classes=cfg.task.n_tokens).float()
        z_t = torch.from_numpy(z).float().unsqueeze(1)  # (B, 1)
        opt.zero_grad()
        w_raw = encoder_forward(encoder, x_oh, maint)      # (B, H)
        # z = 0 means A, 1 means B; W is trained toward S_t (positive for A).
        # BCE(sigma(W), 1[z == A]) pushes W -> +inf for A, -inf for B.
        target_a = (z_t == 0).float()                     # (B, 1)
        loss = F.binary_cross_entropy_with_logits(
            w_raw, target_a.expand(-1, cfg.task.horizon)
        )
        loss.backward()
        opt.step()
        losses.append(float(loss.detach()))
    return losses


def r2_heads(cfg: Phase3Config, hidden: int) -> nn.ModuleDict:
    """R2's three learned heads over h_t (each also reads its specialist context)."""
    heads = nn.ModuleDict()
    heads["spol"] = nn.Linear(hidden + cfg.task.n_tokens, 2)      # h_t + x_t
    heads["splan"] = nn.Linear(hidden + 1, 3)                     # h_t + cost (scalar)
    heads["sreg"] = nn.Linear(hidden + 3, 2)                      # h_t + (E, d, s)
    return heads


def r3_heads(cfg: Phase3Config, hidden: int) -> nn.ModuleDict:
    """R3's three learned heads over each reader feature."""
    heads = nn.ModuleDict()
    heads["spol"] = nn.Linear(hidden + cfg.task.n_tokens, 2)
    heads["splan"] = nn.Linear(hidden + 1, 3)
    heads["sreg"] = nn.Linear(hidden + 3, 2)
    return heads


def _context_inputs(cfg: Phase3Config, x_oh: torch.Tensor, h: torch.Tensor,
                    name: str) -> torch.Tensor:
    """Concatenate h with the specialist's declared context (G3 §2)."""
    B, H, _ = h.shape
    if name == "spol":
        ctx = x_oh  # (B, H, n_tok)
    elif name == "splan":
        ctx = torch.zeros(B, H, 1, device=h.device)  # cost context (fixed scalar)
    else:  # sreg
        regime = torch.zeros(B, H, 1, device=h.device)
        regime[:, H - cfg.task.probe_window:, 0] = 1.0
        e = torch.full((B, H, 1), cfg.persistence.e0, device=h.device)
        d = torch.zeros(B, H, 1, device=h.device)
        ctx = torch.cat([e, d, regime], dim=-1)
    return torch.cat([h, ctx], dim=-1)


def train_r2(cfg: Phase3Config, rnn: nn.Module, heads: nn.ModuleDict, steps: int,
             lr: float, seed: int) -> List[float]:
    """Train R2's RNN + heads to match the specialist targets (supervised)."""
    from phase3.arms import compute_thresholds
    thr = compute_thresholds(cfg)
    params = list(rnn.parameters()) + list(heads.parameters())
    opt = torch.optim.Adam(params, lr=lr, weight_decay=cfg.training.weight_decay)
    losses: List[float] = []
    for step_i in range(steps):
        _rep.seed_all(seed + step_i)
        z, x = sample_episodes(cfg.task, cfg.training.batch_size, seed + step_i)
        x_t = torch.from_numpy(x).long()
        x_oh = F.one_hot(x_t, num_classes=cfg.task.n_tokens).float()
        tgt = specialist_targets(cfg, x_t, thr)
        opt.zero_grad()
        out, _ = rnn(x_oh.transpose(0, 1))
        h = out.transpose(0, 1)  # (B, H, d_h)
        loss = torch.zeros((), device=x_oh.device)
        loss = loss + F.cross_entropy(
            heads["spol"](_context_inputs(cfg, x_oh, h, "spol")).reshape(-1, 2),
            tgt["spol"].reshape(-1))
        loss = loss + F.cross_entropy(
            heads["splan"](_context_inputs(cfg, x_oh, h, "splan")).reshape(-1, 3),
            tgt["splan"].reshape(-1))
        loss = loss + F.cross_entropy(
            heads["sreg"](_context_inputs(cfg, x_oh, h, "sreg")).reshape(-1, 2),
            tgt["sreg"].reshape(-1))
        loss.backward()
        opt.step()
        losses.append(float(loss.detach()))
    return losses


def train_r3(cfg: Phase3Config, readers: List[nn.Module], heads: nn.ModuleDict,
             steps: int, lr: float, seed: int) -> List[float]:
    """Train R3's three readers + heads (each reader specializes one function)."""
    from phase3.arms import compute_thresholds
    thr = compute_thresholds(cfg)
    params = list(heads.parameters())
    for r in readers:
        params += list(r.parameters())
    opt = torch.optim.Adam(params, lr=lr, weight_decay=cfg.training.weight_decay)
    losses: List[float] = []
    names = ["spol", "splan", "sreg"]
    for step_i in range(steps):
        _rep.seed_all(seed + step_i)
        z, x = sample_episodes(cfg.task, cfg.training.batch_size, seed + step_i)
        x_t = torch.from_numpy(x).long()
        x_oh = F.one_hot(x_t, num_classes=cfg.task.n_tokens).float()
        tgt = specialist_targets(cfg, x_t, thr)
        opt.zero_grad()
        loss = torch.zeros((), device=x_oh.device)
        for i, name in enumerate(names):
            out, _ = readers[i](x_oh.transpose(0, 1))
            h = out.transpose(0, 1)
            n_out = heads[name].out_features
            loss = loss + F.cross_entropy(
                heads[name](_context_inputs(cfg, x_oh, h, name)).reshape(-1, n_out),
                tgt[name].reshape(-1))
        loss.backward()
        opt.step()
        losses.append(float(loss.detach()))
    return losses
