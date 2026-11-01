"""Untrained NumPy reference model of the RWM architecture (DESIGN ONLY).

Each discrete RWM-8 node is a neural population; population j receives a
weight block from population i iff (i -> j) is an effective edge of the
discrete topology (`population_edges()` equals `rwm8().effective_edges()`).
Every environment step runs `n_settle` recurrent settling iterations with the
observation clamped: state is estimated by recurrent feedback, not a single
feedforward pass.

This module defines forward dynamics and the objective terms only. It contains
no optimizer, no gradient code and no training loop: training is blocked until
a separately approved protocol exists (RWM_DESIGN_v1.md, section 10).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import numpy as np

from .primitives import Network, TABLE
from .topology import EXTERNAL, RWM_MODULES, rwm8, _net
from . import world as W


@dataclass
class RWMConfig:
    d_x: int = 16       # exteroceptive population
    d_i: int = 8        # interoceptive population
    d_w: int = 4        # workspace content: the central bottleneck (d_w << d_x)
    d_c: int = 8        # monitor population
    n_settle: int = 3   # recurrent settling iterations per environment step
    alpha: float = 0.5  # leak
    ignition_gain: float = 8.0
    ignition_self: float = 1.5   # > 1 / (gain/4) gives bistable (hysteretic) ignition
    correct_tol: float = 0.5     # first-order prediction counted correct if |eps| < tol
    setpoint: float = 0.0        # SUPPLIED interoceptive setpoint (alarm expected off)
    pi_int: float = 8.0          # SUPPLIED interoceptive precision
    seed: int = 0


def _sig(z):
    return 1.0 / (1.0 + np.exp(-z))


def _softplus(z):
    return np.log1p(np.exp(-np.abs(z))) + np.maximum(z, 0.0)


class RWMNet:
    def __init__(self, cfg: Optional[RWMConfig] = None):
        self.cfg = cfg or RWMConfig()
        c = self.cfg
        rng = np.random.default_rng(c.seed)
        self.dims = {"X": c.d_x, "E": 1, "A": 2, "I": c.d_i, "G": 1, "K": c.d_w, "C": c.d_c, "M": 1}
        self.edges = sorted(rwm8().effective_edges())
        self.W: Dict[Tuple[str, str], np.ndarray] = {}
        for src, dst in self.edges:
            if dst in ("E", "M"):
                continue  # E and M are fixed comparators (difference operators), not learned maps
            scale = 1.0 / np.sqrt(self.dims[src])
            self.W[(src, dst)] = rng.normal(0.0, scale, (self.dims[dst], self.dims[src]))
        if ("G", "G") in self.W:
            self.W[("G", "G")][:] = c.ignition_self
        self.U = {"X": rng.normal(0, 1, (c.d_x, 1)), "I": rng.normal(0, 1, (c.d_i, 1))}
        self.b = {k: np.zeros(d) for k, d in self.dims.items()}
        self.readout_x = rng.normal(0, 1 / np.sqrt(c.d_x), (1, c.d_x))   # X -> predicted oR
        self.conf_head = rng.normal(0, 1 / np.sqrt(c.d_c), (1, c.d_c))   # C -> predicted correctness
        self.prec_head = rng.normal(0, 1 / np.sqrt(c.d_c), (1, c.d_c))   # C -> sensory precision
        self.reset()

    # ------------------------------------------------------------------
    def population_edges(self) -> List[Tuple[str, str]]:
        fixed = [("X", "E"), ("C", "M"), ("E", "M")]
        return sorted(set(self.W) | set(fixed))

    def reset(self) -> None:
        self.h = {k: np.zeros(d) for k, d in self.dims.items()}
        self.h["A"][:] = 0.5

    def _in(self, dst: str) -> np.ndarray:
        tot = self.b[dst].copy()
        for (src, d), w in self.W.items():
            if d == dst:
                tot = tot + w @ self.h[src]
        return tot

    def confidence(self) -> float:
        return float(_sig(self.conf_head @ self.h["C"])[0])

    def precision(self) -> float:
        return float(_softplus(self.prec_head @ self.h["C"])[0]) + 1e-3

    def prediction(self) -> float:
        return float((self.readout_x @ self.h["X"])[0])

    def step(self, oR: float, oH: float) -> Dict[str, float]:
        c = self.cfg
        a = c.alpha
        pred_before = self.prediction()
        conf_before = self.confidence()
        for _ in range(c.n_settle):
            h = self.h
            pi = self.precision()
            new = {}
            new["X"] = (1 - a) * h["X"] + a * np.tanh(self._in("X") + (self.U["X"] @ [pi * oR]))
            new["E"] = np.array([oR - self.prediction()])
            logits = self._in("A")
            ex = np.exp(logits - logits.max())
            new["A"] = ex / ex.sum()
            new["I"] = (1 - a) * h["I"] + a * np.tanh(self._in("I") + (self.U["I"] @ [oH - c.setpoint]))
            new["G"] = _sig(c.ignition_gain * (self._in("G") - 0.5))
            write = np.tanh(self._in("K") - (self.W[("K", "K")] @ h["K"] if ("K", "K") in self.W else 0))
            new["K"] = new["G"] * write + (1 - new["G"]) * h["K"]
            new["C"] = (1 - a) * h["C"] + a * np.tanh(self._in("C"))
            correct = float(abs(h["E"][0]) < c.correct_tol)
            new["M"] = np.array([correct - self.confidence()])
            self.h = new
        eps = oR - pred_before
        pi = self.precision()
        return {
            "eps_ext": eps,
            "precision": pi,
            "F_ext": 0.5 * pi * eps ** 2 - 0.5 * np.log(pi),
            "F_int": 0.5 * c.pi_int * (oH - c.setpoint) ** 2,
            "L_meta": (conf_before - float(abs(eps) < c.correct_tol)) ** 2,
            "p_forage": float(self.h["A"][1]),
            "ignition": float(self.h["G"][0]),
        }


def rollout(net: RWMNet, steps: int, rng: np.random.Generator) -> Dict[str, object]:
    """Run the untrained model in the simulated forage world (no learning)."""
    net.reset()
    L, H = 0, W.H_MAX
    rows = []
    deaths = 0
    for _ in range(steps):
        F = int(rng.random() < float(W.P_FOOD))
        oR, oH = W.observe(L, H, F)
        out = net.step(float(oR), float(oH))
        act = int(rng.random() < out["p_forage"])
        H2 = W.next_energy(L, H, F)
        if H2 <= 0:
            deaths += 1
            L, H = 0, W.H_MAX
            net.reset()
        else:
            L, H = act, H2
        rows.append(out)
    keys = ["F_ext", "F_int", "L_meta", "ignition", "p_forage"]
    return {"steps": steps, "deaths": deaths,
            **{f"mean_{k}": float(np.mean([r[k] for r in rows])) for k in keys}}


def macro_skeleton(net: RWMNet) -> Network:
    """Binary mean-field abstraction of the current parameters, for re-running
    the pre-scale gate at initialization or at any future checkpoint.

    Each population becomes one threshold unit whose weight from population i
    is the sum of the block W[i -> j]; K keeps its gated-hold form and E, M
    keep their comparator (parity) form. The abstraction is a declared
    coarse-graining; Phi of a macro description is not Phi of the micro system.
    """
    srcs = {dst: [s for (s, d) in net.W if d == dst] for dst in net.dims}

    def thr_gate(dst, extra_inputs=(), extra_w=()):
        names = srcs[dst] + list(extra_inputs)
        ws = [float(net.W[(s, dst)].sum()) for s in srcs[dst]] + list(extra_w)
        bias = float(net.b[dst].sum())

        def fn(*bits):
            return int(sum(w * (2 * b - 1) for w, b in zip(ws, bits)) + bias > 0)
        return tuple(names), TABLE(f"MF-THR({dst})", len(names), fn)

    spec = []
    xi, xg = thr_gate("X", ["oR"], [float(net.U["X"].sum())])
    spec.append(("X", xi, xg))
    spec.append(("E", ("X", "oR"), TABLE("XOR", 2, lambda x, o: x ^ o)))
    spec.append(("A",) + thr_gate("A"))
    ii, ig = thr_gate("I", ["oH"], [float(net.U["I"].sum())])
    spec.append(("I", ii, ig))
    spec.append(("G",) + thr_gate("G"))
    k_srcs = [s for s in srcs["K"] if s not in ("G", "K")]
    kw = [float(net.W[(s, "K")].sum()) for s in k_srcs]
    spec.append(("K", tuple(["G", "K"] + k_srcs),
                 TABLE("MF-HOLD(K)", 2 + len(k_srcs),
                       lambda g, k, *b: int(sum(w * (2 * x - 1) for w, x in zip(kw, b)) > 0) if g else k)))
    spec.append(("C",) + thr_gate("C"))
    spec.append(("M", ("C", "E"), TABLE("XNOR", 2, lambda c, e: 1 - (c ^ e))))
    return _net("RWM-NEURAL-MACRO", spec, RWM_MODULES)
