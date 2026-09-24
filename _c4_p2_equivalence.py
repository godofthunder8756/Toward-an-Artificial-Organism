"""C4 P2 — resolve the sufficient-statistic rival.

Question (t_dac7256e): under C4's stated stationary two-cause model, is the graded
posterior computationally equivalent to an integer ambiguous-failure counter?

Stated concern: every ambiguous (occluded-unproductive) failure contributes the SAME
log-likelihood increment L_n = L_0 + n*log(4/3), so a fixed posterior threshold is an
integer ambiguous-failure threshold n >= ceil((logit(theta) - L_0) / log(4/3)).

This script:
  1. implements the integer counter `regret_int` with the SAME decisive-observation
     handling as `regret_graded` (open held -> act now; open blind OR productive ->
     hold forever; occluded-unproductive -> increment the counter),
  2. proves the equivalence ANALYTICALLY (finite accumulator = n*log(4/3); the threshold
     sits in a gap between two such values; ceil aligns them exactly),
  3. verifies EXECUTABLY and exactly: exhaustive over the full 6-symbol observation
     alphabet for horizons up to 7, plus random length-96 histories — graded(theta) and
     int(ceil(logit(theta)/LR)) return the identical act-tick on every history,
  4. checks the numerical boundary (no grid theta within float noise of an integer
     multiple of the irrational LR),
  5. attributes the C4 dominance: `binary+imm` omits the occluded-productive-is-decisive-C
     observation; upgrading it (`binary_imm_full`) makes it exactly the integer counter,
     i.e. exactly the graded policy, so the reported dominance is a rival defect, not a
     property of gradedness.

No frozen artifact is edited or re-run; the frozen probe functions are imported.
"""
import math

import numpy as np

from _c4_uncertainty_probe import LR, R, H, P_YIELD

# ---------------------------------------------------------------- scalar rivals
def regret_int(obs, cause, N):
    """Integer mirror of regret_graded, exact on the FULL observation alphabet.

    regret_graded keeps a float log-odds L in { -inf, 0, LR, 2*LR, ..., +inf }:
        blind or productive -> L = -inf   (decisive C)
        held                 -> L = +inf   (decisive M)
        occluded-unproductive-> L += LR
        act when L >= logit(theta).
    regret_int keeps the same three-valued state as an integer (mode in {-1,0,+1})
    plus a counter n.  With N = ceil(logit(theta)/LR) the decision is identical on every
    history, because L = n*LR in the finite branch and logit(theta) never equals an
    integer multiple of the irrational LR.
    """
    mode = 0
    n = 0
    for t, (u, p) in enumerate(obs):
        if u == 'blind' or p == 1:
            mode = -1
        elif u == 'held':
            mode = +1
        else:
            if mode == 0:
                n += 1
        if mode == +1 or (mode == 0 and n >= N):
            return R if cause == 'C' else float(t)
    return 0.0 if cause == 'C' else float(H)


def regret_binary_immediate_full(obs, cause, N):
    """binary+imm with the occluded-productive observation recognized as decisive C."""
    e, n = 'M', 0
    for t, (u, p) in enumerate(obs):
        if u == 'blind':
            e = 'C'
        elif u == 'held':
            return R if cause == 'C' else float(t)
        if p == 1:
            e = 'C'          # occluded-productive is decisive C (M never yields)
        elif e == 'M':
            n += 1
        if e == 'M' and n >= N:
            return R if cause == 'C' else float(t)
    return 0.0 if cause == 'C' else float(H)


def theta_to_N(theta):
    return int(math.ceil(math.log(theta / (1.0 - theta)) / LR))


# ---------------------------------------------------------------- vectorized
def decision_int(used, prod, N):
    n_ep, Hh = used.shape
    mode = np.zeros(n_ep, dtype=np.int8)
    n = np.zeros(n_ep, dtype=np.int32)
    act_t = np.full(n_ep, -1, dtype=np.int32)
    for t in range(Hh):
        u = used[:, t]
        p = prod[:, t]
        decC = (u == 1) | p
        decM = (u == 0)
        mode = np.where(decC, -1, np.where(decM, 1, mode))
        fin = mode == 0
        n = np.where(fin & ~decC & ~decM, n + 1, n)
        act = (mode == 1) | (fin & (n >= N))
        new = (act_t < 0) & act
        act_t[new] = t
    return act_t


def decision_graded(used, prod, theta):
    logit = np.log(theta / (1.0 - theta))
    n_ep, Hh = used.shape
    mode = np.zeros(n_ep, dtype=np.int8)
    L = np.zeros(n_ep)
    act_t = np.full(n_ep, -1, dtype=np.int32)
    for t in range(Hh):
        u = used[:, t]
        p = prod[:, t]
        decC = (u == 1) | p
        decM = (u == 0)
        mode = np.where(decC, -1, np.where(decM, 1, mode))
        fin = mode == 0
        L = np.where(fin & ~decC & ~decM, L + LR, L)
        act = (mode == 1) | (fin & (L >= logit))
        new = (act_t < 0) & act
        act_t[new] = t
    return act_t


