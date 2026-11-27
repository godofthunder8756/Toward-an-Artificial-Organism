"""P1p: the second architecture (replication of the Layer 4 integrity monitor outside the 70-unit GRU).

Additive module; every earlier module is imported, never modified. Protocol: P1P_REPLICATION_PROTOCOL.md.

Architecture. A coupled-input-forget-gate LSTM (CIFG; Greff et al. 2017) with N_CELL = 35 cells:
    f, o = sigmoid(W_f x + U_f h + b_f), sigmoid(W_o x + U_o h + b_o);  g = tanh(W_g x + U_g h + b_g)
    c' = f * c + (1 - f) * g;   h' = o * tanh(c')
The carried state is packed as s = [h, c] (70 numbers, the same width as the GRU's state), so every damage
operator, probe, direction, push and lesion of P1g-P1m acts on it unchanged: a damage event overwrites K of the
70 numbers, hidden or cell, as for the GRU. The policy and value heads read h only. c' is a convex combination of
c and g, so |c| <= 1 from c0 = 0, and h is in (-1, 1): the [-1, 1] clamps of P1j-P1m stay harmless. The
forget-gate bias starts at 1 (the usual LSTM practice). The encoder (Linear + ReLU, 70 units) is unchanged.

Installation. `install()` replaces, in the modules that construct runners (selfmon, gradmon, steerint,
transfer, necessity, access), each runner class by a subclass that swaps the agent's core and heads for the
CIFG ones right after construction (initialized from torch seed seed + 300007) and rebuilds the optimizer. The
runners' code, the training loop, the evaluations and the analyses are the original ones. Called in each worker
before any runner is built (run_p1p_replication.py). Simulated variables only.
"""
from __future__ import annotations

import torch
from torch import nn

N_CELL = 35
SWAP_SEED = 300007


class CIFGCore(nn.Module):
    """CIFG-LSTM cell on the packed state [h, c]."""

    def __init__(self, n_in: int, n_cell: int = N_CELL):
        super().__init__()
        self.n = n_cell
        self.x2g = nn.Linear(n_in, 3 * n_cell)
        self.h2g = nn.Linear(n_cell, 3 * n_cell, bias=False)
        with torch.no_grad():
            self.x2g.bias[:n_cell].fill_(1.0)          # forget gate opens toward keeping

    def forward(self, x: torch.Tensor, s: torch.Tensor) -> torch.Tensor:
        n = self.n
        h, c = s[:, :n], s[:, n:]
        z = self.x2g(x) + self.h2g(h)
        f, o, g = torch.sigmoid(z[:, :n]), torch.sigmoid(z[:, n:2 * n]), torch.tanh(z[:, 2 * n:])
        c = f * c + (1.0 - f) * g
        return torch.cat([o * torch.tanh(c), c], 1)


class HeadH(nn.Module):
    """A linear head on the hidden half of the packed state."""

    def __init__(self, n_cell: int, n_out: int):
        super().__init__()
        self.n = n_cell
        self.lin = nn.Linear(n_cell, n_out)

    def forward(self, s: torch.Tensor) -> torch.Tensor:
        return self.lin(s[..., :self.n])


def to_cifg(agent, seed: int) -> None:
    """Swap the agent's GRU core and heads for the CIFG ones (in place)."""
    assert agent.hidden == 2 * N_CELL, agent.hidden
    torch.manual_seed(seed + SWAP_SEED)
    agent.core = CIFGCore(agent.enc.out_features, N_CELL)
    agent.pi = HeadH(N_CELL, agent.pi.out_features)
    agent.v = HeadH(N_CELL, 1)


def _swapping(cls):
    if getattr(cls, "arch", None) == "CIFG":
        return cls

    class Swapped(cls):
        def __init__(self, *a, **kw):
            super().__init__(*a, **kw)
            seed = a[1] if len(a) > 1 else kw["seed"]
            to_cifg(self.agent, seed)
            self.opt = torch.optim.Adam(self.agent.parameters(), lr=self.tc.lr)
            self.h = self.agent.init_state(self.tc.n_envs)
    Swapped.__name__ = Swapped.__qualname__ = "CIFG" + cls.__name__
    Swapped.arch = "CIFG"
    return Swapped


_TARGETS = (("selfmon", "MonRunner"), ("gradmon", "GradRunner"), ("steerint", "SteerRunner"),
            ("transfer", "TransferRunner"), ("necessity", "LesionRunner"), ("access", "SteerRunner"),
            ("access", "TransferRunner"))
_ORIGINAL: dict = {}


def install() -> None:
    """Make every runner built from now on in this process a CIFG runner (idempotent)."""
    import importlib
    mods = {m: importlib.import_module(f"{__package__}.{m}") for m, _ in _TARGETS}    # import all, then patch
    for m, name in _TARGETS:
        cls = getattr(mods[m], name)
        if getattr(cls, "arch", None) == "CIFG":
            continue
        _ORIGINAL[(m, name)] = cls
        setattr(mods[m], name, _swapping(cls))


def uninstall() -> None:
    """Restore the original runner classes (tests)."""
    import importlib
    for (m, name), cls in list(_ORIGINAL.items()):
        setattr(importlib.import_module(f"{__package__}.{m}"), name, cls)
        del _ORIGINAL[(m, name)]
