"""Phase-III encoder (learned) and maintenance substrate (no gradient).

The encoder f_enc is a GRU mapping (W_{t-1}, x_t) -> W_t (G4 §2): it receives
the current token x_t (one-hot) and the *decayed* maintained slot W_{t-1}, and
emits the scalar log-likelihood-ratio estimate W_raw_t, quantized to b bits.
It is trained (supervised) toward the running sufficient statistic S_t via
BCE(sigma(W_raw_t), z) summed over steps — the "trained toward the quantized
S_H with z as the training-only label" objective of G2 §1.1.

The maintenance substrate (pi + A) is a pure law with no parameters and no
gradient path (N4 §7.3): between steps the stored W relaxes toward neutral by
``(1 - delta)`` unless the paid refresh pi (cost c) holds it. The rule A is
fixed/reactive on (s, E, d) only (verdict D) — never W.
"""

from __future__ import annotations

from typing import Optional, Tuple

import torch
import torch.nn as nn

from phase3.config import Phase3Config

__all__ = ["Encoder", "Maintenance", "count_parameters"]


def count_parameters(module: nn.Module) -> int:
    return sum(p.numel() for p in module.parameters() if p.requires_grad)


class Encoder(nn.Module):
    """GRU encoder: h_t = GRU(h_{t-1}, [onehot(x_t); W_{t-1}]); W_raw = linear(h_t).

    The hidden state h_t is the acquisition machinery (L1 in the leakage audit).
    W_raw_t is the unquantized scalar LLR estimate; quantization happens in the
    caller (the maintained slot stores the float, specialists read the quantized
    value). Trained by BCE(sigma(W_raw_t), z) over all steps.
    """

    def __init__(self, cfg: Phase3Config, hidden_size: Optional[int] = None):
        super().__init__()
        self.input_size = cfg.task.n_tokens + 1       # one-hot x_t + scalar W_{t-1}
        self.hidden_size = hidden_size or cfg.arm.p_levels[cfg.arm.p_level]
        self.gru = nn.GRU(
            input_size=self.input_size,
            hidden_size=self.hidden_size,
            batch_first=False,
        )
        self.head = nn.Linear(self.hidden_size, 1)
        self._init()

    def _init(self) -> None:
        for p in self.gru.parameters():
            if p.dim() >= 2:
                nn.init.xavier_uniform_(p)
            else:
                nn.init.zeros_(p)
        nn.init.xavier_uniform_(self.head.weight)
        nn.init.zeros_(self.head.bias)

    def step(self, x_t: torch.Tensor, w_prev: torch.Tensor,
             h_prev: Optional[torch.Tensor]) -> Tuple[torch.Tensor, torch.Tensor]:
        """One step: x_t (B, n_tokens) one-hot, w_prev (B,) scalar -> (h_t, W_raw_t).

        Residual form W_raw_t = W_{t-1} + head(GRU(h_{t-1}, [x_t; W_{t-1}])):
        the GRU learns the *increment* (the lambda mapping), while the running
        accumulation is carried structurally by the W feedback. This is what
        makes MAINTAINED testable — with W zeroed (F1), the encoder emits only
        the single-step increment, so the recurrence h_t cannot accumulate z
        independently of the paid-maintained W.
        """
        inp = torch.cat([x_t, w_prev.unsqueeze(-1)], dim=-1).unsqueeze(0)  # (1, B, in)
        out, h_t = self.gru(inp, h_prev)                                   # (1, B, h), (1, B, h)
        increment = self.head(out).squeeze(0).squeeze(-1)                   # (B,)
        w_raw = w_prev + increment
        return h_t, w_raw

    def forward(self, x: torch.Tensor, w_prev: torch.Tensor,
                h_prev: Optional[torch.Tensor]) -> Tuple[torch.Tensor, torch.Tensor]:
        return self.step(x, w_prev, h_prev)


class Maintenance:
    """The paid-persistence substrate (no parameters, no gradient).

    Owns the per-batch bookkeeping: energy E, decay age d, regime s, and the
    stored slot value W_stored. Each step the caller asks for the refresh
    decision (A) and applies the persistence transition.

    ``decide_refresh(s, E, d)`` is A: fixed/reactive on (s, E, d) only.
    ``persist(w_raw, refresh)`` returns the next stored value — ``w_raw`` held
    where refreshed, else ``w_raw * (1 - delta)`` decayed — and the energy
    ledger update.
    """

    def __init__(self, cfg: Phase3Config):
        self.cfg = cfg
        self.p = cfg.persistence
        self.m = cfg.maintenance

    def decide_refresh(self, s: torch.Tensor, e: torch.Tensor, d: torch.Tensor) -> torch.Tensor:
        """A: refresh iff affordable and (probe or d >= interval). z-blind."""
        affordable = e >= self.p.cost
        probe = (s == 1)
        interval = d >= self.m.refresh_interval
        return (affordable & (probe | interval)).float()

    def refresh_cost(self, refresh: torch.Tensor) -> torch.Tensor:
        return refresh * self.p.cost

    def persist(self, w_raw: torch.Tensor, refresh: torch.Tensor) -> torch.Tensor:
        """Next stored value: hold where refreshed, decay elsewhere."""
        decayed = w_raw * (1.0 - self.p.delta)
        return torch.where(refresh > 0.5, w_raw, decayed)

    def apply_decay(self, w_raw: torch.Tensor, refresh: torch.Tensor) -> torch.Tensor:
        return self.persist(w_raw, refresh)
