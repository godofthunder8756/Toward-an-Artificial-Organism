"""Independent second implementation for ITEM-9.

Does not import H0Solver, the indexed criterion evaluator, or pm.refine.
Observation likelihoods are recomputed from per-bit Bernoulli parameters or
from one-trial enumeration. A disagreement with the primary is an integrity
failure and is returned, not patched.
"""

from __future__ import annotations

from fractions import Fraction

from .world import F, M_ACT, N, N_Y, P_ACT, R_ACT, World, read_class

CLASSES = tuple(
    (nac, naw, N - nac - naw) for nac in range(N + 1) for naw in range(N - nac + 1)
)


def _bits(w: Fraction, e: Fraction):
    p_ac = (1 - w) * (1 - e) ** 2 + w * e ** 2
    p_aw = (1 - w) * e ** 2 + w * (1 - e) ** 2
    p_dir = e * (1 - e)
    return p_ac, p_aw, p_dir


def _L_pattern(y, yp, x, p_ac, p_aw, p_dir) -> Fraction:
    target = 0 if x == 0 else N_Y - 1
    out = F(1)
    for i in range(N):
        yb = (y >> i) & 1
        pb = (yp >> i) & 1
        tb = (target >> i) & 1
        if yb != pb:
            out *= p_dir
        elif yb == tb:
            out *= p_ac
        else:
            out *= p_aw
    return out


