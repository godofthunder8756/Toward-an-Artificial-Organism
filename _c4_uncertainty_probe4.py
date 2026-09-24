"""C4 probe, part 4: per-cause breakdown at high occlusion — WHERE the graded posterior's
advantage comes from (faster under M via correct weak-evidence weighting, without more
wrong-relinquish under C? or a different mechanism?).
"""
import numpy as np
from _c4_uncertainty_probe import episode, mc, P_YIELD, R, H
from _c4_uncertainty_probe2 import regret_binary_immediate, regret_graded


def main():
    qs = [0.5, 0.7, 0.9]
    Ns = [2, 3, 4, 5, 6, 8, 12, 24]
    thetas = [0.55, 0.6, 0.66, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
    n_ep = 8000
    print(f"P_YIELD={P_YIELD} R={R} H={H} n_ep={n_ep}")
    for q in qs:
        print(f"\nq={q}:")
        # best N for binary+immediate, best theta for graded (minimize mean regret)
        bN = min(Ns, key=lambda g: (mc(regret_binary_immediate, 'M', q, n_ep, N=g)
                                    + mc(regret_binary_immediate, 'C', q, n_ep, N=g)) / 2)
        bT = min(thetas, key=lambda g: (mc(regret_graded, 'M', q, n_ep, theta=g)
                                        + mc(regret_graded, 'C', q, n_ep, theta=g)) / 2)
        for name, fn, kw, val in [('bin+imm', regret_binary_immediate, 'N', bN),
                                  ('graded', regret_graded, 'theta', bT)]:
            m = mc(fn, 'M', q, n_ep, **{kw: val})
            c = mc(fn, 'C', q, n_ep, **{kw: val})
            print(f"  {name:8s} (best {kw}={val}):  regret_M={m:.3f}  regret_C={c:.3f}  mean={(m+c)/2:.3f}")
        # the WRONG-RELINQUISH rate under C is the key error: compare at the same M-speed
        print(f"  (a wrong relinquish under C costs R={R:.0f}; regret_C/R = wrong-relinquish rate)")


if __name__ == '__main__':
    main()