def decision_binary_imm(used, prod, N):
    n_ep, Hh = used.shape
    e = np.ones(n_ep, dtype=bool)
    n = np.zeros(n_ep, dtype=np.int32)
    act_t = np.full(n_ep, -1, dtype=np.int32)
    for t in range(Hh):
        u = used[:, t]
        p = prod[:, t]
        is_blind = u == 1
        is_held = u == 0
        e = np.where(is_blind, False, np.where(is_held, True, e))
        act_held = is_held
        n = np.where(p, 0, n)                       # productive -> RESET streak
        n = np.where((~p) & e, n + 1, n)
        act = act_held | (e & (n >= N))
        new = (act_t < 0) & act
        act_t[new] = t
    return act_t


def decision_binary_imm_full(used, prod, N):
    n_ep, Hh = used.shape
    e = np.ones(n_ep, dtype=bool)
    n = np.zeros(n_ep, dtype=np.int32)
    act_t = np.full(n_ep, -1, dtype=np.int32)
    for t in range(Hh):
        u = used[:, t]
        p = prod[:, t]
        is_blind = u == 1
        is_held = u == 0
        e = np.where(is_blind, False, np.where(is_held, True, e))
        act_held = is_held
        e = np.where(p, False, e)                   # productive -> decisive C
        n = np.where((~p) & e, n + 1, n)
        act = act_held | (e & (n >= N))
        new = (act_t < 0) & act
        act_t[new] = t
    return act_t


def regrets(act_t, cause):
    acted = act_t >= 0
    if cause == 'M':
        return float(np.where(acted, act_t.astype(float), float(H)).mean())
    return float(np.where(acted, R, 0.0).mean())


def gen_episodes(cause, q, n_ep, seed):
    rng = np.random.default_rng(seed)
    if cause == 'M':
        uset = np.zeros((n_ep, H), dtype=np.int8)
        prod = np.zeros((n_ep, H), dtype=bool)
    else:
        uset = np.ones((n_ep, H), dtype=np.int8)
        prod = rng.random((n_ep, H)) < P_YIELD
    occ = rng.random((n_ep, H)) < q
    used = np.where(occ, 2, uset).astype(np.int8)
    return used, prod


# ---------------------------------------------------------------- checks
THETAS = [0.5, 0.52, 0.55, 0.58, 0.6, 0.62, 0.66, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]


def analytic_mapping():
    print("== analytic threshold mapping: graded(theta) <-> int(N) ==")
    print(f"LR = log(4/3) = {LR!r}")
    print(f"{'theta':>6} {'logit(theta)':>13} {'logit/LR':>11} {'N=ceil':>6} {'gap(frac)':>10}")
    for th in THETAS:
        logit = math.log(th / (1.0 - th))
        ratio = logit / LR
        N = theta_to_N(th)
        frac = ratio - math.floor(ratio)
        print(f"{th:>6.2f} {logit:>13.6f} {ratio:>11.6f} {N:>6d} {frac:>10.6f}")


def boundary_check():
    print("\n== numerical boundary check ==")
    min_gap, worst = 1.0, None
    for th in THETAS:
        logit = math.log(th / (1.0 - th))
        ratio = logit / LR
        frac = ratio - math.floor(ratio)
        gap = min(frac, 1.0 - frac)
        if gap < min_gap:
            min_gap, worst = gap, th
    accum = 0.0
    for _ in range(96):
        accum += LR
    accum_err = abs(accum - 96 * LR)
    print(f"  min distance from logit(theta)/LR to an integer: {min_gap:.3e} (theta={worst})")
    print(f"  float accumulation error in n*LR after 96 adds:    {accum_err:.3e}")
    print(f"  margin {min_gap / accum_err:.1f}x -> no theta sits within float noise of a "
          f"boundary")
    print(f"  (theta=0.5 has logit=0 exactly == 0*LR: an exact boundary, but aligned -- the "
          f"exhaustive test below confirms graded(0.5) == int(0) on every history)")