def replay_item1(world: World, max_len: int = 2) -> dict:
    """(a), (c), (d) and (b) for lengths <= max_len, from the bit model."""
    # (a) latent default channel
    p_bad = None
    m_bad = None
    for x in (0, 1):
        for y in range(N_Y):
            s = F(1, 2) * world.latent_p_default(0, y, x)
            e = F(1, 2) * world.latent_p_default(1, y, x)
            if s != e and p_bad is None:
                p_bad = {"X": x, "y": y}
    for x in (0, 1):
        for y in range(N_Y):
            for ypp in range(N_Y):
                s = F(1, 2) * world.latent_p_default(0, y, x) * world.latent_p_default(0, ypp, x)
                e = F(1, 2) * world.latent_p_default(1, y, x) * world.latent_p_default(1, ypp, x)
                if s != e and m_bad is None:
                    m_bad = {"X": x, "y": y, "ypp": ypp}
    # (c) ratios from the bit formula, constant on each class by construction of the formula.
    # Check every pattern's ratio equals its class formula.
    params = [_bits(world.w[z], world.e[z]) for z in (0, 1)]
    ratio_of = []
    for nac, naw, nd in CLASSES:
        ls = params[0][0] ** nac * params[0][1] ** naw * params[0][2] ** nd
        le = params[1][0] ** nac * params[1][1] ** naw * params[1][2] ** nd
        ratio_of.append(ls / le)
    bad_c = None
    nonempty = [0] * 10
    for x in (0, 1):
        for y in range(N_Y):
            for yp in range(N_Y):
                ls = _L_pattern(y, yp, x, *params[0])
                le = _L_pattern(y, yp, x, *params[1])
                # class from bits
                target = 0 if x == 0 else N_Y - 1
                nac = naw = nd = 0
                for i in range(N):
                    yb = (y >> i) & 1
                    pb = (yp >> i) & 1
                    tb = (target >> i) & 1
                    if yb != pb:
                        nd += 1
                    elif yb == tb:
                        nac += 1
                    else:
                        naw += 1
                cid = CLASSES.index((nac, naw, nd))
                nonempty[cid] += 1
                if ls / le != ratio_of[cid] and bad_c is None:
                    bad_c = {"y": y, "yp": yp, "X": x}
    # (d) decisions from the same likelihoods
    def p_default(b, y):
        # P(y|X) from latent, mixture
        num = den = F(0)
        for x in (0, 1):
            mix = F(0)
            for z, bz in ((0, b), (1, 1 - b)):
                mix += bz * world.latent_p_default(z, y, x)
            den += mix
            if x == 1:
                num += mix
        return num / den

    def p_re(b, y, yp):
        num = den = F(0)
        for x, bit in ((0, F(0)), (1, F(1))):
            mix = b * _L_pattern(y, yp, x, *params[0]) + (1 - b) * _L_pattern(y, yp, x, *params[1])
            den += mix
            num += bit * mix
        return num / den

    d_bad = None
    for y in range(N_Y):
        decs = [1 if p_default(b, y) > F(1, 2) else 0 for b in (F(0), F(1, 2), F(1))]
        if len(set(decs)) != 1 and d_bad is None:
            d_bad = {"kind": "default", "y": y}
    for y in range(N_Y):
        for yp in range(N_Y):
            decs = [1 if p_re(b, y, yp) > F(1, 2) else 0 for b in (F(0), F(1, 2), F(1))]
            if len(set(decs)) != 1 and d_bad is None:
                d_bad = {"kind": "recheck", "y": y, "yp": yp}
    # resample decisions: independent reads
    def p_rs(b, y, ypp):
        num = den = F(0)
        for x, bit in ((0, F(0)), (1, F(1))):
            mix = F(0)
            for z, bz in ((0, b), (1, 1 - b)):
                mix += bz * world.latent_p_default(z, y, x) * world.latent_p_default(z, ypp, x)
            den += mix
            num += bit * mix
        return num / den

    for y in range(N_Y):
        for ypp in range(N_Y):
            decs = [1 if p_rs(b, y, ypp) > F(1, 2) else 0 for b in (F(0), F(1, 2), F(1))]
            if len(set(decs)) != 1 and d_bad is None:
                d_bad = {"kind": "resample", "y": y, "ypp": ypp}
    # (b) no-recheck histories, lengths 0..max_len. Branch prob from latent P and latent M.
    branches = []
    for x in (0, 1):
        for y in range(N_Y):
            branches.append(tuple(F(1, 2) * world.latent_p_default(z, y, x) for z in (0, 1)))
    for x in (0, 1):
        for y in range(N_Y):
            for ypp in range(N_Y):
                branches.append(
                    tuple(
                        F(1, 2) * world.latent_p_default(z, y, x) * world.latent_p_default(z, ypp, x)
                        for z in (0, 1)
                    )
                )
    assert len(branches) == 144
    first = None
    n_hist = 1  # empty
    for L in range(1, max_len + 1):
        n_paths = 1 << L
        idx = [0] * L
        while True:
            n_hist += 1
            acc = [F(1)] * n_paths
            for t in range(L):
                br = branches[idx[t]]
                acc = [acc[path] * br[(path >> t) & 1] for path in range(n_paths)]
            if any(acc[path] != acc[0] for path in range(1, n_paths)):
                first = {"length": L, "branches": list(idx)}
                break
            for t in range(L - 1, -1, -1):
                idx[t] += 1
                if idx[t] < 144:
                    break
                idx[t] = 0
            else:
                break
        if first is not None:
            break
    return {
        "P_equal": p_bad is None,
        "M_equal": m_bad is None,
        "ratios_constant": bad_c is None and all(n > 0 for n in nonempty),
        "n_classes_nonempty": sum(1 for n in nonempty if n),
        "decisions_coincide": d_bad is None,
        "n_histories_checked": n_hist,
        "path_likelihoods_equal": first is None,
        "first_counterexample": first,
        "ratio_by_class": ratio_of,
    }


def _enum_counts(max_sum: int):
    counts = []
    cur = [0] * 10

    def rec(pos, remaining):
        if pos == 9:
            cur[pos] = remaining
            counts.append(tuple(cur))
            return
        for v in range(remaining + 1):
            cur[pos] = v
            rec(pos + 1, remaining - v)

    for s in range(max_sum + 1):
        rec(0, s)
    return counts


def _choose(qP, qR, qM):
    q, a = qP, P_ACT
    if qR > q:
        q, a = qR, R_ACT
    if qM > q:
        q, a = qM, M_ACT
    return a, q


