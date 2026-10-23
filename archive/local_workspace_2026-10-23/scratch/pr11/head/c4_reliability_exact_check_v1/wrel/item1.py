"""ITEM-1 A-SYM. Exhaustive no-RECHECK histories and the emission / decision audits."""

from __future__ import annotations

from fractions import Fraction

from .util import R
from .world import F, N_Y, World


def _cells(world: World):
    """144 branch emissions as (num, den) per regime. P then M."""
    branches = []
    for x in (0, 1):
        for y in range(N_Y):
            row = []
            for z in (0, 1):
                w = world.pyx[z][y][x]
                row.append((w.numerator, w.denominator))
            branches.append(row)
    assert len(branches) == 16
    for x in (0, 1):
        for y in range(N_Y):
            for ypp in range(N_Y):
                row = []
                for z in (0, 1):
                    w = F(1, 2) * world.Ldef[z][y][x] * world.Ldef[z][ypp][x]
                    row.append((w.numerator, w.denominator))
                branches.append(row)
    assert len(branches) == 144
    return branches


def _eq(a, b) -> bool:
    return a[0] * b[1] == b[0] * a[1]


def _mul(a, b):
    return (a[0] * b[0], a[1] * b[1])


def audit(world: World, max_len: int = 3, budget=None) -> dict:
    p_cells, m_cells = world.enumerate_nonrecheck_cells()
    p_mismatch = next((c for c in p_cells if c["S"] != c["E"]), None)
    m_mismatch = next((c for c in m_cells if c["S"] != c["E"]), None)
    # (c) classes
    by_class = {i: [] for i in range(10)}
    ratio_bad = None
    for x in (0, 1):
        for y in range(N_Y):
            for yp in range(N_Y):
                cid = world.cls[y][yp][x]
                ls = world.Lre[0][y][yp][x]
                le = world.Lre[1][y][yp][x]
                ratio = ls / le
                by_class[cid].append(ratio)
                if ratio != world.ratio[cid] and ratio_bad is None:
                    ratio_bad = {"y": y, "yp": yp, "X": x, "class": cid}
    class_ok = ratio_bad is None and all(len(v) > 0 and all(r == v[0] for r in v) for v in by_class.values())
    # (d) decisions at b=0, 1/2, 1
    endpoints = (F(0), F(1, 2), F(1))
    d_fail = None
    n_patterns = 0
    for y in range(N_Y):
        n_patterns += 1
        decs = []
        for b in endpoints:
            # default p does not use b when emissions match; still evaluate the mixture formula at b
            p = _p_default_b(world, b, y)
            decs.append(1 if p > F(1, 2) else 0)
        if len(set(decs)) != 1 and d_fail is None:
            d_fail = {"kind": "default", "y": y, "decisions": decs}
    for y in range(N_Y):
        for yp in range(N_Y):
            n_patterns += 1
            decs = [world.d_recheck(b, y, yp) for b in endpoints]
            if len(set(decs)) != 1 and d_fail is None:
                d_fail = {"kind": "recheck", "y": y, "yp": yp, "decisions": decs}
    for y in range(N_Y):
        for ypp in range(N_Y):
            n_patterns += 1
            decs = [world.d_resample(b, y, ypp) for b in endpoints]
            if len(set(decs)) != 1 and d_fail is None:
                d_fail = {"kind": "resample", "y": y, "ypp": ypp, "decisions": decs}
    # (b) histories
    branches = _cells(world)
    hist = _histories(branches, world.h, max_len, budget)
    verified = (
        p_mismatch is None
        and m_mismatch is None
        and class_ok
        and d_fail is None
        and hist["first_counterexample"] is None
    )
    out = {
        "verified": verified,
        "part_a": {
            "n_P_cells": len(p_cells),
            "n_M_cells": len(m_cells),
            "P_equal": p_mismatch is None,
            "M_equal": m_mismatch is None,
            "first_P_mismatch": _cell(p_mismatch),
            "first_M_mismatch": _cell(m_mismatch),
        },
        "part_b": hist,
        "part_c": {
            "n_classes_nonempty": sum(1 for v in by_class.values() if v),
            "ratios_constant": class_ok,
            "ratio_by_class": [R(v[0]) if v else None for v in (by_class[i] for i in range(10))],
            "ratios_all_distinct": len({v[0] for v in by_class.values() if v}) == 10,
            "first_ratio_mismatch": ratio_bad,
            "patterns_checked": 128,
        },
        "part_d": {
            "n_patterns": n_patterns,
            "decisions_coincide": d_fail is None,
            "first_disagreement": d_fail,
            "a11_withdrawn": d_fail is not None,
        },
    }
    if verified:
        out["conclusion"] = (
            "Without recheck observations, the observation history supplies no information "
            "about Z beyond its propagated prior. Recheck observations can be informative. "
            "This does not imply perfect identification of the realized regime within a finite horizon."
        )
        out["outcome"] = "VERIFIED"
    else:
        out["outcome"] = "DISCREPANCY"
        out["conclusion"] = "ITEM-1 found a discrepancy. Diagnosed as an implementation error or an assumption violation; see first_counterexample."
    return out


