"""Exact integration and causal-density instruments for small gate networks.

Definitions (stated in full in RWM_DESIGN_v1.md, section 6):

* Phi_s -- system integration in the style of IIT 4.0 (Albantakis et al. 2023):
  intrinsic cause/effect states selected by intrinsic information
  ii = selectivity * informativeness, integration measured against DIRECTED
  bipartitions (connections A -> B replaced by uniform noise), phi_s = min of
  cause and effect integration, minimum-information partition chosen by
  phi / (|A| * |B|). Restricted to directed BIpartitions; ties in the intrinsic
  state are resolved by maximal phi. This is NOT a PyPhi-certified IIT 3.0/4.0
  Phi; it is an explicitly defined quantity with the same structural signature
  (any purely feedforward or severable system has Phi_s = 0).
* Causal density -- an interventional / closed-loop discrete analogue of Seth's
  Granger causal density: conditional mutual information
  I(X_i(t); X_j(t+1) | X_{-i}(t), inputs(t)) for ordered pairs i != j.

All logs are base 2.
"""
from __future__ import annotations

import math
from itertools import combinations, product
from typing import Dict, List, Mapping, Optional, Sequence, Tuple

import numpy as np

from .primitives import Network, all_input_assignments

TIE_TOL = 1e-12


def _h(p: float) -> float:
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -(p * math.log2(p) + (1 - p) * math.log2(1 - p))


class Subsystem:
    """A candidate system S within a network; everything else is background.

    Outside nodes are clamped to their values in `full_state`; external inputs
    are clamped to `ext`. Past/future states of S are indexed little-endian over
    S's own ordering.
    """

    def __init__(self, net: Network, members: Sequence[str], full_state: int, ext: Mapping[str, int]):
        self.net = net
        self.members = list(members)
        self.m = len(self.members)
        self.pos = {n: k for k, n in enumerate(self.members)}
        bits = net.state_bits(full_state)
        self.fixed: Dict[str, int] = dict(ext)
        for name, b in zip(net.nodes, bits):
            if name not in self.pos:
                self.fixed[name] = b
        self.current = sum(bits[net.index(n)] << k for k, n in enumerate(self.members))
        self._cache: Dict[Tuple, float] = {}
        self.effective = set(net.effective_edges())
        self._T: Optional[np.ndarray] = None

    # node probability with a set of cut sources replaced by uniform noise
    def p1(self, j: str, past: int, cut_sources: frozenset) -> float:
        ins = self.net.inputs[j]
        key = (j, cut_sources, tuple(
            None if (src in cut_sources) else
            ((past >> self.pos[src]) & 1 if src in self.pos else self.fixed[src])
            for src in ins))
        hit = self._cache.get(key)
        if hit is not None:
            return hit
        gate = self.net.gates[j]
        free = [k for k, v in enumerate(key[2]) if v is None]
        total = 0.0
        for combo in product((0, 1), repeat=len(free)):
            vals = list(key[2])
            for k, b in zip(free, combo):
                vals[k] = b
            total += gate.p1(vals)
        val = total / (1 << len(free))
        self._cache[key] = val
        return val

    def trans(self, past: int, future: int, cut: Optional[Tuple[frozenset, frozenset]] = None) -> float:
        """P(S(t+1) = future | S(t) = past), optionally under directed cut A -> B."""
        prob = 1.0
        for k, j in enumerate(self.members):
            cs = frozenset()
            if cut is not None and j in cut[1]:
                cs = frozenset(src for src in self.net.inputs[j] if src in cut[0])
            p = self.p1(j, past, cs)
            prob *= p if (future >> k) & 1 else 1.0 - p
            if prob == 0.0:
                return 0.0
        return prob

    @property
    def T(self) -> np.ndarray:
        """Intact transition matrix T[past, future]."""
        if self._T is None:
            m = self.m
            size = 1 << m
            P1 = np.array([[self.p1(j, s, frozenset()) for j in self.members] for s in range(size)])
            bits = np.array([[(f >> k) & 1 for k in range(m)] for f in range(size)])
            T = np.ones((size, size))
            for k in range(m):
                pk = P1[:, k][:, None]
                T *= np.where(bits[:, k][None, :] == 1, pk, 1.0 - pk)
            self._T = T
        return self._T

    def cut_has_edges(self, A: frozenset, B: frozenset) -> bool:
        return any((a, b) in self.effective for a in A for b in B)


def directed_bipartitions(members: Sequence[str]) -> List[Tuple[frozenset, frozenset]]:
    out = []
    m = len(members)
    for mask in range(1, (1 << m) - 1):
        A = frozenset(members[k] for k in range(m) if (mask >> k) & 1)
        B = frozenset(members) - A
        out.append((A, B))
    return out


def _argmax_set(values: np.ndarray, valid: np.ndarray) -> List[int]:
    vals = np.where(valid, values, -np.inf)
    best = vals.max()
    if not np.isfinite(best):
        return []
    return [int(i) for i in np.flatnonzero(vals >= best - TIE_TOL)]