def replay_h0_values(world: World, T: int, cr: Fraction, cs: Fraction, myopic: bool = False) -> Fraction:
    """Recursive-memo style backward value on count tuples. Scalar V_T(empty) only."""
    if not world.emissions_match:
        raise RuntimeError("replay requires matched emissions")
    counts = _enum_counts(T)
    index = {c: i for i, c in enumerate(counts)}
    sm = [sum(c) for c in counts]
    trans = []
    for i, c in enumerate(counts):
        row = []
        base = list(c)
        for k in range(10):
            if sm[i] >= T:
                row.append(-1)
            else:
                base[k] += 1
                row.append(index[tuple(base)])
                base[k] -= 1
        trans.append(tuple(row))
    b = [world.belief_from_counts(c) for c in counts]
    # class probs
    pc = [[[F(0)] * 10 for _ in range(N_Y)] for _ in (0, 1)]
    for z in (0, 1):
        for y in range(N_Y):
            py = world.py[z][y]
            for c in range(10):
                pc[z][y][c] = world.p_y_class[z][y][c] / py
    inv = all(world.d_recheck(F(0), y, yp) == world.d_recheck(F(1), y, yp) for y in range(N_Y) for yp in range(N_Y))
    if inv:
        kS = [world.expected_correct_R(F(0), F(1), y) for y in range(N_Y)]
        kE = [world.expected_correct_R(F(0), F(0), y) for y in range(N_Y)]

        def ec(i, y):
            bb = b[i]
            return bb * kS[y] + (1 - bb) * kE[y]
    else:
        def ec(i, y):
            return world.expected_correct_R(b[i], b[i], y)

    immP, immM = world.imm_PM()
    py = world.py[0]
    # memo[k][i] computed from small k upward; this is a bottom-up memo, not the indexed solver's arrays of policies.
    memo = {0: [F(0)] * len(counts)}
    for k in range(1, T + 1):
        prev = memo[k - 1]
        cur = [F(0)] * len(counts)
        max_sum = T - k
        for i in range(len(counts)):
            if sm[i] > max_sum:
                continue
            acc = F(0)
            bb = b[i]
            for y in range(N_Y):
                cont = prev[i]
                ev = F(0)
                if k > 1:
                    b1 = 1 - bb
                    tr = trans[i]
                    for c in range(10):
                        p = bb * pc[0][y][c] + b1 * pc[1][y][c]
                        j = tr[c]
                        if p != 0 and j >= 0:
                            ev += p * prev[j]
                if myopic:
                    a, _ = _choose(immP[y], ec(i, y) - cr, immM[y] - cs)
                    if a == P_ACT:
                        q = immP[y] + (cont if k > 1 else F(0))
                    elif a == R_ACT:
                        q = ec(i, y) - cr + (ev if k > 1 else F(0))
                    else:
                        q = immM[y] - cs + (cont if k > 1 else F(0))
                else:
                    a, q = _choose(
                        immP[y] + (cont if k > 1 else F(0)),
                        ec(i, y) - cr + (ev if k > 1 else F(0)),
                        immM[y] - cs + (cont if k > 1 else F(0)),
                    )
                acc += py[y] * q
            cur[i] = acc
        memo[k] = cur
        del memo[k - 1]
    return memo[T][0]


def replay_blind(world: World, cr, cs, T: int) -> Fraction:
    costs = (F(0), cr, cs)

    def choose(r):
        best_a, best_q = 0, None
        for a in range(3):
            q = world.g0[a][r] - costs[a]
            if best_q is None or q > best_q:
                best_q, best_a = q, a
        return best_a

    table = [choose(0), choose(1)]

    def action_of_y(y):
        return table[read_class(y)]

    def dec(a, y, obs):
        if a == P_ACT:
            return world.d_def[y]
        if a == R_ACT:
            return world.d_recheck(F(1, 2), y, obs)
        return world.d_resample(F(1, 2), y, obs)

    vS = world.one_trial_value(0, action_of_y, dec, cr, cs)
    vE = world.one_trial_value(1, action_of_y, dec, cr, cs)
    return (vS + vE) / 2 * T