def _p_default_b(world, b, y) -> Fraction:
    num = F(0)
    den = F(0)
    for z, bz in ((0, b), (1, 1 - b)):
        for x in (0, 1):
            w = bz * world.pyx[z][y][x]
            den += w
            if x == 1:
                num += w
    return num / den


def _cell(c):
    if c is None:
        return None
    return {k: (R(v) if isinstance(v, Fraction) else v) for k, v in c.items()}


def _histories(branches, h: Fraction, max_len: int, budget) -> dict:
    """Equal path likelihoods => posterior equals the path prior.

    Propagated marginal of Z_t is 1/2 for every t when the prior is 1/2, under
    both H0 (h_eff=0) and H1 (the supplied h), which is checked algebraically
    and by the likelihood identity.
    """
    nB = 144
    # Algebraic prior propagation.
    b = F(1, 2)
    prior_ok = True
    for _ in range(max_len):
        b = (1 - h) * b + h * (1 - b)
        if b != F(1, 2):
            prior_ok = False
    b0 = F(1, 2)
    for _ in range(max_len):
        b0 = b0  # H0
        if b0 != F(1, 2):
            prior_ok = False
    first = None
    counts = []
    # length 0
    counts.append(1)
    # Precompute regime index per (path, t) for t < max_len, paths 0..7.
    # Only paths up to the length we need: for length L, 2^L paths, but using 8
    # and ignoring high bits for L<3 is wrong. Handle each length with its own width.
    for L in range(1, max_len + 1):
        if budget:
            budget.check(f"ITEM-1 len={L}")
        n_paths = 1 << L
        n_hist = 0
        # iterative mixed radix
        idx = [0] * L
        while True:
            n_hist += 1
            # products per path
            acc = [(1, 1)] * n_paths
            for t in range(L):
                br = branches[idx[t]]
                new_acc = []
                for path in range(n_paths):
                    z = (path >> t) & 1
                    new_acc.append(_mul(acc[path], br[z]))
                acc = new_acc
            base = acc[0]
            for path in range(1, n_paths):
                if not _eq(base, acc[path]):
                    if first is None:
                        first = {
                            "length": L,
                            "branches": list(idx),
                            "path_a": 0,
                            "path_b": path,
                            "like_a": f"{base[0]}/{base[1]}",
                            "like_b": f"{acc[path][0]}/{acc[path][1]}",
                        }
                    break
            if first is not None:
                break
            # increment
            for t in range(L - 1, -1, -1):
                idx[t] += 1
                if idx[t] < nB:
                    break
                idx[t] = 0
            else:
                break
        counts.append(n_hist)
        if first is not None:
            break
    return {
        "lengths_completed": counts,
        "n_histories_checked": sum(counts),
        "propagated_prior_is_half": prior_ok,
        "path_likelihoods_equal": first is None,
        "posterior_equals_propagated_prior": first is None and prior_ok,
        "first_counterexample": first,
        "laws": ["H0", "H1"],
    }
