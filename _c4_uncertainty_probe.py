"""C4 diagnostic: does a first-order uncertainty estimate (a graded posterior over the cause)
support better decisions than ordinary uncertainty heuristics in the occluded-gate world?

Design-level diagnostic, mirroring _c2_identifiability.py: no organism-scale run, no frozen
study. It simulates the OBSERVATION PROCESS under the C2 occluded-used_held gate and measures
DECISION UTILITY (expected regret) plus CALIBRATION of four same-information policies:

  raw        : relinquish after N consecutive unproductive contacts (r2/r4, state-blind).
  binary     : AC107 cause bit e; open blind -> C(hold), open held-fail -> M; under M
               relinquish after N unproductive (the frozen streak); under C hold forever.
  binary+imm : binary estimate PLUS immediate-relinquish-on-open-held-fail (the strongest
               ordinary heuristic -- closes the binary estimate's decisive-action gap).
  graded     : Bayesian posterior P(move|history); relinquish when P>=theta. This is the
               first-order uncertainty estimate under test.

The question C4 asks is whether `graded` predicts errors / improves decisions beyond
`raw`/`binary`/`binary+imm`. The answer that falls out: `graded` is well-calibrated everywhere
(predicts errors), and it improves decisions over the strongest heuristic ONLY in the
high-occlusion regime (q >= ~0.7), where open (decisive) observations are rare and the
correct likelihood-ratio weighting of the weak occluded-unproductive observation (LR = 4/3)
becomes decision-relevant. At low q the heuristic matches it (open observations dominate).

Observation process (hold-and-observe probe, C2 section 4):
  cause M (move): held entry stale; every contact unproductive; used='held'.
  cause C (cut) : blind fallback productive w.p. P_YIELD=1/4; used='blind'.
  The gate occludes used_held on a Bernoulli(q) fraction -> 'occluded'.
Likelihoods: open held (only M) -> decisive M; open blind (only C) -> decisive C;
occluded productive (only C) -> decisive C; occluded unproductive -> LR = q*1 / (q*3/4) = 4/3.

Regret model (per contact, faithful to the AC107 economics):
  hold under M: +1 per contact held (sustained lost income).
  relinquish under M: 0 (correct; loss ends).  hold under C: 0 (correct).
  relinquish under C: +R (drop a valid entry; one-time re-bind cost).
Horizon H = the cut window; never acting under M costs H.
"""
import numpy as np

PORTS = 4
P_YIELD = 1.0 / PORTS
R = 4.0
H = 96
LR = np.log(4.0 / 3.0)          # occluded-unproductive log-likelihood-ratio toward M


def episode(cause, q, rng):
    obs = []
    for _ in range(H):
        if cause == 'M':
            used_true, productive = 'held', 0
        else:
            used_true, productive = ('blind', 1) if rng.random() < P_YIELD else ('blind', 0)
        used_obs = 'occluded' if rng.random() < q else used_true
        obs.append((used_obs, productive))
    return obs


def regret_raw(obs, cause, N):
    n = 0
    for t, (u, p) in enumerate(obs):
        n = 0 if p == 1 else n + 1
        if n >= N:
            return R if cause == 'C' else float(t)
    return 0.0 if cause == 'C' else float(H)


def regret_binary(obs, cause, N):
    e, n = 'M', 0
    for t, (u, p) in enumerate(obs):
        if u == 'blind':
            e = 'C'
        elif u == 'held':
            e = 'M'
        if p == 1:
            n = 0
        elif e == 'M':
            n += 1
        if e == 'M' and n >= N:
            return R if cause == 'C' else float(t)
    return 0.0 if cause == 'C' else float(H)


def regret_binary_immediate(obs, cause, N):
    e, n = 'M', 0
    for t, (u, p) in enumerate(obs):
        if u == 'blind':
            e = 'C'
        elif u == 'held':
            return R if cause == 'C' else float(t)     # decisive M -> act now
        if p == 1:
            n = 0
        elif e == 'M':
            n += 1
        if e == 'M' and n >= N:
            return R if cause == 'C' else float(t)
    return 0.0 if cause == 'C' else float(H)


def regret_graded(obs, cause, theta):
    L = 0.0
    logit = np.log(theta / (1.0 - theta))
    for t, (u, p) in enumerate(obs):
        if u == 'blind' or p == 1:
            L = -np.inf
        elif u == 'held':
            L = np.inf
        else:
            L += LR
        if L >= logit:
            return R if cause == 'C' else float(t)
    return 0.0 if cause == 'C' else float(H)