def replay_oracle(world: World, cr, cs, T: int) -> Fraction:
    total = F(0)
    for z in (0, 1):
        b = F(1) if z == 0 else F(0)
        costs = (F(0), cr, cs)

        def action_of_y(y, b=b, z=z):
            py = world.py[z][y]
            d0 = 1 if _p_point(world, b, y) > F(1, 2) else 0
            qP = world.pyx[z][y][d0] / py
            qR = world.expected_correct_R(b, b, y) - cr
            num = den = F(0)
            for ypp in range(N_Y):
                for x in (0, 1):
                    w = world.pyx[z][y][x] * world.Ldef[z][ypp][x]
                    den += w
                    if world.d_resample(b, y, ypp) == x:
                        num += w
            qM = num / den - cs
            return _choose(qP, qR, qM)[0]

        acts = [action_of_y(y) for y in range(N_Y)]

        def aoy(y, acts=acts):
            return acts[y]

        def dec(a, y, obs, b=b):
            if a == P_ACT:
                return 1 if _p_point(world, b, y) > F(1, 2) else 0
            if a == R_ACT:
                return world.d_recheck(b, y, obs)
            return world.d_resample(b, y, obs)

        total += world.one_trial_value(z, aoy, dec, cr, cs)
    return total / 2 * T


def _p_point(world, b, y) -> Fraction:
    num = den = F(0)
    for z, bz in ((0, b), (1, 1 - b)):
        for x in (0, 1):
            w = bz * world.pyx[z][y][x]
            den += w
            if x == 1:
                num += w
    return num / den


def replay_h1_value(world: World, T: int, cr, cs, myopic: bool = False) -> Fraction:
    """Value at the prior by depth-bounded recursion with an explicit cache of (belief, k)."""
    if not world.emissions_match:
        raise RuntimeError("replay h1 requires matched emissions")
    immP, immM = world.imm_PM()
    py = world.py[0]
    pc = []
    for z in (0, 1):
        pc.append([[world.p_y_class[z][y][c] / world.py[z][y] for c in range(10)] for y in range(N_Y)])
    inv = all(world.d_recheck(F(0), y, yp) == world.d_recheck(F(1), y, yp) for y in range(N_Y) for yp in range(N_Y))
    cache = {}

    def ec(b, y):
        if inv:
            return b * world.expected_correct_R(F(0), F(1), y) + (1 - b) * world.expected_correct_R(F(0), F(0), y)
        return world.expected_correct_R(b, b, y)

    def V(b, k):
        if k == 0:
            return F(0)
        key = (b, k, myopic)
        hit = cache.get(key)
        if hit is not None:
            return hit
        acc = F(0)
        for y in range(N_Y):
            same = world.mix_h1(b)
            cont = V(same, k - 1) if k > 1 else F(0)

            def ev():
                if k == 1:
                    return F(0)
                s = F(0)
                b1 = 1 - b
                for c in range(10):
                    p = b * pc[0][y][c] + b1 * pc[1][y][c]
                    if p == 0:
                        continue
                    bn = world.mix_h1(world.update_belief(b, c))
                    s += p * V(bn, k - 1)
                return s

            if myopic:
                a, _ = _choose(immP[y], ec(b, y) - cr, immM[y] - cs)
                if a == P_ACT:
                    q = immP[y] + cont
                elif a == R_ACT:
                    q = ec(b, y) - cr + ev()
                else:
                    q = immM[y] - cs + cont
            else:
                econt = ev() if k > 1 else F(0)
                _a, q = _choose(immP[y] + cont, ec(b, y) - cr + econt, immM[y] - cs + cont)
            acc += py[y] * q
        cache[key] = acc
        return acc

    return V(F(1, 2), T)


