"""C4 probe, part 2: (a) calibration of the first-order posterior ("predicts errors"),
(b) a stronger rival — binary estimate PLUS immediate-relinquish-on-open-held-fail — to
confirm the graded posterior's advantage is the likelihood-ratio WEIGHTING, not the
binary estimate merely missing a decisive-action rule.

Same observation process and regret model as _c4_uncertainty_probe.py.
"""
import numpy as np
from _c4_uncertainty_probe import (episode, regret_raw, regret_binary, regret_graded,
                                   mc, P_YIELD, R, H)


def regret_binary_immediate(obs, cause, N):
    """Binary estimate + 'relinquish immediately on an open held-fail' (decisive M).
    Closes the binary estimate's most obvious gap so the comparison is against the
    strongest ordinary heuristic, not a strawman."""
    e = 'M'
    n = 0
    for t, (u, p) in enumerate(obs):
        if u == 'blind':
            e = 'C'
        elif u == 'held':
            return R if cause == 'C' else float(t)   # decisive M -> act now
        if p == 1:
            n = 0
        elif e == 'M':
            n += 1
        if e == 'M' and n >= N:
            return R if cause == 'C' else float(t)
    return 0.0 if cause == 'C' else float(H)


def calibration_table(cause, q, theta, n_ep=60000):
    """At each RELINQUISH decision of the graded policy, record the posterior P(M) at the
    moment of acting and whether the action was correct (cause=='M'). Binned confidence vs
    empirical accuracy is the calibration check: a well-calibrated estimate's reported
    confidence tracks the true error rate."""
    rng = np.random.default_rng([99, int(q * 1000), 3])
    logit = np.log(theta / (1.0 - theta))
    confs = []      # posterior at decision time
    corrects = []   # 1 if relinquish was correct (cause M), 0 if wrong (cause C)
    for _ in range(n_ep):
        L = 0.0
        acted = False
        for t, (u, p) in enumerate(episode(cause, q, rng)):
            if u == 'blind':
                L = -np.inf
            elif u == 'held':
                L = np.inf
            elif p == 1:
                L = -np.inf
            else:
                L += np.log(4.0 / 3.0)
            if L >= logit:
                conf = 1.0 if np.isinf(L) else np.exp(L) / (1.0 + np.exp(L))
                confs.append(conf)
                corrects.append(1 if cause == 'M' else 0)
                acted = True
                break
        if not acted:
            confs.append(np.nan); corrects.append(np.nan)
    confs = np.array(confs, dtype=float)
    corrects = np.array(corrects, dtype=float)
    return confs, corrects


def main():
    q = 0.5
    Ns = [2, 3, 4, 5, 6, 8, 12, 24]
    thetas = [0.55, 0.6, 0.66, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
    n_ep = 6000
    print(f"P_YIELD={P_YIELD} R={R} H={H}")

    # (a) binary+immediate vs graded: the stronger rival
    print("\n-- strongest-rival comparison at q=0.5 (each policy at its best parameter) --")
    out = {}
    for name, fn, grid, kw in [('raw', regret_raw, Ns, 'N'),
                               ('binary', regret_binary, Ns, 'N'),
                               ('binary+imm', regret_binary_immediate, Ns, 'N'),
                               ('graded', regret_graded, thetas, 'theta')]:
        b = min(grid, key=lambda g: (mc(fn, 'M', q, n_ep, **{kw: g})
                                     + mc(fn, 'C', q, n_ep, **{kw: g})) / 2)
        m = mc(fn, 'M', q, n_ep, **{kw: b})
        c = mc(fn, 'C', q, n_ep, **{kw: b})
        out[name] = (b, m, c, (m + c) / 2)
        print(f"  {name:12s} best {kw}={b}:  regret_M={m:.3f}  regret_C={c:.3f}  mean={(m+c)/2:.3f}")
    g = out['graded'][3]
    bi = out['binary+imm'][3]
    print(f"  -> graded beats binary+immediate by {bi-g:+.3f} (mean regret)")

    # (b) calibration: does the posterior's confidence predict correctness?
    print("\n-- calibration of the graded posterior (theta=0.75, q=0.5) --")
    for cause in ('M', 'C'):
        confs, corrects = calibration_table(cause, q, 0.75)
        acted = ~np.isnan(confs)
        print(f"  cause={cause}: acted in {acted.sum()}/{len(confs)} episodes; "
              f"mean confidence at action = {np.nanmean(confs):.3f}")
    # joint calibration: bin confidence over BOTH causes, compare reported p to P(correct)
    confs_m, corr_m = calibration_table('M', q, 0.75)
    confs_c, corr_c = calibration_table('C', q, 0.75)
    confs = np.concatenate([confs_m, confs_c])
    correct = np.concatenate([corr_m, corr_c])          # 1 = action was correct
    valid = ~np.isnan(confs)
    confs, correct = confs[valid], correct[valid]
    print("\n  binned calibration (reported confidence vs P(correct action)):")
    bins = [0.5, 0.7, 0.8, 0.9, 1.0]
    for lo, hi in zip(bins[:-1], bins[1:]):
        sel = (confs > lo) & (confs <= hi + 1e-9)
        if sel.sum() == 0:
            continue
        print(f"    conf in ({lo},{hi}]:  n={sel.sum():5d}  empirical P(correct)={correct[sel].mean():.3f}")


if __name__ == '__main__':
    main()