def exhaustive_equivalence():
    print("\n== exhaustive equivalence over the FULL 6-symbol alphabet, H up to 7 ==")
    syms = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)]  # (used, productive)
    for Hh in [1, 2, 3, 4, 5, 6, 7]:
        n_hist = len(syms) ** Hh
        used = np.empty((n_hist, Hh), dtype=np.int8)
        prod = np.empty((n_hist, Hh), dtype=bool)
        idx = np.arange(n_hist)
        used_arr = np.array([s[0] for s in syms], dtype=np.int8)
        prod_arr = np.array([s[1] for s in syms], dtype=bool)
        for t in range(Hh):
            code = (idx // (len(syms) ** t)) % len(syms)
            used[:, t] = used_arr[code]
            prod[:, t] = prod_arr[code]
        mism = 0
        for th in THETAS:
            N = theta_to_N(th)
            g = decision_graded(used, prod, th)
            i = decision_int(used, prod, N)
            mism += int((g != i).sum())
        print(f"  H={Hh}: {n_hist} histories x {len(THETAS)} thetas -> "
              f"{'OK' if mism == 0 else f'{mism} MISMATCHES'}")


def random_fullalphabet_equivalence():
    print("\n== random length-96 histories, FULL alphabet (n=200000) ==")
    rng = np.random.default_rng(12345)
    used = rng.integers(0, 3, size=(200000, H)).astype(np.int8)
    prod = rng.integers(0, 2, size=(200000, H)).astype(bool)
    mism = 0
    for th in THETAS:
        N = theta_to_N(th)
        g = decision_graded(used, prod, th)
        i = decision_int(used, prod, N)
        d = int((g != i).sum())
        if d:
            print(f"  theta={th} N={N}: {d} mismatches")
        mism += d
    print(f"  graded == int on all sampled full-alphabet histories: "
          f"{'OK' if mism == 0 else 'MISMATCH'}")

    # binary_imm_full == int == graded on ADMISSIBLE histories (both causes).
    # The only full-alphabet divergence is the impossible (held, productive) corner:
    # the frozen binary's `elif held: return` fires before the productive check, while
    # graded/int treat any productive contact (including a held+productive, which the
    # model cannot produce) as decisive C.  Under the stated model held => p=0 always.
    for cause in ('M', 'C'):
        ua, pa = gen_episodes(cause, 0.7, 200000, seed=[7, 700, 5, 9])
        for N in [1, 2, 3, 4, 5, 7, 8, 11]:
            b = decision_binary_imm_full(ua, pa, N)
            i = decision_int(ua, pa, N)
            assert (b == i).all(), (cause, N)
    print("  binary_imm_full == int on all sampled ADMISSIBLE histories (M and C): OK")
    print("  (full-alphabet corner noted: held+productive is impossible under the model)")


def counterexample_binary_imm():
    print("\n== the one-observation defect in binary+imm (as-is) ==")
    # Under cause C, an occluded-productive contact conclusively identifies C (M never
    # yields). graded sets L = -inf (hold forever); binary+imm (as-is) only RESETS the
    # streak, so it can later wrongly relinquish.
    obs = [('occluded', 0), ('occluded', 1), ('occluded', 0), ('occluded', 0),
           ('occluded', 0), ('occluded', 0)]
    from _c4_uncertainty_probe import regret_graded, regret_binary_immediate
    for th, N in [(0.75, 4), (0.9, 8)]:
        g = regret_graded(obs, 'C', th)
        b = regret_binary_immediate(obs, 'C', N)
        print(f"  cause=C, obs={obs}  ->  graded(theta={th})={g}   "
              f"binary+imm(N={N})={b}")


def mc_attribution():
    print("\n== min-mean regret: graded vs int vs binary+imm (as-is vs full) ==")
    print("  (same episode stream per (cause,q); n_ep=200000, vectorized)")
    Ns = list(range(1, 25))
    for q in [0.5, 0.7, 0.9]:
        um, pm = gen_episodes('M', q, 200000, seed=[7, int(q * 1000), 5, 9])
        uc, pc = gen_episodes('C', q, 200000, seed=[7, int(q * 1000), 5, 9])

        def best(fn, grid, kw):
            scored = []
            for g in grid:
                am = fn(um, pm, **{kw: g})
                ac = fn(uc, pc, **{kw: g})
                scored.append((0.5 * (regrets(am, 'M') + regrets(ac, 'C')), g))
            return min(scored)

        b_imm, g_imm = best(decision_binary_imm, Ns, 'N')
        b_full, g_full = best(decision_binary_imm_full, Ns, 'N')
        b_int, g_int = best(decision_int, Ns, 'N')
        b_gr, g_gr = best(decision_graded, THETAS, 'theta')
        print(f"  q={q}: binary+imm(as-is) {b_imm:.3f}@N={g_imm} | "
              f"binary+imm(full) {b_full:.3f}@N={g_full} | "
              f"int {b_int:.3f}@N={g_int} | graded {b_gr:.3f}@theta={g_gr}")
        # graded(theta*) and int(N*) and binary_imm_full(N*) must coincide exactly:
        assert abs(b_full - b_int) < 1e-12, (q, b_full, b_int)
        assert abs(b_int - b_gr) < 1e-12, (q, b_int, b_gr)
    print("  graded == int == binary+imm(full) at their optima (to 1e-12): OK")


def main():
    analytic_mapping()
    boundary_check()
    exhaustive_equivalence()
    random_fullalphabet_equivalence()
    counterexample_binary_imm()
    mc_attribution()


if __name__ == '__main__':
    main()