def replay_conf_path(world: World, eta, alpha, cr, cs, T: int, theta0: Fraction) -> Fraction:
    """Explicit 2^T error-path sum. Independent of the theta-distribution dict."""
    err_p = [F(0), F(0)]
    tab = world.err_table()
    for r in (0, 1):
        for e in (0, 1):
            err_p[e] += tab[r][e]
    sU = world.s_def[0]
    sSp = next(world.s_def[y] for y in range(N_Y) if read_class(y) == 1)
    # path bits, low bit is trial 0
    n = 1 << T
    total_S = F(0)
    total_E = F(0)
    for mask in range(n):
        p = F(1)
        th = theta0
        vS = F(0)
        vE = F(0)
        for t in range(T):
            ebit = (mask >> t) & 1
            p *= err_p[ebit]
            costs = (F(0), cr, cs)
            for r in (0, 1):
                sr = sU if r == 0 else sSp
                if sr > th:
                    a = P_ACT
                else:
                    best_a, best_q = 0, None
                    for aa in range(3):
                        q = world.g0[aa][r] - costs[aa]
                        if best_q is None or q > best_q:
                            best_q, best_a = q, aa
                    a = best_a
                for z in (0, 1):
                    rew = world.p_read[z][r] * (world.p_correct_f0[z][a][r] - costs[a])
                    if z == 0:
                        vS += rew
                    else:
                        vE += rew
            nxt = th + eta * (ebit - alpha)
            if nxt < 0:
                nxt = F(0)
            elif nxt > F(1, 2):
                nxt = F(1, 2)
            th = nxt
        total_S += p * vS
        total_E += p * vE
    return (total_S + total_E) / 2


