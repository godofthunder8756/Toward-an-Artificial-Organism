"""C4 probe, part 5: Pareto-frontier comparison at high occlusion.

The decisive test of "does the graded posterior improve decisions beyond the strongest
heuristic, or does it just re-label the same tradeoff curve?"  For binary+imm (streak
threshold N) and graded (posterior threshold theta), sweep the full parameter range and
plot (regret_M, regret_C) pairs. If the graded posterior's frontier sits strictly below
the heuristic's at high q, the weighting is genuinely load-bearing; if the two frontiers
coincide, the graded posterior is a re-labelled streak (non-discriminating).
"""
import numpy as np
from _c4_uncertainty_probe import episode, mc, regret_binary_immediate, regret_graded, R, H


def frontier(fn, q, grid, kw, n_ep):
    pts = []
    for g in grid:
        pts.append((mc(fn, 'M', q, n_ep, **{kw: g}), mc(fn, 'C', q, n_ep, **{kw: g}), g))
    return pts


def pareto(pts):
    """Return the subset of pts not dominated (lower is better on both axes)."""
    out = []
    for m, c, g in pts:
        if not any(m2 <= m - 1e-9 and c2 <= c - 1e-9 and (m2, c2) != (m, c)
                   for m2, c2, _ in pts):
            out.append((m, c, g))
    return sorted(out)


def main():
    n_ep = 20000
    Ns = list(range(1, 25))
    thetas = [0.5, 0.52, 0.55, 0.58, 0.6, 0.62, 0.66, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
    for q in [0.5, 0.7, 0.9]:
        print(f"\nq={q}: (regret_M, regret_C, param) on the Pareto frontier")
        for name, fn, grid, kw in [('binary+imm', regret_binary_immediate, Ns, 'N'),
                                   ('graded', regret_graded, thetas, 'theta')]:
            pts = frontier(fn, q, grid, kw, n_ep)
            print(f"  {name}:")
            for m, c, g in pareto(pts):
                print(f"    ({m:.3f}, {c:.3f}, {kw}={g})")
            # the min-mean point
            best = min(pts, key=lambda p: p[0] + p[1])
            print(f"    -> min-mean: ({best[0]:.3f}, {best[1]:.3f}, {kw}={best[2]}), "
                  f"mean={(best[0]+best[1])/2:.3f}")


if __name__ == '__main__':
    main()