_POLICY_SEED = {
    # Deterministic per-policy RNG key, replacing the previous `hash(policy) % 1000`.
    # `hash()` of a function object is id-based (memory address) and varies across
    # processes, so the old seed made the Monte Carlo regret estimates non-reproducible
    # bit-for-bit.  These fixed integers keep the model identical while making every
    # `mc()` draw deterministic across runs.  (P1 reproducibility fix, 2026-09-24.)
    'regret_raw': 1,
    'regret_binary': 2,
    'regret_binary_immediate': 3,
    'regret_graded': 4,
}


def mc(policy, cause, q, n_ep, **kw):
    rng = np.random.default_rng([0, _POLICY_SEED[policy.__name__], int(q * 1000), 7])
    return sum(policy(episode(cause, q, rng), cause, **kw) for _ in range(n_ep)) / n_ep


POLICIES = [
    ('raw', regret_raw, list(range(1, 25)), 'N'),
    ('binary', regret_binary, [2, 3, 4, 5, 6, 8, 12, 24], 'N'),
    ('binary+imm', regret_binary_immediate, [2, 3, 4, 5, 6, 8, 12, 24], 'N'),
    ('graded', regret_graded, [0.55, 0.6, 0.66, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95], 'theta'),
]


def best_regret(fn, q, grid, kw, n_ep):
    return min(grid, key=lambda g: (mc(fn, 'M', q, n_ep, **{kw: g})
                                    + mc(fn, 'C', q, n_ep, **{kw: g})) / 2)


def calibration_table(cause, q, theta, n_ep=60000):
    rng = np.random.default_rng([99, int(q * 1000), 3])
    logit = np.log(theta / (1.0 - theta))
    confs, corrects = [], []
    for _ in range(n_ep):
        L = 0.0
        for t, (u, p) in enumerate(episode(cause, q, rng)):
            if u == 'blind' or p == 1:
                L = -np.inf
            elif u == 'held':
                L = np.inf
            else:
                L += LR
            if L >= logit:
                confs.append(1.0 if np.isinf(L) else np.exp(L) / (1.0 + np.exp(L)))
                corrects.append(1 if cause == 'M' else 0)
                break
    return np.array(confs), np.array(corrects)


def main():
    n_ep = 6000
    print(f"P_YIELD={P_YIELD}  R={R}  H={H}  n_ep={n_ep}")
    print("\n== A. mean regret, each policy at its own best parameter (minimized over M+C) ==")
    print(f"{'q':>5} " + " ".join(f"{name:>11}" for name, _, _, _ in POLICIES) + "   graded - binary+imm")
    for q in [0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 0.99]:
        row = {}
        for name, fn, grid, kw in POLICIES:
            b = best_regret(fn, q, grid, kw, n_ep)
            row[name] = (mc(fn, 'M', q, n_ep, **{kw: b}) + mc(fn, 'C', q, n_ep, **{kw: b})) / 2
        gap = row['graded'] - row['binary+imm']
        print(f"{q:>5.2f} " + " ".join(f"{row[name]:>11.3f}" for name, _, _, _ in POLICIES)
              + f"   {gap:+.3f}")

    print("\n== B. per-cause regret (best parameter per policy) ==")
    for q in [0.5, 0.7, 0.9]:
        print(f"  q={q}:")
        for name, fn, grid, kw in POLICIES:
            b = best_regret(fn, q, grid, kw, n_ep)
            m = mc(fn, 'M', q, n_ep, **{kw: b})
            c = mc(fn, 'C', q, n_ep, **{kw: b})
            print(f"    {name:10s} (best {kw}={b}):  regret_M={m:.3f}  regret_C={c:.3f}  mean={(m+c)/2:.3f}")

    print("\n== C. calibration of the graded posterior (theta=0.75, q=0.5) ==")
    confs_m, corr_m = calibration_table('M', 0.5, 0.75)
    confs_c, corr_c = calibration_table('C', 0.5, 0.75)
    print(f"  cause M: acted {len(confs_m)} eps, mean confidence at action = {confs_m.mean():.3f}")
    print(f"  cause C: acted {len(confs_c)} eps, mean confidence at action = {confs_c.mean():.3f}")
    confs = np.concatenate([confs_m, confs_c])
    correct = np.concatenate([corr_m, corr_c])
    print("  binned calibration (reported confidence vs P(correct action)):")
    for lo, hi in [(0.5, 0.7), (0.7, 0.8), (0.8, 0.9), (0.9, 1.0)]:
        sel = (confs > lo) & (confs <= hi + 1e-9)
        if sel.sum():
            print(f"    conf in ({lo},{hi}]: n={sel.sum():5d}  P(correct)={correct[sel].mean():.3f}")


if __name__ == '__main__':
    main()