def replay_reference_core(world: World, T: int, action_of, cr: Fraction, cs: Fraction) -> dict:
    """Second aggregation of the MB core pattern.

    action_of(k, count_tuple, y) -> action. Count transitions are rebuilt here.
    """
    counts = _enum_counts(T)
    index = {c: i for i, c in enumerate(counts)}
    trans = []
    for c in counts:
        row = []
        base = list(c)
        if sum(c) >= T:
            trans.append(tuple(-1 for _ in range(10)))
            continue
        for k in range(10):
            base[k] += 1
            row.append(index[tuple(base)])
            base[k] -= 1
        trans.append(tuple(row))
    belief = [world.belief_from_counts(c) for c in counts]
    pc = [[[world.p_y_class[z][y][c] / world.py[z][y] for c in range(10)] for y in range(N_Y)] for z in (0, 1)]
    split = tuple(y for y in range(N_Y) if read_class(y) == 1)
    bhalf = F(1, 2)
    ecS = [world.expected_correct_R(bhalf, F(1), y) for y in range(N_Y)]
    ecE = [world.expected_correct_R(bhalf, F(0), y) for y in range(N_Y)]
    immP, immM = world.imm_PM()

    def m_obs(i, y):
        bb = belief[i]
        # MB readout is its own posterior predictive. Under decision invariance this is
        # the belief mixture of the endpoint correctness of the common decision.
        if world.d_recheck(F(0), y, 0) == world.d_recheck(F(1), y, 0) or True:
            return world.expected_correct_R(bb, bb, y)

    snaps = []
    for z in (0, 1):
        mass = {0: F(1)}
        layers = []
        for t in range(T):
            layers.append(list(mass.items()))
            k = T - t
            new = {}
            for i, p in mass.items():
                ct = counts[i]
                for y in range(N_Y):
                    a = action_of(k, ct, y)
                    w = p * world.py[z][y]
                    if a != R_ACT:
                        new[i] = new.get(i, F(0)) + w
                    else:
                        for c in range(10):
                            wc = w * pc[z][y][c]
                            if wc == 0:
                                continue
                            new[trans[i][c]] = new.get(trans[i][c], F(0)) + wc
            mass = new
        snaps.append(layers)

    def cref(z, act):
        total = F(0)
        for t in range(T):
            k = T - t
            for i, p in snaps[z][t]:
                ct = counts[i]
                for y in split:
                    if action_of(k, ct, y) == act:
                        total += p * world.py[0][y]
        return total

    dR = cref(0, R_ACT) - cref(1, R_ACT)
    dM = cref(1, M_ACT) - cref(0, M_ACT)

    def e_err(use_agent: bool):
        acc = F(0)
        for act in (R_ACT, M_ACT):
            trial = F(0)
            for t in range(T):
                num = den = F(0)
                k = T - t
                for z in (0, 1):
                    for i, p in snaps[z][t]:
                        bb = belief[i]
                        for y in split:
                            w = F(1, 2) * p * world.py[0][y]
                            den += w
                            if act == R_ACT:
                                m = m_obs(i, y)
                            else:
                                m = immM[y]
                            mh = m if use_agent else world.g0[act][read_class(y)]
                            num += w * (mh - m) ** 2
                trial += num / den
            acc += trial / T
        return acc / 2

    e_agent = e_err(True)
    e_base = e_err(False)
    # donors at t = T-2
    t_star = T - 2
    best = [None, None]
    donor_i = [None, None]

    def better(cand, other, minimize):
        if other is None:
            return True
        if cand[0] != other[0]:
            return cand[0] < other[0] if minimize else cand[0] > other[0]
        if cand[1] != other[1]:
            return cand[1] > other[1]
        return cand[2] < other[2]

    for z in (0, 1):
        for i, p in snaps[z][t_star]:
            if p == 0:
                continue
            cand = (belief[i], p * F(1, 2), counts[i])
            for slot, minimize in ((0, False), (1, True)):
                if better(cand, best[slot], minimize):
                    best[slot] = cand
                    donor_i[slot] = i
    contrast = donor_i[0] is not None and donor_i[0] != donor_i[1]
    if contrast:
        for z_rec, don in ((1, donor_i[0]), (0, donor_i[1])):
            if all(i == don for i, p in snaps[z_rec][t_star] if p != 0):
                contrast = False

    def stats(rows, z, k, mhat_i):
        num_e = num_q = den = F(0)
        point = F(1) if z == 0 else F(0)
        for i, p in rows:
            if p == 0:
                continue
            ct = counts[i]
            for y in split:
                w = p * world.py[z][y]
                den += w
                if action_of(k, ct, y) == R_ACT:
                    num_q += w
                mh = mhat_i(i, y)
                m = world.expected_correct_R(belief[i] if False else belief[mhat_i.pred], point, y) if False else world.expected_correct_R(belief[mhat_i.pred], point, y)
                num_e += w * (mh - m)
        if den == 0:
            return None
        return num_e / den, num_q / den

    def own_mhat(i, y):
        return m_obs(i, y)

    class Pred:
        def __init__(self, i):
            self.pred = i

        def __call__(self, i, y):
            return m_obs(self.pred, y)

    def advance(rows, donor, clamp, z, k):
        A, B = {}, {}
        for i, p in rows:
            ctrl = i if donor is None else donor
            ct = counts[ctrl]
            for y in range(N_Y):
                a = action_of(k, ct, y)
                w = p * world.py[z][y]
                if a != R_ACT:
                    A[ctrl] = A.get(ctrl, F(0)) + w
                    B[i] = B.get(i, F(0)) + w
                else:
                    for c in range(10):
                        wc = w * pc[z][y][c]
                        if wc == 0:
                            continue
                        sA = ctrl if clamp else trans[ctrl][c]
                        sB = trans[i][c]
                        A[sA] = A.get(sA, F(0)) + wc
                        B[sB] = B.get(sB, F(0)) + wc
        return A, B

    out_swap = {}
    if donor_i[0] is None:
        contrast = False
    for name, z, don in (("S", 1, donor_i[0]), ("E", 0, donor_i[1])):
        if don is None:
            out_swap[name] = None
            continue
        rec = snaps[z][t_star]

        def stats_own(rows, z, k):
            num_e = num_q = den = F(0)
            point = F(1) if z == 0 else F(0)
            for i, p in rows:
                if p == 0:
                    continue
                for y in split:
                    w = p * world.py[z][y]
                    den += w
                    if action_of(k, counts[i], y) == R_ACT:
                        num_q += w
                    mh = m_obs(i, y)
                    m = world.expected_correct_R(belief[i], point, y)
                    num_e += w * (mh - m)
            if den == 0:
                return None
            return num_e / den, num_q / den

        def stats_fixed(rows, z, k, pred_i):
            num_e = num_q = den = F(0)
            point = F(1) if z == 0 else F(0)
            for i, p in rows:
                if p == 0:
                    continue
                for y in split:
                    w = p * world.py[z][y]
                    den += w
                    if action_of(k, counts[i], y) == R_ACT:
                        num_q += w
                    mh = m_obs(pred_i, y)
                    m = world.expected_correct_R(belief[pred_i], point, y)
                    num_e += w * (mh - m)
            if den == 0:
                return None
            return num_e / den, num_q / den

        intact = stats_own(rec, z, 2)
        block = {}
        for mode, donor, clamp in (("SWAP", don, False), ("CORRUPT", don, True), ("SUSPEND", None, True)):
            if mode == "SUSPEND":
                now = intact
            else:
                now = stats_fixed([(don, F(1))], z, 2, don)
            A, B = advance(rec, donor, clamp, z, 2)
            stA = stats_own(A.items(), z, 1)
            stB = stats_own(B.items(), z, 1)
            block[mode] = {
                "D_e": None if now is None or intact is None else now[0] - intact[0],
                "D_q": None if now is None or intact is None else now[1] - intact[1],
                "eA": None if stA is None else stA[0],
                "eB": None if stB is None else stB[0],
                "qA": None if stA is None else stA[1],
                "qB": None if stB is None else stB[1],
            }
        out_swap[name] = block
    swap_s = None if out_swap.get("S") is None else out_swap["S"]["SWAP"]
    swap_e = None if out_swap.get("E") is None else out_swap["E"]["SWAP"]

    def pull(block, key):
        return None if block is None else block[key]

    return {
        "delta_R": dR,
        "delta_M": dM,
        "E_err_agent": e_agent,
        "E_err_baseline": e_base,
        "D_e_S": pull(swap_s, "D_e"),
        "D_q_S": pull(swap_s, "D_q"),
        "D_e_E": pull(swap_e, "D_e"),
        "D_q_E": pull(swap_e, "D_q"),
        "e_A_S": pull(swap_s, "eA"),
        "e_B_S": pull(swap_s, "eB"),
        "q_A_S": pull(swap_s, "qA"),
        "q_B_S": pull(swap_s, "qB"),
        "e_A_E": pull(swap_e, "eA"),
        "e_B_E": pull(swap_e, "eB"),
        "q_A_E": pull(swap_e, "qA"),
        "q_B_E": pull(swap_e, "qB"),
        "contrast": contrast,
    }


def replay_cg_y(world: World, T, cr, cs, alpha_s, alpha_f, beta, z: int) -> Fraction:
    """Per-read-pattern expansion using y_atoms, not the read-class atom table."""
    from .agents import cg_choose

    ya = world.y_atoms()
    mass = {tuple(0 for _ in range(12)): F(1)}
    value = F(0)
    for _t in range(T):
        new = {}
        for st, p in mass.items():
            for y in range(N_Y):
                r = read_class(y)
                a = cg_choose(st, r, cr, cs, alpha_s, alpha_f, beta)
                wy = p * world.py[z][y]
                slot = a * 2 + r
                for corr, _cid, _g, pc in ya[z][y][a]:
                    w = wy * pc
                    value += w * (corr - (F(0), cr, cs)[a])
                    lst = list(st)
                    if corr:
                        lst[slot] += 1
                    else:
                        lst[6 + slot] += 1
                    key = tuple(lst)
                    new[key] = new.get(key, F(0)) + w
        mass = new
    return value
