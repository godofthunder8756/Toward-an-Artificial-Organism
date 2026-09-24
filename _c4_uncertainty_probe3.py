"""C4 probe, part 3: robustness — does the graded posterior beat the binary+immediate
rival at ANY occlusion rate q, or is the equivalence uniform (heuristics match everywhere)?
"""
import numpy as np
from _c4_uncertainty_probe import (episode, regret_raw, regret_binary, regret_graded, mc,
                                   P_YIELD, R, H)
from _c4_uncertainty_probe2 import regret_binary_immediate


def main():
    qs = [0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 0.99]
    Ns = [2, 3, 4, 5, 6, 8, 12, 24]
    thetas = [0.55, 0.6, 0.66, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
    n_ep = 6000
    print(f"P_YIELD={P_YIELD} R={R} H={H}  n_ep={n_ep}")
    print(f"{'q':>5} {'raw':>7} {'binary':>7} {'bin+imm':>7} {'graded':>7}   graded-bin+imm")
    for q in qs:
        best = {}
        for name, fn, grid, kw in [('raw', regret_raw, Ns, 'N'),
                                   ('binary', regret_binary, Ns, 'N'),
                                   ('bin+imm', regret_binary_immediate, Ns, 'N'),
                                   ('graded', regret_graded, thetas, 'theta')]:
            b = min(grid, key=lambda g: (mc(fn, 'M', q, n_ep, **{kw: g})
                                         + mc(fn, 'C', q, n_ep, **{kw: g})) / 2)
            best[name] = (mc(fn, 'M', q, n_ep, **{kw: b}) + mc(fn, 'C', q, n_ep, **{kw: b})) / 2
        gap = best['graded'] - best['bin+imm']
        print(f"{q:>5.2f} {best['raw']:7.3f} {best['binary']:7.3f} {best['bin+imm']:7.3f} "
              f"{best['graded']:7.3f}   {gap:+.3f}")


if __name__ == '__main__':
    main()