def phi_s(net: Network, full_state: int, ext: Mapping[str, int],
          members: Optional[Sequence[str]] = None, stop_at_zero: bool = True) -> Dict[str, object]:
    """System integration Phi_s of subsystem `members` (default: all nodes).

    A zero-phi directed cut is the minimum of the normalized criterion, so with
    `stop_at_zero` the partition scan stops there (exact, not a heuristic)."""
    members = list(net.nodes if members is None else members)
    if len(members) < 2:
        return {"phi": 0.0, "reason": "fewer than two nodes", "members": members}
    sub = Subsystem(net, members, full_state, ext)
    s = sub.current
    T = sub.T
    q = T.mean(axis=0)  # unconstrained repertoire under uniform past

    # effect side
    pe = T[s, :]
    with np.errstate(divide="ignore", invalid="ignore"):
        ii_e = np.where(pe > 0, pe * np.log2(pe / q), -np.inf)
    eff_cands = _argmax_set(ii_e, pe > 0)

    # cause side (uniform prior over past states)
    col = T[:, s]
    if col.sum() == 0.0:
        return {"phi": 0.0, "reason": "no cause under clamped background (IIT convention)", "members": members}
    pc = col / col.sum()
    with np.errstate(divide="ignore", invalid="ignore"):
        ii_c = np.where(pc > 0, pc * np.log2(col / q[s]), -np.inf)
    cau_cands = _argmax_set(ii_c, pc > 0)

    parts = sorted(directed_bipartitions(members), key=lambda ab: min(len(ab[0]), len(ab[1])))
    for A, B in parts:
        if not sub.cut_has_edges(A, B):
            return {"phi": 0.0, "reason": "severable: no effective edges across directed cut",
                    "mip": [sorted(A), sorted(B)], "members": members,
                    "ii_c": float(ii_c[cau_cands[0]]), "ii_e": float(ii_e[eff_cands[0]])}

    best: Optional[Dict[str, object]] = None
    for sc in cau_cands:
        for se in eff_cands:
            mip = None
            for A, B in parts:
                cut = (A, B)
                pe_cut = sub.trans(s, se, cut)
                phi_e = max(0.0, pe[se] * math.log2(pe[se] / pe_cut))
                pc_cut = sub.trans(sc, s, cut)
                phi_c = max(0.0, pc[sc] * math.log2(col[sc] / pc_cut))
                val = min(phi_c, phi_e)
                if val <= TIE_TOL and stop_at_zero:
                    mip = (0.0, 0.0, phi_c, phi_e, A, B)
                    break
                norm = val / (len(A) * len(B))
                if mip is None or norm < mip[0] - TIE_TOL:
                    mip = (norm, val, phi_c, phi_e, A, B)
            cand = {"phi": float(mip[1]), "phi_c": float(mip[2]), "phi_e": float(mip[3]),
                    "mip": [sorted(mip[4], key=members.index), sorted(mip[5], key=members.index)],
                    "cause_state": sc, "effect_state": se,
                    "ii_c": float(ii_c[sc]), "ii_e": float(ii_e[se])}
            if best is None or cand["phi"] > best["phi"] + TIE_TOL:
                best = cand
    best["members"] = members
    best["reason"] = "integrated" if best["phi"] > 0 else "zero at MIP"
    best["n_cause_ties"] = len(cau_cands)
    best["n_effect_ties"] = len(eff_cands)
    return best


def major_complex(net: Network, full_state: int, ext: Mapping[str, int],
                  min_size: int = 2) -> Dict[str, object]:
    """Exhaustive search for the subset with maximal Phi_s (exclusion step)."""
    best_phi = 0.0
    winners: List[List[str]] = []
    for r in range(min_size, net.n + 1):
        for subset in combinations(net.nodes, r):
            val = phi_s(net, full_state, ext, subset)["phi"]
            if val > best_phi + TIE_TOL:
                best_phi, winners = val, [list(subset)]
            elif val > 0 and abs(val - best_phi) <= TIE_TOL:
                winners.append(list(subset))
    return {"phi": float(best_phi), "complexes": winners}


# ---------------------------------------------------------------------------
# Causal density
# ---------------------------------------------------------------------------

def _cmi_pair(net: Network, i: int, j: int, weight: Dict[Tuple[int, Tuple], float]) -> float:
    """I(X_i; X_j' | X_-i, inputs) under the joint weight over (state, ext-tuple)."""
    ext_names = net.external
    groups: Dict[Tuple[int, Tuple], List[Tuple[float, float]]] = {}
    for (s, e), w in weight.items():
        if w == 0.0:
            continue
        rest = s & ~(1 << i)
        vals = dict(zip(ext_names, e))
        vals.update(zip(net.nodes, net.state_bits(s)))
        groups.setdefault((rest, e), []).append((w, net.node_p1(net.nodes[j], vals)))
    total = 0.0
    for items in groups.values():
        wsum = sum(w for w, _ in items)
        m = sum(w * p for w, p in items) / wsum
        total += wsum * (_h(m) - sum(w * _h(p) for w, p in items) / wsum)
    return total


def uniform_weight(net: Network, ext: Optional[Mapping[str, int]] = None) -> Dict[Tuple[int, Tuple], float]:
    exts = [tuple(ext[n] for n in net.external)] if ext is not None else \
        [tuple(a[n] for n in net.external) for a in all_input_assignments(net.external)]
    w = 1.0 / ((1 << net.n) * len(exts))
    return {(s, e): w for s in range(1 << net.n) for e in exts}


def causal_density(net: Network, weight: Dict[Tuple[int, Tuple], float]) -> Dict[str, object]:
    n = net.n
    pairs = {}
    for i in range(n):
        for j in range(n):
            pairs[(net.nodes[i], net.nodes[j])] = _cmi_pair(net, i, j, weight)
    off = [v for (a, b), v in pairs.items() if a != b]
    active = [v for v in off if v > 1e-12]
    return {
        "cd_binary": len(active) / (n * (n - 1)),
        "cd_weighted": float(sum(off) / (n * (n - 1))),
        "cmi": {f"{a}->{b}": float(v) for (a, b), v in pairs.items()},
    }
